<script setup lang="ts">
import type { PortalApplicationUpsert } from '../../../../api/portal'

defineProps<{
  form: PortalApplicationUpsert
  resumeAttachmentAccept: string
  isAttachmentUploading: (key: string) => boolean
  buildAttachmentUploadKey: (section: string, index: number | string, field: string) => string
  handleResumeAttachmentUpload: (event: Event) => void | Promise<void>
  submitForm: () => void | Promise<void>
  submitting: boolean
}>()
</script>

<template>
  <section class="section-page">
    <div class="section-card">
      <div class="section-grid">
        <label class="section-grid__full"><span><span class="required-mark">*</span>个人陈述</span><textarea v-model="form.personal_statement!.personal_statement_text" rows="7" placeholder="请输入申请动机、研究基础与职业规划" /></label>
        <label class="section-grid__full"><span>AI 关键问题思考</span><textarea v-model="form.personal_statement!.ai_problem_statement" rows="6" placeholder="请输入你关注的 AI 关键问题" /></label>
        <label class="section-grid__full"><span>AI 行业不同观点</span><textarea v-model="form.personal_statement!.ai_industry_opinion" rows="6" placeholder="请输入你对行业议题的不同观点或补充说明" /></label>
      </div>

      <div class="upload-card">
        <span>个人简历附件</span>
        <input :value="form.personal_statement!.resume_attachment_url || ''" readonly placeholder="支持 PDF / Word 简历" />
        <input
          class="upload-file"
          type="file"
          :disabled="isAttachmentUploading(buildAttachmentUploadKey('statement', 0, 'resume'))"
          :accept="resumeAttachmentAccept"
          @change="handleResumeAttachmentUpload"
        />
        <small>{{ isAttachmentUploading(buildAttachmentUploadKey('statement', 0, 'resume')) ? '上传中...' : '支持 PDF/DOC/DOCX，单个文件不超过 20MB' }}</small>
      </div>

      <label class="agreement-row">
        <input v-model="form.declaration!.has_read_declaration" type="checkbox" />
        <span class="agreement-row__text"><span class="required-mark">*</span>{{ form.declaration!.declaration_text || '我已同意并仔细阅读使用条款和隐私政策。' }}</span>
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

.upload-card small {
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
.upload-card input {
  width: 100%;
  min-height: 52px;
  padding: 10px 14px;
  border: 1px solid #d6e0ee;
  border-radius: 14px;
  background: #fff;
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
  align-items: flex-start;
  margin-top: 18px;
  color: #4b607d;
  line-height: 1.7;
}

.agreement-row__text {
  display: inline-flex;
  align-items: flex-start;
  flex-wrap: wrap;
}

.agreement-row input {
  margin-top: 4px;
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