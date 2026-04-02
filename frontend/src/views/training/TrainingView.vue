<script setup lang="ts">
import axios from 'axios'
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRoute } from 'vue-router'

import {
  batchDeleteOutboundStudies,
  batchDeleteScientificReports,
  batchDeleteTrainingPlans,
  createOutboundStudy,
  createScientificReport,
  createTrainingPlan,
  deleteOutboundStudy,
  deleteScientificReport,
  deleteTrainingPlan,
  getTrainingOptions,
  getTrainingStats,
  listOutboundStudies,
  listScientificReports,
  listTrainingPlans,
  updateOutboundStudy,
  updateScientificReport,
  updateTrainingPlan,
  type OutboundStudyRecord,
  type OutboundStudyUpsert,
  type ScientificReportRecord,
  type ScientificReportUpsert,
  type TrainingOptions,
  type TrainingPlanRecord,
  type TrainingPlanUpsert,
  type TrainingStats,
} from '../../api/training'

const route = useRoute()
const loading = ref(false)
const bootstrapping = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const dialogMode = ref<'create' | 'edit'>('create')
const currentId = ref<number | null>(null)
const selectedIds = ref<number[]>([])

const stats = ref<TrainingStats>({
  training_plan_total: 0,
  pending_confirmation_total: 0,
  report_pending_total: 0,
  outbound_active_total: 0,
})

const trainingOptions = ref<TrainingOptions>({
  plan_status_options: [],
  report_cycle_options: [],
  report_status_options: [],
  study_type_options: [],
  approval_status_options: [],
  advisor_options: [],
  reviewer_options: [],
})

const trainingPlans = ref<TrainingPlanRecord[]>([])
const scientificReports = ref<ScientificReportRecord[]>([])
const outboundStudies = ref<OutboundStudyRecord[]>([])

const planFilters = reactive({
  keyword: '',
  plan_status: '',
  advisor_name: '',
  report_cycle: '',
})

const reportFilters = reactive({
  keyword: '',
  status: '',
  reviewer_name: '',
})

const outboundFilters = reactive({
  keyword: '',
  status: '',
  study_type: '',
  advisor_name: '',
})

const planForm = reactive<TrainingPlanUpsert>({
  student_no: '',
  student_name: '',
  advisor_name: '',
  version_no: 'v1.0',
  report_cycle: '季度',
  plan_status: '待学生确认',
  scientific_goal: '',
  assessment_rule: '',
})

const reportForm = reactive<ScientificReportUpsert>({
  student_no: '',
  student_name: '',
  period_label: '',
  report_status: '待导师审阅',
  reviewer_name: '',
  review_score: undefined,
  summary: '',
})

const outboundForm = reactive<OutboundStudyUpsert>({
  student_no: '',
  student_name: '',
  advisor_name: '',
  study_type: '联合培养',
  destination: '',
  start_date: '',
  end_date: '',
  approval_status: '审批中',
  expected_outcome: '',
})

const activeSection = computed(() => String(route.meta.section || 'plans'))
const sectionMeta: Record<string, { title: string; tag: string; createLabel: string; batchDeleteLabel: string }> = {
  plans: { title: '培养方案管理', tag: '培养控制', createLabel: '登记培养方案', batchDeleteLabel: '批量删除方案' },
  reports: { title: '科研报告管理', tag: '过程审阅', createLabel: '登记科研报告', batchDeleteLabel: '批量删除报告' },
  outbound: { title: '外出研修管理', tag: '过程审批', createLabel: '发起外出研修', batchDeleteLabel: '批量删除研修' },
}
const sectionConfig = computed(() => sectionMeta[activeSection.value] || sectionMeta.plans)
const advisorOptions = computed(() => trainingOptions.value.advisor_options)
const reviewerOptions = computed(() => trainingOptions.value.reviewer_options)
const currentTotal = computed(() => {
  if (activeSection.value === 'plans') return trainingPlans.value.length
  if (activeSection.value === 'reports') return scientificReports.value.length
  return outboundStudies.value.length
})
const statCards = computed(() => [
  { label: '培养方案', value: stats.value.training_plan_total },
  { label: '待确认方案', value: stats.value.pending_confirmation_total },
  { label: '待审报告', value: stats.value.report_pending_total },
  { label: '在途研修', value: stats.value.outbound_active_total },
])

