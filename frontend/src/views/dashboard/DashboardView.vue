<script setup lang="ts">
import { BarChart, LineChart } from 'echarts/charts'
import {
  GridComponent,
  LegendComponent,
  TooltipComponent,
  type GridComponentOption,
  type LegendComponentOption,
  type TooltipComponentOption,
} from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { use, init, type ComposeOption, type ECharts } from 'echarts/core'
import { onBeforeUnmount, onMounted, ref } from 'vue'

import KpiCard from '../../components/dashboard/KpiCard.vue'

use([BarChart, LineChart, GridComponent, LegendComponent, TooltipComponent, CanvasRenderer])

type DashboardChartOption = ComposeOption<
  GridComponentOption | LegendComponentOption | TooltipComponentOption
>

const lifecycleCards = [
  { title: '核心实体', value: '10', description: '学生、导师、招生计划、培养方案等统一本体域对象。', status: 'healthy' as const },
  { title: '一级模块', value: '10', description: '主数据、招生、培养、学位、毕业、通知、分析等模块协同。', status: 'healthy' as const },
  { title: '关键审批流', value: '4', description: '招生、导师变更、外出研修、学位申请多级审批留痕。', status: 'attention' as const },
  { title: '审计对象', value: '3层', description: '登录日志、操作日志、同步日志形成全程可追溯。', status: 'warning' as const },
]

const recruitmentMetrics = [
  { title: '进行中计划', value: '4', description: '覆盖资格审核、评分推荐、面试、预录取。', status: 'healthy' as const },
  { title: '资格通过率', value: '79%', description: '结合学校、研究领域和资料完整度进行初筛。', status: 'healthy' as const },
  { title: '预录取池', value: '121', description: '含候补、调剂和已确认录取多个状态。', status: 'attention' as const },
]

const alerts = [
  { level: '高', title: '导师超期未审科研报告', detail: '3 名导师超过 14 天未完成审阅，已进入升级提醒链。' },
  { level: '中', title: '导师关系待确认', detail: '12 条新生关系超过 3 天未确认，需要学合管理员跟催。' },
  { level: '中', title: '学位论文查重失败', detail: '2 篇论文查重率超过 20%，已退回学生与导师联合整改。' },
]

const chartRef = ref<HTMLDivElement>()
let chart: ECharts | undefined

onMounted(() => {
  if (!chartRef.value) {
    return
  }

  chart = init(chartRef.value)
  const option: DashboardChartOption = {
    color: ['#2157f2', '#18a889', '#ffaf2e'],
    tooltip: { trigger: 'axis' },
    legend: { bottom: 0 },
    grid: { left: 16, right: 16, top: 24, bottom: 44, containLabel: true },
    xAxis: {
      type: 'category',
      data: ['资格审核', '材料评分', '面试安排', '培养方案', '科研报告', '学位流程'],
      axisLine: { lineStyle: { color: '#d2deef' } },
    },
    yAxis: {
      type: 'value',
      splitLine: { lineStyle: { color: '#eaf1fb' } },
    },
    series: [
      {
        name: '当前完成率',
        type: 'bar',
        barWidth: 18,
        data: [79, 68, 92, 100, 94, 88],
        itemStyle: { borderRadius: [10, 10, 0, 0] },
      },
      {
        name: '目标值',
        type: 'line',
        smooth: true,
        data: [75, 70, 95, 100, 95, 90],
      },
    ],
  }
  chart.setOption(option)
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  chart?.dispose()
})

function handleResize() {
  chart?.resize()
}
</script>

<template>
  <section class="page-grid">
    <div class="panel-stack">
      <section class="section-card">
        <div class="section-card__header">
          <div>
            <p class="section-tag">全局视角</p>
            <h2>生命周期总览</h2>
          </div>
          <el-tag type="primary">Ontology + Stanford + Palantir</el-tag>
        </div>
        <div class="kpi-grid kpi-grid--four">
          <KpiCard
            v-for="card in lifecycleCards"
            :key="card.title"
            :title="card.title"
            :value="card.value"
            :description="card.description"
            :status="card.status"
          />
        </div>
      </section>

      <section class="section-card">
        <div class="section-card__header">
          <div>
            <p class="section-tag">过程指标</p>
            <h2>关键链路达成度</h2>
          </div>
        </div>
        <div ref="chartRef" class="chart-panel"></div>
      </section>
    </div>

    <aside class="side-stack">
      <section class="section-card">
        <div class="section-card__header compact">
          <div>
            <p class="section-tag">招生运营</p>
            <h2>当期运行态</h2>
          </div>
        </div>
        <div class="kpi-grid">
          <KpiCard
            v-for="card in recruitmentMetrics"
            :key="card.title"
            :title="card.title"
            :value="card.value"
            :description="card.description"
            :status="card.status"
          />
        </div>
      </section>

      <section class="section-card">
        <div class="section-card__header compact">
          <div>
            <p class="section-tag">治理预警</p>
            <h2>待处置事项</h2>
          </div>
        </div>
        <ul class="alert-list">
          <li v-for="alert in alerts" :key="alert.title">
            <span class="alert-badge">{{ alert.level }}</span>
            <div>
              <strong>{{ alert.title }}</strong>
              <p>{{ alert.detail }}</p>
            </div>
          </li>
        </ul>
      </section>
    </aside>
  </section>
</template>

<style scoped>
.page-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.7fr) minmax(320px, 0.9fr);
  gap: 22px;
}

.panel-stack,
.side-stack {
  display: grid;
  gap: 22px;
}

.section-card {
  border: 1px solid rgba(18, 50, 95, 0.08);
  border-radius: 26px;
  padding: 22px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 18px 44px rgba(14, 40, 88, 0.07);
}

.section-card__header {
  display: flex;
  align-items: start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 18px;
}

.section-card__header.compact {
  margin-bottom: 16px;
}

.section-tag,
.section-card h2,
.alert-list p {
  margin: 0;
}

.section-tag {
  color: #7183a0;
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.section-card h2 {
  margin-top: 6px;
  color: #12284d;
  font-size: 22px;
}

.kpi-grid {
  display: grid;
  gap: 14px;
}

.kpi-grid--four {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.chart-panel {
  height: 320px;
}

.alert-list {
  display: grid;
  gap: 12px;
  padding: 0;
  margin: 0;
  list-style: none;
}

.alert-list li {
  display: grid;
  grid-template-columns: 52px minmax(0, 1fr);
  gap: 12px;
  padding: 14px;
  border-radius: 18px;
  background: linear-gradient(135deg, rgba(245, 248, 255, 0.96), rgba(255, 248, 235, 0.9));
}

.alert-badge {
  display: grid;
  place-items: center;
  border-radius: 14px;
  background: #0f4cbd;
  color: #fff;
  font-weight: 700;
}

.alert-list strong {
  color: #12315e;
}

.alert-list p {
  margin-top: 6px;
  color: #5f7090;
  line-height: 1.6;
}

@media (max-width: 1180px) {
  .page-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .kpi-grid--four {
    grid-template-columns: 1fr;
  }
}
</style>
