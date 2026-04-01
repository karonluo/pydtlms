<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'

import {
  createStudent,
  deleteStudent,
  getStudentStats,
  listStudents,
  updateStudent,
  type StudentRecord,
  type StudentStats,
  type StudentUpsert,
} from '../../api/students'


const statusOptions = ['在校', '实习中', '外出研修', '请假中', '学位论文阶段', '已毕业']
const degreeOptions = ['工程博士', '学术博士']

const loading = ref(false)
const submitting = ref(false)
const total = ref(0)
const students = ref<StudentRecord[]>([])
const stats = ref<StudentStats>({
  total_students: 0,
  active_students: 0,
  outbound_students: 0,
  thesis_students: 0,
  advisor_count: 0,
})

const filters = reactive({
  keyword: '',
  status: '',
  advisor_name: '',
})

const dialogVisible = ref(false)
const dialogMode = ref<'create' | 'edit'>('create')
const formRef = ref<FormInstance>()
const form = reactive<StudentUpsert>({
  student_no: '',
  full_name: '',
  status: '在校',
  advisor_name: '',
  team_name: '',
  degree_type: '工程博士',
  enrollment_year: new Date().getFullYear(),
  phone_number: '',
  political_status: '',
})
const editingId = ref<number | null>(null)

const rules: FormRules<StudentUpsert> = {
  student_no: [{ required: true, message: '请输入学号', trigger: 'blur' }],
  full_name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }],
  advisor_name: [{ required: true, message: '请输入导师', trigger: 'blur' }],
  team_name: [{ required: true, message: '请输入团队', trigger: 'blur' }],
  degree_type: [{ required: true, message: '请选择学位类型', trigger: 'change' }],
  enrollment_year: [{ required: true, message: '请输入入学年份', trigger: 'change' }],
}

const stateCards = computed(() => [
  { label: '学生总量', count: stats.value.total_students, tone: 'healthy' },
  { label: '在校与实习', count: stats.value.active_students, tone: 'attention' },
  { label: '外出研修', count: stats.value.outbound_students, tone: 'neutral' },
  { label: '论文阶段', count: stats.value.thesis_students, tone: 'warning' },
])

const advisorOptions = computed(() => Array.from(new Set(students.value.map((item) => item.advisor_name))))

function normalizePayload(payload: StudentUpsert): StudentUpsert {
  return {
    ...payload,
    phone_number: payload.phone_number?.trim() || '',
    political_status: payload.political_status?.trim() || '',
  }
}

async function loadStats() {
  const response = await getStudentStats()
  stats.value = response.data
}

async function loadStudentsData() {
  loading.value = true
  try {
    const response = await listStudents({
      keyword: filters.keyword || undefined,
      status: filters.status || undefined,
      advisor_name: filters.advisor_name || undefined,
    })
    students.value = response.data.items
    total.value = response.data.total
  } finally {
    loading.value = false
  }
}

async function refreshAll() {
  await Promise.all([loadStats(), loadStudentsData()])
}

function resetForm() {
  editingId.value = null
  Object.assign(form, {
    student_no: '',
    full_name: '',
    status: '在校',
    advisor_name: '',
    team_name: '',
    degree_type: '工程博士',
    enrollment_year: new Date().getFullYear(),
    phone_number: '',
    political_status: '',
  })
  formRef.value?.clearValidate()
}

function openCreateDialog() {
  dialogMode.value = 'create'
  resetForm()
  dialogVisible.value = true
}

function openEditDialog(row: StudentRecord) {
  dialogMode.value = 'edit'
  editingId.value = row.id
  Object.assign(form, {
    student_no: row.student_no,
    full_name: row.full_name,
    status: row.status,
    advisor_name: row.advisor_name,
    team_name: row.team_name,
    degree_type: row.degree_type,
    enrollment_year: row.enrollment_year,
    phone_number: row.phone_number || '',
    political_status: row.political_status || '',
  })
  dialogVisible.value = true
}

async function submitForm() {
  const formInstance = formRef.value
  if (!formInstance) {
    return
  }

  const isValid = await formInstance.validate().catch(() => false)
  if (!isValid) {
    return
  }

  submitting.value = true
  try {
    const payload = normalizePayload(form)
    if (dialogMode.value === 'create') {
      await createStudent(payload)
      ElMessage.success('学生已新增')
    } else if (editingId.value !== null) {
      await updateStudent(editingId.value, payload)
      ElMessage.success('学生信息已更新')
    }

    dialogVisible.value = false
    await refreshAll()
  } finally {
    submitting.value = false
  }
}

async function handleDelete(row: StudentRecord) {
  await ElMessageBox.confirm(`确定删除学生 ${row.full_name} 吗？`, '删除确认', {
    type: 'warning',
  })

  await deleteStudent(row.id)
  ElMessage.success('学生已删除')
  await refreshAll()
}

async function handleSearch() {
  await loadStudentsData()
}

async function handleReset() {
  filters.keyword = ''
  filters.status = ''
  filters.advisor_name = ''
  await loadStudentsData()
}

function tagType(status: string) {
  if (status === '在校' || status === '学位论文阶段') {
    return 'success'
  }
  if (status === '实习中' || status === '外出研修') {
    return 'warning'
  }
  if (status === '已毕业') {
    return 'info'
  }
  return 'danger'
}

onMounted(() => {
  void refreshAll()
})
</script>