function getErrorMessage(error: unknown) {
  if (axios.isAxiosError(error)) {
    return String(error.response?.data?.detail || error.message || '请求失败')
  }
  return '请求失败'
}

function getStatusTagType(status: string) {
  if (['执行中', '已通过', '已批准', '研修中'].includes(status)) return 'success'
  if (['待学生确认', '待导师审阅', '审批中'].includes(status)) return 'warning'
  if (['退回修改', '已驳回'].includes(status)) return 'danger'
  return 'info'
}

function resetSelection() {
  selectedIds.value = []
}

function resetForms() {
  currentId.value = null
  Object.assign(planForm, {
    student_no: '',
    student_name: '',
    advisor_name: '',
    version_no: 'v1.0',
    report_cycle: '季度',
    plan_status: '待学生确认',
    scientific_goal: '',
    assessment_rule: '',
  })
  Object.assign(reportForm, {
    student_no: '',
    student_name: '',
    period_label: '',
    report_status: '待导师审阅',
    reviewer_name: '',
    review_score: undefined,
    summary: '',
  })
  Object.assign(outboundForm, {
    student_no: '',
    student_name: '',
    advisor_name: '',
    study_type: '联合培养',
    destination: '',
    start_date: '',
    end_date: '',
    approval_status: '审批中',
    expected_outcome: '',
  })
}

function openCreateDialog() {
  dialogMode.value = 'create'
  resetForms()
  dialogVisible.value = true
}

function openEditDialog(row: TrainingPlanRecord | ScientificReportRecord | OutboundStudyRecord) {
  dialogMode.value = 'edit'
  currentId.value = row.id
  if (activeSection.value === 'plans') {
    Object.assign(planForm, row)
  } else if (activeSection.value === 'reports') {
    Object.assign(reportForm, row)
  } else {
    Object.assign(outboundForm, row)
  }
  dialogVisible.value = true
}

function handleSelectionChange(rows: Array<{ id: number }>) {
  selectedIds.value = rows.map((item) => item.id)
}

async function loadStats() {
  const response = await getTrainingStats()
  stats.value = response.data
}

async function loadBootstrapData() {
  bootstrapping.value = true
  try {
    const [statsResponse, optionsResponse] = await Promise.all([getTrainingStats(), getTrainingOptions()])
    stats.value = statsResponse.data
    trainingOptions.value = optionsResponse.data
  } finally {
    bootstrapping.value = false
  }
}

async function loadCurrentSection() {
  loading.value = true
  try {
    if (activeSection.value === 'plans') {
      const response = await listTrainingPlans(planFilters)
      trainingPlans.value = response.data.items
      return
    }
    if (activeSection.value === 'reports') {
      const response = await listScientificReports(reportFilters)
      scientificReports.value = response.data.items
      return
    }
    const response = await listOutboundStudies(outboundFilters)
    outboundStudies.value = response.data.items
  } finally {
    loading.value = false
  }
}

async function searchCurrentSection() {
  resetSelection()
  await loadCurrentSection()
}

async function resetCurrentFilters() {
  if (activeSection.value === 'plans') {
    Object.assign(planFilters, { keyword: '', plan_status: '', advisor_name: '', report_cycle: '' })
  } else if (activeSection.value === 'reports') {
    Object.assign(reportFilters, { keyword: '', status: '', reviewer_name: '' })
  } else {
    Object.assign(outboundFilters, { keyword: '', status: '', study_type: '', advisor_name: '' })
  }
  await searchCurrentSection()
}

async function submit() {
  submitting.value = true
  try {
    if (activeSection.value === 'plans') {
      if (dialogMode.value === 'create') {
        await createTrainingPlan(planForm)
      } else if (currentId.value !== null) {
        await updateTrainingPlan(currentId.value, planForm)
      }
    } else if (activeSection.value === 'reports') {
      if (dialogMode.value === 'create') {
        await createScientificReport(reportForm)
      } else if (currentId.value !== null) {
        await updateScientificReport(currentId.value, reportForm)
      }
    } else if (dialogMode.value === 'create') {
      await createOutboundStudy(outboundForm)
    } else if (currentId.value !== null) {
      await updateOutboundStudy(currentId.value, outboundForm)
    }
    ElMessage.success('保存成功')
    dialogVisible.value = false
    await Promise.all([loadStats(), loadCurrentSection()])
  } catch (error) {
    ElMessage.error(getErrorMessage(error))
  } finally {
    submitting.value = false
  }
}

