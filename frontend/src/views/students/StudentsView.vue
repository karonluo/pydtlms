<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { useRoute } from 'vue-router'
import TableRowActions from '../../components/table/TableRowActions.vue'
import { buildDictColorMap, resolveDictTagType, type DictColorMap } from '../../utils/dictTag'

import {
  batchDeleteTeams,
  createStudent,
  createTeam,
  deleteStudent,
  deleteTeam,
  getStudentOptions,
  getStudentStats,
  listStudents,
  listTeams,
  updateStudent,
  updateTeam,
  type SelectOption,
  type StudentOptions,
  type StudentRecord,
  type StudentStats,
  type StudentUpsert,
  type TeamRecord,
  type TeamUpsert,
} from '../../api/students'

const route = useRoute()
const loading = ref(false)
const bootstrapping = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const dialogMode = ref<'create' | 'edit'>('create')
const currentId = ref<number | null>(null)
const selectedTeamIds = ref<number[]>([])
const studentStatusColors = ref<DictColorMap>({})
const teamStatusColors = ref<DictColorMap>({})

const stats = ref<StudentStats>({
  total_students: 0,
  active_students: 0,
  outbound_students: 0,
  thesis_students: 0,
  advisor_count: 0,
  team_total: 0,
  active_team_total: 0,
})
const options = ref<StudentOptions>({
  status_options: [],
  degree_options: [],
  advisor_options: [],
  team_options: [],
  team_status_options: [],
  political_status_options: [],
  department_options: [],
  discipline_options: [],
  team_advisor_map: [],
})
const students = ref<StudentRecord[]>([])
const teams = ref<TeamRecord[]>([])

const studentFilters = reactive({
  keyword: '',
  status: '',
  advisor_name: '',
  team_name: '',
})
const teamFilters = reactive({
  keyword: '',
  status: '',
  department_name: '',
  lead_advisor_name: '',
})

const studentFormRef = ref<FormInstance>()
const teamFormRef = ref<FormInstance>()
const studentForm = reactive<StudentUpsert>({
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
const teamForm = reactive<TeamUpsert>({
  team_code: '',
  team_name: '',
  department_name: '',
  discipline_name: '',
  lead_advisor_name: '',
  advisor_names: [],
  research_directions: [],
  status: '启用',
  established_on: '',
  description: '',
})

const studentRules: FormRules<StudentUpsert> = {
  student_no: [{ required: true, message: '请输入学号', trigger: 'blur' }],
  full_name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }],
  advisor_name: [{ required: true, message: '请选择导师', trigger: 'change' }],
  team_name: [{ required: true, message: '请选择团队', trigger: 'change' }],
  degree_type: [{ required: true, message: '请选择学位类型', trigger: 'change' }],
  enrollment_year: [{ required: true, message: '请输入入学年份', trigger: 'change' }],
}
const teamRules: FormRules<TeamUpsert> = {
  team_code: [{ required: true, message: '请输入团队编码', trigger: 'blur' }],
  team_name: [{ required: true, message: '请输入团队名称', trigger: 'blur' }],
  department_name: [{ required: true, message: '请输入所属院系', trigger: 'blur' }],
  discipline_name: [{ required: true, message: '请输入所属学科', trigger: 'blur' }],
  lead_advisor_name: [{ required: true, message: '请选择负责人导师', trigger: 'change' }],
  advisor_names: [{ required: true, message: '请选择团队导师', trigger: 'change', type: 'array' }],
  status: [{ required: true, message: '请选择团队状态', trigger: 'change' }],
}

