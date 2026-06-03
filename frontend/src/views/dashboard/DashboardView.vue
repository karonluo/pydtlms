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
import { BarChart, PieChart, type BarSeriesOption, type PieSeriesOption } from 'echarts/charts'
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
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'

import {
  getDashboardOverview,
  getDashboardUndergraduateSchoolGroupDistribution,
  getDashboardUndergraduateSchoolGroupStudents,
  getDashboardUndergraduateSchoolRankings,
  getDashboardUndergraduateSchoolStudents,
  type DashboardUndergraduateSchoolGroupDistribution,
  type DashboardUndergraduateSchoolGroupDistributionResponse,
  type DashboardOverview,
  type DashboardUndergraduateSchoolRankingItem,
  type DashboardUndergraduateSchoolStudentItem,
} from '../../api/dashboard'
import RecruitmentPortalApplicationDrawer from '../../components/recruitment/RecruitmentPortalApplicationDrawer.vue'
import { getRecruitmentPortalApplicationDetail, type RecruitPortalApplicationDetail } from '../../api/recruitment'
import { executeWorkflowTaskAction, listWorkflowTasks, type WorkflowActionOption, type WorkflowTaskRecord } from '../../api/workflow'
import KpiCard from '../../components/dashboard/KpiCard.vue'

use([BarChart, PieChart, GridComponent, LegendComponent, TooltipComponent, CanvasRenderer])

type DashboardChartOption = ComposeOption<
  BarSeriesOption | PieSeriesOption | GridComponentOption | LegendComponentOption | TooltipComponentOption
>

type SchoolGroupDisplayItem = {
  school_name: string
  student_count: number
  percentage: number
  bucket?: 'other'
}

type SchoolStudentDialogSource =
  | { type: 'school'; schoolName: string }
  | { type: 'group'; title: string; dictType: string; schoolName?: string; bucket?: 'other' }

const schoolRankingChartRef = ref<HTMLDivElement>()
const loading = ref(false)
const overview = ref<DashboardOverview | null>(null)
const schoolGroupDistribution = ref<DashboardUndergraduateSchoolGroupDistributionResponse>({ total_applications: 0, groups: [] })
const schoolRankings = ref<DashboardUndergraduateSchoolRankingItem[]>([])
const schoolStudentDialogVisible = ref(false)
const schoolStudentListLoading = ref(false)
const selectedSchoolName = ref('')
const selectedSchoolStudents = ref<DashboardUndergraduateSchoolStudentItem[]>([])
const selectedSchoolStudentFilter = ref('')
const selectedSchoolDialogSource = ref<SchoolStudentDialogSource | null>(null)
const portalApplicationDetailVisible = ref(false)
const portalViewingApplication = ref<RecruitPortalApplicationDetail | null>(null)
const portalViewingWorkflowTask = ref<WorkflowTaskRecord | null>(null)
const portalWorkflowTaskLoading = ref(false)
const portalWorkflowActionSubmitting = ref(false)
const portalWorkflowCommentDialogVisible = ref(false)
const pendingPortalWorkflowAction = ref<WorkflowActionOption | null>(null)
const portalWorkflowComment = ref('')
const schoolGroupPieChartRefs = ref<Record<string, HTMLDivElement | null>>({})
let schoolRankingChart: ECharts | undefined
let schoolGroupPieCharts: Record<string, ECharts | undefined> = {}

const schoolGroupPalette = ['#2e9bea', '#36b59a', '#e4a53d', '#e47857', '#8d72d9', '#4675bb', '#60c4a4', '#f0b45a', '#d86666', '#7a8796']

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

const selectedSchoolStudentStats = computed(() => {
  const counter = new Map<string, number>()
  selectedSchoolStudents.value.forEach((item) => {
    const schoolName = String(item.school_name || '').trim() || '未记录学校'
    counter.set(schoolName, (counter.get(schoolName) || 0) + 1)
  })
  return Array.from(counter.entries())
    .map(([school_name, student_count]) => ({ school_name, student_count }))
    .sort((left, right) => right.student_count - left.student_count || left.school_name.localeCompare(right.school_name, 'zh-Hans-CN'))
})

