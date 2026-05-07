<script setup lang="ts">
import type { PortalApplicationUpsert } from '../../../../api/portal'

function resolveAttachmentDisplayName(url: string | null | undefined, fileName: string | null | undefined, fallbackLabel: string) {
  const preferred = String(fileName || '').trim()
  if (preferred) {
    return preferred
  }
  const normalized = String(url || '').trim()
  if (!normalized) {
    return fallbackLabel
  }
  const lastSegment = normalized.split('/').pop() || ''
  return decodeURIComponent(lastSegment) || fallbackLabel
}

function isPreviewableAttachment(fileName: string | null | undefined, fileUrl: string | null | undefined) {
  const candidate = String(fileName || fileUrl || '').toLowerCase()
  return candidate.endsWith('.pdf')
}

defineProps<{
  form: PortalApplicationUpsert
  declarationReminderText: string
  resumeAttachmentAccept: string
  supportingMaterialAttachmentAccept: string
  isAttachmentUploading: (key: string) => boolean
  buildAttachmentUploadKey: (section: string, index: number | string, field: string) => string
  handleResumeAttachmentUpload: (event: Event) => void | Promise<void>
  handleSupportingMaterialAttachmentUpload: (event: Event) => void | Promise<void>
  submitForm: () => void | Promise<void>
  submitting: boolean
}>()
</script>

<template>
  <section class="section-page">
    <div class="section-card">
      <div class="section-intro">
        <strong>个人陈述</strong>
        <p>请填写个人陈述并上传简历。</p>
      </div>

      <div class="section-grid">
        <label class="section-grid__full">
          <span><span class="required-mark">*</span>请简要描述个人经历、申请上海人工智能实验室联培博士生项目的原因以及未来规划等（必填，1200字以内）</span>
          <textarea v-model="form.personal_statement!.personal_statement_text" rows="7" maxlength="1200" placeholder="请简要描述个人经历、申请上海人工智能实验室联培博士生项目的原因以及未来规划等" />
          <small class="textarea-counter">已输入 {{ (form.personal_statement!.personal_statement_text || '').length }}/1200</small>
        </label>
        <label class="section-grid__full"><span>你认为目前 AI 技术发展过程中还未被解决的，且你未来希望去作为科研目标解决的最重要问题是什么？</span><textarea v-model="form.personal_statement!.ai_problem_statement" rows="5" placeholder="选填，请填写你最关注、未来希望作为科研目标解决的 AI 关键问题" /></label>
        <label class="section-grid__full"><span>请陈述一个目前 AI 行业基本形成共识，但你不同意的观点，可以适当展开</span><textarea v-model="form.personal_statement!.ai_industry_opinion" rows="5" placeholder="选填，请填写你不同意的行业共识观点及理由" /></label>
      </div>

      <div class="upload-card">
        <span><span class="required-mark">*</span>个人简历附件</span>
        <a
          v-if="form.personal_statement!.resume_attachment_url"
          class="upload-link-input"
          :href="form.personal_statement!.resume_attachment_url"
          :target="isPreviewableAttachment(form.personal_statement!.resume_attachment_name, form.personal_statement!.resume_attachment_url) ? '_blank' : undefined"
          :rel="isPreviewableAttachment(form.personal_statement!.resume_attachment_name, form.personal_statement!.resume_attachment_url) ? 'noopener noreferrer' : undefined"
          :download="isPreviewableAttachment(form.personal_statement!.resume_attachment_name, form.personal_statement!.resume_attachment_url) ? undefined : (resolveAttachmentDisplayName(form.personal_statement!.resume_attachment_url, form.personal_statement!.resume_attachment_name, '个人简历附件') || true)"
          :title="resolveAttachmentDisplayName(form.personal_statement!.resume_attachment_url, form.personal_statement!.resume_attachment_name, '个人简历附件')"
        >{{ resolveAttachmentDisplayName(form.personal_statement!.resume_attachment_url, form.personal_statement!.resume_attachment_name, '个人简历附件') }}</a>
        <input v-else :value="''" readonly placeholder="支持 PDF / Word 简历" />
        <input
          class="upload-file"
          type="file"
          :disabled="isAttachmentUploading(buildAttachmentUploadKey('statement', 0, 'resume'))"
          :accept="resumeAttachmentAccept"
          @change="handleResumeAttachmentUpload"
        />
        <small>{{ isAttachmentUploading(buildAttachmentUploadKey('statement', 0, 'resume')) ? '上传中...' : '支持 PDF/DOC/DOCX，单个文件不超过 20MB；PDF 可在线预览，Word 文件将直接下载' }}</small>
      </div>

      <div class="upload-card">
        <span>其他支撑材料（选填）</span>
        <a
          v-if="form.personal_statement!.supporting_material_attachment_url"
          class="upload-link-input"
          :href="form.personal_statement!.supporting_material_attachment_url"
          target="_blank"
          rel="noopener noreferrer"
          :title="resolveAttachmentDisplayName(form.personal_statement!.supporting_material_attachment_url, form.personal_statement!.supporting_material_attachment_name, '其他支撑材料')"
        >{{ resolveAttachmentDisplayName(form.personal_statement!.supporting_material_attachment_url, form.personal_statement!.supporting_material_attachment_name, '其他支撑材料') }}</a>
        <input v-else :value="''" readonly placeholder="建议上传 zip 压缩包，单文件上传" />
        <input
          class="upload-file"
          type="file"
          :disabled="isAttachmentUploading(buildAttachmentUploadKey('statement', 0, 'supporting-material'))"
          :accept="supportingMaterialAttachmentAccept"
          @change="handleSupportingMaterialAttachmentUpload"
        />
        <small>{{ isAttachmentUploading(buildAttachmentUploadKey('statement', 0, 'supporting-material')) ? '上传中...' : '建议使用 ZIP 压缩包，也支持 PDF/DOC/DOCX/JPG/PNG/WEBP，单个文件不超过 20MB' }}</small>
      </div>

      <label class="agreement-row">
        <input v-model="form.declaration!.has_read_declaration" type="checkbox" />
        <span class="agreement-row__text"><span class="required-mark">*</span>本表及证明材料仅作为申请上海人工智能实验室联培博士项目的参考依据，并承诺提交材料的所有内容均真实、准确、完整。所提供的材料中如有任何不实信息，将被取消录取资格。</span>
      </label>

      <div class="submit-row">
        <button type="button" class="submit-button" :disabled="submitting" @click="submitForm">{{ submitting ? '提交中...' : '提交申请表' }}</button>
      </div>
    </div>
  </section>
