<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'

import {
  createRecruitmentApplication,
  createRecruitmentPlan,
  deleteRecruitmentApplication,
  getRecruitmentStats,
  getRecruitmentWorkbench,
  listRecruitmentApplications,
  listRecruitmentPlans,
  updateRecruitmentApplication,
  updateRecruitmentPlan,
  type RecruitApplicationRecord,
  type RecruitApplicationUpsert,
  type RecruitPlanRecord,
  type RecruitPlanUpsert,
  type RecruitStats,
  type RecruitWorkbench,
} from '../../api/recruitment'


const stageMeta = [
  { title: '报名配置', detail: '招生计划、学期名额与开放策略' },
  { title: '资格审核', detail: '材料齐套性与规则校验' },
  { title: '材料评分', detail: '评分人配置与专家评审' },
  { title: '面试执行', detail: '分组排期、面试成绩归集' },
  { title: '预录取', detail: '拟录取、候补和结果确认' },
]

const semesterOptions = ['春', '秋']
const planStageOptions = ['报名配置', '资格审核', '评分推荐', '材料评分', '面试执行', '预录取']
const materialStatusOptions = ['材料齐全', '待补材料', '已退回修改']
const applicationStatusOptions = ['报名已提交', '资格审核通过', '材料评分中', '面试待安排', '面试完成', '预录取', '同意录取', '不录取']
const degreeOptions = ['硕士', '本科', '博士']

const plans = ref<RecruitPlanRecord[]>([])
const applications = ref<RecruitApplicationRecord[]>([])
const workbench = ref<RecruitWorkbench>({ plans: [], pipeline: [], pending_tasks: [] })
const stats = ref<RecruitStats>({
  plan_count: 0,
  open_plan_count: 0,
  application_total: 0,
  pending_review_total: 0,
  pre_admit_total: 0,
})

const plansLoading = ref(false)
const applicationsLoading = ref(false)
const planDialogVisible = ref(false)
const applicationDialogVisible = ref(false)
const planMode = ref<'create' | 'edit'>('create')
const applicationMode = ref<'create' | 'edit'>('create')
const planSubmitting = ref(false)
const applicationSubmitting = ref(false)
const selectedPlanId = ref<number | undefined>()
const editingPlanId = ref<number | null>(null)
const editingApplicationId = ref<number | null>(null)

const planFormRef = ref<FormInstance>()
const applicationFormRef = ref<FormInstance>()

const applicationFilters = reactive({
  keyword: '',
  status: '',
})

const planForm = reactive<RecruitPlanUpsert>({
  plan_name: '',
  academic_year: String(new Date().getFullYear()),
  semester: '秋',
  current_stage: '报名配置',
  target_quota: 30,
  interview_group_count: 3,
  is_open: true,
})

const applicationForm = reactive<RecruitApplicationUpsert>({
  plan_id: 0,
  candidate_no: '',
  student_name: '',
  graduation_school: '',
  highest_degree: '硕士',
  intended_field: '',
  material_status: '材料齐全',
  application_status: '报名已提交',
  reviewer_name: '',
  final_score: undefined,
})

const planRules: FormRules<RecruitPlanUpsert> = {
  plan_name: [{ required: true, message: '请输入计划名称', trigger: 'blur' }],
  academic_year: [{ required: true, message: '请输入学年', trigger: 'blur' }],
  semester: [{ required: true, message: '请选择学期', trigger: 'change' }],
  current_stage: [{ required: true, message: '请选择当前阶段', trigger: 'change' }],
  target_quota: [{ required: true, message: '请输入计划名额', trigger: 'change' }],
  interview_group_count: [{ required: true, message: '请输入面试组数', trigger: 'change' }],
}

const applicationRules: FormRules<RecruitApplicationUpsert> = {
  plan_id: [{ required: true, message: '请选择招生计划', trigger: 'change' }],
  candidate_no: [{ required: true, message: '请输入报名号', trigger: 'blur' }],
  student_name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  graduation_school: [{ required: true, message: '请输入毕业院校', trigger: 'blur' }],
  highest_degree: [{ required: true, message: '请选择最高学历', trigger: 'change' }],
  intended_field: [{ required: true, message: '请输入研究方向', trigger: 'blur' }],
  material_status: [{ required: true, message: '请选择材料状态', trigger: 'change' }],
  application_status: [{ required: true, message: '请选择申请状态', trigger: 'change' }],
}

