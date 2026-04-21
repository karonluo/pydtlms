<script setup lang="ts">
import type { PortalApplicationPreferenceItem, PortalApplicationUpsert, PortalTeamRecord } from '../../../../api/portal'

defineProps<{
  form: PortalApplicationUpsert
  teams: PortalTeamRecord[]
  sourceChannelOptions: string[]
  canAddPreference: boolean
  addPreference: () => void
  removePreference: (index: number) => void
  advisorsForCenter: (centerName: string) => string[]
  handlePreferenceCenterChange: (item: PortalApplicationPreferenceItem) => void
}>()
</script>

<template>
  <section class="section-page">
    <div class="section-card">
      <div class="section-grid">
        <label>
          <span>了解项目方式</span>
          <select v-model="form.source_channel">
            <option value="">请选择</option>
            <option v-for="item in sourceChannelOptions" :key="item" :value="item">{{ item }}</option>
          </select>
        </label>
        <label v-if="form.source_channel === '其他'" class="section-grid__wide">
          <span><span class="required-mark">*</span>其他说明</span>
          <input v-model="form.source_channel_other" placeholder="请补充获知渠道" />
        </label>
      </div>
    </div>

    <div class="toolbar-card">
      <div>
        <strong>研究中心志愿</strong>
        <span>默认保留第一志愿，可追加第二志愿。</span>
      </div>
      <button type="button" class="action-button" :disabled="!canAddPreference" @click="addPreference">添加第二志愿</button>
    </div>

    <div class="record-list">
      <section v-for="(item, index) in form.preferences" :key="`preference-${index}`" class="record-card">
        <div class="record-card__header">
          <div>
            <strong>第 {{ item.preference_order }} 志愿</strong>
            <span>{{ index === 0 ? '必填' : '选填' }}</span>
          </div>
          <button v-if="index > 0" type="button" class="link-button" @click="removePreference(index)">删除</button>
        </div>

        <div class="section-grid">
          <label>
            <span><span v-if="index === 0" class="required-mark">*</span>研究中心</span>
            <select v-model="item.research_center_name" @change="handlePreferenceCenterChange(item)">
              <option value="">请选择研究中心</option>
              <option v-for="team in teams" :key="team.id" :value="team.team_name">{{ team.team_name }}</option>
            </select>
          </label>
          <label>
            <span>意向导师</span>
            <select v-model="item.advisor_name">
              <option value="">请选择导师</option>
              <option v-for="advisor in advisorsForCenter(item.research_center_name)" :key="advisor" :value="advisor">{{ advisor }}</option>
            </select>
          </label>
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

.section-card,
.toolbar-card,
.record-card {
  padding: 24px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 18px 44px rgba(28, 70, 137, 0.08);
}

.record-card__header span,
.toolbar-card span {
  color: #627896;
  font-size: 12px;
}

.toolbar-card strong,
.record-card__header strong {
  margin: 0;
  color: #173459;
}

.required-mark {
  margin-right: 4px;
  color: #e34d59;
  font-style: normal;
  font-weight: 700;
}

.section-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
}

.section-grid label {
  display: grid;
  gap: 8px;
  color: #4b607d;
}

.section-grid__wide {
  grid-column: span 2;
}

.section-grid input,
.section-grid select {
  width: 100%;
  min-height: 46px;
  padding: 10px 14px;
  border: 1px solid #d6e0ee;
  border-radius: 14px;
  background: #fff;
}

.toolbar-card,
.record-card__header {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 12px;
  align-items: center;
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
  .section-grid,
  .toolbar-card,
  .record-card__header {
    grid-template-columns: 1fr;
  }

  .section-grid__wide {
    grid-column: auto;
  }
}
</style>