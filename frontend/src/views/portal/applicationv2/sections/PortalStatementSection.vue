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
        <p>请围绕“个人成长经历、为何申报本项目或本专业、未来职业发展规划”三个主题填写。个人陈述总字数需控制在 800-1200 字，中英文皆可。</p>
      </div>

      <div class="section-grid">
        <label class="section-grid__full"><span><span class="required-mark">*</span>个人成长经历</span><textarea v-model="form.personal_statement!.growth_experience_text" rows="6" placeholder="请结合学习、科研、实践或重要阶段经历进行说明" /></label>
        <label class="section-grid__full"><span><span class="required-mark">*</span>为何申报本项目或本专业</span><textarea v-model="form.personal_statement!.program_application_reason_text" rows="6" placeholder="请说明申报动机、研究兴趣、与项目方向的匹配度等" /></label>
        <label class="section-grid__full"><span><span class="required-mark">*</span>未来职业发展规划</span><textarea v-model="form.personal_statement!.career_plan_text" rows="6" placeholder="请说明未来职业目标、发展路径和阶段规划" /></label>
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