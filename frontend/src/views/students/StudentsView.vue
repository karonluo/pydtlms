<script setup lang="ts">
import axios from 'axios'
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { useRoute } from 'vue-router'

import TableRowActions, { type TableRowAction } from '../../components/table/TableRowActions.vue'
import { useServerPagination } from '../../composables/useServerPagination'
import { buildDictColorMap, resolveDictTagType, type DictColorMap } from '../../utils/dictTag'
import {
  activateRegisteredPortalStudent,
  batchDeleteCenters,
  createCenter,
  createStudent,
  deactivateRegisteredPortalStudent,
  deleteCenter,
  deleteStudent,
  getStudentOptions,
  getStudentStats,
  listCenters,
  listRegisteredPortalStudents,
  listStudents,
  resetRegisteredPortalStudentPassword,
  sendRegisteredPortalStudentEmail,
  updateCenter,
  updateStudent,
  type RegisteredPortalStudentActionResponse,
  type CenterRecord,
  type CenterUpsert,
  type RegisteredPortalStudentEmailRequest,
  type RegisteredPortalStudentRecord,
  type SelectOption,
  type StudentOptions,
  type StudentRecord,
  type StudentStats,
  type StudentUpsert,
} from '../../api/students'

const route = useRoute()
const loading = ref(false)
const bootstrapping = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const portalEmailDialogVisible = ref(false)
const portalEmailSubmitting = ref(false)
const dialogMode = ref<'create' | 'edit'>('create')
const currentId = ref<number | null>(null)
const selectedCenterIds = ref<number[]>([])
const studentStatusColors = ref<DictColorMap>({})
const portalEmailTarget = ref<RegisteredPortalStudentRecord | null>(null)

const stats = ref<StudentStats>({
  total_students: 0,
  active_students: 0,
  outbound_students: 0,
  thesis_students: 0,
  advisor_count: 0,
  center_total: 0,
  enabled_center_total: 0,
  registered_portal_total: 0,
  portal_submitted_total: 0,
  portal_unsubmitted_total: 0,
})
const options = ref<StudentOptions>({
  status_options: [],
  degree_options: [],
  advisor_options: [],
  center_options: [],
  political_status_options: [],
  center_advisor_map: [],
})
const students = ref<StudentRecord[]>([])
const centers = ref<CenterRecord[]>([])
const registeredPortalStudents = ref<RegisteredPortalStudentRecord[]>([])

const studentFilters = reactive({
  keyword: '',
  status: '',
  advisor_name: '',
  center_name: '',
})
const centerFilters = reactive({
  keyword: '',
  is_enabled: '',
  director_name: '',
})
const registeredPortalFilters = reactive({
  keyword: '',
  application_form_status: '',
})
const portalEmailForm = reactive<RegisteredPortalStudentEmailRequest>({
  subject: '',
  content: '',
})

const studentFormRef = ref<FormInstance>()
const centerFormRef = ref<FormInstance>()
const studentForm = reactive<StudentUpsert>({
  student_no: '',
  full_name: '',
  status: '在校',
  advisor_name: '',
  center_name: '',
  degree_type: '工程博士',
  enrollment_year: new Date().getFullYear(),
  phone_number: '',
  political_status: '',
})
const centerForm = reactive<CenterUpsert>({
  center_name: '',
  director_name: '',
  advisor_names: [],
  is_enabled: true,
  created_date: new Date().toISOString().slice(0, 10),
})

const centerEnabledOptions = [
  { label: '启用', value: 'true' },
  { label: '停用', value: 'false' },
]
const portalApplicationFormStatusOptions = [
  { label: '已填写报名', value: '已填写报名' },
  { label: '未填写报名', value: '未填写报名' },
]