const activeSection = computed(() => String(route.meta.section || 'records'))
const isRecordSection = computed(() => activeSection.value === 'records')
const sectionConfig = computed(() => {
  if (activeSection.value === 'teams') {
    return {
      title: '团队管理',
      tag: '团队主数据',
      createLabel: '新增团队',
      total: teams.value.length,
    }
  }
  return {
    title: '学生主档',
    tag: '主数据管理',
    createLabel: '新增学生',
    total: students.value.length,
  }
})
const statCards = computed(() => {
  if (activeSection.value === 'teams') {
    return [
      { label: '团队总量', count: stats.value.team_total, tone: 'healthy' },
      { label: '启用团队', count: stats.value.active_team_total, tone: 'attention' },
      { label: '导师总量', count: stats.value.advisor_count, tone: 'neutral' },
      { label: '在读学生', count: stats.value.active_students, tone: 'warning' },
    ]
  }
  return [
    { label: '学生总量', count: stats.value.total_students, tone: 'healthy' },
    { label: '在校与实习', count: stats.value.active_students, tone: 'attention' },
    { label: '外出研修', count: stats.value.outbound_students, tone: 'neutral' },
    { label: '论文阶段', count: stats.value.thesis_students, tone: 'warning' },
  ]
})
const teamAdvisorMap = computed(() => {
  const mapping = new Map<string, SelectOption[]>()
  options.value.team_advisor_map.forEach((item) => mapping.set(item.team_name, item.advisors))
  return mapping
})
const advisorOptions = computed(() => {
  if (!studentForm.team_name) {
    return options.value.advisor_options
  }
  return teamAdvisorMap.value.get(studentForm.team_name) || []
})
const departmentOptions = computed(() => {
  return options.value.department_options
})
const disciplineOptions = computed(() => options.value.discipline_options)
const teamResearchDirectionText = computed(() => teamForm.research_directions.join('、'))

function splitTextValues(value: string) {
  return Array.from(new Set(value.split(/[,，、\n]/).map((item) => item.trim()).filter(Boolean)))
}

function normalizeStudentPayload(payload: StudentUpsert): StudentUpsert {
  return {
    ...payload,
    phone_number: payload.phone_number?.trim() || '',
    political_status: payload.political_status?.trim() || '',
  }
}

function normalizeTeamPayload(payload: TeamUpsert): TeamUpsert {
  return {
    ...payload,
    team_code: payload.team_code.trim(),
    team_name: payload.team_name.trim(),
    department_name: payload.department_name.trim(),
    discipline_name: payload.discipline_name.trim(),
    lead_advisor_name: payload.lead_advisor_name.trim(),
    advisor_names: Array.from(new Set(payload.advisor_names.filter(Boolean))),
    research_directions: Array.from(new Set(payload.research_directions.filter(Boolean))),
    established_on: payload.established_on || '',
    description: payload.description?.trim() || '',
  }
}

async function loadStats() {
  const response = await getStudentStats()
  stats.value = response.data
}

async function loadOptions() {
  const response = await getStudentOptions()
  options.value = response.data
  studentStatusColors.value = buildDictColorMap(response.data.status_options)
  teamStatusColors.value = buildDictColorMap(response.data.team_status_options)
}

async function loadRecords() {
  const response = await listStudents({
    keyword: studentFilters.keyword || undefined,
    status: studentFilters.status || undefined,
    advisor_name: studentFilters.advisor_name || undefined,
    team_name: studentFilters.team_name || undefined,
  })
  students.value = response.data.items
}

async function loadTeams() {
  const response = await listTeams({
    keyword: teamFilters.keyword || undefined,
    status: teamFilters.status || undefined,
    department_name: teamFilters.department_name || undefined,
    lead_advisor_name: teamFilters.lead_advisor_name || undefined,
  })
  teams.value = response.data.items
}

async function loadSectionData() {
  loading.value = true
  try {
    if (activeSection.value === 'teams') {
      await loadTeams()
      return
    }
    await loadRecords()
  } finally {
    loading.value = false
  }
}

async function bootstrap() {
  bootstrapping.value = true
  try {
    await Promise.all([loadStats(), loadOptions(), loadSectionData()])
  } finally {
    bootstrapping.value = false
  }
}

async function refreshAfterMutation() {
  await Promise.all([loadStats(), loadOptions(), loadSectionData()])
}

