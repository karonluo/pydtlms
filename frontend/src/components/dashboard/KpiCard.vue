<script setup lang="ts">
defineProps<{
  title: string
  value: string
  description: string
  status: 'healthy' | 'attention' | 'warning'
  icon?: unknown
}>()
</script>

<template>
  <article class="kpi-card page-card" :data-status="status">
    <div class="kpi-card__icon">
      <el-icon v-if="icon"><component :is="icon" /></el-icon>
    </div>
    <div class="kpi-card__body">
      <p class="kpi-card__title">{{ title }}</p>
      <strong class="kpi-card__value">{{ value }}</strong>
      <p class="kpi-card__description">{{ description }}</p>
    </div>
  </article>
</template>

<style scoped>
.kpi-card {
  display: grid;
  grid-template-columns: 46px minmax(0, 1fr);
  gap: 12px;
  align-items: start;
  padding: 16px;
}

.kpi-card__icon {
  display: grid;
  place-items: center;
  width: 46px;
  height: 46px;
  border-radius: 14px;
  background: var(--brand);
  color: #ffffff;
  font-size: 20px;
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

.kpi-card__title,
.kpi-card__description {
  margin: 0;
}

.kpi-card__title {
  color: var(--text-subtle);
  font-size: 13px;
}

.kpi-card__value {
  display: block;
  margin: 2px 0 4px;
  color: var(--text-main);
  font-family: var(--title-font);
  font-size: 28px;
}

.kpi-card__description {
  color: var(--text-subtle);
  font-size: 12px;
}
</style>