const studentRules: FormRules<StudentUpsert> = {
  student_no: [{ required: true, message: '请输入学号', trigger: 'blur' }],
  full_name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }],
  advisor_name: [{ required: true, message: '请选择导师', trigger: 'change' }],
  center_name: [{ required: true, message: '请选择中心', trigger: 'change' }],
  degree_type: [{ required: true, message: '请选择学位类型', trigger: 'change' }],
  enrollment_year: [{ required: true, message: '请输入入学年份', trigger: 'change' }],
}
const centerRules: FormRules<CenterUpsert> = {
  center_name: [{ required: true, message: '请输入中心名称', trigger: 'blur' }],
  director_name: [{ required: true, message: '请选择负责人', trigger: 'change' }],
  advisor_names: [{ required: true, message: '请选择导师团队', trigger: 'change', type: 'array' }],
}

const activeSection = computed(() => String(route.meta.section || 'records'))
const isRecordSection = computed(() => activeSection.value === 'records')
const isCenterSection = computed(() => activeSection.value === 'centers')
const isRegisteredPortalSection = computed(() => activeSection.value === 'portal-registrations')
const canMutateSection = computed(() => !isRegisteredPortalSection.value)
const sectionConfig = computed(() => {
  if (activeSection.value === 'portal-registrations') {
    return {
      title: '注册学生管理',
      tag: '门户注册学生',
      createLabel: '',
      total: registeredStudentPager.pagination.total,
    }
  }
  if (activeSection.value === 'centers') {
    return {
      title: '研究中心管理',
      tag: '研究中心主数据',
      createLabel: '新增研究中心',
      total: centerPager.pagination.total,
    }
  }
  return {
    title: '学生主档',
    tag: '主数据管理',
    createLabel: '新增学生',
    total: studentPager.pagination.total,
  }
})
const statCards = computed(() => {
  if (activeSection.value === 'portal-registrations') {
    return [
      { label: '注册学生总量', count: stats.value.registered_portal_total, tone: 'healthy' },
      { label: '已填写报名', count: stats.value.portal_submitted_total, tone: 'attention' },
      { label: '未填写报名', count: stats.value.portal_unsubmitted_total, tone: 'neutral' },
      { label: '研究中心总量', count: stats.value.center_total, tone: 'warning' },
    ]
  }
  if (activeSection.value === 'centers') {
    return [
      { label: '研究中心总量', count: stats.value.center_total, tone: 'healthy' },
      { label: '启用研究中心', count: stats.value.enabled_center_total, tone: 'attention' },
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
const centerAdvisorMap = computed(() => {
  const mapping = new Map<string, SelectOption[]>()
  options.value.center_advisor_map.forEach((item) => mapping.set(item.center_name, item.advisors))
  return mapping
})
const advisorOptions = computed(() => {
  if (!studentForm.center_name) {
    return options.value.advisor_options
  }
  return centerAdvisorMap.value.get(studentForm.center_name) || []
})
const studentPager = useServerPagination()
const centerPager = useServerPagination()
const registeredStudentPager = useServerPagination()

function normalizeStudentPayload(payload: StudentUpsert): StudentUpsert {
  return {
    ...payload,
    center_name: payload.center_name.trim(),
    phone_number: payload.phone_number?.trim() || '',
    political_status: payload.political_status?.trim() || '',
  }
}

function normalizeCenterPayload(payload: CenterUpsert): CenterUpsert {
  return {
    ...payload,
    center_name: payload.center_name.trim(),
    director_name: payload.director_name.trim(),
    advisor_names: Array.from(new Set(payload.advisor_names.filter(Boolean))),
    created_date: payload.created_date || new Date().toISOString().slice(0, 10),
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
}

async function loadRecords() {
  const response = await listStudents({
    keyword: studentFilters.keyword || undefined,
    status: studentFilters.status || undefined,
    advisor_name: studentFilters.advisor_name || undefined,
    center_name: studentFilters.center_name || undefined,
    page: studentPager.pagination.currentPage,
    page_size: studentPager.pagination.pageSize,
  })
  students.value = response.data.items
  studentPager.sync(response.data.total)
}

async function loadCenters() {
  const response = await listCenters({
    keyword: centerFilters.keyword || undefined,
    is_enabled: centerFilters.is_enabled ? centerFilters.is_enabled === 'true' : undefined,
    director_name: centerFilters.director_name || undefined,
    page: centerPager.pagination.currentPage,
    page_size: centerPager.pagination.pageSize,
  })
  centers.value = response.data.items
  centerPager.sync(response.data.total)
}

async function loadRegisteredPortalStudents() {
  const response = await listRegisteredPortalStudents({
    keyword: registeredPortalFilters.keyword || undefined,
    application_form_status: registeredPortalFilters.application_form_status || undefined,
    page: registeredStudentPager.pagination.currentPage,
    page_size: registeredStudentPager.pagination.pageSize,
  })
  registeredPortalStudents.value = response.data.items
  registeredStudentPager.sync(response.data.total)
}

async function loadSectionData() {
  loading.value = true
  try {
    if (activeSection.value === 'portal-registrations') {
      await loadRegisteredPortalStudents()
      return
    }
    if (activeSection.value === 'centers') {
      await loadCenters()
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
    center_name: '',
    degree_type: '工程博士',
    enrollment_year: new Date().getFullYear(),
    phone_number: '',
    political_status: '',
  })
  studentFormRef.value?.clearValidate()
}

function resetCenterForm() {
  currentId.value = null
  Object.assign(centerForm, {
    center_name: '',
    director_name: '',
    advisor_names: [],
    is_enabled: true,
    created_date: new Date().toISOString().slice(0, 10),
  })
  centerFormRef.value?.clearValidate()
}

function openCreateDialog() {
  if (!canMutateSection.value) {
    return
  }
  dialogMode.value = 'create'
  if (activeSection.value === 'centers') {
    resetCenterForm()
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
    center_name: row.center_name,
    degree_type: row.degree_type,
    enrollment_year: row.enrollment_year,
    phone_number: row.phone_number || '',
    political_status: row.political_status || '',
  })
  dialogVisible.value = true
}

function openCenterEditDialog(row: CenterRecord) {
  dialogMode.value = 'edit'
  currentId.value = row.id
  Object.assign(centerForm, {
    center_name: row.center_name,
    director_name: row.director_name,
    advisor_names: [...row.advisor_names],
    is_enabled: row.is_enabled,
    created_date: row.created_date || new Date().toISOString().slice(0, 10),
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

async function submitCenterForm() {
  const formInstance = centerFormRef.value
  if (!formInstance) {
    return
  }
  const isValid = await formInstance.validate().catch(() => false)
  if (!isValid) {
    return
  }
  submitting.value = true
  try {
    const payload = normalizeCenterPayload(centerForm)
    if (dialogMode.value === 'create') {
      await createCenter(payload)
      ElMessage.success('研究中心已新增')
    } else if (currentId.value !== null) {
      await updateCenter(currentId.value, payload)
      ElMessage.success('研究中心信息已更新')
    }
    dialogVisible.value = false
    await refreshAfterMutation()
  } catch (error) {
    const detail = axios.isAxiosError(error) ? String(error.response?.data?.detail || error.message || '研究中心保存失败') : '研究中心保存失败'
    ElMessage.error(detail)
  } finally {
    submitting.value = false
  }
}

async function submitDialog() {
  if (isCenterSection.value) {
    await submitCenterForm()
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

async function handleDeleteCenter(row: CenterRecord) {
  try {
    await ElMessageBox.confirm(`确定删除研究中心 ${row.center_name} 吗？`, '删除确认', { type: 'warning' })
    await deleteCenter(row.id)
    ElMessage.success('研究中心已删除')
    await refreshAfterMutation()
  } catch (error) {
    if (error === 'cancel') {
      return
    }
    const detail = axios.isAxiosError(error) ? String(error.response?.data?.detail || error.message || '研究中心删除失败') : '研究中心删除失败'
    ElMessage.error(detail)
  }
}

async function handleBatchDeleteCenters() {
  if (!selectedCenterIds.value.length) {
    ElMessage.warning('请先选择研究中心')
    return
  }
  await ElMessageBox.confirm(`确定批量删除已选 ${selectedCenterIds.value.length} 个研究中心吗？`, '批量删除确认', { type: 'warning' })
  const response = await batchDeleteCenters(selectedCenterIds.value)
  ElMessage.success(`已删除 ${response.data.success_count} 个研究中心`)
  selectedCenterIds.value = []
  await refreshAfterMutation()
}

async function handleSearch() {
  if (isRegisteredPortalSection.value) {
    registeredStudentPager.reset()
  } else if (isCenterSection.value) {
    centerPager.reset()
  } else {
    studentPager.reset()
  }
  await loadSectionData()
}

async function handleReset() {
  Object.assign(studentFilters, { keyword: '', status: '', advisor_name: '', center_name: '' })
  Object.assign(centerFilters, { keyword: '', is_enabled: '', director_name: '' })
  Object.assign(registeredPortalFilters, { keyword: '', application_form_status: '' })
  selectedCenterIds.value = []
  studentPager.reset()
  centerPager.reset()
  registeredStudentPager.reset()
  await loadSectionData()
}

async function handleStudentPageChange(page: number) {
  studentPager.handleCurrentChange(page)
  await loadSectionData()
}

async function handleStudentPageSizeChange(size: number) {
  studentPager.handleSizeChange(size)
  await loadSectionData()
}

async function handleCenterPageChange(page: number) {
  centerPager.handleCurrentChange(page)
  await loadSectionData()
}

async function handleCenterPageSizeChange(size: number) {
  centerPager.handleSizeChange(size)
  await loadSectionData()
}

async function handleRegisteredStudentPageChange(page: number) {
  registeredStudentPager.handleCurrentChange(page)
  await loadSectionData()
}

async function handleRegisteredStudentPageSizeChange(size: number) {
  registeredStudentPager.handleSizeChange(size)
  await loadSectionData()
}

function handleCenterSelectionChange(selection: CenterRecord[]) {
  selectedCenterIds.value = selection.map((item) => item.id)
}

function handleStudentCenterChange(value: string) {
  const availableAdvisors = centerAdvisorMap.value.get(value) || []
  if (!availableAdvisors.some((item) => item.value === studentForm.advisor_name)) {
    studentForm.advisor_name = ''
  }
}

function handleCenterDirectorChange(value: string) {
  if (!centerForm.advisor_names.includes(value)) {
    centerForm.advisor_names = Array.from(new Set([...centerForm.advisor_names, value]))
  }
}

function syncCenterDirector() {
  if (!centerForm.advisor_names.includes(centerForm.director_name)) {
    centerForm.director_name = centerForm.advisor_names[0] || ''
  }
}

function statusTagType(status: string) {
  return resolveDictTagType(status, studentStatusColors.value)
}

function portalApplicationFormStatusTagType(status: string) {
  if (status === '已填写报名') {
    return 'success'
  }
  return 'info'
}

function portalRecruitmentStatusTagType(status: string | null | undefined) {
  if (!status) {
    return 'info'
  }
  if (status === '报名已提交' || status === '资格审核通过' || status === '材料评分中' || status === '面试完成') {
    return 'warning'
  }
  if (status === '预录取' || status === '同意录取') {
    return 'success'
  }
  return 'info'
}

function portalAccountStatusTagType(status: string) {
  return status === '启用' ? 'success' : 'danger'
}

function buildRegisteredStudentActionMessage(response: RegisteredPortalStudentActionResponse, sentText: string, skippedText: string) {
  if (response.email_sent === true) {
    return `${response.message}\n\n${sentText}`
  }
  if (response.email_sent === false) {
    return `${response.message}\n\n${skippedText}`
  }
  return response.message
}

function resetPortalEmailForm() {
  portalEmailTarget.value = null
  portalEmailForm.subject = ''
  portalEmailForm.content = ''
}

async function handleDeactivateRegisteredPortalStudent(row: RegisteredPortalStudentRecord) {
  if (row.account_status === '停用') {
    await ElMessageBox.alert('该注册学生账号已停用。', '提示', { type: 'info' })
    return
  }
  await ElMessageBox.confirm(`确定停用 ${row.full_name} 的门户账号吗？停用后将无法登录和提交报名。`, '停用确认', { type: 'warning' })
  const response = await deactivateRegisteredPortalStudent(row.id)
  await ElMessageBox.alert(response.data.message, '操作成功', { type: 'success' })
  await refreshAfterMutation()
}

async function handleActivateRegisteredPortalStudent(row: RegisteredPortalStudentRecord) {
  if (row.account_status === '启用') {
    await ElMessageBox.alert('该注册学生账号已启用。', '提示', { type: 'info' })
    return
  }
  await ElMessageBox.confirm(`确定重新启用 ${row.full_name} 的门户账号吗？启用后可恢复登录和报名操作。`, '启用确认', { type: 'warning' })
  const response = await activateRegisteredPortalStudent(row.id)
  await ElMessageBox.alert(response.data.message, '操作成功', { type: 'success' })
  await refreshAfterMutation()
}

async function handleResetRegisteredPortalStudentPassword(row: RegisteredPortalStudentRecord) {
  if (row.account_status !== '启用') {
    await ElMessageBox.alert('已停用账号不可重置密码。', '提示', { type: 'warning' })
    return
  }
  await ElMessageBox.confirm(`确定重置 ${row.full_name} 的门户密码吗？系统将生成临时密码。`, '重置密码确认', { type: 'warning' })
  const response = await resetRegisteredPortalStudentPassword(row.id)
  const detailLines = [buildRegisteredStudentActionMessage(response.data, '重置密码邮件已发送。', '当前未配置邮件服务，本次未发送邮件。')]
  if (response.data.temporary_password) {
    detailLines.push(`临时密码：${response.data.temporary_password}`)
  }
  await ElMessageBox.alert(detailLines.join('\n\n'), '重置密码成功', { type: 'success' })
  await refreshAfterMutation()
}

function openRegisteredPortalStudentEmailDialog(row: RegisteredPortalStudentRecord) {
  portalEmailTarget.value = row
  portalEmailForm.subject = '博士生招生门户通知'
  portalEmailForm.content = ''
  portalEmailDialogVisible.value = true
}

function registeredPortalMainActions(row: RegisteredPortalStudentRecord): TableRowAction<RegisteredPortalStudentRecord>[] {
  return [
    {
      key: row.account_status === '启用' ? 'deactivate' : 'activate',
      label: row.account_status === '启用' ? '停用账号' : '启用账号',
      type: row.account_status === '启用' ? 'danger' : 'success',
      onClick: row.account_status === '启用' ? handleDeactivateRegisteredPortalStudent : handleActivateRegisteredPortalStudent,
    },
  ]
}

function registeredPortalMoreActions(row: RegisteredPortalStudentRecord): TableRowAction<RegisteredPortalStudentRecord>[] {
  return [
    { key: 'reset-password', label: '重置密码', type: 'primary', disabled: row.account_status !== '启用', onClick: handleResetRegisteredPortalStudentPassword },
    { key: 'send-email', label: '发送邮件', type: 'success', onClick: openRegisteredPortalStudentEmailDialog },
  ]
}

async function submitPortalEmailDialog() {
  if (!portalEmailTarget.value) {
    return
  }
  const subject = portalEmailForm.subject.trim()
  const content = portalEmailForm.content.trim()
  if (!subject) {
    await ElMessageBox.alert('请输入邮件主题。', '提示', { type: 'warning' })
    return
  }
  if (!content) {
    await ElMessageBox.alert('请输入邮件内容。', '提示', { type: 'warning' })
    return
  }
  portalEmailSubmitting.value = true
  try {
    const response = await sendRegisteredPortalStudentEmail(portalEmailTarget.value.id, { subject, content })
    portalEmailDialogVisible.value = false
    await ElMessageBox.alert(
      buildRegisteredStudentActionMessage(response.data, '邮件已发送。', '当前未配置邮件服务，本次未发送邮件。'),
      '发送结果',
      { type: response.data.email_sent === false ? 'warning' : 'success' },
    )
    resetPortalEmailForm()
  } finally {
    portalEmailSubmitting.value = false
  }
}

watch(() => studentForm.center_name, handleStudentCenterChange)
watch(() => centerForm.director_name, handleCenterDirectorChange)
watch(() => centerForm.advisor_names, syncCenterDirector)
watch(() => portalEmailDialogVisible.value, (visible) => {
  if (!visible) {
    resetPortalEmailForm()
  }
})
watch(() => activeSection.value, () => {
  dialogVisible.value = false
  portalEmailDialogVisible.value = false
  selectedCenterIds.value = []
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
            v-if="activeSection === 'centers'"
            plain
            type="danger"
            :disabled="!selectedCenterIds.length"
            @click="handleBatchDeleteCenters"
          >
            批量删除研究中心
          </el-button>
          <span class="summary-text">共 {{ sectionConfig.total }} 条记录</span>
          <el-button v-if="canMutateSection" type="primary" round @click="openCreateDialog">{{ sectionConfig.createLabel }}</el-button>
        </div>
      </div>

      <el-form v-if="isRecordSection" class="filter-form" :inline="true">
        <el-form-item label="关键字">
          <el-input v-model="studentFilters.keyword" placeholder="学号 / 姓名 / 研究中心" clearable />
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
        <el-form-item label="研究中心">
          <el-select v-model="studentFilters.center_name" placeholder="全部研究中心" clearable filterable style="width: 180px">
            <el-option v-for="item in options.center_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <el-form v-else-if="isCenterSection" class="filter-form" :inline="true">
        <el-form-item label="关键字">
          <el-input v-model="centerFilters.keyword" placeholder="研究中心名称 / 负责人 / 导师团队" clearable />
        </el-form-item>
        <el-form-item label="是否启用">
          <el-select v-model="centerFilters.is_enabled" placeholder="全部状态" clearable style="width: 160px">
            <el-option v-for="item in centerEnabledOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="负责人">
          <el-select v-model="centerFilters.director_name" placeholder="全部负责人" clearable filterable style="width: 180px">
            <el-option v-for="item in options.advisor_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <el-form v-else class="filter-form" :inline="true">
        <el-form-item label="关键字">
          <el-input v-model="registeredPortalFilters.keyword" placeholder="姓名 / 手机号 / 邮箱 / 招生计划" clearable />
        </el-form-item>
        <el-form-item label="报名状态">
          <el-select v-model="registeredPortalFilters.application_form_status" placeholder="全部状态" clearable style="width: 180px">
            <el-option v-for="item in portalApplicationFormStatusOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <div class="table-host">
        <el-table v-if="isRecordSection" :data="students" stripe border v-loading="loading" table-layout="fixed">
          <el-table-column prop="student_no" label="学号" width="128" show-overflow-tooltip />
          <el-table-column prop="full_name" label="姓名" width="96" show-overflow-tooltip />
          <el-table-column prop="degree_type" label="学位类型" width="112" show-overflow-tooltip />
          <el-table-column prop="advisor_name" label="导师" width="96" show-overflow-tooltip />
          <el-table-column prop="center_name" label="所属研究中心" min-width="130" show-overflow-tooltip />
          <el-table-column prop="enrollment_year" label="入学年份" width="96" />
          <el-table-column label="当前状态" width="112">
            <template #default="scope">
              <el-tag :type="statusTagType(scope.row.status)">{{ scope.row.status }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="phone_number" label="联系电话" width="128" show-overflow-tooltip />
          <el-table-column prop="political_status" label="政治面貌" width="110" show-overflow-tooltip />
          <el-table-column label="操作" width="118" align="left">
            <template #default="scope">
              <TableRowActions :row="scope.row" :main-actions="[{ key: 'edit', label: '编辑', type: 'primary', onClick: openStudentEditDialog }]" :more-actions="[{ key: 'delete', label: '删除', type: 'danger', onClick: handleDeleteStudent }]" />
            </template>
          </el-table-column>
        </el-table>

        <el-table v-else-if="isCenterSection" :data="centers" stripe border v-loading="loading" table-layout="fixed" @selection-change="handleCenterSelectionChange">
          <el-table-column type="selection" width="44" />
          <el-table-column prop="center_name" label="研究中心名称" min-width="180" show-overflow-tooltip />
          <el-table-column prop="director_name" label="负责人" width="120" show-overflow-tooltip />
          <el-table-column label="导师团队" min-width="220" show-overflow-tooltip>
            <template #default="scope">
              <span :title="scope.row.advisor_names.join('、')">{{ scope.row.advisor_names.join('、') || '未配置' }}</span>
            </template>
          </el-table-column>
          <el-table-column label="是否启用" width="110" align="center">
            <template #default="scope">
              <el-tag :type="scope.row.is_enabled ? 'success' : 'info'">{{ scope.row.is_enabled ? '启用' : '停用' }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_date" label="创建日期" width="120" />
          <el-table-column label="学生数" width="120" align="center">
            <template #default="scope">
              <div class="stat-stack">
                <strong>{{ scope.row.member_student_count }}</strong>
                <span>活跃 {{ scope.row.active_student_count }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="118" align="left">
            <template #default="scope">
              <TableRowActions :row="scope.row" :main-actions="[{ key: 'edit', label: '编辑', type: 'primary', onClick: openCenterEditDialog }]" :more-actions="[{ key: 'delete', label: '删除', type: 'danger', onClick: handleDeleteCenter }]" />
            </template>
          </el-table-column>
        </el-table>

        <el-table v-else :data="registeredPortalStudents" stripe border v-loading="loading" table-layout="fixed">
          <el-table-column prop="full_name" label="姓名" width="96" show-overflow-tooltip />
          <el-table-column prop="phone_number" label="手机号" width="128" show-overflow-tooltip />
          <el-table-column prop="email" label="邮箱" min-width="180" show-overflow-tooltip />
          <el-table-column label="账号状态" width="96" align="center">
            <template #default="scope">
              <el-tag :type="portalAccountStatusTagType(scope.row.account_status)">{{ scope.row.account_status }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="报名状态" width="110" align="center">
            <template #default="scope">
              <el-tag :type="portalApplicationFormStatusTagType(scope.row.application_form_status)">{{ scope.row.application_form_status }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="selected_plan_name" label="招生计划" min-width="160" show-overflow-tooltip />
          <el-table-column label="申请流转状态" width="130" align="center">
            <template #default="scope">
              <el-tag :type="portalRecruitmentStatusTagType(scope.row.recruitment_application_status)">{{ scope.row.recruitment_application_status || '未提交' }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="registered_at" label="注册时间" width="160" show-overflow-tooltip />
          <el-table-column label="操作" width="170" align="left">
            <template #default="scope">
              <TableRowActions
                :row="scope.row"
                :main-actions="registeredPortalMainActions(scope.row)"
                :more-actions="registeredPortalMoreActions(scope.row)"
              />
            </template>
          </el-table-column>
        </el-table>

        <div class="pagination-bar">
          <el-pagination
            v-if="isRecordSection"
            :current-page="studentPager.pagination.currentPage"
            :page-size="studentPager.pagination.pageSize"
            :page-sizes="[10, 20, 50, 100]"
            :total="studentPager.pagination.total"
            layout="total, sizes, prev, pager, next, jumper"
            @current-change="handleStudentPageChange"
            @size-change="handleStudentPageSizeChange"
          />
          <el-pagination
            v-else-if="isCenterSection"
            :current-page="centerPager.pagination.currentPage"
            :page-size="centerPager.pagination.pageSize"
            :page-sizes="[10, 20, 50, 100]"
            :total="centerPager.pagination.total"
            layout="total, sizes, prev, pager, next, jumper"
            @current-change="handleCenterPageChange"
            @size-change="handleCenterPageSizeChange"
          />
          <el-pagination
            v-else
            :current-page="registeredStudentPager.pagination.currentPage"
            :page-size="registeredStudentPager.pagination.pageSize"
            :page-sizes="[10, 20, 50, 100]"
            :total="registeredStudentPager.pagination.total"
            layout="total, sizes, prev, pager, next, jumper"
            @current-change="handleRegisteredStudentPageChange"
            @size-change="handleRegisteredStudentPageSizeChange"
          />
        </div>
      </div>
    </article>

    <el-dialog
      v-if="canMutateSection"
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
          <el-form-item label="所属研究中心" prop="center_name">
            <el-select v-model="studentForm.center_name" placeholder="请选择研究中心" filterable>
              <el-option v-for="item in options.center_options" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
          <el-form-item label="导师" prop="advisor_name">
            <el-select v-model="studentForm.advisor_name" placeholder="请选择导师" filterable :disabled="!studentForm.center_name">
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
        v-else-if="isCenterSection"
        ref="centerFormRef"
        :model="centerForm"
        :rules="centerRules"
        label-width="96px"
        class="dialog-form"
      >
        <div class="dialog-grid">
          <el-form-item label="中心名称" prop="center_name">
            <el-input v-model="centerForm.center_name" placeholder="请输入中心名称" />
          </el-form-item>
          <el-form-item label="负责人" prop="director_name">
            <el-select v-model="centerForm.director_name" placeholder="请选择负责人" filterable>
              <el-option v-for="item in options.advisor_options" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
          <el-form-item label="导师团队" prop="advisor_names" class="dialog-grid--full">
            <el-select v-model="centerForm.advisor_names" multiple filterable placeholder="请选择导师团队">
              <el-option v-for="item in options.advisor_options" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
          <el-form-item label="是否启用">
            <el-switch v-model="centerForm.is_enabled" inline-prompt active-text="启用" inactive-text="停用" />
          </el-form-item>
          <el-form-item label="创建日期">
            <el-date-picker v-model="centerForm.created_date" type="date" value-format="YYYY-MM-DD" placeholder="请选择创建日期" />
          </el-form-item>
        </div>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submitDialog">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="portalEmailDialogVisible" title="发送邮件" width="640px" destroy-on-close>
      <el-form label-width="88px" class="dialog-form">
        <div class="dialog-grid">
          <el-form-item label="收件人" class="dialog-grid--full">
            <el-input :model-value="portalEmailTarget?.email || ''" disabled />
          </el-form-item>
          <el-form-item label="主题" class="dialog-grid--full">
            <el-input v-model="portalEmailForm.subject" maxlength="120" show-word-limit placeholder="请输入邮件主题" />
          </el-form-item>
          <el-form-item label="内容" class="dialog-grid--full">
            <el-input v-model="portalEmailForm.content" type="textarea" :rows="8" placeholder="请输入邮件正文内容" />
          </el-form-item>
        </div>
      </el-form>
      <template #footer>
        <el-button @click="portalEmailDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="portalEmailSubmitting" @click="submitPortalEmailDialog">发送</el-button>
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