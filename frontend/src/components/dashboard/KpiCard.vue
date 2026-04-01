<script setup lang="ts">
defineProps<{
  title: string
  value: string
  description: string
  status: 'healthy' | 'attention' | 'warning'
}>()
</script>

<template>
  <article class="kpi-card" :data-status="status">
    <p class="kpi-card__title">{{ title }}</p>
    <strong class="kpi-card__value">{{ value }}</strong>
    <p class="kpi-card__description">{{ description }}</p>
  </article>
</template>

<style scoped>
.kpi-card {
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(18, 50, 95, 0.08);
  border-radius: 24px;
  padding: 22px;
  background: linear-gradient(160deg, rgba(255, 255, 255, 0.98), rgba(239, 245, 255, 0.92));
  box-shadow: 0 18px 45px rgba(15, 52, 106, 0.08);
}

.kpi-card::after {
  content: '';
  position: absolute;
  inset: auto 16px 14px auto;
  width: 78px;
  height: 78px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.22);
  filter: blur(4px);
}

.kpi-card[data-status='healthy'] {
  background: linear-gradient(160deg, rgba(255, 255, 255, 0.98), rgba(232, 248, 241, 0.96));
}

.kpi-card[data-status='attention'] {
  background: linear-gradient(160deg, rgba(255, 255, 255, 0.98), rgba(255, 243, 220, 0.96));
}

.kpi-card[data-status='warning'] {
  background: linear-gradient(160deg, rgba(255, 255, 255, 0.98), rgba(255, 233, 229, 0.96));
}

.kpi-card__title,
.kpi-card__description {
  margin: 0;
}

.kpi-card__title {
  color: #5f7090;
  font-size: 13px;
}

.kpi-card__value {
  display: block;
  margin-top: 10px;
  color: #10284d;
  font-size: 28px;
  line-height: 1.15;
}

.kpi-card__description {
  margin-top: 10px;
  color: #5c6985;
  font-size: 13px;
  max-width: 220px;
}
</style>