const isSchoolStudentFiltered = computed(() => !!selectedSchoolStudentFilter.value)
const filteredSelectedSchoolStudents = computed(() => {
  const activeFilter = selectedSchoolStudentFilter.value.trim()
  if (!activeFilter) {
    return selectedSchoolStudents.value
  }
  return selectedSchoolStudents.value.filter((item) => (String(item.school_name || '').trim() || '未记录学校') === activeFilter)
})

async function loadOverview() {
  loading.value = true
  try {
    const [{ data: overviewData }, { data: rankingData }, { data: groupDistributionData }] = await Promise.all([
      getDashboardOverview(),
      getDashboardUndergraduateSchoolRankings(20),
      getDashboardUndergraduateSchoolGroupDistribution(),
    ])
    overview.value = overviewData
    schoolRankings.value = rankingData.items
    schoolGroupDistribution.value = groupDistributionData
    await nextTick()
    renderSchoolGroupPieCharts()
    renderSchoolRankingChart()
  } catch {
    ElMessage.error('驾驶舱数据加载失败')
  } finally {
    loading.value = false
  }
}

function setSchoolGroupPieChartRef(dictType: string, element: unknown) {
  schoolGroupPieChartRefs.value[dictType] = element instanceof HTMLDivElement ? element : null
}

function formatRate(value: number) {
  if (!Number.isFinite(value) || value <= 0) {
    return '0%'
  }
  return `${value.toFixed(value >= 10 ? 1 : 2).replace(/\.0+$/, '')}%`
}

function schoolGroupShareOfAll(total: number) {
  const applications = schoolGroupDistribution.value.total_applications
  if (!applications) {
    return '0%'
  }
  return formatRate((total * 100) / applications)
}

function getSchoolGroupDisplayItems(group: DashboardUndergraduateSchoolGroupDistribution): SchoolGroupDisplayItem[] {
  const positiveItems = group.items.filter((item) => item.student_count > 0)
  if (group.dict_type === 'system_211_university' || group.dict_type === 'system_985_university') {
    const topItems = positiveItems.slice(0, 5)
    const otherCount = positiveItems.slice(5).reduce((sum, item) => sum + item.student_count, 0)
    if (otherCount <= 0) {
      return topItems
    }
    return [
      ...topItems,
      {
        school_name: '其他',
        student_count: otherCount,
        percentage: group.total ? Number(((otherCount * 100) / group.total).toFixed(2)) : 0,
        bucket: 'other',
      },
    ]
  }
  return positiveItems
}

function schoolGroupLegendDotStyle(index: number) {
  return { backgroundColor: schoolGroupPalette[index % schoolGroupPalette.length] }
}

function formatSchoolGroupPieLabel(name: string) {
  const normalizedName = String(name || '').trim()
  if (normalizedName.length <= 7) {
    return normalizedName
  }
  return `${normalizedName.slice(0, 7)}\n${normalizedName.slice(7)}`
}

function renderSchoolGroupPieCharts() {
  Object.values(schoolGroupPieCharts).forEach((pieChart) => pieChart?.dispose())
  schoolGroupPieCharts = {}

  schoolGroupDistribution.value.groups.forEach((group) => {
    const chartElement = schoolGroupPieChartRefs.value[group.dict_type]
    const visibleItems = getSchoolGroupDisplayItems(group)
    if (!chartElement || !visibleItems.length) {
      return
    }

    const pieChart = init(chartElement)
    schoolGroupPieCharts[group.dict_type] = pieChart
    const option: DashboardChartOption = {
      color: schoolGroupPalette,
      tooltip: {
        trigger: 'item',
        formatter: (params: any) => {
          const value = Number(params?.value || 0)
          const rate = typeof params?.data?.percentage === 'number' ? formatRate(params.data.percentage) : `${params?.percent || 0}%`
          return `${params?.name || ''}<br/>报名学生 ${value} 名<br/>占本组 ${rate}`
        },
      },
      series: [
        {
          name: group.group_name,
          type: 'pie',
          radius: '50%',
          center: ['50%', '48%'],
          avoidLabelOverlap: true,
          minAngle: 4,
          cursor: 'pointer',
          data: visibleItems.map((item) => ({
            name: item.school_name,
            value: item.student_count,
            percentage: item.percentage,
            schoolName: item.bucket === 'other' ? undefined : item.school_name,
            bucket: item.bucket,
          })),
          label: {
            formatter: (params: any) => {
              const percent = typeof params?.data?.percentage === 'number' ? formatRate(params.data.percentage) : `${params?.percent || 0}%`
              return `${formatSchoolGroupPieLabel(String(params?.name || ''))}\n${params?.value || 0}人 ${percent}`
            },
            color: '#24415f',
            fontSize: 10,
            lineHeight: 13,
          },
          labelLine: {
            length: 8,
            length2: 6,
          },
          labelLayout: {
            hideOverlap: false,
          },
        },
      ],
    }
    pieChart.setOption(option)
    pieChart.on('click', (params: any) => {
      const data = params?.data || {}
      const item: SchoolGroupDisplayItem = {
        school_name: String(params?.name || ''),
        student_count: Number(params?.value || 0),
        percentage: typeof data.percentage === 'number' ? data.percentage : 0,
        bucket: data.bucket === 'other' ? 'other' : undefined,
      }
      void openSchoolGroupStudentDialog(group, item)
    })
  })
}