async function removeCurrentRecord(row: TrainingPlanRecord | ScientificReportRecord | OutboundStudyRecord) {
  await ElMessageBox.confirm(`确定删除 ${row.student_name} 的当前记录吗？`, '删除确认', { type: 'warning' })
  try {
    if (activeSection.value === 'plans') {
      await deleteTrainingPlan(row.id)
    } else if (activeSection.value === 'reports') {
      await deleteScientificReport(row.id)
    } else {
      await deleteOutboundStudy(row.id)
    }
    ElMessage.success('删除成功')
    resetSelection()
    await Promise.all([loadStats(), loadCurrentSection()])
  } catch (error) {
    ElMessage.error(getErrorMessage(error))
  }
}

async function batchRemoveCurrentSection() {
  if (!selectedIds.value.length) {
    ElMessage.warning('请先选择需要删除的记录')
    return
  }
  await ElMessageBox.confirm(`已选择 ${selectedIds.value.length} 条记录，确认批量删除吗？`, '批量删除确认', { type: 'warning' })
  try {
    if (activeSection.value === 'plans') {
      await batchDeleteTrainingPlans(selectedIds.value)
    } else if (activeSection.value === 'reports') {
      await batchDeleteScientificReports(selectedIds.value)
    } else {
      await batchDeleteOutboundStudies(selectedIds.value)
    }
    ElMessage.success('批量删除成功')
    resetSelection()
    await Promise.all([loadStats(), loadCurrentSection()])
  } catch (error) {
    ElMessage.error(getErrorMessage(error))
  }
}

watch(
  activeSection,
  () => {
    dialogVisible.value = false
    resetForms()
    resetSelection()
    void loadCurrentSection()
  },
)

onMounted(() => {
  void loadBootstrapData().then(() => loadCurrentSection())
})
</script>