const statsCards = computed(() => [
  { label: '招生计划', value: stats.value.plan_count, tone: 'healthy' },
  { label: '开放计划', value: stats.value.open_plan_count, tone: 'attention' },
  { label: '报名申请', value: stats.value.application_total, tone: 'neutral' },
  { label: '待审核', value: stats.value.pending_review_total, tone: 'warning' },
  { label: '预录取', value: stats.value.pre_admit_total, tone: 'healthy' },
])

const selectedPlan = computed(() => plans.value.find((item) => item.id === selectedPlanId.value))

const currentStepIndex = computed(() => {
  const stage = selectedPlan.value?.current_stage || plans.value[0]?.current_stage || '报名配置'
  const stageMap: Record<string, number> = {
    报名配置: 0,
    资格审核: 1,
    评分推荐: 2,
    材料评分: 2,
    面试执行: 3,
    面试待安排: 3,
    面试完成: 3,
    预录取: 4,
  }
  return stageMap[stage] ?? 0
})

function applicationTagType(status: string) {
  if (['预录取', '同意录取'].includes(status)) {
    return 'success'
  }
  if (['资格审核通过', '材料评分中', '面试完成'].includes(status)) {
    return 'warning'
  }
  if (status === '不录取') {
    return 'danger'
  }
  return 'info'
}

function materialTagType(status: string) {
  if (status === '材料齐全') {
    return 'success'
  }
  if (status === '待补材料') {
    return 'warning'
  }
  return 'danger'
}

async function loadOverview() {
  const [statsResponse, workbenchResponse] = await Promise.all([getRecruitmentStats(), getRecruitmentWorkbench()])
  stats.value = statsResponse.data
  workbench.value = workbenchResponse.data
}

async function loadPlans() {
  plansLoading.value = true
  try {
    const response = await listRecruitmentPlans()
    plans.value = response.data.items
    if (selectedPlanId.value && !plans.value.some((item) => item.id === selectedPlanId.value)) {
      selectedPlanId.value = undefined
    }
    if (!selectedPlanId.value && plans.value.length > 0) {
      selectedPlanId.value = plans.value[0].id
    }
  } finally {
    plansLoading.value = false
  }
}

async function loadApplications() {
  applicationsLoading.value = true
  try {
    const response = await listRecruitmentApplications({
      keyword: applicationFilters.keyword || undefined,
      status: applicationFilters.status || undefined,
      plan_id: selectedPlanId.value,
    })
    applications.value = response.data.items
  } finally {
    applicationsLoading.value = false
  }
}

async function refreshAll() {
  await loadPlans()
  await Promise.all([loadOverview(), loadApplications()])
}

function resetPlanForm() {
  editingPlanId.value = null
  Object.assign(planForm, {
    plan_name: '',
    academic_year: String(new Date().getFullYear()),
    semester: '秋',
    current_stage: '报名配置',
    target_quota: 30,
    interview_group_count: 3,
    is_open: true,
  })
  planFormRef.value?.clearValidate()
}

function resetApplicationForm() {
  editingApplicationId.value = null
  Object.assign(applicationForm, {
    plan_id: selectedPlanId.value ?? plans.value[0]?.id ?? 0,
    candidate_no: '',
    student_name: '',
    graduation_school: '',
    highest_degree: '硕士',
    intended_field: '',
    material_status: '材料齐全',
    application_status: '报名已提交',
    reviewer_name: '',
    final_score: undefined,
  })
  applicationFormRef.value?.clearValidate()
}

function openCreatePlanDialog() {
  planMode.value = 'create'
  resetPlanForm()
  planDialogVisible.value = true
}

function openEditPlanDialog(row: RecruitPlanRecord) {
  planMode.value = 'edit'
  editingPlanId.value = row.id
  Object.assign(planForm, {
    plan_name: row.plan_name,
    academic_year: row.academic_year,
    semester: row.semester,
    current_stage: row.current_stage,
    target_quota: row.target_quota,
    interview_group_count: row.interview_group_count,
    is_open: row.is_open,
  })
  planDialogVisible.value = true
}

function openCreateApplicationDialog() {
  applicationMode.value = 'create'
  resetApplicationForm()
  applicationDialogVisible.value = true
}

function openEditApplicationDialog(row: RecruitApplicationRecord) {
  applicationMode.value = 'edit'
  editingApplicationId.value = row.id
  Object.assign(applicationForm, {
    plan_id: row.plan_id,
    candidate_no: row.candidate_no,
    student_name: row.student_name,
    graduation_school: row.graduation_school,
    highest_degree: row.highest_degree,
    intended_field: row.intended_field,
    material_status: row.material_status,
    application_status: row.application_status,
    reviewer_name: row.reviewer_name || '',
    final_score: row.final_score ?? undefined,
  })
  applicationDialogVisible.value = true
}

