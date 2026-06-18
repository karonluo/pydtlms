<script setup lang="ts">
defineOptions({ inheritAttrs: false })

defineProps<{
  title: string
  value: string
  description?: string
  status: 'healthy' | 'attention' | 'warning'
  icon?: unknown
}>()
</script>

<template>
  <article class="kpi-card page-card" :data-status="status" v-bind="$attrs">
    <div class="kpi-card__top">
      <div class="kpi-card__icon">
        <el-icon v-if="icon"><component :is="icon" /></el-icon>
      </div>
      <strong class="kpi-card__value">{{ value }}</strong>
    </div>
    <p class="kpi-card__title">{{ title }}</p>
  </article>
</template>

<style scoped>
.kpi-card {
  display: flex;
  min-height: 111px;
  flex-direction: column;
  justify-content: space-between;
  gap: 3px;
  padding: 12px 16px;
}

.kpi-card__top {
  display: flex;
  align-items: center;
  gap: 8px;
}

.kpi-card__icon {
  display: grid;
  place-items: center;
  width: 42px;
  height: 42px;
  border-radius: 12px;
  background: var(--brand);
  color: #ffffff;
  font-size: 18px;
  box-shadow: 0 10px 22px rgba(34, 166, 238, 0.22);
}

.kpi-card[data-status='attention'] .kpi-card__icon {
  background: #f2a531;
  box-shadow: 0 10px 22px rgba(242, 165, 49, 0.22);
}

.kpi-card[data-status='warning'] .kpi-card__icon {
  background: #ea725b;
  box-shadow: 0 10px 22px rgba(234, 114, 91, 0.22);
}

.kpi-card__title {
  margin: 0;
  color: var(--text-subtle);
  font-size: 13px;
  line-height: 1.25;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.kpi-card__value {
  display: block;
  margin: 0;
  color: var(--text-main);
  font-family: var(--title-font);
  font-size: 26px;
}
</style>