function renderSchoolRankingChart() {
  if (!schoolRankingChartRef.value) {
    return
  }

  schoolRankingChart?.dispose()
  schoolRankingChart = undefined
  if (!schoolRankings.value.length) {
    return
  }

  schoolRankingChart = init(schoolRankingChartRef.value)
  const option: DashboardChartOption = {
    color: ['#36b59a'],
    tooltip: {
      trigger: 'item',
      formatter: (params: any) => `${params?.name || ''}<br/>报名学生 ${params?.value || 0} 名`,
    },
    grid: { left: 24, right: 24, top: 16, bottom: 18, containLabel: true },
    xAxis: {
      type: 'value',
      splitLine: { lineStyle: { color: '#eaf1fb' } },
    },
    yAxis: {
      type: 'category',
      inverse: true,
      data: schoolRankings.value.map((item) => item.school_name),
      axisTick: { show: false },
      axisLine: { show: false },
      axisLabel: {
        color: '#36506c',
        width: 160,
        overflow: 'truncate',
      },
    },
    series: [
      {
        type: 'bar',
        barWidth: 16,
        data: schoolRankings.value.map((item) => item.student_count),
        itemStyle: { borderRadius: [0, 10, 10, 0] },
        label: {
          show: true,
          position: 'right',
          color: '#24415f',
        },
      },
    ],
  }
  schoolRankingChart.setOption(option)
  schoolRankingChart.on('click', (params: { name?: string }) => {
    const schoolName = String(params.name || '').trim()
    if (schoolName) {
      void openSchoolStudentDialog(schoolName)
    }
  })
}

async function openSchoolStudentDialog(schoolName: string) {
  selectedSchoolName.value = schoolName
  selectedSchoolStudentFilter.value = ''
  selectedSchoolDialogSource.value = { type: 'school', schoolName }
  schoolStudentDialogVisible.value = true
  schoolStudentListLoading.value = true
  try {
    const { data } = await getDashboardUndergraduateSchoolStudents(schoolName)
    selectedSchoolStudents.value = data.items
  } catch {
    selectedSchoolStudents.value = []
    ElMessage.error('加载院校报名学生清单失败')
  } finally {
    schoolStudentListLoading.value = false
  }
}

async function openSchoolGroupStudentDialog(group: DashboardUndergraduateSchoolGroupDistribution, item: SchoolGroupDisplayItem) {
  const title = item.bucket === 'other' ? `${group.group_name}其他院校` : item.school_name
  selectedSchoolName.value = title
  selectedSchoolStudentFilter.value = ''
  selectedSchoolDialogSource.value = {
    type: 'group',
    title,
    dictType: group.dict_type,
    schoolName: item.bucket === 'other' ? undefined : item.school_name,
    bucket: item.bucket,
  }
  schoolStudentDialogVisible.value = true
  schoolStudentListLoading.value = true
  try {
    const { data } = await getDashboardUndergraduateSchoolGroupStudents({
      dict_type: group.dict_type,
      school_name: item.bucket === 'other' ? undefined : item.school_name,
      bucket: item.bucket,
    })
    selectedSchoolStudents.value = data.items
  } catch {
    selectedSchoolStudents.value = []
    ElMessage.error('加载重点院校报名学生清单失败')
  } finally {
    schoolStudentListLoading.value = false
  }
}

