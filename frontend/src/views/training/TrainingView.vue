<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useRoute } from 'vue-router'

import {
  createOutboundStudy,
  createScientificReport,
  createTrainingPlan,
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
  type TrainingPlanRecord,
  type TrainingPlanUpsert,
  type TrainingStats,
} from '../../api/training'

const route = useRoute()
const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const dialogMode = ref<'create' | 'edit'>('create')
const currentId = ref<number | null>(null)

const stats = ref<TrainingStats>({
  training_plan_total: 0,
  pending_confirmation_total: 0,
  report_pending_total: 0,
  outbound_active_total: 0,
})

const trainingPlans = ref<TrainingPlanRecord[]>([])
const scientificReports = ref<ScientificReportRecord[]>([])
const outboundStudies = ref<OutboundStudyRecord[]>([])

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
const sectionTitle = computed(
  () =>
    ({
      plans: '培养方案管理',
      reports: '科研报告管理',
      outbound: '外出研修管理',
    }[activeSection.value] || '培养管理'),
)
const statCards = computed(() => [
  { label: '培养方案', value: stats.value.training_plan_total },
  { label: '待确认方案', value: stats.value.pending_confirmation_total },
  { label: '待审报告', value: stats.value.report_pending_total },
  { label: '在途研修', value: stats.value.outbound_active_total },
])

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

