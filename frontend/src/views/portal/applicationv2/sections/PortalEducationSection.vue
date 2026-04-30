<script setup lang="ts">
import { computed } from 'vue'
import type { PortalApplicationUpsert, PortalEducationExperienceItem } from '../../../../api/portal'

const props = defineProps<{
  form: PortalApplicationUpsert
  getEducationStageOptions: (index: number) => string[]
  certificateAttachmentAccept: string
  isAttachmentUploading: (key: string) => boolean
  buildAttachmentUploadKey: (section: string, index: number | string, field: string) => string
  handleEducationAttachmentUpload: (index: number, field: 'transcript' | 'degree_certificate' | 'graduation_certificate', event: Event) => void | Promise<void>
  handleEducationStageChange: (item: PortalEducationExperienceItem) => void
  addEducation: () => void
  removeEducation: (index: number) => void
}>()

const displayedEducationItems = computed(() => (props.form.education_experiences || [])
  .map((item, actualIndex) => ({ item, actualIndex }))
  .reverse())
</script>

<template>
  <section class="section-page">
    <div class="toolbar-card">
      <div>
        <strong>教育经历列表</strong>
      </div>
      <p class="toolbar-card__hint">请按最高学历到高中的顺序填写，默认包含高中经历，最多填写 3 条教育经历。</p>
      <button type="button" class="action-button" @click="addEducation">新增教育经历</button>
    </div>

    <div class="record-list">
      <section v-for="({ item, actualIndex }) in displayedEducationItems" :key="`education-${actualIndex}`" class="record-card">
        <div class="record-card__header">
          <div><strong>教育经历 {{ actualIndex + 1 }}</strong></div>
          <button v-if="actualIndex > 0" type="button" class="link-button" @click="removeEducation(actualIndex)">删除</button>
        </div>

        <div class="section-grid">
          <label><span><span v-if="actualIndex < 2" class="required-mark">*</span>教育阶段</span><select v-model="item.education_stage" @change="handleEducationStageChange(item)"><option value="">请选择</option><option v-for="stage in getEducationStageOptions(actualIndex)" :key="stage" :value="stage">{{ stage }}</option></select></label>
          <label><span><span class="required-mark">*</span>开始年月</span><input v-model="item.start_month" type="month" /></label>
          <label><span><span v-if="!item.education_stage.endsWith('在读')" class="required-mark">*</span>结束年月</span><input v-model="item.end_month" type="month" /></label>
          <label><span><span v-if="actualIndex < 2" class="required-mark">*</span>就读学校</span><input v-model="item.school_name" placeholder="请输入就读学校" /></label>
          <label v-if="item.education_stage !== '高中毕业'"><span><span class="required-mark">*</span>就读专业</span><input v-model="item.major_name" placeholder="请输入就读专业" /></label>
          <label v-if="item.education_stage !== '高中毕业'"><span><span class="required-mark">*</span>期间平均成绩</span><input v-model="item.average_score" placeholder="如 88.5" /></label>
          <label v-if="item.education_stage !== '高中毕业'"><span><span class="required-mark">*</span>期间绩点</span><input v-model="item.gpa" placeholder="如 3.7/4.0" /></label>
          <label v-if="item.education_stage !== '高中毕业'"><span><span class="required-mark">*</span>成绩排名</span><input v-model="item.ranking" placeholder="如 5/120" /></label>
          <label><span><span class="required-mark">*</span>证明人姓名</span><input v-model="item.verifier_name" placeholder="请输入证明人姓名" /></label>
          <label><span><span class="required-mark">*</span>证明人手机</span><input v-model="item.verifier_phone" placeholder="请输入证明人手机" /></label>
        </div>

        <div class="upload-grid">
          <div v-if="item.education_stage !== '高中毕业'" class="upload-card">
            <span>成绩单附件</span>
            <a
              v-if="item.transcript_attachment_url && item.transcript_attachment_name"
              class="upload-link-input"
              :href="item.transcript_attachment_url"
              target="_blank"
              rel="noopener noreferrer"
              :title="item.transcript_attachment_name || ''"
            >{{ item.transcript_attachment_name }}</a>
            <input v-else :value="''" readonly placeholder="未上传时不可提交" />
            <input
              class="upload-file"
              type="file"
              :disabled="isAttachmentUploading(buildAttachmentUploadKey('education', actualIndex, 'transcript'))"
              :accept="certificateAttachmentAccept"
              @change="handleEducationAttachmentUpload(actualIndex, 'transcript', $event)"
            />
            <small>{{ isAttachmentUploading(buildAttachmentUploadKey('education', actualIndex, 'transcript')) ? '上传中...' : '必传；支持 PDF/JPG/PNG/WEBP，单个文件不超过 20MB' }}</small>
          </div>
          <div v-if="item.education_stage !== '高中毕业' && item.education_stage.endsWith('毕业')" class="upload-card">
            <span>学位证附件</span>
            <a
              v-if="item.degree_certificate_attachment_url && item.degree_certificate_attachment_name"
              class="upload-link-input"
              :href="item.degree_certificate_attachment_url"
              target="_blank"
              rel="noopener noreferrer"
              :title="item.degree_certificate_attachment_name || ''"
            >{{ item.degree_certificate_attachment_name }}</a>
            <input v-else :value="''" readonly placeholder="未上传时不可提交" />
            <input
              class="upload-file"
              type="file"
              :disabled="isAttachmentUploading(buildAttachmentUploadKey('education', actualIndex, 'degree_certificate'))"
              :accept="certificateAttachmentAccept"
              @change="handleEducationAttachmentUpload(actualIndex, 'degree_certificate', $event)"
            />
            <small>{{ isAttachmentUploading(buildAttachmentUploadKey('education', actualIndex, 'degree_certificate')) ? '上传中...' : '毕业阶段必传；支持 PDF/JPG/PNG/WEBP，单个文件不超过 20MB' }}</small>
          </div>
          <div v-if="item.education_stage !== '高中毕业' && item.education_stage.endsWith('毕业')" class="upload-card">
            <span>毕业证附件</span>
            <a
              v-if="item.graduation_certificate_attachment_url && item.graduation_certificate_attachment_name"
              class="upload-link-input"
              :href="item.graduation_certificate_attachment_url"
              target="_blank"
              rel="noopener noreferrer"
              :title="item.graduation_certificate_attachment_name || ''"
            >{{ item.graduation_certificate_attachment_name }}</a>
            <input v-else :value="''" readonly placeholder="未上传时不可提交" />
            <input
              class="upload-file"
              type="file"
              :disabled="isAttachmentUploading(buildAttachmentUploadKey('education', actualIndex, 'graduation_certificate'))"
              :accept="certificateAttachmentAccept"
              @change="handleEducationAttachmentUpload(actualIndex, 'graduation_certificate', $event)"
            />
            <small>{{ isAttachmentUploading(buildAttachmentUploadKey('education', actualIndex, 'graduation_certificate')) ? '上传中...' : '毕业阶段必传；支持 PDF/JPG/PNG/WEBP，单个文件不超过 20MB' }}</small>
          </div>
        </div>
      </section>
    </div>
  </section>
