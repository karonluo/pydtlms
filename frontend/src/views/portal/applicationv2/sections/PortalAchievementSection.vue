<script setup lang="ts">
import type { PortalApplicationUpsert } from '../../../../api/portal'

function trimText(value: string | null | undefined) {
  return String(value || '').trim()
}

function isPaperAchievement(type: string | null | undefined) {
  return trimText(type) === '论文发表'
}

function isAwardAchievement(type: string | null | undefined) {
  return trimText(type) === '获奖经历'
}

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

defineProps<{
  form: PortalApplicationUpsert
  achievementTypeOptions: string[]
  achievementAwardAttachmentAccept: string
  isAttachmentUploading: (key: string) => boolean
  buildAttachmentUploadKey: (section: string, index: number | string, field: string) => string
  addAchievement: () => void | Promise<void>
  handleAchievementTypeChange: (index: number) => void
  handleAchievementAwardAttachmentUpload: (index: number, event: Event) => void | Promise<void>
  removeAchievement: (index: number) => void
}>()
</script>

<template>
  <section class="section-page">
    <div class="toolbar-card">
      <div>
        <strong>成果经历</strong>
      </div>
      <p class="toolbar-card__hint">成果经历非必填，如有则填写论文发表与获奖经历，最多填写4条。若超过4条可在个人陈述与补充材料中体现。</p>
      <button type="button" class="action-button" @click="addAchievement">新增成果经历</button>
    </div>

    <div v-if="!(form.achievement_records && form.achievement_records.length)" class="empty-card">当前未填写成果经历，可留空提交。</div>

    <div v-else class="record-list">
      <section v-for="(item, index) in form.achievement_records" :key="`achievement-${index}`" class="record-card">
        <div class="record-card__header">
          <div><strong>成果经历 {{ index + 1 }}</strong><span>非必填</span></div>
          <button type="button" class="link-button" @click="removeAchievement(index)">删除</button>
        </div>

        <div class="section-grid">
          <label>
            <span>类型</span>
            <select v-model="item.achievement_type" @change="handleAchievementTypeChange(index)">
              <option value="">请选择</option>
              <option v-for="type in achievementTypeOptions" :key="type" :value="type">{{ type }}</option>
            </select>
          </label>
          <label><span>日期</span><input v-model="item.achievement_month" type="month" /></label>

          <template v-if="isPaperAchievement(item.achievement_type)">
            <label><span>论文名称</span><input v-model="item.paper_title" placeholder="请输入论文名称" /></label>
            <label><span>作者序位</span><input v-model="item.author_order" placeholder="如 第一作者" /></label>
            <label class="section-grid__full"><span>期刊名称</span><input v-model="item.journal_or_conference" placeholder="请输入期刊名称" /></label>
            <label class="section-grid__full"><span>描述</span><textarea v-model="item.description_text" rows="5" placeholder="请输入论文发表相关说明" /></label>
          </template>

          <template v-else-if="isAwardAchievement(item.achievement_type)">
            <label><span>奖项名称</span><input v-model="item.award_name" placeholder="请输入奖项名称" /></label>
            <label><span>获奖名次</span><input v-model="item.award_rank" placeholder="如 一等奖 / 第1名" /></label>
            <div class="upload-card section-grid__full">
              <span>获奖证明上传</span>
              <a
                v-if="item.award_certificate_attachment_url"
                class="upload-link-input"
                :href="item.award_certificate_attachment_url"
                target="_blank"
                rel="noopener noreferrer"
                :title="resolveAttachmentDisplayName(item.award_certificate_attachment_url, item.award_certificate_attachment_name, '获奖证明')"
              >{{ resolveAttachmentDisplayName(item.award_certificate_attachment_url, item.award_certificate_attachment_name, '获奖证明') }}</a>
              <input v-else :value="''" readonly placeholder="请上传获奖证明附件" />
              <input
                class="upload-file"
                type="file"
                :accept="achievementAwardAttachmentAccept"
                :disabled="isAttachmentUploading(buildAttachmentUploadKey('achievement', index, 'award-certificate'))"
                @change="handleAchievementAwardAttachmentUpload(index, $event)"
              />
              <small>{{ isAttachmentUploading(buildAttachmentUploadKey('achievement', index, 'award-certificate')) ? '上传中...' : '支持 PDF/JPG/PNG/WEBP，单个文件不超过 20MB' }}</small>
            </div>
            <label class="section-grid__full"><span>描述</span><textarea v-model="item.description_text" rows="5" placeholder="请输入获奖背景或成果说明" /></label>
          </template>

          <p v-else class="section-grid__full section-hint">请选择成果类型后再填写对应字段。</p>
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
.empty-card {
  color: #627896;
  font-size: 12px;
}

.toolbar-card__hint {
  margin: 0;
  color: #627896;
  font-size: 12px;
  line-height: 1.6;
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

.toolbar-card {
  grid-template-columns: auto minmax(0, 1fr) auto;
}

.section-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
  margin-top: 18px;
}

.section-grid label {
  display: grid;
  gap: 8px;
  color: #4b607d;
}

.section-grid input,
.section-grid select,
.section-grid textarea,
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

.section-grid textarea {
  min-height: 120px;
}

.section-grid__full {
  grid-column: 1 / -1;
}

.upload-card {
  display: grid;
  gap: 10px;
  padding: 18px;
  border: 1px dashed #cbdcf5;
  border-radius: 18px;
  background: #f8fbff;
  color: #4b607d;
}

.upload-card small,
.section-hint {
  color: #627896;
  font-size: 12px;
}

.upload-file {
  padding: 0;
  border: none;
  background: transparent;
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