<script setup lang="ts">
import axios from 'axios'
import { computed, nextTick, onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import TableRowActions from '../../components/table/TableRowActions.vue'
import { useServerPagination } from '../../composables/useServerPagination'
import { type SelectOption } from '../../api/system'
import {
  batchOfflineNewsArticles,
  batchPublishNewsArticles,
  createNewsArticle,
  deleteNewsArticle,
  getNewsTypeOptions,
  offlineNewsArticle,
  listNewsArticles,
  NEWS_STATUS_OPTIONS,
  publishNewsArticle,
  updateNewsArticle,
  uploadNewsImage,
  type NewsArticleRecord,
  type NewsArticleUpsert,
} from '../../api/news'

const loading = ref(false)
const bootstrapping = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const dialogMode = ref<'create' | 'edit'>('create')
const currentId = ref<number | null>(null)
const newsActionDialogVisible = ref(false)
const newsActionSubmitting = ref(false)
const pendingNewsAction = ref<{
  title: string
  lead: string
  confirmText: string
  successText: string
  summaryItems: Array<{ label: string, value: string }>
  run: () => Promise<void>
} | null>(null)
const articles = ref<NewsArticleRecord[]>([])
const selectedArticles = ref<NewsArticleRecord[]>([])
const newsTypeOptions = ref<SelectOption[]>([])
const editorRef = ref<HTMLDivElement | null>(null)
const imageInputRef = ref<HTMLInputElement | null>(null)
const pagination = useServerPagination(10)
const selectionRange = ref<Range | null>(null)
const selectedFontFamily = ref('微软雅黑, Microsoft YaHei, sans-serif')
const selectedFontSize = ref('16px')
const selectedFontColor = ref('#1f2937')
const selectedTablePreset = ref('3x3')
const defaultNewsTypeOptions: SelectOption[] = [
  { label: '学生门户通知消息', value: '学生门户通知消息' },
  { label: '学生门户新闻信息', value: '学生门户新闻信息' },
]

const fontFamilyOptions = [
  { label: '宋体', value: '宋体, SimSun, serif' },
  { label: '黑体', value: '黑体, SimHei, sans-serif' },
  { label: '微软雅黑', value: '微软雅黑, Microsoft YaHei, sans-serif' },
  { label: '楷体', value: '楷体, KaiTi, serif' },
  { label: '仿宋', value: '仿宋, FangSong, serif' },
  { label: 'Arial', value: 'Arial, sans-serif' },
  { label: 'Times New Roman', value: 'Times New Roman, serif' },
]

const fontSizeOptions = [
  { label: '12px', value: '12px' },
  { label: '14px', value: '14px' },
  { label: '16px', value: '16px' },
  { label: '18px', value: '18px' },
  { label: '20px', value: '20px' },
  { label: '24px', value: '24px' },
  { label: '28px', value: '28px' },
]

const tablePresetOptions = [
  { label: '2 × 2', value: '2x2' },
  { label: '3 × 3', value: '3x3' },
  { label: '4 × 4', value: '4x4' },
]

const selectedArticlesCount = computed(() => selectedArticles.value.length)

const filters = reactive({
  keyword: '',
  news_type: '',
  status: '',
})

const form = reactive<NewsArticleUpsert>({
  news_title: '',
  news_content: '',
  news_type: '',
  published_at: null,
  status: '草稿',
  is_pinned: false,
  display_order: 0,
})

const statusColorMap: Record<string, 'success' | 'warning' | 'info' | 'danger'> = {
  草稿: 'info',
  待发布: 'warning',
  已发布: 'success',
  已下线: 'danger',
}

const pageTitle = computed(() => '新闻管理')
const currentNewsTypeLabel = (value: string) => newsTypeOptions.value.find((item) => item.value === value)?.label || value || '-'

function getErrorMessage(error: unknown) {
  if (axios.isAxiosError(error)) {
    return String(error.response?.data?.detail || error.message || '请求失败')
  }
  return '请求失败'
}

function stripHtml(html: string) {
  return String(html || '')
    .replace(/<[^>]*>/g, '')
    .replace(/&nbsp;/gi, ' ')
    .trim()
}

function hasMeaningfulContent(html: string) {
  return stripHtml(html).length > 0 || /<img\b/i.test(html)
}

function formatNewsActionTime() {
  return new Date()
}

function formatNewsSummaryValue(value: unknown) {
  if (value === null || value === undefined || value === '') {
    return '-'
  }
  return String(value)
}

function openNewsActionDialog(options: {
  title: string
  lead: string
  confirmText: string
  successText: string
  summaryItems: Array<{ label: string, value: string }>
  run: () => Promise<void>
}) {
  pendingNewsAction.value = options
  newsActionDialogVisible.value = true
}

function closeNewsActionDialog() {
  if (newsActionSubmitting.value) {
    return
  }
  newsActionDialogVisible.value = false
}

function resetNewsActionDialog() {
  pendingNewsAction.value = null
}

async function confirmNewsAction() {
  if (!pendingNewsAction.value) {
    return
  }
  try {
    newsActionSubmitting.value = true
    await pendingNewsAction.value.run()
    ElMessage.success(pendingNewsAction.value.successText)
    newsActionDialogVisible.value = false
    await loadArticles()
  } catch (error) {
    ElMessage.error(getErrorMessage(error))
  } finally {
    newsActionSubmitting.value = false
  }
}

function formatDateTime(value?: string | Date | null) {
  if (!value) {
    return '-'
  }
  const date = value instanceof Date ? value : new Date(value)
  if (Number.isNaN(date.getTime())) {
    return String(value)
  }
  return new Intl.DateTimeFormat('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  }).format(date)
}

function syncEditorContent() {
  if (!editorRef.value) {
    return
  }
  form.news_content = editorRef.value.innerHTML
}

function captureSelection() {
  const editor = editorRef.value
  const selection = window.getSelection()
  if (!editor || !selection || selection.rangeCount === 0) {
    return
  }
  const range = selection.getRangeAt(0)
  if (!editor.contains(range.commonAncestorContainer)) {
    return
  }
  selectionRange.value = range.cloneRange()
}

function restoreSelection() {
  const editor = editorRef.value
  const selection = window.getSelection()
  if (!editor || !selectionRange.value || !selection) {
    return false
  }
  selection.removeAllRanges()
  selection.addRange(selectionRange.value)
  return true
}

function setEditorContent(html: string) {
  if (editorRef.value) {
    editorRef.value.innerHTML = html || ''
  }
  form.news_content = html || ''
}

function applyEditorCommand(command: string, value?: string) {
  editorRef.value?.focus()
  restoreSelection()
  document.execCommand(command, false, value)
  syncEditorContent()
  captureSelection()
}

function applyInlineStyle(style: Partial<CSSStyleDeclaration>) {
  editorRef.value?.focus()
  if (!restoreSelection()) {
    return
  }
  const selection = window.getSelection()
  if (!selection || selection.rangeCount === 0) {
    return
  }
  const range = selection.getRangeAt(0)
  if (range.collapsed) {
    return
  }
  const wrapper = document.createElement('span')
  Object.assign(wrapper.style, style)
  wrapper.appendChild(range.extractContents())
  range.insertNode(wrapper)
  range.setStartAfter(wrapper)
  range.collapse(true)
  selection.removeAllRanges()
  selection.addRange(range)
  syncEditorContent()
  captureSelection()
}

function applyFontFamily() {
  applyInlineStyle({ fontFamily: selectedFontFamily.value })
}

function applyFontSize() {
  applyInlineStyle({ fontSize: selectedFontSize.value })
}

function applyFontColor() {
  applyInlineStyle({ color: selectedFontColor.value })
}

function insertTable() {
  const [rowsText, colsText] = selectedTablePreset.value.split('x')
  const rows = Math.max(1, Number(rowsText || 3))
  const cols = Math.max(1, Number(colsText || 3))
  const cells = Array.from({ length: cols })
    .map(() => '<td style="min-width: 96px; padding: 8px; border: 1px solid #cbd5e1;">请输入内容</td>')
    .join('')
  const tableHtml = `
    <table style="border-collapse: collapse; width: 100%; margin: 12px 0; table-layout: fixed;">
      <tbody>
        ${Array.from({ length: rows }).map(() => `<tr>${cells}</tr>`).join('')}
      </tbody>
    </table>
  `.trim()
  editorRef.value?.focus()
  restoreSelection()
  document.execCommand('insertHTML', false, tableHtml)
  syncEditorContent()
  captureSelection()
}

function triggerImageUpload() {
  imageInputRef.value?.click()
}

async function handleImageInputChange(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  input.value = ''
  if (!file) {
    return
  }
  try {
    const response = await uploadNewsImage(file)
    const imageUrl = response.data.url
    editorRef.value?.focus()
    restoreSelection()
    document.execCommand('insertHTML', false, `<img src="${imageUrl}" alt="${file.name}" style="max-width: 100%; height: auto;" />`)
    syncEditorContent()
    ElMessage.success('图片上传成功')
  } catch (error) {
    ElMessage.error(getErrorMessage(error))
  }
}

function resetForm() {
  currentId.value = null
  Object.assign(form, {
    news_title: '',
    news_content: '',
    news_type: '',
    published_at: null,
    status: '草稿',
    is_pinned: false,
    display_order: 0,
  })
  setEditorContent('')
}

function openCreateDialog() {
  resetForm()
  dialogMode.value = 'create'
  dialogVisible.value = true
  void nextTick(() => setEditorContent(''))
}

function openEditDialog(row: NewsArticleRecord) {
  currentId.value = row.id
  Object.assign(form, {
    news_title: row.news_title,
    news_content: row.news_content,
    news_type: row.news_type,
    published_at: row.published_at ? new Date(row.published_at) : null,
    status: row.status,
    is_pinned: row.is_pinned,
    display_order: row.display_order,
  })
  dialogMode.value = 'edit'
  dialogVisible.value = true
  void nextTick(() => setEditorContent(row.news_content))
}

function handleSelectionChange(rows: NewsArticleRecord[]) {
  selectedArticles.value = rows
}

function handleSearch() {
  pagination.reset()
  void loadArticles()
}

function handleReset() {
  Object.assign(filters, { keyword: '', news_type: '', status: '' })
  pagination.reset()
  void loadArticles()
}

async function submitForm(targetStatus: '草稿' | '已发布') {
  if (!form.news_title.trim() || !form.news_type.trim()) {
    ElMessage.warning('请先填写新闻标题和新闻类型')
    return
  }
  if (!hasMeaningfulContent(form.news_content)) {
    ElMessage.warning('请先填写新闻正文')
    return
  }
  submitting.value = true
  try {
    const publishedAt = targetStatus === '已发布' ? form.published_at || formatNewsActionTime() : form.published_at
    const payload: NewsArticleUpsert = {
      ...form,
      published_at: publishedAt,
      status: targetStatus,
      news_content: form.news_content,
    }
    if (dialogMode.value === 'create') {
      await createNewsArticle(payload)
      ElMessage.success(targetStatus === '已发布' ? '新闻已创建并发布' : '新闻草稿已保存')
    } else if (currentId.value !== null) {
      await updateNewsArticle(currentId.value, payload)
      ElMessage.success(targetStatus === '已发布' ? '新闻已更新并发布' : '新闻草稿已保存')
    }
    dialogVisible.value = false
    await loadArticles()
  } catch (error) {
    ElMessage.error(getErrorMessage(error))
  } finally {
    submitting.value = false
  }
}

async function loadBootstrapData() {
  bootstrapping.value = true
  try {
    const response = await getNewsTypeOptions()
    newsTypeOptions.value = response.data.length > 0 ? response.data : defaultNewsTypeOptions
  } finally {
    bootstrapping.value = false
  }
}

async function loadArticles() {
  loading.value = true
  try {
    const response = await listNewsArticles({
      keyword: filters.keyword || undefined,
      news_type: filters.news_type || undefined,
      status: filters.status || undefined,
      page: pagination.pagination.currentPage,
      page_size: pagination.pagination.pageSize,
    })
    articles.value = response.data.items
    selectedArticles.value = []
    pagination.sync(response.data.total)
  } finally {
    loading.value = false
  }
}

function getNewsRowActions(row: NewsArticleRecord) {
  const publishOrOfflineAction = row.status === '已发布'
    ? { key: 'offline', label: '下线', type: 'warning' as const, onClick: () => handleOfflineNewsArticle(row) }
    : { key: 'publish', label: '发布', type: 'success' as const, onClick: () => handlePublishNewsArticle(row) }
  return [
    { key: 'edit', label: '编辑', onClick: () => openEditDialog(row) },
    publishOrOfflineAction,
  ]
}

async function handlePublishNewsArticle(row: NewsArticleRecord) {
  openNewsActionDialog({
    title: '发布新闻确认',
    lead: `确认发布新闻“${row.news_title}”吗？`,
    confirmText: '发布',
    successText: '新闻已发布',
    summaryItems: [
      { label: '新闻标题', value: formatNewsSummaryValue(row.news_title) },
      { label: '新闻类型', value: formatNewsSummaryValue(currentNewsTypeLabel(row.news_type)) },
      { label: '当前状态', value: formatNewsSummaryValue(row.status) },
      { label: '发布者', value: formatNewsSummaryValue(row.publisher_name || row.publisher_username) },
    ],
    run: async () => {
    await publishNewsArticle(row.id)
    },
  })
}

async function handleOfflineNewsArticle(row: NewsArticleRecord) {
  openNewsActionDialog({
    title: '下线新闻确认',
    lead: `确认下线新闻“${row.news_title}”吗？`,
    confirmText: '下线',
    successText: '新闻已下线',
    summaryItems: [
      { label: '新闻标题', value: formatNewsSummaryValue(row.news_title) },
      { label: '新闻类型', value: formatNewsSummaryValue(currentNewsTypeLabel(row.news_type)) },
      { label: '当前状态', value: formatNewsSummaryValue(row.status) },
      { label: '发布日期', value: formatNewsSummaryValue(formatDateTime(row.published_at)) },
    ],
    run: async () => {
    await offlineNewsArticle(row.id)
    },
  })
}

async function handleBatchPublishNewsArticles() {
  if (!selectedArticles.value.length) {
    ElMessage.warning('请先选择要发布的新闻')
    return
  }
  openNewsActionDialog({
    title: '批量发布确认',
    lead: `确认批量发布选中的 ${selectedArticles.value.length} 条新闻吗？`,
    confirmText: '发布',
    successText: '新闻已批量发布',
    summaryItems: [
      { label: '选中数量', value: formatNewsSummaryValue(selectedArticles.value.length) },
      { label: '操作类型', value: '批量发布' },
      { label: '提示', value: '仅会发布当前勾选的新闻' },
      { label: '说明', value: '发布后将立即对门户可见' },
    ],
    run: async () => {
    await batchPublishNewsArticles(selectedArticles.value.map((item) => item.id))
    },
  })
}

async function handleBatchOfflineNewsArticles() {
  if (!selectedArticles.value.length) {
    ElMessage.warning('请先选择要下线的新闻')
    return
  }
  openNewsActionDialog({
    title: '批量下线确认',
    lead: `确认批量下线选中的 ${selectedArticles.value.length} 条新闻吗？`,
    confirmText: '下线',
    successText: '新闻已批量下线',
    summaryItems: [
      { label: '选中数量', value: formatNewsSummaryValue(selectedArticles.value.length) },
      { label: '操作类型', value: '批量下线' },
      { label: '提示', value: '下线后门户将不再展示这些新闻' },
      { label: '说明', value: '该操作可随时重新发布' },
    ],
    run: async () => {
    await batchOfflineNewsArticles(selectedArticles.value.map((item) => item.id))
    },
  })
}

async function handleDelete(row: NewsArticleRecord) {
  openNewsActionDialog({
    title: '删除新闻确认',
    lead: `确认删除新闻“${row.news_title}”吗？`,
    confirmText: '删除',
    successText: '新闻已删除',
    summaryItems: [
      { label: '新闻标题', value: formatNewsSummaryValue(row.news_title) },
      { label: '新闻类型', value: formatNewsSummaryValue(currentNewsTypeLabel(row.news_type)) },
      { label: '当前状态', value: formatNewsSummaryValue(row.status) },
      { label: '更新时间', value: formatNewsSummaryValue(formatDateTime(row.updated_at)) },
    ],
    run: async () => {
    await deleteNewsArticle(row.id)
    },
  })
}

async function handlePageChange(page: number) {
  pagination.handleCurrentChange(page)
  await loadArticles()
}

async function handleSizeChange(size: number) {
  pagination.handleSizeChange(size)
  await loadArticles()
}

onMounted(async () => {
  await loadBootstrapData()
  await loadArticles()
})
</script>

<template>
  <div class="news-management-page">
    <el-card shadow="never" class="page-card page-intro-card">
      <div class="page-intro">
        <div>
          <el-tag type="primary" effect="light" round>招生管理</el-tag>
          <h1>{{ pageTitle }}</h1>
          <p>用于维护招生管理下的新闻内容、门户通知与图文信息，正文支持富文本编辑和图片上传。</p>
        </div>
        <div class="page-intro-actions">
          <el-button type="primary" @click="openCreateDialog">新增新闻</el-button>
          <el-button :disabled="!selectedArticlesCount" @click="handleBatchPublishNewsArticles">批量发布</el-button>
          <el-button :disabled="!selectedArticlesCount" @click="handleBatchOfflineNewsArticles">批量下线</el-button>
          <el-button @click="handleReset">重置筛选</el-button>
        </div>
      </div>
    </el-card>

    <el-card shadow="never" class="page-card">
      <el-form :inline="true" :model="filters" class="filter-form">
        <el-form-item label="关键词">
          <el-input v-model="filters.keyword" placeholder="标题 / 内容 / 编号" clearable style="width: 240px" />
        </el-form-item>
        <el-form-item label="新闻类型">
          <el-select v-model="filters.news_type" placeholder="全部" clearable style="width: 220px">
            <el-option v-for="option in newsTypeOptions" :key="option.value" :label="option.label" :value="option.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="filters.status" placeholder="全部" clearable style="width: 180px">
            <el-option v-for="option in NEWS_STATUS_OPTIONS" :key="option.value" :label="option.label" :value="option.value" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading || bootstrapping" @click="handleSearch">查询</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="articles" v-loading="loading || bootstrapping" stripe border class="news-table" row-key="id" @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="52" />
        <el-table-column prop="news_title" label="新闻标题" min-width="220" show-overflow-tooltip />
        <el-table-column label="新闻类型" width="180">
          <template #default="{ row }">
            {{ currentNewsTypeLabel(row.news_type) }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="110">
          <template #default="{ row }">
            <el-tag :type="statusColorMap[row.status] || 'info'" effect="light">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_pinned" label="置顶" width="90">
          <template #default="{ row }">
            <el-tag :type="row.is_pinned ? 'success' : 'info'" effect="plain">{{ row.is_pinned ? '是' : '否' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="display_order" label="排序" width="90" align="center" />
        <el-table-column label="发布日期" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.published_at) }}
          </template>
        </el-table-column>
        <el-table-column label="发布者" width="140">
          <template #default="{ row }">
            {{ row.publisher_name || row.publisher_username || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="更新时间" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.updated_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="160" fixed="right">
          <template #default="{ row }">
            <TableRowActions
              :row="row"
              :main-actions="getNewsRowActions(row)"
              :more-actions="[{ key: 'delete', label: '删除', type: 'danger', onClick: () => handleDelete(row) }]"
            />
          </template>
        </el-table-column>
      </el-table>

      <div class="pager-row">
        <el-pagination
          background
          layout="total, sizes, prev, pager, next, jumper"
          :current-page="pagination.pagination.currentPage"
          :page-size="pagination.pagination.pageSize"
          :total="pagination.pagination.total"
          :page-sizes="[10, 20, 50, 100]"
          @current-change="handlePageChange"
          @size-change="handleSizeChange"
        />
      </div>
    </el-card>

    <el-dialog
      v-model="dialogVisible"
      :title="dialogMode === 'create' ? '新增新闻' : '编辑新闻'"
      width="960px"
      destroy-on-close
      class="news-management-dialog"
      @closed="resetForm"
    >
      <div class="dialog-form reset-password-dialog">
        <el-form :model="form" label-width="110px" class="news-form">
          <div class="dialog-grid">
            <el-form-item label="新闻标题" required class="dialog-grid--full">
              <el-input v-model="form.news_title" maxlength="255" placeholder="请输入新闻标题" />
            </el-form-item>
            <el-form-item label="新闻类型" required>
              <el-select v-model="form.news_type" placeholder="请选择新闻类型">
                <el-option v-for="option in newsTypeOptions" :key="option.value" :label="option.label" :value="option.value" />
              </el-select>
            </el-form-item>
            <el-form-item label="发布日期">
              <el-date-picker
                v-model="form.published_at"
                type="datetime"
                placeholder="选择发布日期时间"
              />
            </el-form-item>
            <el-form-item label="置顶">
              <el-switch v-model="form.is_pinned" />
            </el-form-item>
            <el-form-item label="排序">
              <el-input-number v-model="form.display_order" :min="0" :max="9999" :controls-position="'right'" />
            </el-form-item>
            <el-form-item label="新闻正文" required class="dialog-grid--full">
            <div class="editor-shell">
              <div class="editor-toolbar">
                <div class="editor-toolbar-row">
                  <el-button-group>
                    <el-button size="small" type="button" @click="applyEditorCommand('bold')">加粗</el-button>
                    <el-button size="small" type="button" @click="applyEditorCommand('italic')">斜体</el-button>
                    <el-button size="small" type="button" @click="applyEditorCommand('underline')">下划线</el-button>
                    <el-button size="small" type="button" @click="applyEditorCommand('insertOrderedList')">有序列表</el-button>
                    <el-button size="small" type="button" @click="applyEditorCommand('insertUnorderedList')">无序列表</el-button>
                    <el-button size="small" type="button" @click="triggerImageUpload">插入图片</el-button>
                  </el-button-group>
                  <el-select v-model="selectedFontFamily" size="small" class="editor-select" @change="applyFontFamily">
                    <el-option v-for="option in fontFamilyOptions" :key="option.value" :label="option.label" :value="option.value" />
                  </el-select>
                  <el-select v-model="selectedFontSize" size="small" class="editor-select" @change="applyFontSize">
                    <el-option v-for="option in fontSizeOptions" :key="option.value" :label="option.label" :value="option.value" />
                  </el-select>
                  <el-color-picker v-model="selectedFontColor" size="small" @change="applyFontColor" />
                  <el-select v-model="selectedTablePreset" size="small" class="editor-select" @change="insertTable">
                    <el-option v-for="option in tablePresetOptions" :key="option.value" :label="option.label" :value="option.value" />
                  </el-select>
                </div>
                <span class="editor-hint">支持粘贴富文本、设置字体、字号、颜色、插入图片和基础表格。</span>
              </div>
              <div
                ref="editorRef"
                class="news-editor"
                contenteditable="true"
                spellcheck="false"
                @focus="captureSelection"
                @mouseup="captureSelection"
                @keyup="captureSelection"
                @input="syncEditorContent"
                @blur="syncEditorContent"
              ></div>
              <input
                ref="imageInputRef"
                class="visually-hidden"
                type="file"
                accept="image/*"
                @change="handleImageInputChange"
              />
            </div>
            </el-form-item>
          </div>
        </el-form>
      </div>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button :loading="submitting" @click="submitForm('草稿')">保存草稿</el-button>
          <el-button type="primary" :loading="submitting" @click="submitForm('已发布')">直接发布</el-button>
        </div>
      </template>
    </el-dialog>

    <el-dialog
      v-model="newsActionDialogVisible"
      :title="pendingNewsAction?.title || '确认操作'"
      width="640px"
      destroy-on-close
      class="news-management-dialog"
      @closed="resetNewsActionDialog"
    >
      <div v-if="pendingNewsAction" class="dialog-form reset-password-dialog management-confirm-dialog">
        <p class="management-confirm-dialog__lead">{{ pendingNewsAction.lead }}</p>
        <div class="management-confirm-dialog__summary">
          <div v-for="item in pendingNewsAction.summaryItems" :key="item.label">
            <span class="management-confirm-dialog__label">{{ item.label }}</span>
            <strong>{{ item.value }}</strong>
          </div>
        </div>
        <p class="management-confirm-dialog__hint">确认后操作将立即生效，请再次核对上面的信息。</p>
      </div>
      <template #footer>
        <el-button :disabled="newsActionSubmitting" @click="closeNewsActionDialog">取消</el-button>
        <el-button type="primary" :loading="newsActionSubmitting" @click="confirmNewsAction">
          {{ pendingNewsAction?.confirmText || '确认' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.news-management-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.page-card {
  border-radius: 20px;
  border: 1px solid rgba(15, 76, 189, 0.12);
  box-shadow: 0 18px 50px rgba(15, 23, 42, 0.08);
}

.page-intro-card {
  background:
    radial-gradient(circle at top right, rgba(15, 76, 189, 0.14), transparent 30%),
    linear-gradient(135deg, rgba(255, 255, 255, 0.94), rgba(244, 248, 255, 0.92));
}

.page-intro {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 20px;
}

.page-intro h1 {
  margin: 10px 0 8px;
  font-size: 30px;
  font-weight: 800;
  letter-spacing: 0.02em;
}

.page-intro p {
  margin: 0;
  color: #5c677d;
  line-height: 1.75;
  max-width: 740px;
}

.page-intro-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.filter-form {
  margin-bottom: 8px;
}

.news-table {
  margin-top: 12px;
}

.pager-row {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}

.news-form {
  max-height: 68vh;
  overflow: auto;
  padding-right: 4px;
}

.news-management-dialog :deep(.el-dialog__body) {
  padding-top: 12px;
}

.editor-shell {
  width: 100%;
  border: 1px solid #dcdfe6;
  border-radius: 14px;
  background: #fff;
  overflow: hidden;
}

.editor-toolbar {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  justify-content: flex-start;
  gap: 10px;
  padding: 12px;
  border-bottom: 1px solid #ebeef5;
  background: linear-gradient(135deg, rgba(15, 76, 189, 0.05), rgba(255, 255, 255, 0.9));
}

.editor-toolbar-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.editor-select {
  width: 150px;
}

.editor-hint {
  color: #6b7280;
  font-size: 12px;
}

.news-editor {
  min-height: 320px;
  padding: 16px;
  outline: none;
  line-height: 1.85;
}

.news-editor :deep(img) {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 10px 0;
}

.news-editor :deep(table) {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
  margin: 12px 0;
}

.news-editor :deep(td),
.news-editor :deep(th) {
  border: 1px solid #cbd5e1;
  min-width: 96px;
  padding: 8px;
  vertical-align: top;
}

.news-editor :deep(th) {
  background: #f8fafc;
  font-weight: 700;
}

.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

@media (max-width: 960px) {
  .page-intro {
    flex-direction: column;
    align-items: flex-start;
  }

  .editor-toolbar {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
