<script setup lang="ts">
import type { PortalApplicationUpsert } from '../../../../api/portal'

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
        <strong>个人陈述与附件</strong>
        <p>请按以下三个问题填写个人陈述内容，其中第 1 题必填，第 2、3 题选填。</p>
      </div>

      <div class="section-grid">
        <label class="section-grid__full"><span><span class="required-mark">*</span>1. 个人成长经历、自我个性描述、为何申报本项目或本专业以及未来职业发展规划等</span><textarea v-model="form.personal_statement!.personal_statement_text" rows="6" placeholder="请填写个人成长经历、自我个性描述、申报动机及未来职业发展规划等内容" /></label>
        <label class="section-grid__full"><span>2. 你认为目前AI技术发展过程中还未被解决的，且你未来希望去作为科研目标解决的最重要问题是什么？（选填）</span><textarea v-model="form.personal_statement!.ai_problem_statement" rows="6" placeholder="请输入你希望未来作为科研目标解决的重要问题" /></label>
        <label class="section-grid__full"><span>3. 请陈述一个目前AI行业基本形成共识，但你不同意的观点，可以适当展开。（选填）</span><textarea v-model="form.personal_statement!.ai_industry_opinion" rows="6" placeholder="请输入你不同意的 AI 行业共识观点及说明" /></label>
      </div>

      <div class="upload-card">
        <span><span class="required-mark">*</span>个人简历附件</span>
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

      <div class="upload-card">
        <span>其他支撑材料（选填）</span>
        <input :value="form.personal_statement!.supporting_material_attachment_url || ''" readonly placeholder="建议上传 zip 压缩包，单文件上传" />
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
        <span class="agreement-row__text"><span class="required-mark">*</span>{{ form.declaration!.declaration_text || declarationReminderText }}</span>
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
  margin-top: 0;
  flex: 0 0 auto;
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