function resetStudentForm() {
  currentId.value = null
  Object.assign(studentForm, {
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
  studentFormRef.value?.clearValidate()
}

function resetTeamForm() {
  currentId.value = null
  Object.assign(teamForm, {
    team_code: '',
    team_name: '',
    department_name: '',
    discipline_name: '',
    lead_advisor_name: '',
    advisor_names: [],
    research_directions: [],
    status: '启用',
    established_on: '',
    description: '',
  })
  teamFormRef.value?.clearValidate()
}

function openCreateDialog() {
  dialogMode.value = 'create'
  if (activeSection.value === 'teams') {
    resetTeamForm()
  } else {
    resetStudentForm()
  }
  dialogVisible.value = true
}

function openStudentEditDialog(row: StudentRecord) {
  dialogMode.value = 'edit'
  currentId.value = row.id
  Object.assign(studentForm, {
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

function openTeamEditDialog(row: TeamRecord) {
  dialogMode.value = 'edit'
  currentId.value = row.id
  Object.assign(teamForm, {
    team_code: row.team_code,
    team_name: row.team_name,
    department_name: row.department_name,
    discipline_name: row.discipline_name,
    lead_advisor_name: row.lead_advisor_name,
    advisor_names: [...row.advisor_names],
    research_directions: [...row.research_directions],
    status: row.status,
    established_on: row.established_on || '',
    description: row.description || '',
  })
  dialogVisible.value = true
}

async function submitStudentForm() {
  const formInstance = studentFormRef.value
  if (!formInstance) {
    return
  }
  const isValid = await formInstance.validate().catch(() => false)
  if (!isValid) {
    return
  }
  submitting.value = true
  try {
    const payload = normalizeStudentPayload(studentForm)
    if (dialogMode.value === 'create') {
      await createStudent(payload)
      ElMessage.success('学生已新增')
    } else if (currentId.value !== null) {
      await updateStudent(currentId.value, payload)
      ElMessage.success('学生信息已更新')
    }
    dialogVisible.value = false
    await refreshAfterMutation()
  } finally {
    submitting.value = false
  }
}

async function submitTeamForm() {
  const formInstance = teamFormRef.value
  if (!formInstance) {
    return
  }
  const isValid = await formInstance.validate().catch(() => false)
  if (!isValid) {
    return
  }
  submitting.value = true
  try {
    const payload = normalizeTeamPayload(teamForm)
    if (dialogMode.value === 'create') {
      await createTeam(payload)
      ElMessage.success('团队已新增')
    } else if (currentId.value !== null) {
      await updateTeam(currentId.value, payload)
      ElMessage.success('团队信息已更新')
    }
    dialogVisible.value = false
    await refreshAfterMutation()
  } finally {
    submitting.value = false
  }
}

async function submitDialog() {
  if (activeSection.value === 'teams') {
    await submitTeamForm()
    return
  }
  await submitStudentForm()
}

async function handleDeleteStudent(row: StudentRecord) {
  await ElMessageBox.confirm(`确定删除学生 ${row.full_name} 吗？`, '删除确认', { type: 'warning' })
  await deleteStudent(row.id)
  ElMessage.success('学生已删除')
  await refreshAfterMutation()
}

async function handleDeleteTeam(row: TeamRecord) {
  await ElMessageBox.confirm(`确定删除团队 ${row.team_name} 吗？`, '删除确认', { type: 'warning' })
  await deleteTeam(row.id)
  ElMessage.success('团队已删除')
  await refreshAfterMutation()
}

async function handleBatchDeleteTeams() {
  if (!selectedTeamIds.value.length) {
    ElMessage.warning('请先选择团队')
    return
  }
  await ElMessageBox.confirm(`确定批量删除已选 ${selectedTeamIds.value.length} 个团队吗？`, '批量删除确认', { type: 'warning' })
  const response = await batchDeleteTeams(selectedTeamIds.value)
  ElMessage.success(`已删除 ${response.data.success_count} 个团队`)
  selectedTeamIds.value = []
  await refreshAfterMutation()
}

async function handleSearch() {
  await loadSectionData()
}

async function handleReset() {
  Object.assign(studentFilters, { keyword: '', status: '', advisor_name: '', team_name: '' })
  Object.assign(teamFilters, { keyword: '', status: '', department_name: '', lead_advisor_name: '' })
  selectedTeamIds.value = []
  await loadSectionData()
}

function handleTeamSelectionChange(selection: TeamRecord[]) {
  selectedTeamIds.value = selection.map((item) => item.id)
}

function handleStudentTeamChange(value: string) {
  const availableAdvisors = teamAdvisorMap.value.get(value) || []
  if (!availableAdvisors.some((item) => item.value === studentForm.advisor_name)) {
    studentForm.advisor_name = ''
  }
}

function handleTeamLeadAdvisorChange(value: string) {
  if (!teamForm.advisor_names.includes(value)) {
    teamForm.advisor_names = Array.from(new Set([...teamForm.advisor_names, value]))
  }
}

function syncTeamLeadAdvisor() {
  if (!teamForm.advisor_names.includes(teamForm.lead_advisor_name)) {
    teamForm.lead_advisor_name = teamForm.advisor_names[0] || ''
  }
}

function statusTagType(status: string) {
  return resolveDictTagType(status, studentStatusColors.value)
}

function teamStatusTagType(status: string) {
  return resolveDictTagType(status, teamStatusColors.value)
}

watch(() => studentForm.team_name, handleStudentTeamChange)
watch(() => teamForm.lead_advisor_name, handleTeamLeadAdvisorChange)
watch(() => teamForm.advisor_names, syncTeamLeadAdvisor)
watch(() => activeSection.value, () => {
  dialogVisible.value = false
  selectedTeamIds.value = []
  void loadSectionData()
})

onMounted(() => {
  void bootstrap()
})
</script>

<template>
  <section class="content-stack" v-loading="bootstrapping">
    <section class="state-grid">
      <article v-for="card in statCards" :key="card.label" class="state-card" :data-tone="card.tone">
        <p>{{ card.label }}</p>
        <strong>{{ card.count }}</strong>
      </article>
    </section>

    <article class="section-card">
      <div class="section-card__header">
        <div>
          <p class="section-tag">{{ sectionConfig.tag }}</p>
          <h2>{{ sectionConfig.title }}</h2>
        </div>
        <div class="header-actions">
          <el-button
            v-if="activeSection === 'teams'"
            plain
            type="danger"
            :disabled="!selectedTeamIds.length"
            @click="handleBatchDeleteTeams"
          >
            批量删除团队
          </el-button>
          <span class="summary-text">共 {{ sectionConfig.total }} 条记录</span>
          <el-button type="primary" round @click="openCreateDialog">{{ sectionConfig.createLabel }}</el-button>
        </div>
      </div>

      <el-form v-if="isRecordSection" class="filter-form" :inline="true">
        <el-form-item label="关键字">
          <el-input v-model="studentFilters.keyword" placeholder="学号 / 姓名 / 团队" clearable />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="studentFilters.status" placeholder="全部状态" clearable style="width: 168px">
            <el-option v-for="item in options.status_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="导师">
          <el-select v-model="studentFilters.advisor_name" placeholder="全部导师" clearable filterable style="width: 180px">
            <el-option v-for="item in options.advisor_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="团队">
          <el-select v-model="studentFilters.team_name" placeholder="全部团队" clearable filterable style="width: 180px">
            <el-option v-for="item in options.team_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <el-form v-else class="filter-form" :inline="true">
        <el-form-item label="关键字">
          <el-input v-model="teamFilters.keyword" placeholder="团队编码 / 名称 / 方向" clearable />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="teamFilters.status" placeholder="全部状态" clearable style="width: 160px">
            <el-option v-for="item in options.team_status_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="院系">
          <el-select v-model="teamFilters.department_name" placeholder="全部院系" clearable filterable style="width: 180px">
            <el-option v-for="item in departmentOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="负责人导师">
          <el-select v-model="teamFilters.lead_advisor_name" placeholder="全部导师" clearable filterable style="width: 180px">
            <el-option v-for="item in options.advisor_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <div class="table-host">
        <el-table v-if="isRecordSection" :data="students" stripe v-loading="loading" table-layout="fixed">
          <el-table-column prop="student_no" label="学号" width="128" show-overflow-tooltip />
          <el-table-column prop="full_name" label="姓名" width="96" show-overflow-tooltip />
          <el-table-column prop="degree_type" label="学位类型" width="112" show-overflow-tooltip />
          <el-table-column prop="advisor_name" label="导师" width="96" show-overflow-tooltip />
          <el-table-column prop="team_name" label="所属团队" min-width="130" show-overflow-tooltip />
          <el-table-column prop="enrollment_year" label="入学年份" width="96" />
          <el-table-column label="当前状态" width="112">
            <template #default="scope">
              <el-tag :type="statusTagType(scope.row.status)">{{ scope.row.status }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="phone_number" label="联系电话" width="128" show-overflow-tooltip />
          <el-table-column prop="political_status" label="政治面貌" width="110" show-overflow-tooltip />
          <el-table-column label="操作" width="118" align="center">
            <template #default="scope">
              <TableRowActions :row="scope.row" :main-actions="[{ key: 'edit', label: '编辑', type: 'primary', onClick: openStudentEditDialog }]" :more-actions="[{ key: 'delete', label: '删除', type: 'danger', onClick: handleDeleteStudent }]" />
            </template>
          </el-table-column>
        </el-table>

        <el-table v-else :data="teams" stripe v-loading="loading" table-layout="fixed" @selection-change="handleTeamSelectionChange">
          <el-table-column type="selection" width="44" />
          <el-table-column prop="team_code" label="团队编码" width="128" show-overflow-tooltip />
          <el-table-column label="团队信息" min-width="220">
            <template #default="scope">
              <div class="cell-stack">
                <strong>{{ scope.row.team_name }}</strong>
                <span>{{ scope.row.department_name }} / {{ scope.row.discipline_name }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="导师配置" min-width="210">
            <template #default="scope">
              <div class="cell-stack">
                <strong>{{ scope.row.lead_advisor_name || '未指定' }}</strong>
                <span :title="scope.row.advisor_names.join('、')">{{ scope.row.advisor_names.join('、') || '未配置团队导师' }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="研究方向" min-width="170" show-overflow-tooltip>
            <template #default="scope">
              <span :title="scope.row.research_directions.join('、')">{{ scope.row.research_directions.join('、') || '未配置' }}</span>
            </template>
          </el-table-column>
          <el-table-column label="状态 / 学生" width="126" align="center">
            <template #default="scope">
              <div class="stat-stack">
                <el-tag :type="teamStatusTagType(scope.row.status)">{{ scope.row.status }}</el-tag>
                <span>{{ scope.row.active_student_count }}/{{ scope.row.member_student_count }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="118" align="center">
            <template #default="scope">
              <TableRowActions :row="scope.row" :main-actions="[{ key: 'edit', label: '编辑', type: 'primary', onClick: openTeamEditDialog }]" :more-actions="[{ key: 'delete', label: '删除', type: 'danger', onClick: handleDeleteTeam }]" />
            </template>
          </el-table-column>
        </el-table>
      </div>
    </article>

    <el-dialog
      v-model="dialogVisible"
      :title="dialogMode === 'create' ? sectionConfig.createLabel : `编辑${sectionConfig.title.replace('管理', '')}`"
      width="760px"
      destroy-on-close
    >
      <el-form
        v-if="isRecordSection"
        ref="studentFormRef"
        :model="studentForm"
        :rules="studentRules"
        label-width="96px"
        class="dialog-form"
      >
        <div class="dialog-grid">
          <el-form-item label="学号" prop="student_no">
            <el-input v-model="studentForm.student_no" placeholder="例如 D20250012" />
          </el-form-item>
          <el-form-item label="姓名" prop="full_name">
            <el-input v-model="studentForm.full_name" placeholder="请输入姓名" />
          </el-form-item>
          <el-form-item label="当前状态" prop="status">
            <el-select v-model="studentForm.status" placeholder="请选择状态">
              <el-option v-for="item in options.status_options" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
          <el-form-item label="学位类型" prop="degree_type">
            <el-select v-model="studentForm.degree_type" placeholder="请选择学位类型">
              <el-option v-for="item in options.degree_options" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
          <el-form-item label="所属团队" prop="team_name">
            <el-select v-model="studentForm.team_name" placeholder="请选择团队" filterable>
              <el-option v-for="item in options.team_options" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
          <el-form-item label="导师" prop="advisor_name">
            <el-select v-model="studentForm.advisor_name" placeholder="请选择导师" filterable :disabled="!studentForm.team_name">
              <el-option v-for="item in advisorOptions" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
          <el-form-item label="入学年份" prop="enrollment_year">
            <el-input-number v-model="studentForm.enrollment_year" :min="2018" :max="2100" controls-position="right" />
          </el-form-item>
          <el-form-item label="联系电话">
            <el-input v-model="studentForm.phone_number" placeholder="请输入联系电话" />
          </el-form-item>
          <el-form-item label="政治面貌">
            <el-select v-model="studentForm.political_status" placeholder="请选择政治面貌" clearable filterable>
              <el-option v-for="item in options.political_status_options" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
        </div>
      </el-form>

      <el-form
        v-else
        ref="teamFormRef"
        :model="teamForm"
        :rules="teamRules"
        label-width="110px"
        class="dialog-form"
      >
        <div class="dialog-grid">
          <el-form-item label="团队编码" prop="team_code">
            <el-input v-model="teamForm.team_code" placeholder="例如 TEAM-IM-001" />
          </el-form-item>
          <el-form-item label="团队名称" prop="team_name">
            <el-input v-model="teamForm.team_name" placeholder="请输入团队名称" />
          </el-form-item>
          <el-form-item label="所属院系" prop="department_name">
            <el-select v-model="teamForm.department_name" filterable allow-create default-first-option placeholder="请选择所属院系">
              <el-option v-for="item in departmentOptions" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
          <el-form-item label="所属学科" prop="discipline_name">
            <el-select v-model="teamForm.discipline_name" filterable allow-create default-first-option placeholder="请选择所属学科">
              <el-option v-for="item in disciplineOptions" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
          <el-form-item label="负责人导师" prop="lead_advisor_name">
            <el-select v-model="teamForm.lead_advisor_name" placeholder="请选择负责人导师" filterable>
              <el-option v-for="item in options.advisor_options" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
          <el-form-item label="团队状态" prop="status">
            <el-select v-model="teamForm.status" placeholder="请选择团队状态">
              <el-option v-for="item in options.team_status_options" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
          <el-form-item label="团队导师" prop="advisor_names" class="dialog-grid--full">
            <el-select v-model="teamForm.advisor_names" multiple filterable placeholder="请选择团队导师">
              <el-option v-for="item in options.advisor_options" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
          <el-form-item label="研究方向" class="dialog-grid--full">
            <el-input
              :model-value="teamResearchDirectionText"
              placeholder="请输入研究方向，使用逗号或顿号分隔"
              @update:model-value="teamForm.research_directions = splitTextValues($event)"
            />
          </el-form-item>
          <el-form-item label="成立日期">
            <el-date-picker v-model="teamForm.established_on" type="date" value-format="YYYY-MM-DD" placeholder="请选择成立日期" />
          </el-form-item>
          <el-form-item label="团队说明" class="dialog-grid--full">
            <el-input v-model="teamForm.description" type="textarea" :rows="4" placeholder="请输入团队说明" />
          </el-form-item>
        </div>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submitDialog">保存</el-button>
      </template>
    </el-dialog>
  </section>
</template>

<style scoped>
.content-stack,
.state-grid {
  display: grid;
  gap: 14px;
}

.content-stack {
  height: 100%;
  min-height: 0;
  grid-template-rows: auto minmax(0, 1fr);
}

.state-grid {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.state-card,
.section-card {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #ffffff;
  box-shadow: 0 1px 2px rgba(15, 23, 42, 0.05);
}

.state-card {
  padding: 14px 16px;
}

.state-card p,
.section-tag,
.section-card h2 {
  margin: 0;
}

.state-card strong {
  display: block;
  margin-top: 4px;
  color: #111827;
  font-size: 28px;
  line-height: 1.1;
}

.state-card[data-tone='healthy'] {
  background: #ffffff;
}

.state-card[data-tone='attention'] {
  background: #ffffff;
}

.state-card[data-tone='warning'],
.state-card[data-tone='neutral'] {
  background: #ffffff;
}

.section-card {
  padding: 14px 16px;
  min-height: 0;
  display: flex;
  flex-direction: column;
}

.section-card__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 10px;
}

.section-tag {
  color: #909399;
  font-size: 12px;
}

.section-card h2 {
  margin-top: 4px;
  color: #303133;
  font-size: 20px;
  font-weight: 600;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.summary-text {
  color: #909399;
  font-size: 12px;
}

.filter-form {
  margin-bottom: 12px;
  flex: 0 0 auto;
  padding: 12px 12px 2px;
  border-radius: 8px;
  background: #f5f7fa;
}

.filter-form :deep(.el-form-item) {
  margin-bottom: 10px;
}

.table-host {
  flex: 1;
  min-height: 0;
  overflow-x: hidden;
  overflow-y: auto;
}

.table-host :deep(.el-table) {
  width: 100%;
}

.cell-stack {
  display: grid;
  gap: 4px;
  min-width: 0;
}

.cell-stack strong,
.cell-stack span {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.cell-stack strong {
  color: #303133;
  font-weight: 600;
}

.cell-stack span {
  color: #909399;
  font-size: 12px;
}

.stat-stack {
  display: grid;
  justify-items: center;
  gap: 6px;
}

.stat-stack span {
  color: #606266;
  font-size: 12px;
}

.dialog-form {
  padding-top: 8px;
}

.dialog-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 2px 16px;
}

.dialog-grid :deep(.el-select),
.dialog-grid :deep(.el-input-number),
.dialog-grid :deep(.el-date-editor) {
  width: 100%;
}

.dialog-grid--full {
  grid-column: 1 / -1;
}

@media (max-width: 1120px) {
  .content-stack {
    height: auto;
  }

  .state-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .dialog-grid {
    grid-template-columns: minmax(0, 1fr);
  }
}

@media (max-width: 720px) {
  .state-grid,
  .section-card__header {
    grid-template-columns: minmax(0, 1fr);
  }

  .content-stack,
  .section-card,
  .table-host {
    height: auto;
    min-height: unset;
    overflow: visible;
  }

  .section-card__header,
  .header-actions {
    display: grid;
  }
}
</style>