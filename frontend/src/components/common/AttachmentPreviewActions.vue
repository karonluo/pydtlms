<script setup lang="ts">
import { Document, Download, View, ZoomIn, ZoomOut, FullScreen } from '@element-plus/icons-vue'
import { computed, nextTick, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { renderAsync } from 'docx-preview'

const props = withDefaults(defineProps<{
  url?: string | null
  fileName?: string | null
  fallbackLabel: string
  previewTitle?: string
  stacked?: boolean
  inlineImage?: boolean
  imageAlt?: string
}>(), {
  url: '',
  fileName: '',
  previewTitle: '',
  stacked: false,
  inlineImage: false,
  imageAlt: '',
})

const previewVisible = ref(false)
const previewLoading = ref(false)
const previewError = ref('')
const docxContainerRef = ref<HTMLDivElement | null>(null)
const imageScale = ref(1)
const imageFitMode = ref<'fit' | 'manual'>('fit')
let docxRenderToken = 0

const normalizedUrl = computed(() => String(props.url || '').trim())

const displayName = computed(() => {
  const preferred = String(props.fileName || '').trim()
  if (preferred) {
    return preferred
  }
  if (!normalizedUrl.value) {
    return props.fallbackLabel
  }
  const sanitizedUrl = normalizedUrl.value.split('?')[0]?.split('#')[0] || normalizedUrl.value
  const lastSegment = sanitizedUrl.split('/').pop() || ''
  return decodeURIComponent(lastSegment) || props.fallbackLabel
})

const attachmentType = computed<'image' | 'pdf' | 'docx' | 'other'>(() => {
  const normalizedName = displayName.value.toLowerCase()
  if (/\.(png|jpe?g|gif|bmp|webp|svg)$/.test(normalizedName)) {
    return 'image'
  }
  if (normalizedName.endsWith('.pdf')) {
    return 'pdf'
  }
  if (normalizedName.endsWith('.docx')) {
    return 'docx'
  }
  return 'other'
})

const canPreview = computed(() => attachmentType.value !== 'other' && !!normalizedUrl.value)
const inlineImageEnabled = computed(() => props.inlineImage && attachmentType.value === 'image' && !!normalizedUrl.value)
const dialogTitle = computed(() => props.previewTitle || displayName.value)
const showImageControls = computed(() => attachmentType.value === 'image' && previewVisible.value && !previewError.value)

const imagePreviewStyle = computed(() => {
  if (imageFitMode.value === 'fit') {
    return {
      transform: 'scale(1)',
      maxWidth: '100%',
      maxHeight: '68vh',
    }
  }
  return {
    transform: `scale(${imageScale.value})`,
    maxWidth: 'none',
    maxHeight: 'none',
  }
})

function clearDocxPreview() {
  if (docxContainerRef.value) {
    docxContainerRef.value.innerHTML = ''
  }
}

async function triggerAttachmentDownload() {
  if (!normalizedUrl.value) {
    ElMessage.warning('附件地址不存在')
    return
  }
  try {
    const response = await fetch(normalizedUrl.value)
    if (!response.ok) {
      throw new Error('download failed')
    }
    const blob = await response.blob()
    const objectUrl = window.URL.createObjectURL(blob)
    const anchor = document.createElement('a')
    anchor.href = objectUrl
    anchor.download = displayName.value
    document.body.appendChild(anchor)
    anchor.click()
    document.body.removeChild(anchor)
    window.URL.revokeObjectURL(objectUrl)
  } catch {
    ElMessage.error('附件下载失败')
  }
}

async function openPreview() {
  if (!canPreview.value) {
    return
  }
  imageScale.value = 1
  imageFitMode.value = 'fit'
  previewVisible.value = true
}

function zoomInImage() {
  imageFitMode.value = 'manual'
  imageScale.value = Math.min(4, Number((imageScale.value + 0.25).toFixed(2)))
}

function zoomOutImage() {
  imageFitMode.value = 'manual'
  imageScale.value = Math.max(0.5, Number((imageScale.value - 0.25).toFixed(2)))
}

function fitImageToViewport() {
  imageFitMode.value = 'fit'
  imageScale.value = 1
}

async function renderDocxPreview() {
  if (attachmentType.value !== 'docx' || !normalizedUrl.value) {
    return
  }
  const currentToken = ++docxRenderToken
  previewLoading.value = true
  previewError.value = ''
  clearDocxPreview()
  try {
    const response = await fetch(normalizedUrl.value)
    if (!response.ok) {
      throw new Error('preview failed')
    }
    const buffer = await response.arrayBuffer()
    if (currentToken !== docxRenderToken || !docxContainerRef.value) {
      return
    }
    await renderAsync(buffer, docxContainerRef.value, undefined, {
      inWrapper: true,
      useBase64URL: true,
      breakPages: true,
    })
  } catch {
    if (currentToken === docxRenderToken) {
      previewError.value = 'DOCX 预览失败，请尝试下载后查看。'
    }
  } finally {
    if (currentToken === docxRenderToken) {
      previewLoading.value = false
    }
  }
}

watch(() => previewVisible.value, async (visible) => {
  if (!visible) {
    previewLoading.value = false
    previewError.value = ''
    imageScale.value = 1
    imageFitMode.value = 'fit'
    clearDocxPreview()
    return
  }
  if (attachmentType.value !== 'docx') {
    previewLoading.value = false
    previewError.value = ''
    return
  }
  await nextTick()
  await renderDocxPreview()
})
</script>

<template>
  <div v-if="normalizedUrl" class="attachment-preview-block">
    <div v-if="inlineImageEnabled" class="attachment-preview-block__image-shell">
      <img :src="normalizedUrl" :alt="imageAlt || displayName" class="attachment-preview-block__image" @click="openPreview" />
    </div>
    <div :class="['attachment-preview-block__actions', { 'attachment-preview-block__actions--stacked': stacked }]">
      <span v-if="attachmentType === 'image'" class="attachment-preview-block__link attachment-preview-block__file-name" :title="displayName">
        <el-icon><Document /></el-icon>
        <span>{{ displayName }}</span>
      </span>
      <a v-else class="attachment-preview-block__link" :href="normalizedUrl" target="_blank" rel="noopener noreferrer" :title="displayName">
        <el-icon><Document /></el-icon>
        <span>{{ displayName }}</span>
      </a>
      <button v-if="canPreview" type="button" class="attachment-preview-block__button" @click="openPreview">
        <el-icon><View /></el-icon>
        <span>预览</span>
      </button>
      <button type="button" class="attachment-preview-block__button" @click="triggerAttachmentDownload">
        <el-icon><Download /></el-icon>
        <span>下载</span>
      </button>
    </div>

    <el-dialog v-model="previewVisible" :title="dialogTitle" width="960px" append-to-body draggable>
      <div v-loading="previewLoading" class="attachment-preview-dialog">
        <el-empty v-if="previewError" :description="previewError" />
        <div v-else-if="attachmentType === 'image'" class="attachment-preview-dialog__image-shell">
          <img :src="normalizedUrl" :alt="imageAlt || displayName" class="attachment-preview-dialog__image" :style="imagePreviewStyle" />
        </div>
        <iframe
          v-else-if="attachmentType === 'pdf'"
          :src="normalizedUrl"
          title="PDF 预览"
          class="attachment-preview-dialog__frame"
        />
        <div v-else-if="attachmentType === 'docx'" ref="docxContainerRef" class="attachment-preview-dialog__docx" />
      </div>
      <template v-if="showImageControls" #footer>
        <div class="attachment-preview-dialog__footer">
          <el-button @click="zoomOutImage">
            <el-icon><ZoomOut /></el-icon>
            缩小
          </el-button>
          <el-button @click="zoomInImage">
            <el-icon><ZoomIn /></el-icon>
            放大
          </el-button>
          <el-button @click="fitImageToViewport">
            <el-icon><FullScreen /></el-icon>
            适应
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.attachment-preview-block {
  display: grid;
  gap: 6px;
  min-width: 0;
}

.attachment-preview-block__image-shell {
  display: flex;
  justify-content: center;
  padding: 6px;
  border: 1px solid rgba(18, 50, 95, 0.08);
  border-radius: 12px;
  background: rgba(246, 249, 253, 0.92);
}

.attachment-preview-block__image {
  display: block;
  max-width: 100%;
  max-height: 150px;
  object-fit: contain;
  border-radius: 10px;
  cursor: zoom-in;
}

.attachment-preview-block__actions {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
  max-width: 100%;
  flex-wrap: nowrap;
}

.attachment-preview-block__actions--stacked {
  align-items: center;
}

.attachment-preview-block__link,
.attachment-preview-block__button {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  color: #17598d;
  font: inherit;
}

.attachment-preview-block__link {
  flex: 1 1 auto;
  min-width: 0;
  overflow: hidden;
}

.attachment-preview-block__button {
  flex: 0 0 auto;
}

.attachment-preview-block__link span,
.attachment-preview-block__button span {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.attachment-preview-block__link {
  text-decoration: none;
}

.attachment-preview-block__file-name {
  color: #334155;
}

.attachment-preview-block__button-link {
  border: none;
  padding: 0;
  background: transparent;
  cursor: pointer;
  text-align: left;
}

.attachment-preview-block__button {
  border: none;
  padding: 0;
  background: transparent;
  cursor: pointer;
}

.attachment-preview-dialog {
  min-height: 320px;
}

.attachment-preview-dialog__image-shell {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-height: 70vh;
  overflow: auto;
  border-radius: 12px;
  background: #f5f7fa;
}

.attachment-preview-dialog__image,
.attachment-preview-dialog__frame {
  display: block;
  border: none;
  border-radius: 12px;
  background: #ffffff;
}

.attachment-preview-dialog__image {
  width: auto;
  min-width: 280px;
  transform-origin: top center;
  transition: transform 0.18s ease;
  object-fit: contain;
  background: transparent;
}

.attachment-preview-dialog__frame {
  width: 100%;
  min-height: 70vh;
}

.attachment-preview-dialog__docx {
  min-height: 70vh;
  overflow: auto;
  border-radius: 12px;
  background: #f5f7fa;
}

.attachment-preview-dialog__docx :deep(.docx-wrapper) {
  padding: 20px 0;
  background: #f5f7fa;
}

.attachment-preview-dialog__docx :deep(.docx) {
  margin: 0 auto;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.12);
}

.attachment-preview-dialog__footer {
  display: flex;
  justify-content: center;
  gap: 10px;
  width: 100%;
}

@media (max-width: 768px) {
  .attachment-preview-block__image {
    max-height: 130px;
  }

  .attachment-preview-block__actions {
    gap: 10px;
    flex-wrap: wrap;
  }

  .attachment-preview-dialog__image-shell,
  .attachment-preview-dialog__image,
  .attachment-preview-dialog__frame,
  .attachment-preview-dialog__docx {
    min-height: 60vh;
  }

  .attachment-preview-dialog__footer {
    flex-wrap: wrap;
  }
}
</style>