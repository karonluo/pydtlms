<script setup lang="ts">
import type { PortalApplicationUpsert } from '../../../../api/portal'

defineProps<{
  form: PortalApplicationUpsert
  achievementTypeOptions: string[]
  addAchievement: () => void
  removeAchievement: (index: number) => void
}>()
</script>

<template>
  <section class="section-page">
    <div class="toolbar-card">
      <div>
        <strong>成果记录</strong>
        <span>支持论文、科研项目、学生活动和获奖经历。</span>
      </div>
      <button type="button" class="action-button" @click="addAchievement">新增成果记录</button>
    </div>

    <div v-if="!(form.achievement_records && form.achievement_records.length)" class="empty-card">当前未填写论文或获奖经历，可留空提交。</div>

    <div v-else class="record-list">
      <section v-for="(item, index) in form.achievement_records" :key="`achievement-${index}`" class="record-card">
        <div class="record-card__header">
          <div><strong>成果记录 {{ index + 1 }}</strong><span>非必填</span></div>
          <button type="button" class="link-button" @click="removeAchievement(index)">删除</button>
        </div>

        <div class="section-grid">
          <label><span>类型</span><select v-model="item.achievement_type"><option value="">请选择</option><option v-for="type in achievementTypeOptions" :key="type" :value="type">{{ type }}</option></select></label>
          <label><span>论文名称</span><input v-model="item.paper_title" placeholder="论文发表时填写" /></label>
          <label><span>作者序位</span><input v-model="item.author_order" placeholder="如 第一作者" /></label>
          <label><span>期刊/会议名称</span><input v-model="item.journal_or_conference" placeholder="请输入期刊或会议名称" /></label>
          <label><span>发表/收录日期</span><input v-model="item.publish_or_index_month" type="month" /></label>
          <label><span>奖项名称</span><input v-model="item.award_name" placeholder="获奖时填写" /></label>
          <label><span>颁发机构</span><input v-model="item.awarding_organization" placeholder="请输入颁发机构" /></label>
          <label><span>获奖等级</span><input v-model="item.award_level" placeholder="如 全国一等奖" /></label>
          <label><span>获奖年份</span><input v-model="item.award_year" placeholder="如 2025" /></label>
          <label class="section-grid__full"><span>职责内容</span><textarea v-model="item.responsibility_text" rows="5" placeholder="请输入成果说明、职责或获奖背景" /></label>
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

.section-grid label {
  display: grid;
  gap: 8px;
  color: #4b607d;
}

.section-grid input,
.section-grid select,
.section-grid textarea {
  width: 100%;
  min-height: 46px;
  padding: 10px 14px;
  border: 1px solid #d6e0ee;
  border-radius: 14px;
  background: #fff;
}

.section-grid textarea {
  min-height: 120px;
}

.section-grid__full {
  grid-column: 1 / -1;
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