async function submitPlanForm() {
  const formInstance = planFormRef.value
  if (!formInstance) {
    return
  }

  const isValid = await formInstance.validate().catch(() => false)
  if (!isValid) {
    return
  }

  planSubmitting.value = true
  try {
    if (planMode.value === 'create') {
      await createRecruitmentPlan(planForm)
      ElMessage.success('招生计划已新增')
    } else if (editingPlanId.value !== null) {
      await updateRecruitmentPlan(editingPlanId.value, planForm)
      ElMessage.success('招生计划已更新')
    }

    planDialogVisible.value = false
    await refreshAll()
  } finally {
    planSubmitting.value = false
  }
}

async function submitApplicationForm() {
  const formInstance = applicationFormRef.value
  if (!formInstance) {
    return
  }

  const isValid = await formInstance.validate().catch(() => false)
  if (!isValid) {
    return
  }

  applicationSubmitting.value = true
  try {
    const payload: RecruitApplicationUpsert = {
      ...applicationForm,
      reviewer_name: applicationForm.reviewer_name?.trim() || '',
      final_score: applicationForm.final_score ?? null,
    }

    if (applicationMode.value === 'create') {
      await createRecruitmentApplication(payload)
      ElMessage.success('报名申请已新增')
    } else if (editingApplicationId.value !== null) {
      await updateRecruitmentApplication(editingApplicationId.value, payload)
      ElMessage.success('报名申请已更新')
    }

    applicationDialogVisible.value = false
    await refreshAll()
  } finally {
    applicationSubmitting.value = false
  }
}

async function handleDeleteApplication(row: RecruitApplicationRecord) {
  await ElMessageBox.confirm(`确定删除报名申请 ${row.student_name} 吗？`, '删除确认', {
    type: 'warning',
  })
  await deleteRecruitmentApplication(row.id)
  ElMessage.success('报名申请已删除')
  await refreshAll()
}

async function handlePlanSelection(row: RecruitPlanRecord) {
  selectedPlanId.value = row.id
  await loadApplications()
}

async function handleFilterSearch() {
  await loadApplications()
}

async function handleFilterReset() {
  applicationFilters.keyword = ''
  applicationFilters.status = ''
  await loadApplications()
}

onMounted(() => {
  void refreshAll()
})
</script>

