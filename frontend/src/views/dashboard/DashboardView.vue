<script setup lang="ts">
import {
  DataAnalysis,
  DocumentChecked,
  Histogram,
  Reading,
  UserFilled,
  WarningFilled,
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
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
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'

import { getDashboardOverview, type DashboardMetricCard } from '../../api/dashboard'
import KpiCard from '../../components/dashboard/KpiCard.vue'

use([BarChart, LineChart, GridComponent, LegendComponent, TooltipComponent, CanvasRenderer])

type DashboardChartOption = ComposeOption<
  GridComponentOption | LegendComponentOption | TooltipComponentOption
>

type StageNode = {
  step: string
  title: string
  subtitle: string
  bullets: string[]
  tone: string
}

const chartRef = ref<HTMLDivElement>()
const loading = ref(false)
const flowchartLaneRef = ref<HTMLDivElement>()
const flowScrollState = ref({ left: 0, width: 0, scrollWidth: 0 })
const overview = ref<{
  lifecycle_coverage: DashboardMetricCard[]
  recruitment_metrics: DashboardMetricCard[]
  training_metrics: DashboardMetricCard[]
  degree_metrics: DashboardMetricCard[]
  workflow_metrics: DashboardMetricCard[]
  alerts: Array<{ level: string; title: string; owner: string; due_text: string }>
} | null>(null)
let chart: ECharts | undefined

const lifecycleStages: StageNode[] = [
  { step: '01', title: '招生准备', subtitle: '招生管理', bullets: ['维护招生计划', '核验报名材料', '组织资格初筛'], tone: 'ocean' },
  { step: '02', title: '入学录取', subtitle: '招生管理', bullets: ['安排面试评审', '生成拟录取名单', '同步新生基础数据'], tone: 'sky' },
  { step: '03', title: '导师建立', subtitle: '学生管理', bullets: ['确认导师关系', '记录团队归属', '建立培养台账'], tone: 'teal' },
  { step: '04', title: '培养执行', subtitle: '培养管理', bullets: ['下发培养方案', '提交科研报告', '处理外出研修申请'], tone: 'amber' },
  { step: '05', title: '学位收口', subtitle: '学位管理', bullets: ['论文查重与盲审', '安排预答辩', '形成授位结论'], tone: 'coral' },
  { step: '06', title: '毕业归档', subtitle: '系统治理', bullets: ['归档日志留痕', '同步外部系统', '保留业务证据链'], tone: 'violet' },
]

const iconMap: Record<string, unknown> = {
  学生总量: UserFilled,
  开放招生计划: Histogram,
  在途审批: WarningFilled,
  招生计划: Histogram,
  待审核申请: DataAnalysis,
  预录取池: Histogram,
  培养方案: Reading,
  科研报告待审: Reading,
  外出研修在途: Reading,
  论文总量: DocumentChecked,
  盲审待办: DocumentChecked,
  待答辩: DocumentChecked,
  待处理审批: WarningFilled,
  处理中审批: DataAnalysis,
  超期审批: WarningFilled,
}

const summaryCards = computed(() => {
  if (!overview.value) {
    return []
  }

  const cards = [
    ...overview.value.recruitment_metrics.slice(0, 2),
    ...overview.value.lifecycle_coverage.slice(0, 1),
    ...overview.value.training_metrics.slice(0, 1),
    ...overview.value.degree_metrics.slice(0, 1),
    ...overview.value.workflow_metrics.slice(0, 1),
  ]

  return cards.map((card) => ({
    title: card.label,
    value: card.value,
    description: card.trend || card.target || '',
    status: (card.status === 'attention' || card.status === 'warning' ? card.status : 'healthy') as 'healthy' | 'attention' | 'warning',
    icon: iconMap[card.label] || DataAnalysis,
  }))
})

const alertItems = computed(() => overview.value?.alerts || [])

const canScrollFlowLeft = computed(() => flowScrollState.value.left > 8)
const canScrollFlowRight = computed(() => {
  const { left, width, scrollWidth } = flowScrollState.value
  return left + width < scrollWidth - 8
})

function updateFlowScrollState() {
  const lane = flowchartLaneRef.value
  if (!lane) {
    flowScrollState.value = { left: 0, width: 0, scrollWidth: 0 }
    return
  }
  flowScrollState.value = {
    left: lane.scrollLeft,
    width: lane.clientWidth,
    scrollWidth: lane.scrollWidth,
  }
}

function scrollFlowchart(direction: number) {
  const lane = flowchartLaneRef.value
  if (!lane) {
    return
  }
  const nodes = Array.from(lane.querySelectorAll('.flow-node'))
  if (!nodes.length) {
    return
  }
  const currentLeft = lane.scrollLeft
  if (direction > 0) {
    const nextNode = nodes.find((node) => (node as HTMLElement).offsetLeft > currentLeft + 12) as HTMLElement | undefined
    lane.scrollTo({ left: nextNode ? nextNode.offsetLeft : lane.scrollWidth, behavior: 'smooth' })
    return
  }
  const previousNode = [...nodes].reverse().find((node) => (node as HTMLElement).offsetLeft < currentLeft - 12) as HTMLElement | undefined
  lane.scrollTo({ left: previousNode ? previousNode.offsetLeft : 0, behavior: 'smooth' })
}

async function loadOverview() {
  loading.value = true
  try {
    const { data } = await getDashboardOverview()
    overview.value = data
    renderChart()
    updateFlowScrollState()
  } catch {
    ElMessage.error('驾驶舱数据加载失败')
  } finally {
    loading.value = false
  }
}

function renderChart() {
  if (!chartRef.value || !overview.value) {
    return
  }

  const bars = [
    overview.value.recruitment_metrics[0]?.value || '0',
    overview.value.lifecycle_coverage[0]?.value || '0',
    overview.value.training_metrics[0]?.value || '0',
    overview.value.training_metrics[1]?.value || '0',
    overview.value.degree_metrics[0]?.value || '0',
    overview.value.workflow_metrics[0]?.value || '0',
  ].map((value) => Number(value))

  chart?.dispose()
  chart = init(chartRef.value)
  const option: DashboardChartOption = {
    color: ['#27a3ea', '#4675bb'],
    tooltip: { trigger: 'axis' },
    legend: { bottom: 0 },
    grid: { left: 16, right: 16, top: 24, bottom: 44, containLabel: true },
    xAxis: {
      type: 'category',
      data: ['招生计划', '学生规模', '培养方案', '报告待审', '论文总量', '流程待办'],
      axisLine: { lineStyle: { color: '#d2deef' } },
      axisTick: { show: false },
    },
    yAxis: {
      type: 'value',
      splitLine: { lineStyle: { color: '#eaf1fb' } },
    },
    series: [
      {
        name: '当前规模',
        type: 'bar',
        barWidth: 18,
        data: bars,
        itemStyle: { borderRadius: [10, 10, 0, 0] },
      },
      {
        name: '目标线',
        type: 'line',
        smooth: true,
        data: bars.map((value) => Math.max(value, 1)),
      },
    ],
  }
  chart.setOption(option)
}

function handleResize() {
  chart?.resize()
  updateFlowScrollState()
}

onMounted(() => {
  void loadOverview()
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  chart?.dispose()
})
</script>

<template>
  <section class="dashboard-grid" v-loading="loading">
    <KpiCard
      v-for="card in summaryCards"
      :key="card.title"
      :title="card.title"
      :value="card.value"
      :description="card.description"
      :status="card.status"
      :icon="card.icon"
    />

    <section class="page-card dashboard-panel full-span">
      <div class="page-heading">
        <div>
          <h2>端到端业务流程图</h2>
          <p>从招生准备到毕业归档，按业务顺序展示关键动作，并在节点上直接标记参与角色。</p>
        </div>
      </div>

      <div class="flowchart-shell">
        <div class="flowchart-header">
          <div>
            <span class="flowchart-kicker">主链路</span>
            <h3>招生 → 入学 → 导师关系 → 培养执行 → 学位审核 → 毕业归档</h3>
          </div>
          <p>用于给管理人员快速判断当前业务主线位置，也可作为新用户培训时的操作导航。</p>
        </div>

        <div class="flowchart-lane-wrap">
          <button
            type="button"
            class="flowchart-nav flowchart-nav--left"
            :class="{ 'is-disabled': !canScrollFlowLeft }"
            :disabled="!canScrollFlowLeft"
            @click="scrollFlowchart(-1)"
          >
            <span aria-hidden="true">‹</span>
          </button>

          <div ref="flowchartLaneRef" class="flowchart-lane" @scroll="updateFlowScrollState">
            <template v-for="(node, index) in lifecycleStages" :key="node.step">
              <article class="flow-node" :class="`is-${node.tone}`">
                <div class="flow-node__top">
                  <span class="flow-node__step">{{ node.step }}</span>
                  <span class="flow-node__subtitle">{{ node.subtitle }}</span>
                </div>
                <h4>{{ node.title }}</h4>
                <ul class="flow-node__actions">
                  <li v-for="action in node.bullets" :key="action">{{ action }}</li>
                </ul>
              </article>
              <div v-if="index < lifecycleStages.length - 1" class="flow-arrow" aria-hidden="true"><span></span></div>
            </template>
          </div>

          <button
            type="button"
            class="flowchart-nav flowchart-nav--right"
            :class="{ 'is-disabled': !canScrollFlowRight }"
            :disabled="!canScrollFlowRight"
            @click="scrollFlowchart(1)"
          >
            <span aria-hidden="true">›</span>
          </button>
        </div>
      </div>
    </section>

    <section class="page-card dashboard-panel chart-span">
      <div class="page-heading">
        <div>
          <h2>经营总览趋势</h2>
          <p>基于真实接口数据汇总招生、学生、培养、学位与流程待办规模。</p>
        </div>
      </div>
      <div ref="chartRef" class="chart-panel"></div>
    </section>

    <section class="page-card dashboard-panel alert-span">
      <div class="page-heading">
        <div>
          <h2>预警事项</h2>
          <p>优先展示需要管理人员介入的异常和待办。</p>
        </div>
      </div>
      <ul class="alert-list">
        <li v-for="alert in alertItems" :key="alert.title">
          <span class="alert-level">{{ alert.level }}</span>
          <div>
            <strong>{{ alert.title }}</strong>
            <p>{{ alert.owner }} · {{ alert.due_text }}</p>
          </div>
        </li>
      </ul>
    </section>
  </section>
</template>

<style scoped>
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18px;
}