<template>
  <section class="content-stack">
    <section class="stat-grid">
      <article v-for="card in statCards" :key="card.label" class="pill-card">
        <p>{{ card.label }}</p>
        <strong>{{ card.value }}</strong>
      </article>
    </section>

    <section class="section-card">
      <div class="section-card__header">
        <div>
          <p class="section-tag">{{ sectionConfig.tag }}</p>
          <h2>{{ sectionConfig.title }}</h2>
          <p class="section-summary">当前共 {{ currentTotal }} 条记录，可按状态、导师和关键字快速筛选。</p>
        </div>
        <div class="header-actions">
          <el-button plain :disabled="!selectedIds.length" @click="batchRemoveCurrentSection">{{ sectionConfig.batchDeleteLabel }}</el-button>
          <el-button type="primary" round @click="openCreateDialog">{{ sectionConfig.createLabel }}</el-button>
        </div>
      </div>

      <div v-if="activeSection === 'plans'" class="filter-grid">
        <el-input v-model="planFilters.keyword" placeholder="输入学号、学生姓名或科研目标" clearable @keyup.enter="searchCurrentSection" />
        <el-select v-model="planFilters.plan_status" placeholder="方案状态" clearable>
          <el-option v-for="item in trainingOptions.plan_status_options" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
        <el-select v-model="planFilters.advisor_name" placeholder="导师" clearable filterable>
          <el-option v-for="item in advisorOptions" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
        <el-select v-model="planFilters.report_cycle" placeholder="汇报周期" clearable>
          <el-option v-for="item in trainingOptions.report_cycle_options" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
        <div class="filter-actions">
          <el-button type="primary" @click="searchCurrentSection">查询方案</el-button>
          <el-button @click="resetCurrentFilters">重置</el-button>
        </div>
      </div>

      <div v-else-if="activeSection === 'reports'" class="filter-grid">
        <el-input v-model="reportFilters.keyword" placeholder="输入学号、学生姓名、周期或摘要" clearable @keyup.enter="searchCurrentSection" />
        <el-select v-model="reportFilters.status" placeholder="报告状态" clearable>
          <el-option v-for="item in trainingOptions.report_status_options" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
        <el-select v-model="reportFilters.reviewer_name" placeholder="审阅人" clearable filterable>
          <el-option v-for="item in reviewerOptions" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
        <div class="filter-actions">
          <el-button type="primary" @click="searchCurrentSection">查询报告</el-button>
          <el-button @click="resetCurrentFilters">重置</el-button>
        </div>
      </div>

      <div v-else class="filter-grid">
        <el-input v-model="outboundFilters.keyword" placeholder="输入学号、学生姓名、目的地或预期成果" clearable @keyup.enter="searchCurrentSection" />
        <el-select v-model="outboundFilters.status" placeholder="审批状态" clearable>
          <el-option v-for="item in trainingOptions.approval_status_options" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
        <el-select v-model="outboundFilters.study_type" placeholder="研修类型" clearable>
          <el-option v-for="item in trainingOptions.study_type_options" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
        <el-select v-model="outboundFilters.advisor_name" placeholder="导师" clearable filterable>
          <el-option v-for="item in advisorOptions" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
        <div class="filter-actions">
          <el-button type="primary" @click="searchCurrentSection">查询研修</el-button>
          <el-button @click="resetCurrentFilters">重置</el-button>
        </div>
      </div>

      <el-table v-if="activeSection === 'plans'" :data="trainingPlans" stripe v-loading="loading || bootstrapping" @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="52" />
        <el-table-column prop="student_no" label="学号" width="120" />
        <el-table-column prop="student_name" label="学生" width="100" />
        <el-table-column prop="advisor_name" label="导师" width="100" />
        <el-table-column prop="version_no" label="版本" width="90" />
        <el-table-column prop="report_cycle" label="报告周期" width="100" />
        <el-table-column label="状态" width="120">
          <template #default="scope"><el-tag :type="getStatusTagType(scope.row.plan_status)">{{ scope.row.plan_status }}</el-tag></template>
        </el-table-column>
        <el-table-column prop="scientific_goal" label="科研目标" min-width="220" />
        <el-table-column label="操作" width="170" fixed="right">
          <template #default="scope">
            <el-button link type="primary" @click="openEditDialog(scope.row)">维护方案</el-button>
            <el-button link type="danger" @click="removeCurrentRecord(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-table v-else-if="activeSection === 'reports'" :data="scientificReports" stripe v-loading="loading || bootstrapping" @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="52" />
        <el-table-column prop="student_no" label="学号" width="120" />
        <el-table-column prop="student_name" label="学生" width="100" />
        <el-table-column prop="period_label" label="周期" width="120" />
        <el-table-column label="状态" width="120">
          <template #default="scope"><el-tag :type="getStatusTagType(scope.row.report_status)">{{ scope.row.report_status }}</el-tag></template>
        </el-table-column>
        <el-table-column prop="reviewer_name" label="审阅人" width="110" />
        <el-table-column prop="review_score" label="评分" width="90" />
        <el-table-column prop="summary" label="摘要" min-width="240" />
        <el-table-column label="操作" width="170" fixed="right">
          <template #default="scope">
            <el-button link type="primary" @click="openEditDialog(scope.row)">维护报告</el-button>
            <el-button link type="danger" @click="removeCurrentRecord(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-table v-else :data="outboundStudies" stripe v-loading="loading || bootstrapping" @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="52" />
        <el-table-column prop="student_no" label="学号" width="120" />
        <el-table-column prop="student_name" label="学生" width="100" />
        <el-table-column prop="advisor_name" label="导师" width="100" />
        <el-table-column prop="study_type" label="研修类型" width="120" />
        <el-table-column prop="destination" label="目的地" min-width="180" />
        <el-table-column label="审批状态" width="120">
          <template #default="scope"><el-tag :type="getStatusTagType(scope.row.approval_status)">{{ scope.row.approval_status }}</el-tag></template>
        </el-table-column>
        <el-table-column prop="expected_outcome" label="预期成果" min-width="220" />
        <el-table-column label="操作" width="170" fixed="right">
          <template #default="scope">
            <el-button link type="primary" @click="openEditDialog(scope.row)">维护研修</el-button>
            <el-button link type="danger" @click="removeCurrentRecord(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </section>

    <el-dialog v-model="dialogVisible" :title="dialogMode === 'create' ? sectionConfig.createLabel : `维护${sectionConfig.title}`" width="760px">
      <el-form v-if="activeSection === 'plans'" label-width="110px" class="dialog-grid">
        <el-form-item label="学号"><el-input v-model="planForm.student_no" /></el-form-item>
        <el-form-item label="学生"><el-input v-model="planForm.student_name" /></el-form-item>
        <el-form-item label="导师">
          <el-select v-model="planForm.advisor_name" filterable allow-create default-first-option>
            <el-option v-for="item in advisorOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="版本"><el-input v-model="planForm.version_no" /></el-form-item>
        <el-form-item label="报告周期">
          <el-select v-model="planForm.report_cycle">
            <el-option v-for="item in trainingOptions.report_cycle_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="planForm.plan_status">
            <el-option v-for="item in trainingOptions.plan_status_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="科研目标" class="dialog-grid__full"><el-input v-model="planForm.scientific_goal" type="textarea" :rows="3" /></el-form-item>
        <el-form-item label="考核规则" class="dialog-grid__full"><el-input v-model="planForm.assessment_rule" type="textarea" :rows="3" /></el-form-item>
      </el-form>

      <el-form v-else-if="activeSection === 'reports'" label-width="110px" class="dialog-grid">
        <el-form-item label="学号"><el-input v-model="reportForm.student_no" /></el-form-item>
        <el-form-item label="学生"><el-input v-model="reportForm.student_name" /></el-form-item>
        <el-form-item label="报告周期"><el-input v-model="reportForm.period_label" /></el-form-item>
        <el-form-item label="状态">
          <el-select v-model="reportForm.report_status">
            <el-option v-for="item in trainingOptions.report_status_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="审阅人">
          <el-select v-model="reportForm.reviewer_name" filterable allow-create default-first-option clearable>
            <el-option v-for="item in reviewerOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="评分"><el-input-number v-model="reportForm.review_score" :min="0" :max="100" :precision="1" controls-position="right" /></el-form-item>
        <el-form-item label="摘要" class="dialog-grid__full"><el-input v-model="reportForm.summary" type="textarea" :rows="4" /></el-form-item>
      </el-form>

      <el-form v-else label-width="110px" class="dialog-grid">
        <el-form-item label="学号"><el-input v-model="outboundForm.student_no" /></el-form-item>
        <el-form-item label="学生"><el-input v-model="outboundForm.student_name" /></el-form-item>
        <el-form-item label="导师">
          <el-select v-model="outboundForm.advisor_name" filterable allow-create default-first-option>
            <el-option v-for="item in advisorOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="研修类型">
          <el-select v-model="outboundForm.study_type">
            <el-option v-for="item in trainingOptions.study_type_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="目的地"><el-input v-model="outboundForm.destination" /></el-form-item>
        <el-form-item label="审批状态">
          <el-select v-model="outboundForm.approval_status">
            <el-option v-for="item in trainingOptions.approval_status_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="开始日期"><el-date-picker v-model="outboundForm.start_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" /></el-form-item>
        <el-form-item label="结束日期"><el-date-picker v-model="outboundForm.end_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" /></el-form-item>
        <el-form-item label="预期成果" class="dialog-grid__full"><el-input v-model="outboundForm.expected_outcome" type="textarea" :rows="3" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submit">提交保存</el-button>
      </template>
    </el-dialog>
  </section>