</template>

<style scoped>
.section-page {
  display: grid;
  gap: 20px;
}

.section-card {
  padding: 24px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 18px 44px rgba(28, 70, 137, 0.08);
}

.section-intro {
  display: grid;
  gap: 8px;
  margin-bottom: 18px;
  color: #4b607d;
}

.section-intro strong {
  color: #173459;
}

.section-intro p {
  margin: 0;
  line-height: 1.7;
}

.upload-card small {
  color: #627896;
  font-size: 12px;
}

.textarea-counter {
  justify-self: end;
  color: #627896;
  font-size: 12px;
}

.required-mark {
  margin-right: 4px;
  color: #e34d59;
  font-style: normal;
  font-weight: 700;
}

.section-grid {
  display: grid;
  gap: 16px;
}

.section-grid label,
.upload-card {
  display: grid;
  gap: 8px;
  color: #4b607d;
}

.section-grid textarea,
.upload-card input,
.upload-link-input {
  width: 100%;
  min-height: 52px;
  padding: 10px 14px;
  border: 1px solid #d6e0ee;
  border-radius: 14px;
  background: #fff;
}

.upload-link-input {
  display: flex;
  align-items: center;
  color: #173459;
  text-decoration: none;
  word-break: break-all;
}

.upload-link-input:hover {
  border-color: rgba(20, 75, 147, 0.38);
  background: rgba(236, 245, 255, 0.72);
}

.section-grid textarea {
  min-height: 138px;
}

.upload-card {
  margin-top: 18px;
  padding: 18px;
  border-radius: 18px;
  background: #f8fbff;
  border: 1px solid rgba(145, 170, 209, 0.24);
}

.agreement-row {
  display: flex;
  gap: 12px;
  align-items: center;
  margin-top: 18px;
  color: #4b607d;
  line-height: 1.7;
}

.agreement-row__text {
  display: block;
  flex: 1 1 auto;
}

.agreement-row input {
  margin: 0;
  flex: 0 0 auto;
  align-self: center;
}

.submit-row {
  display: flex;
  justify-content: flex-end;
  margin-top: 18px;
}

.submit-button {
  min-height: 46px;
  padding: 0 24px;
  border: none;
  border-radius: 12px;
  background: linear-gradient(135deg, #154383, #144b93 58%, #2eb1e8);
  color: #fff;
  font-weight: 700;
}
</style>