.dashboard-panel {
  padding: 24px;
}

.full-span {
  grid-column: 1 / -1;
}

.chart-span {
  grid-column: 1 / span 2;
}

.alert-span {
  grid-column: 3 / span 1;
}

.flowchart-shell {
  display: flex;
  flex-direction: column;
  gap: 22px;
}

.flowchart-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
  padding: 22px 24px;
  border-radius: 24px;
  border: 1px solid rgba(34, 166, 238, 0.18);
  background:
    radial-gradient(circle at top left, rgba(34, 166, 238, 0.18), transparent 32%),
    linear-gradient(135deg, rgba(255, 255, 255, 0.96), rgba(240, 248, 255, 0.92));
}

.flowchart-kicker {
  display: inline-flex;
  align-items: center;
  padding: 6px 10px;
  border-radius: 999px;
  background: rgba(53, 108, 184, 0.1);
  color: var(--brand-strong);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.flowchart-header h3 {
  margin: 12px 0 0;
  font-family: var(--title-font);
  font-size: 24px;
  line-height: 1.35;
}

.flowchart-header p {
  margin: 0;
  color: var(--text-subtle);
  max-width: 360px;
  line-height: 1.7;
}

.flowchart-lane-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.flowchart-lane {
  display: flex;
  align-items: stretch;
  gap: 0;
  overflow-x: auto;
  padding-bottom: 6px;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.flowchart-lane::-webkit-scrollbar {
  display: none;
}

.flowchart-nav {
  position: absolute;
  top: 50%;
  z-index: 2;
  width: 42px;
  height: 42px;
  border: 1px solid rgba(53, 108, 184, 0.18);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.92);
  color: var(--brand-strong);
  box-shadow: 0 12px 24px rgba(24, 56, 87, 0.12);
  transform: translateY(-50%);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s ease, transform 0.2s ease, background 0.2s ease;
}

.flowchart-nav span {
  font-size: 28px;
  line-height: 1;
  transform: translateY(-1px);
}

.flowchart-nav:hover:not(.is-disabled) {
  opacity: 0.92;
  background: #ffffff;
  transform: translateY(-50%) scale(1.04);
}

.flowchart-nav.is-disabled {
  opacity: 0.22;
  cursor: default;
  box-shadow: none;
}

.flowchart-lane-wrap:hover .flowchart-nav,
.flowchart-lane-wrap:focus-within .flowchart-nav {
  opacity: 0.56;
  pointer-events: auto;
}

.flowchart-lane-wrap:hover .flowchart-nav.is-disabled,
.flowchart-lane-wrap:focus-within .flowchart-nav.is-disabled {
  opacity: 0.22;
}

.flowchart-nav--left {
  left: -12px;
}

.flowchart-nav--right {
  right: -12px;
}

.flow-node {
  position: relative;
  flex: 0 0 250px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding: 18px;
  border: 1px solid var(--flow-accent-soft);
  background: linear-gradient(180deg, var(--flow-bg-top), var(--flow-bg-bottom));
  box-shadow: 0 18px 40px rgba(24, 56, 87, 0.08);
}

.flow-node::before {
  content: '';
  position: absolute;
  inset: 0 auto auto 0;
  width: 100%;
  height: 5px;
  background: var(--flow-accent);
}

.flow-node.is-ocean {
  --flow-bg-top: #f0f8ff;
  --flow-bg-bottom: #e4f2ff;
  --flow-accent: #2e9bea;
  --flow-accent-soft: rgba(46, 155, 234, 0.24);
}

.flow-node.is-sky {
  --flow-bg-top: #f3f9ff;
  --flow-bg-bottom: #eaf4ff;
  --flow-accent: #5ba9f2;
  --flow-accent-soft: rgba(91, 169, 242, 0.24);
}

.flow-node.is-teal {
  --flow-bg-top: #effbf8;
  --flow-bg-bottom: #e2f7f1;
  --flow-accent: #36b59a;
  --flow-accent-soft: rgba(54, 181, 154, 0.24);
}

.flow-node.is-amber {
  --flow-bg-top: #fffaf0;
  --flow-bg-bottom: #fff1d8;
  --flow-accent: #e4a53d;
  --flow-accent-soft: rgba(228, 165, 61, 0.24);
}

.flow-node.is-coral {
  --flow-bg-top: #fff6f2;
  --flow-bg-bottom: #ffe8e1;
  --flow-accent: #e47857;
  --flow-accent-soft: rgba(228, 120, 87, 0.24);
}

.flow-node.is-violet {
  --flow-bg-top: #f7f3ff;
  --flow-bg-bottom: #ece3ff;
  --flow-accent: #8d72d9;
  --flow-accent-soft: rgba(141, 114, 217, 0.24);
}

.flow-node__top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.flow-node__step {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 44px;
  height: 44px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.72);
  color: var(--flow-accent);
  font-weight: 800;
  font-size: 15px;
}