async function reloadSelectedSchoolStudents() {
  const source = selectedSchoolDialogSource.value
  if (!source) {
    return
  }
  selectedSchoolStudentFilter.value = ''
  if (source.type === 'school') {
    await openSchoolStudentDialog(source.schoolName)
    return
  }
  selectedSchoolName.value = source.title
  schoolStudentDialogVisible.value = true
  schoolStudentListLoading.value = true
  try {
    const { data } = await getDashboardUndergraduateSchoolGroupStudents({
      dict_type: source.dictType,
      school_name: source.schoolName,
      bucket: source.bucket,
    })
    selectedSchoolStudents.value = data.items
  } catch {
    selectedSchoolStudents.value = []
    ElMessage.error('刷新重点院校报名学生清单失败')
  } finally {
    schoolStudentListLoading.value = false
  }
}

function applySchoolStudentFilter(schoolName: string) {
  selectedSchoolStudentFilter.value = schoolName
}

function resetSchoolStudentFilter() {
  selectedSchoolStudentFilter.value = ''
}

async function openPortalApplicationDetail(row: DashboardUndergraduateSchoolStudentItem) {
  if (!row.recruitment_application_id) {
    ElMessage.warning('当前学生缺少报名申请记录')
    return
  }
  try {
    const response = await getRecruitmentPortalApplicationDetail(row.recruitment_application_id)
    portalViewingApplication.value = response.data
    portalApplicationDetailVisible.value = true
    await loadPortalViewingWorkflowTask(response.data.business_key)
  } catch {
    portalViewingWorkflowTask.value = null
    ElMessage.error('加载学生报名详情失败')
  }
}

async function loadPortalViewingWorkflowTask(businessKey?: string | null) {
  const normalizedKey = String(businessKey || '').trim()
  portalViewingWorkflowTask.value = null
  if (!normalizedKey) {
    return
  }
  portalWorkflowTaskLoading.value = true
  try {
    const response = await listWorkflowTasks({ page: 1, page_size: 20, module: '招生管理', keyword: normalizedKey })
    portalViewingWorkflowTask.value = response.data.items.find((item) => item.business_key === normalizedKey) || null
  } catch {
    ElMessage.error('加载审批任务失败')
    portalViewingWorkflowTask.value = null
  } finally {
    portalWorkflowTaskLoading.value = false
  }
}

function handlePortalWorkflowAction(action: WorkflowActionOption) {
  if (!portalViewingWorkflowTask.value) {
    ElMessage.warning('当前未找到可执行的审批任务')
    return
  }
  pendingPortalWorkflowAction.value = action
  portalWorkflowComment.value = ''
  portalWorkflowCommentDialogVisible.value = true
}

async function submitPortalWorkflowCommentDialog() {
  if (!portalViewingWorkflowTask.value || !pendingPortalWorkflowAction.value) {
    return
  }
  const currentAction = pendingPortalWorkflowAction.value
  portalWorkflowActionSubmitting.value = true
  try {
    await executeWorkflowTaskAction(portalViewingWorkflowTask.value.id, {
      action: currentAction.action,
      comment: portalWorkflowComment.value.trim() || undefined,
    })
    portalWorkflowCommentDialogVisible.value = false
    portalApplicationDetailVisible.value = false
    portalViewingApplication.value = null
    portalViewingWorkflowTask.value = null
    ElMessage.success(`${currentAction.label}已完成`)
    await loadOverview()
    if (selectedSchoolDialogSource.value) {
      await reloadSelectedSchoolStudents()
    }
  } catch {
    ElMessage.error(`${currentAction.label}失败`)
  } finally {
    portalWorkflowActionSubmitting.value = false
  }
}

function resetPortalWorkflowCommentDialog() {
  pendingPortalWorkflowAction.value = null
  portalWorkflowComment.value = ''
}

watch(() => portalWorkflowCommentDialogVisible.value, (visible) => {
  if (!visible) {
    resetPortalWorkflowCommentDialog()
  }
})

watch(() => portalApplicationDetailVisible.value, (visible) => {
  if (!visible) {
    portalViewingApplication.value = null
    portalViewingWorkflowTask.value = null
  }
})

