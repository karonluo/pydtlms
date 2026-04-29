<script setup lang="ts">
import type { PortalApplicationUpsert } from '../../../../api/portal'

defineProps<{
  form: PortalApplicationUpsert
  familyRelationOptions: string[]
  addFamilyMember: () => void
  removeFamilyMember: (index: number) => void
}>()
</script>

<template>
  <section class="section-page">
    <div class="toolbar-card">
      <div>
        <strong>家庭成员</strong>
        <span>父母信息至少填写一方，其他成员可按需补充。</span>
      </div>
      <button type="button" class="action-button" @click="addFamilyMember">新增家庭成员</button>
    </div>

    <div class="record-list">
      <section v-for="(item, index) in form.family_members" :key="`family-${index}`" class="record-card">
        <div class="record-card__header">
          <div><strong>家庭成员 {{ index + 1 }}</strong><span>{{ item.relation_type || '请选择关系' }}</span></div>
          <button v-if="(form.family_members?.length || 0) > 2" type="button" class="link-button" @click="removeFamilyMember(index)">删除</button>
        </div>

        <div class="section-grid">
          <label><span>与本人关系</span><select v-model="item.relation_type"><option value="">请选择</option><option v-for="relation in familyRelationOptions" :key="relation" :value="relation">{{ relation }}</option></select></label>
          <label><span>姓名</span><input v-model="item.member_name" placeholder="请输入姓名" /></label>
          <label><span>联系电话</span><input v-model="item.contact_phone" placeholder="请输入联系电话" /></label>
          <label><span>工作单位</span><input v-model="item.employer_name" placeholder="请输入工作单位" /></label>
          <label><span>职务</span><input v-model="item.job_title" placeholder="请输入职务" /></label>
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
.toolbar-card span {
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
.section-grid select {
  width: 100%;
  min-height: 46px;
  padding: 10px 14px;
  border: 1px solid #d6e0ee;
  border-radius: 14px;
  background: #fff;
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