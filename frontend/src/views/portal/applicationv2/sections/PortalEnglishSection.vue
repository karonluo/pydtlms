<script setup lang="ts">
import type { PortalApplicationUpsert } from '../../../../api/portal'

defineProps<{
  form: PortalApplicationUpsert
  englishExamOptions: string[]
  certificateAttachmentAccept: string
  isAttachmentUploading: (key: string) => boolean
  buildAttachmentUploadKey: (section: string, index: number | string, field: string) => string
  handleEnglishAttachmentUpload: (index: number, event: Event) => void | Promise<void>
  addEnglish: () => void
  removeEnglish: (index: number) => void | Promise<void>
}>()
</script>

<template>
  <section class="section-page">
    <div class="toolbar-card">
      <div>
        <strong>英语能力列表</strong>
        <span>该章节必填，请至少填写 1 条英语考试记录并上传英语证明附件。</span>
      </div>
      <button type="button" class="action-button" @click="addEnglish">新增英语成绩</button>
    </div>

    <div class="record-list">
      <section v-for="(item, index) in form.english_proficiencies" :key="`english-${index}`" class="record-card">
        <div class="record-card__header">
          <div><strong>英语成绩 {{ index + 1 }}</strong><span>支持多条</span></div>
          <button v-if="(form.english_proficiencies?.length || 0) > 1" type="button" class="link-button" @click="removeEnglish(index)">删除</button>
        </div>

        <div class="section-grid">
          <label><span>英语考试名称</span><select v-model="item.exam_name"><option value="">请选择</option><option v-for="exam in englishExamOptions" :key="exam" :value="exam">{{ exam }}</option></select></label>
          <label><span>成绩</span><input v-model="item.score_text" placeholder="请输入成绩" /></label>
        </div>

        <div class="upload-card">
          <span>英语证明附件</span>
          <input :value="item.certificate_attachment_url || ''" readonly placeholder="英语证明附件必传" />
          <input
            class="upload-file"
            type="file"
            :disabled="isAttachmentUploading(buildAttachmentUploadKey('english', index, 'certificate'))"
            :accept="certificateAttachmentAccept"
            @change="handleEnglishAttachmentUpload(index, $event)"
          />
          <small>{{ isAttachmentUploading(buildAttachmentUploadKey('english', index, 'certificate')) ? '上传中...' : '支持 PDF/JPG/PNG/WEBP，单个文件不超过 20MB' }}</small>
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
.record-card,
.empty-card {
  padding: 24px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 18px 44px rgba(28, 70, 137, 0.08);
}

.record-card__header span,
.toolbar-card span,
.upload-card small,
.empty-card {
  color: #627896;
  font-size: 12px;
}

.toolbar-card strong,
.record-card__header strong {
  margin: 0;
  color: #173459;
}

.toolbar-card,
.record-card__header {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 12px;
  align-items: center;
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
.upload-card input {
  width: 100%;
  min-height: 46px;
  padding: 10px 14px;
  border: 1px solid #d6e0ee;
  border-radius: 14px;
  background: #fff;
}

.upload-card {
  margin-top: 18px;
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
  .section-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 720px) {
  .toolbar-card,
  .record-card__header,
  .section-grid {
    grid-template-columns: 1fr;
  }
}
</style>