watch(() => schoolStudentDialogVisible.value, (visible) => {
  if (!visible) {
    selectedSchoolStudentFilter.value = ''
  }
})

function handleResize() {
  schoolRankingChart?.resize()
  Object.values(schoolGroupPieCharts).forEach((pieChart) => pieChart?.resize())
}

onMounted(() => {
  void loadOverview()
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  schoolRankingChart?.dispose()
  Object.values(schoolGroupPieCharts).forEach((pieChart) => pieChart?.dispose())
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
          <h2>本科院校报名人数前二十</h2>
          <p>按最新报名申请统计本科院校来源分布。点击柱状图可查看该院校学生清单，并继续打开完整报名信息。</p>
        </div>
      </div>

      <div class="school-ranking-shell">
        <div class="school-ranking-summary">
          <strong>统计口径：门户注册学生的最新报名申请</strong>
          <!-- <span>展示前二十名本科学校。若同一学生存在多次申请，仅按最新一条报名申请计入排名。</span> -->
        </div>
        <div class="school-group-card">
          <div class="school-group-card__header">
            <div>
              <span class="school-group-card__kicker">重点院校报名分布</span>
              <h3>C9、211、985 院校报名占比</h3>
            </div>
            <div class="school-group-card__total">
              <span>本科院校有效报名</span>
              <strong>{{ schoolGroupDistribution.total_applications }}</strong>
            </div>
          </div>
          <div class="school-group-grid">
            <article v-for="group in schoolGroupDistribution.groups" :key="group.dict_type" class="school-group-panel">
              <div class="school-group-panel__head">
                <div>
                  <h4>{{ group.group_name }}</h4>
                  <span>占有效报名 {{ schoolGroupShareOfAll(group.total) }}</span>
                </div>
                <strong>{{ group.total }}<small>人</small></strong>
              </div>
              <div v-if="group.total" :ref="(element) => setSchoolGroupPieChartRef(group.dict_type, element)" class="school-group-pie"></div>
              <ul v-if="group.total" class="school-group-legend">
                <li v-for="(item, index) in getSchoolGroupDisplayItems(group)" :key="item.school_name">
                  <span class="school-group-legend__dot" :style="schoolGroupLegendDotStyle(index)"></span>
                  <span class="school-group-legend__name">{{ item.school_name }}</span>
                  <strong>{{ item.student_count }}人</strong>
                  <span>{{ formatRate(item.percentage) }}</span>
                </li>
              </ul>
              <div v-else class="school-group-empty">暂无匹配报名数据</div>
            </article>
          </div>
        </div>
        <div v-if="schoolRankings.length" ref="schoolRankingChartRef" class="chart-panel school-ranking-chart"></div>
        <div v-else class="dashboard-empty">当前暂无可展示的本科院校报名数据。</div>
      </div>
    </section>

    <el-dialog v-model="schoolStudentDialogVisible" :title="`${selectedSchoolName || '本科院校'}报名学生清单`" width="960px" destroy-on-close>
      <div class="school-student-summary">
        <div class="school-student-summary__total">
          <strong>共 {{ filteredSelectedSchoolStudents.length }} 名学生</strong>
          <span v-if="isSchoolStudentFiltered">当前筛选：{{ selectedSchoolStudentFilter }}</span>
          <span v-if="isSchoolStudentFiltered">原始共 {{ selectedSchoolStudents.length }} 名</span>
          <span>涉及 {{ selectedSchoolStudentStats.length }} 所学校</span>
        </div>
        <ul v-if="selectedSchoolStudentStats.length" class="school-student-summary__schools">
          <li v-for="item in selectedSchoolStudentStats" :key="item.school_name">
            <button
              type="button"
              class="school-student-summary__chip"
              :class="{ 'is-active': selectedSchoolStudentFilter === item.school_name }"
              @click="applySchoolStudentFilter(item.school_name)"
            >
              <span>{{ item.school_name }}</span>
              <strong>{{ item.student_count }}人</strong>
            </button>
          </li>
          <li>
            <button
              type="button"
              class="school-student-summary__chip school-student-summary__chip--reset"
              :class="{ 'is-disabled': !isSchoolStudentFiltered }"
              :disabled="!isSchoolStudentFiltered"
              @click="resetSchoolStudentFilter"
            >
              <span>重置</span>
            </button>
          </li>
        </ul>
      </div>
      <el-table :data="filteredSelectedSchoolStudents" v-loading="schoolStudentListLoading" border stripe>
        <el-table-column label="学生名称" min-width="160">
          <template #default="scope">
            <el-button link type="primary" @click="openPortalApplicationDetail(scope.row)">
              {{ scope.row.student_name || '未命名学生' }}
            </el-button>
          </template>
        </el-table-column>
        <el-table-column prop="school_name" label="学校" min-width="180" show-overflow-tooltip>
          <template #default="scope">{{ scope.row.school_name || '未记录' }}</template>
        </el-table-column>
        <el-table-column prop="candidate_no" label="报名号" min-width="140">
          <template #default="scope">{{ scope.row.candidate_no || '未生成' }}</template>
        </el-table-column>
        <el-table-column prop="registered_at" label="注册日期" min-width="180">
          <template #default="scope">{{ scope.row.registered_at || '未记录' }}</template>
        </el-table-column>
        <el-table-column prop="phone_number" label="手机" min-width="140">
          <template #default="scope">{{ scope.row.phone_number || '未填写' }}</template>
        </el-table-column>
        <el-table-column prop="email" label="邮件" min-width="220">
          <template #default="scope">{{ scope.row.email || '未填写' }}</template>
        </el-table-column>
      </el-table>
    </el-dialog>

    <RecruitmentPortalApplicationDrawer
      v-model="portalApplicationDetailVisible"
      :detail="portalViewingApplication"
      :workflow-task="portalViewingWorkflowTask"
      :workflow-task-loading="portalWorkflowTaskLoading"
      :action-loading="portalWorkflowActionSubmitting"
      @execute-action="handlePortalWorkflowAction"
    />

    <el-dialog
      v-model="portalWorkflowCommentDialogVisible"
      :title="pendingPortalWorkflowAction ? pendingPortalWorkflowAction.label : '审批处理'"
      width="640px"
      destroy-on-close
    >
      <div class="workflow-comment-dialog">
        <p class="workflow-comment-dialog__hint">请输入审批意见，可留空后直接提交。</p>
        <el-input
          v-model="portalWorkflowComment"
          type="textarea"
          :rows="5"
          maxlength="500"
          show-word-limit
          placeholder="审批意见（可选）"
        />
      </div>
      <template #footer>
        <el-button @click="portalWorkflowCommentDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="portalWorkflowActionSubmitting" @click="submitPortalWorkflowCommentDialog">
          {{ pendingPortalWorkflowAction?.label || '确认' }}
        </el-button>
      </template>
    </el-dialog>
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

.chart-panel {
  height: 350px;
}

.school-ranking-shell {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.school-ranking-summary {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  padding: 18px 20px;
  border-radius: 20px;
  background: linear-gradient(135deg, rgba(54, 181, 154, 0.12), rgba(46, 155, 234, 0.1));
}

.school-ranking-summary strong {
  color: var(--text-main);
}

.school-ranking-summary span {
  max-width: 540px;
  color: var(--text-subtle);
  line-height: 1.7;
}

.school-group-card {
  display: grid;
  gap: 18px;
  padding: 20px;
  border: 1px solid rgba(53, 108, 184, 0.14);
  border-radius: 20px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(246, 250, 255, 0.94));
  box-shadow: 0 14px 32px rgba(24, 56, 87, 0.08);
}

.school-group-card__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 18px;
}

.school-group-card__kicker {
  color: var(--brand-strong);
  font-size: 13px;
  font-weight: 700;
}

.school-group-card__header h3 {
  margin: 6px 0 0;
  font-family: var(--title-font);
  font-size: 22px;
  line-height: 1.35;
}

.school-group-card__total {
  min-width: 150px;
  padding: 12px 16px;
  border-radius: 16px;
  background: rgba(46, 155, 234, 0.1);
  text-align: right;
}

.school-group-card__total span {
  display: block;
  color: var(--text-subtle);
  font-size: 13px;
}

.school-group-card__total strong {
  display: block;
  margin-top: 4px;
  color: var(--brand-strong);
  font-size: 30px;
  line-height: 1;
}

.school-group-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
}