</template>

<style scoped>
.section-page,
.record-list {
  display: grid;
  gap: 20px;
}

.toolbar-card,
.record-card {
  padding: 24px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 18px 44px rgba(28, 70, 137, 0.08);
}

.record-card__header span,
.toolbar-card span,
.upload-card small {
  color: #627896;
  font-size: 12px;
}

.toolbar-card strong,
.record-card__header strong {
  margin: 0;
  color: #173459;
}

.toolbar-card__hint {
  margin: 0;
  color: #627896;
  font-size: 12px;
  line-height: 1.6;
}

.toolbar-card .action-button:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.required-mark {
  margin-right: 4px;
  color: #e34d59;
  font-style: normal;
  font-weight: 700;
}

.toolbar-card,
.record-card__header {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 12px;
  align-items: center;
}

.toolbar-card {
  grid-template-columns: auto minmax(0, 1fr) auto;
}

.section-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
  margin-top: 18px;
}

.section-grid label,
.upload-card {
  display: grid;
  gap: 8px;
  color: #4b607d;
}

.section-grid input,
.section-grid select,
.upload-card input,
.upload-link-input {
  width: 100%;
  min-height: 46px;
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

.upload-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
  margin-top: 18px;
}

.upload-card {
  grid-column: span 2;
  padding: 18px;
  border-radius: 18px;
  background: #f8fbff;
  border: 1px solid rgba(145, 170, 209, 0.24);
}

.action-button {
  min-height: 42px;
  padding: 0 18px;
  border: 1px solid #d4e0ef;
  border-radius: 12px;
  background: linear-gradient(180deg, #edf4ff, #dceafe);
  color: #1c4e92;
}

.link-button {
  padding: 0;
  border: none;
  background: transparent;
  color: #c14d58;
}

@media (max-width: 1180px) {
  .section-grid,
  .upload-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .upload-card {
    grid-column: span 1;
  }
}

@media (max-width: 720px) {
  .toolbar-card,
  .record-card__header,
  .section-grid,
  .upload-grid {
    grid-template-columns: 1fr;
  }

  .upload-card {
    grid-column: auto;
  }
}
</style>