.flow-node__subtitle {
  color: var(--text-subtle);
  font-size: 13px;
  text-align: right;
}

.flow-node h4 {
  margin: 0;
  font-family: var(--title-font);
  font-size: 20px;
}

.flow-node__actions {
  margin: 0;
  padding-left: 18px;
  color: var(--text-main);
  line-height: 1.8;
}

.flow-arrow {
  width: 58px;
  flex: 0 0 58px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.flow-arrow span {
  position: relative;
  display: inline-block;
  width: 38px;
  height: 2px;
  background: rgba(70, 117, 187, 0.72);
}

.flow-arrow span::after {
  content: '';
  position: absolute;
  top: -4px;
  right: 0;
  width: 10px;
  height: 10px;
  border-top: 2px solid rgba(70, 117, 187, 0.72);
  border-right: 2px solid rgba(70, 117, 187, 0.72);
  transform: rotate(45deg);
}

.chart-panel {
  height: 350px;
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

.alert-level {
  display: grid;
  place-items: center;
  border-radius: 14px;
  background: var(--brand-strong);
  color: #ffffff;
  font-weight: 700;
}

.alert-list strong {
  color: var(--text-main);
}

.alert-list p {
  margin: 6px 0 0;
  color: var(--text-subtle);
  line-height: 1.6;
}

@media (max-width: 1180px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }

  .chart-span,
  .alert-span {
    grid-column: 1 / -1;
  }
}

@media (max-width: 768px) {
  .flowchart-header {
    flex-direction: column;
  }
}
</style>