async function loadData() {
  loading.value = true
  try {
    const [statsResponse, plansResponse, reportsResponse, outboundResponse] = await Promise.all([
      getTrainingStats(),
      listTrainingPlans(),
      listScientificReports(),
      listOutboundStudies(),
    ])
    stats.value = statsResponse.data
    trainingPlans.value = plansResponse.data.items
    scientificReports.value = reportsResponse.data.items
    outboundStudies.value = outboundResponse.data.items
  } finally {
    loading.value = false
  }
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
    } else {
      if (dialogMode.value === 'create') {
        await createOutboundStudy(outboundForm)
      } else if (currentId.value !== null) {
        await updateOutboundStudy(currentId.value, outboundForm)
      }
    }
    ElMessage.success('保存成功')
    dialogVisible.value = false
    await loadData()
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  void loadData()
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
          <p class="section-tag">过程控制</p>
          <h2>{{ sectionTitle }}</h2>
        </div>
        <el-button type="primary" round @click="openCreateDialog">新增记录</el-button>
      </div>

      <el-table v-if="activeSection === 'plans'" :data="trainingPlans" stripe v-loading="loading">
        <el-table-column prop="student_no" label="学号" width="120" />
        <el-table-column prop="student_name" label="学生" width="100" />
        <el-table-column prop="advisor_name" label="导师" width="100" />
        <el-table-column prop="version_no" label="版本" width="90" />
        <el-table-column prop="report_cycle" label="报告周期" width="100" />
        <el-table-column prop="plan_status" label="状态" width="120" />
        <el-table-column prop="scientific_goal" label="科研目标" min-width="220" />
        <el-table-column label="操作" width="100">
          <template #default="scope"><el-button link type="primary" @click="openEditDialog(scope.row)">编辑</el-button></template>
        </el-table-column>
      </el-table>

      <el-table v-else-if="activeSection === 'reports'" :data="scientificReports" stripe v-loading="loading">
        <el-table-column prop="student_no" label="学号" width="120" />
        <el-table-column prop="student_name" label="学生" width="100" />
        <el-table-column prop="period_label" label="周期" width="120" />
        <el-table-column prop="report_status" label="状态" width="120" />
        <el-table-column prop="reviewer_name" label="审阅人" width="110" />
        <el-table-column prop="review_score" label="评分" width="90" />
        <el-table-column prop="summary" label="摘要" min-width="240" />
        <el-table-column label="操作" width="100">
          <template #default="scope"><el-button link type="primary" @click="openEditDialog(scope.row)">编辑</el-button></template>
        </el-table-column>
      </el-table>

      <el-table v-else :data="outboundStudies" stripe v-loading="loading">
        <el-table-column prop="student_no" label="学号" width="120" />
        <el-table-column prop="student_name" label="学生" width="100" />
        <el-table-column prop="advisor_name" label="导师" width="100" />
        <el-table-column prop="study_type" label="研修类型" width="120" />
        <el-table-column prop="destination" label="目的地" min-width="180" />
        <el-table-column prop="approval_status" label="审批状态" width="120" />
        <el-table-column prop="expected_outcome" label="预期成果" min-width="220" />
        <el-table-column label="操作" width="100">
          <template #default="scope"><el-button link type="primary" @click="openEditDialog(scope.row)">编辑</el-button></template>
        </el-table-column>
      </el-table>
    </section>

    <el-dialog v-model="dialogVisible" :title="dialogMode === 'create' ? `新增${sectionTitle}` : `编辑${sectionTitle}`" width="760px">
      <el-form v-if="activeSection === 'plans'" label-width="110px" class="dialog-grid">
        <el-form-item label="学号"><el-input v-model="planForm.student_no" /></el-form-item>
        <el-form-item label="学生"><el-input v-model="planForm.student_name" /></el-form-item>
        <el-form-item label="导师"><el-input v-model="planForm.advisor_name" /></el-form-item>
        <el-form-item label="版本"><el-input v-model="planForm.version_no" /></el-form-item>
        <el-form-item label="报告周期"><el-input v-model="planForm.report_cycle" /></el-form-item>
        <el-form-item label="状态"><el-input v-model="planForm.plan_status" /></el-form-item>
        <el-form-item label="科研目标" class="dialog-grid__full"><el-input v-model="planForm.scientific_goal" type="textarea" :rows="3" /></el-form-item>
        <el-form-item label="考核规则" class="dialog-grid__full"><el-input v-model="planForm.assessment_rule" type="textarea" :rows="3" /></el-form-item>
      </el-form>

      <el-form v-else-if="activeSection === 'reports'" label-width="110px" class="dialog-grid">
        <el-form-item label="学号"><el-input v-model="reportForm.student_no" /></el-form-item>
        <el-form-item label="学生"><el-input v-model="reportForm.student_name" /></el-form-item>
        <el-form-item label="报告周期"><el-input v-model="reportForm.period_label" /></el-form-item>
        <el-form-item label="状态"><el-input v-model="reportForm.report_status" /></el-form-item>
        <el-form-item label="审阅人"><el-input v-model="reportForm.reviewer_name" /></el-form-item>
        <el-form-item label="评分"><el-input-number v-model="reportForm.review_score" :min="0" :max="100" :precision="1" controls-position="right" /></el-form-item>
        <el-form-item label="摘要" class="dialog-grid__full"><el-input v-model="reportForm.summary" type="textarea" :rows="4" /></el-form-item>
      </el-form>

      <el-form v-else label-width="110px" class="dialog-grid">
        <el-form-item label="学号"><el-input v-model="outboundForm.student_no" /></el-form-item>
        <el-form-item label="学生"><el-input v-model="outboundForm.student_name" /></el-form-item>
        <el-form-item label="导师"><el-input v-model="outboundForm.advisor_name" /></el-form-item>
        <el-form-item label="研修类型"><el-input v-model="outboundForm.study_type" /></el-form-item>
        <el-form-item label="目的地"><el-input v-model="outboundForm.destination" /></el-form-item>
        <el-form-item label="审批状态"><el-input v-model="outboundForm.approval_status" /></el-form-item>
        <el-form-item label="开始日期"><el-input v-model="outboundForm.start_date" /></el-form-item>
        <el-form-item label="结束日期"><el-input v-model="outboundForm.end_date" /></el-form-item>
        <el-form-item label="预期成果" class="dialog-grid__full"><el-input v-model="outboundForm.expected_outcome" type="textarea" :rows="3" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submit">保存</el-button>
      </template>
    </el-dialog>
  </section>
</template>

<style scoped>
.content-stack,
.stat-grid {
  display: grid;
  gap: 22px;
}

.stat-grid {
  grid-template-columns: repeat(4, minmax(0, 1fr));
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
  justify-content: space-between;
  gap: 16px;
  align-items: center;
  margin-bottom: 18px;
}

.section-tag,
.section-card h2,
.pill-card p {
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
}

.pill-card {
  padding: 18px;
  border-radius: 22px;
  background: linear-gradient(135deg, rgba(245, 248, 255, 0.98), rgba(235, 245, 255, 0.92));
}

.pill-card strong {
  display: block;
  margin-top: 10px;
  color: #12315e;
  font-size: 28px;
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
  .dialog-grid {
    grid-template-columns: 1fr;
  }
}
</style>