</template>

<style scoped>
.content-stack,
.stat-grid {
  display: grid;
  gap: 14px;
}

.header-actions,
.filter-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.stat-grid {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.section-card {
  border: 1px solid rgba(18, 50, 95, 0.08);
  border-radius: 20px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 18px 44px rgba(14, 40, 88, 0.07);
}

.section-card__header {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
  margin-bottom: 12px;
}

.section-tag,
.section-summary,
.section-card h2,
.pill-card p {
  margin: 0;
}

.section-tag {
  color: #7183a0;
  font-size: 11px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.section-card h2 {
  margin-top: 4px;
  color: #12284d;
  font-size: 16px;
}

.section-summary {
  margin-top: 8px;
  color: #6e7f98;
  font-size: 13px;
}

.filter-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 12px;
  margin-bottom: 14px;
}

.pill-card {
  padding: 14px 16px;
  border-radius: 18px;
  background: linear-gradient(135deg, rgba(245, 248, 255, 0.98), rgba(235, 245, 255, 0.92));
}

.pill-card strong {
  display: block;
  margin-top: 6px;
  color: #12315e;
  font-size: 22px;
}

.dialog-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 4px 18px;
}

.dialog-grid__full {
  grid-column: 1 / -1;
}

@media (max-width: 980px) {
  .stat-grid,
  .dialog-grid,
  .filter-grid {
    grid-template-columns: 1fr;
  }

  .section-card__header {
    align-items: flex-start;
    flex-direction: column;
  }
}
</style>