<template>
  <section class="content-stack">
    <section class="stats-grid">
      <article v-for="card in statsCards" :key="card.label" class="stat-card" :data-tone="card.tone">
        <p>{{ card.label }}</p>
        <strong>{{ card.value }}</strong>
      </article>
    </section>

    <section class="section-card">
      <div class="section-card__header">
        <div>
          <p class="section-tag">招生全景</p>
          <h2>工作流阶段推进</h2>
        </div>
        <div class="header-actions">
          <span class="summary-text" v-if="selectedPlan">当前计划：{{ selectedPlan.plan_name }}</span>
          <el-button type="primary" round @click="openCreatePlanDialog">新增招生计划</el-button>
        </div>
      </div>

      <el-steps :active="currentStepIndex" finish-status="success" align-center>
        <el-step
          v-for="stage in stageMeta"
          :key="stage.title"
          :title="stage.title"
          :description="stage.detail"
        />
      </el-steps>
    </section>

    <section class="two-column-grid">
      <article class="section-card">
        <div class="section-card__header compact">
          <div>
            <p class="section-tag">计划矩阵</p>
            <h2>进行中的招生计划</h2>
          </div>
        </div>
        <el-table :data="plans" stripe v-loading="plansLoading" @row-click="handlePlanSelection">
          <el-table-column prop="plan_name" label="计划名称" min-width="220" />
          <el-table-column prop="academic_term" label="学年学期" width="120" />
          <el-table-column prop="current_stage" label="当前阶段" width="120" />
          <el-table-column prop="target_quota" label="计划名额" width="100" />
          <el-table-column prop="application_count" label="申请数" width="100" />
          <el-table-column prop="interview_group_count" label="面试组" width="100" />
          <el-table-column label="开放状态" width="120">
            <template #default="scope">
              <el-tag :type="scope.row.is_open ? 'success' : 'info'">{{ scope.row.is_open ? '开放中' : '已关闭' }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="110" fixed="right">
            <template #default="scope">
              <el-button link type="primary" @click.stop="openEditPlanDialog(scope.row)">编辑</el-button>
            </template>
          </el-table-column>
        </el-table>
      </article>

      <article class="section-card">
        <div class="section-card__header compact">
          <div>
            <p class="section-tag">当日任务</p>
            <h2>招生工作待办</h2>
          </div>
        </div>
        <ul class="task-list">
          <li v-for="task in workbench.pending_tasks" :key="task.title">
            <div>
              <strong>{{ task.title }}</strong>
              <p>{{ task.owner }} · 截止 {{ task.due_text }}</p>
            </div>
            <el-tag type="warning">处理中</el-tag>
          </li>
        </ul>
      </article>
    </section>

    <article class="section-card">
      <div class="section-card__header">
        <div>
          <p class="section-tag">报名申请管理</p>
          <h2>申请池</h2>
        </div>
        <div class="header-actions">
          <span class="summary-text">{{ selectedPlan ? `已筛选计划：${selectedPlan.plan_name}` : '当前显示全部计划' }}</span>
          <el-button type="primary" round @click="openCreateApplicationDialog">新增报名申请</el-button>
        </div>
      </div>

      <el-form class="filter-form" :inline="true">
        <el-form-item label="关键字">
          <el-input v-model="applicationFilters.keyword" placeholder="报名号 / 姓名 / 学校 / 方向" clearable />
        </el-form-item>
        <el-form-item label="申请状态">
          <el-select v-model="applicationFilters.status" placeholder="全部状态" clearable style="width: 180px">
            <el-option v-for="item in applicationStatusOptions" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleFilterSearch">查询</el-button>
          <el-button @click="handleFilterReset">重置</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="applications" stripe v-loading="applicationsLoading">
        <el-table-column prop="candidate_no" label="报名号" width="132" />
        <el-table-column prop="student_name" label="姓名" width="110" />
        <el-table-column prop="graduation_school" label="毕业院校" min-width="180" />
        <el-table-column prop="highest_degree" label="最高学历" width="100" />
        <el-table-column prop="intended_field" label="研究方向" width="140" />
        <el-table-column label="材料状态" width="120">
          <template #default="scope">
            <el-tag :type="materialTagType(scope.row.material_status)">{{ scope.row.material_status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="申请状态" width="130">
          <template #default="scope">
            <el-tag :type="applicationTagType(scope.row.application_status)">{{ scope.row.application_status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="reviewer_name" label="审核人" width="110" />
        <el-table-column prop="final_score" label="得分" width="90" />
        <el-table-column label="操作" fixed="right" width="170">
          <template #default="scope">
            <el-button link type="primary" @click="openEditApplicationDialog(scope.row)">编辑</el-button>
            <el-button link type="danger" @click="handleDeleteApplication(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </article>

    <el-dialog v-model="planDialogVisible" :title="planMode === 'create' ? '新增招生计划' : '编辑招生计划'" width="680px" destroy-on-close>
      <el-form ref="planFormRef" :model="planForm" :rules="planRules" label-width="96px">
        <div class="dialog-grid">
          <el-form-item label="计划名称" prop="plan_name">
            <el-input v-model="planForm.plan_name" placeholder="请输入招生计划名称" />
          </el-form-item>
          <el-form-item label="学年" prop="academic_year">
            <el-input v-model="planForm.academic_year" placeholder="例如 2026" />
          </el-form-item>
          <el-form-item label="学期" prop="semester">
            <el-select v-model="planForm.semester" placeholder="请选择学期">
              <el-option v-for="item in semesterOptions" :key="item" :label="item" :value="item" />
            </el-select>
          </el-form-item>
          <el-form-item label="当前阶段" prop="current_stage">
            <el-select v-model="planForm.current_stage" placeholder="请选择阶段">
              <el-option v-for="item in planStageOptions" :key="item" :label="item" :value="item" />
            </el-select>
          </el-form-item>
          <el-form-item label="计划名额" prop="target_quota">
            <el-input-number v-model="planForm.target_quota" :min="1" :max="999" controls-position="right" />
          </el-form-item>
          <el-form-item label="面试组数" prop="interview_group_count">
            <el-input-number v-model="planForm.interview_group_count" :min="1" :max="99" controls-position="right" />
          </el-form-item>
          <el-form-item label="开放状态">
            <el-switch v-model="planForm.is_open" active-text="开放中" inactive-text="已关闭" />
          </el-form-item>
        </div>
      </el-form>
      <template #footer>
        <el-button @click="planDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="planSubmitting" @click="submitPlanForm">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="applicationDialogVisible" :title="applicationMode === 'create' ? '新增报名申请' : '编辑报名申请'" width="760px" destroy-on-close>
      <el-form ref="applicationFormRef" :model="applicationForm" :rules="applicationRules" label-width="96px">
        <div class="dialog-grid">
          <el-form-item label="招生计划" prop="plan_id">
            <el-select v-model="applicationForm.plan_id" placeholder="请选择计划">
              <el-option v-for="item in plans" :key="item.id" :label="item.plan_name" :value="item.id" />
            </el-select>
          </el-form-item>
          <el-form-item label="报名号" prop="candidate_no">
            <el-input v-model="applicationForm.candidate_no" placeholder="请输入报名号" />
          </el-form-item>
          <el-form-item label="姓名" prop="student_name">
            <el-input v-model="applicationForm.student_name" placeholder="请输入姓名" />
          </el-form-item>
          <el-form-item label="毕业院校" prop="graduation_school">
            <el-input v-model="applicationForm.graduation_school" placeholder="请输入毕业院校" />
          </el-form-item>
          <el-form-item label="最高学历" prop="highest_degree">
            <el-select v-model="applicationForm.highest_degree" placeholder="请选择学历">
              <el-option v-for="item in degreeOptions" :key="item" :label="item" :value="item" />
            </el-select>
          </el-form-item>
          <el-form-item label="研究方向" prop="intended_field">
            <el-input v-model="applicationForm.intended_field" placeholder="请输入研究方向" />
          </el-form-item>
          <el-form-item label="材料状态" prop="material_status">
            <el-select v-model="applicationForm.material_status" placeholder="请选择材料状态">
              <el-option v-for="item in materialStatusOptions" :key="item" :label="item" :value="item" />
            </el-select>
          </el-form-item>
          <el-form-item label="申请状态" prop="application_status">
            <el-select v-model="applicationForm.application_status" placeholder="请选择申请状态">
              <el-option v-for="item in applicationStatusOptions" :key="item" :label="item" :value="item" />
            </el-select>
          </el-form-item>
          <el-form-item label="审核人">
            <el-input v-model="applicationForm.reviewer_name" placeholder="请输入审核人" />
          </el-form-item>
          <el-form-item label="材料得分">
            <el-input-number v-model="applicationForm.final_score" :min="0" :max="100" :precision="1" controls-position="right" />
          </el-form-item>
        </div>
      </el-form>
      <template #footer>
        <el-button @click="applicationDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="applicationSubmitting" @click="submitApplicationForm">保存</el-button>
      </template>
    </el-dialog>
  </section>
</template>

<style scoped>
.content-stack,
.stats-grid,
.two-column-grid {
  display: grid;
  gap: 22px;
}

.stats-grid {
  grid-template-columns: repeat(5, minmax(0, 1fr));
}

.two-column-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.section-card,
.stat-card {
  border: 1px solid rgba(18, 50, 95, 0.08);
  border-radius: 26px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 18px 44px rgba(14, 40, 88, 0.07);
}

.section-card {
  padding: 22px;
}

.stat-card {
  padding: 20px 22px;
}

.stat-card[data-tone='healthy'] {
  background: linear-gradient(150deg, rgba(255, 255, 255, 0.96), rgba(231, 248, 242, 0.96));
}

.stat-card[data-tone='attention'] {
  background: linear-gradient(150deg, rgba(255, 255, 255, 0.96), rgba(255, 244, 224, 0.96));
}

.stat-card[data-tone='warning'],
.stat-card[data-tone='neutral'] {
  background: linear-gradient(150deg, rgba(255, 255, 255, 0.96), rgba(255, 235, 230, 0.96));
}

.stat-card p,
.stat-card strong {
  margin: 0;
}

.stat-card strong {
  display: block;
  margin-top: 10px;
  color: #12284d;
  font-size: 30px;
}

.section-card__header {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: center;
  margin-bottom: 18px;
}

.section-card__header.compact {
  margin-bottom: 16px;
}

.section-tag,
.section-card h2,
.task-list p,
.summary-text {
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

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.summary-text {
  color: #60718f;
  font-size: 14px;
}

.filter-form {
  margin-bottom: 18px;
}

.task-list {
  display: grid;
  gap: 12px;
  list-style: none;
  padding: 0;
  margin: 0;
}

.task-list li {
  display: flex;
  justify-content: space-between;
  gap: 14px;
  align-items: center;
  padding: 14px 16px;
  border-radius: 18px;
  background: linear-gradient(135deg, rgba(245, 248, 255, 0.98), rgba(252, 244, 221, 0.92));
}

.task-list strong {
  color: #12315e;
}

.task-list p {
  margin-top: 6px;
  color: #60718f;
}

.dialog-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 4px 18px;
}

@media (max-width: 980px) {
  .stats-grid,
  .two-column-grid {
    grid-template-columns: 1fr;
  }

  .section-card__header,
  .header-actions {
    flex-direction: column;
    align-items: flex-start;
  }

  .dialog-grid {
    grid-template-columns: 1fr;
  }
}
</style>
