<script setup lang="ts">
import type { PortalApplicationUpsert } from '../../../../api/portal'

defineProps<{
  form: PortalApplicationUpsert
  addPractice: () => void
  removePractice: (index: number) => void
}>()
</script>

<template>
  <section class="section-page">
    <div class="toolbar-card">
      <div>
        <strong>实践经历列表</strong>
      </div>
      <button type="button" class="action-button" @click="addPractice">新增实践经历</button>
    </div>

    <div v-if="!(form.practice_experiences && form.practice_experiences.length)" class="empty-card">当前未填写实践经历，可留空提交。</div>

    <div class="record-list">
      <section v-for="(item, index) in form.practice_experiences" :key="`practice-${index}`" class="record-card">
        <div class="record-card__header">
          <div><strong>实践经历 {{ index + 1 }}</strong><span>非必填</span></div>
          <button type="button" class="link-button" @click="removePractice(index)">删除</button>
        </div>

        <div class="section-grid">
          <label><span>开始年月</span><input v-model="item.start_month" type="month" /></label>
          <label><span>结束年月</span><input v-model="item.end_month" type="month" /></label>
          <label><span>实习实践/工作单位</span><input v-model="item.organization_name" placeholder="请输入实习实践/工作单位" /></label>
          <label><span>岗位</span><input v-model="item.position_name" placeholder="请输入岗位" /></label>
          <label><span><span class="required-mark">*</span>证明人姓名</span><input v-model="item.verifier_name" placeholder="请输入证明人姓名" /></label>
          <label><span><span class="required-mark">*</span>证明人手机</span><input v-model="item.verifier_phone" placeholder="请输入证明人手机" /></label>
          <label class="section-grid__full"><span>职责</span><textarea v-model="item.responsibility_text" rows="5" placeholder="请输入职责、项目内容或实践成果" /></label>
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