.school-group-panel {
  display: flex;
  min-width: 0;
  min-height: 360px;
  flex-direction: column;
  gap: 12px;
  padding: 16px;
  border: 1px solid rgba(53, 108, 184, 0.12);
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.86);
}

.school-group-panel__head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.school-group-panel__head h4 {
  margin: 0;
  color: var(--text-main);
  font-size: 18px;
}

.school-group-panel__head span {
  display: block;
  margin-top: 4px;
  color: var(--text-subtle);
  font-size: 13px;
}

.school-group-panel__head strong {
  color: var(--brand-strong);
  font-size: 28px;
  line-height: 1;
  white-space: nowrap;
}

.school-group-panel__head small {
  margin-left: 2px;
  color: var(--text-subtle);
  font-size: 13px;
  font-weight: 600;
}

.school-group-pie {
  height: 320px;
  min-width: 0;
}

.school-group-legend {
  display: grid;
  gap: 8px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.school-group-legend li {
  display: grid;
  grid-template-columns: 10px minmax(0, 1fr) auto auto;
  align-items: center;
  gap: 8px;
  min-height: 28px;
  padding: 6px 8px;
  border-radius: 10px;
  background: rgba(245, 248, 255, 0.72);
  color: var(--text-subtle);
  font-size: 13px;
}

.school-group-legend__dot {
  width: 10px;
  height: 10px;
  border-radius: 999px;
}

.school-group-legend__name {
  min-width: 0;
  overflow: hidden;
  color: var(--text-main);
  text-overflow: ellipsis;
  white-space: nowrap;
}

.school-group-legend strong {
  color: var(--text-main);
  font-size: 13px;
  white-space: nowrap;
}

.school-group-empty {
  display: grid;
  min-height: 300px;
  place-items: center;
  color: var(--text-subtle);
  border: 1px dashed rgba(53, 108, 184, 0.18);
  border-radius: 16px;
  background: rgba(247, 251, 255, 0.72);
}

.school-ranking-chart {
  height: 460px;
}

.dashboard-empty {
  display: grid;
  place-items: center;
  min-height: 280px;
  padding: 24px;
  border: 1px dashed rgba(53, 108, 184, 0.22);
  border-radius: 24px;
  color: var(--text-subtle);
  background: linear-gradient(135deg, rgba(247, 251, 255, 0.96), rgba(241, 248, 255, 0.92));
}

.school-student-summary {
  display: grid;
  gap: 10px;
  margin-bottom: 12px;
  color: var(--text-subtle);
}

.school-student-summary__total {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.school-student-summary__total strong {
  color: var(--text-main);
}

.school-student-summary__schools {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  max-height: 96px;
  margin: 0;
  padding: 0;
  overflow-y: auto;
  list-style: none;
}

.school-student-summary__schools li {
  list-style: none;
}

.school-student-summary__chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  max-width: 260px;
  padding: 5px 8px;
  border: 1px solid rgba(53, 108, 184, 0.14);
  border-radius: 999px;
  background: rgba(245, 248, 255, 0.86);
  color: inherit;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.school-student-summary__chip:hover:not(:disabled) {
  border-color: rgba(53, 108, 184, 0.32);
  background: rgba(233, 241, 255, 0.96);
}

.school-student-summary__chip.is-active {
  border-color: rgba(46, 155, 234, 0.42);
  background: rgba(223, 238, 255, 0.96);
  box-shadow: inset 0 0 0 1px rgba(46, 155, 234, 0.12);
}

.school-student-summary__chip--reset {
  background: rgba(249, 250, 251, 0.96);
}

.school-student-summary__chip--reset.is-disabled,
.school-student-summary__chip:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.school-student-summary__chip span {
  min-width: 0;
  overflow: hidden;
  color: var(--text-main);
  text-overflow: ellipsis;
  white-space: nowrap;
}

.school-student-summary__chip strong {
  color: var(--brand-strong);
  white-space: nowrap;
}

.workflow-comment-dialog {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.workflow-comment-dialog__hint {
  margin: 0;
  color: var(--text-subtle);
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

  .school-group-grid {
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

  .school-ranking-summary {
    flex-direction: column;
  }

  .school-group-card__header {
    flex-direction: column;
  }

  .school-group-card__total {
    width: 100%;
    text-align: left;
  }
}
</style>