<template>
  <section class="content-stack">
    <section class="state-grid">
      <article v-for="card in stateCards" :key="card.label" class="state-card" :data-tone="card.tone">
        <p>{{ card.label }}</p>
        <strong>{{ card.count }}</strong>
      </article>
    </section>

    <article class="section-card">
      <div class="section-card__header">
        <div>
          <p class="section-tag">主数据管理</p>
          <h2>学生主档</h2>
        </div>
        <div class="header-actions">
          <span class="summary-text">共 {{ total }} 条记录</span>
          <el-button type="primary" round @click="openCreateDialog">新增学生</el-button>
        </div>
      </div>

      <el-form class="filter-form" :inline="true">
        <el-form-item label="关键字">
          <el-input v-model="filters.keyword" placeholder="学号 / 姓名 / 团队" clearable />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="filters.status" placeholder="全部状态" clearable style="width: 168px">
            <el-option v-for="item in statusOptions" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item label="导师">
          <el-select v-model="filters.advisor_name" placeholder="全部导师" clearable filterable style="width: 180px">
            <el-option v-for="item in advisorOptions" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="students" stripe v-loading="loading">
        <el-table-column prop="student_no" label="学号" width="132" />
        <el-table-column prop="full_name" label="姓名" width="110" />
        <el-table-column prop="degree_type" label="学位类型" width="120" />
        <el-table-column prop="advisor_name" label="导师" width="120" />
        <el-table-column prop="team_name" label="所属团队" min-width="180" />
        <el-table-column prop="enrollment_year" label="入学年份" width="110" />
        <el-table-column label="当前状态" width="140">
          <template #default="scope">
            <el-tag :type="tagType(scope.row.status)">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="phone_number" label="联系电话" width="140" />
        <el-table-column prop="political_status" label="政治面貌" width="120" />
        <el-table-column label="操作" fixed="right" width="160">
          <template #default="scope">
            <el-button link type="primary" @click="openEditDialog(scope.row)">编辑</el-button>
            <el-button link type="danger" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </article>

    <el-dialog
      v-model="dialogVisible"
      :title="dialogMode === 'create' ? '新增学生' : '编辑学生'"
      width="720px"
      destroy-on-close
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-width="96px" class="dialog-form">
        <div class="dialog-grid">
          <el-form-item label="学号" prop="student_no">
            <el-input v-model="form.student_no" placeholder="例如 D20250012" />
          </el-form-item>
          <el-form-item label="姓名" prop="full_name">
            <el-input v-model="form.full_name" placeholder="请输入姓名" />
          </el-form-item>
          <el-form-item label="当前状态" prop="status">
            <el-select v-model="form.status" placeholder="请选择状态">
              <el-option v-for="item in statusOptions" :key="item" :label="item" :value="item" />
            </el-select>
          </el-form-item>
          <el-form-item label="学位类型" prop="degree_type">
            <el-select v-model="form.degree_type" placeholder="请选择学位类型">
              <el-option v-for="item in degreeOptions" :key="item" :label="item" :value="item" />
            </el-select>
          </el-form-item>
          <el-form-item label="导师" prop="advisor_name">
            <el-input v-model="form.advisor_name" placeholder="请输入导师姓名" />
          </el-form-item>
          <el-form-item label="所属团队" prop="team_name">
            <el-input v-model="form.team_name" placeholder="请输入团队名称" />
          </el-form-item>
          <el-form-item label="入学年份" prop="enrollment_year">
            <el-input-number v-model="form.enrollment_year" :min="2018" :max="2100" controls-position="right" />
          </el-form-item>
          <el-form-item label="联系电话">
            <el-input v-model="form.phone_number" placeholder="请输入联系电话" />
          </el-form-item>
          <el-form-item label="政治面貌">
            <el-input v-model="form.political_status" placeholder="请输入政治面貌" />
          </el-form-item>
        </div>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submitForm">保存</el-button>
      </template>
    </el-dialog>
  </section>
</template>

<style scoped>
.content-stack,
.state-grid {
  display: grid;
  gap: 22px;
}

.state-grid {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.state-card,
.section-card {
  border: 1px solid rgba(18, 50, 95, 0.08);
  border-radius: 26px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 18px 44px rgba(14, 40, 88, 0.07);
}

.state-card {
  padding: 20px 22px;
}

.state-card p,
.section-tag,
.section-card h2,
.domain-list p {
  margin: 0;
}

.state-card strong {
  display: block;
  margin-top: 10px;
  color: #12284d;
  font-size: 30px;
}

.state-card[data-tone='healthy'] {
  background: linear-gradient(150deg, rgba(255, 255, 255, 0.96), rgba(231, 248, 242, 0.96));
}

.state-card[data-tone='attention'] {
  background: linear-gradient(150deg, rgba(255, 255, 255, 0.96), rgba(255, 244, 224, 0.96));
}

.state-card[data-tone='warning'],
.state-card[data-tone='neutral'] {
  background: linear-gradient(150deg, rgba(255, 255, 255, 0.96), rgba(255, 231, 226, 0.96));
}

.section-card {
  padding: 22px;
}

.section-card__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 18px;
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
  color: #5d7394;
  font-size: 14px;
}

.filter-form {
  margin-bottom: 18px;
}

.dialog-form {
  padding-top: 8px;
}

.dialog-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 4px 18px;
}

@media (max-width: 1080px) {
  .state-grid {
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
