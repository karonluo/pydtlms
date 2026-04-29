<script setup lang="ts">
import axios from 'axios'
import { computed, onMounted, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import TableRowActions from '../../components/table/TableRowActions.vue'
import RecruitmentApplicationReviewDrawer from '../../components/recruitment/RecruitmentApplicationReviewDrawer.vue'
import { buildDictColorMap, resolveDictTagType, type DictColorMap } from '../../utils/dictTag'
import { getEmailValidationMessage, getPhoneValidationMessage, normalizeEmail, normalizePhoneNumber } from '../../utils/contactValidation'
import { getChinaResidentIdValidationMessage, normalizeChinaResidentIdNumber } from '../../utils/chinaResidentId'
import { useServerPagination } from '../../composables/useServerPagination'

import {
  createRecruitmentApplication,
  createRecruitmentPlan,
  deleteRecruitmentPlan,
  deleteRecruitmentApplication,
  downloadRecruitmentTemplate,
  exportRecruitmentApplications,
  getRecruitmentApplicationDetail,
  getRecruitmentOptions,
  getRecruitmentStats,
  getRecruitmentWorkbench,
  importRecruitmentApplications,
  listRecruitmentApplications,
  listRecruitmentPlans,
  uploadRecruitmentBrochureImage,
  updateRecruitmentApplication,
  updateRecruitmentPlan,
  type RecruitApplicationRecord,
  type RecruitApplicationUpsert,
  type RecruitmentOptions,
  type RecruitPlanRecord,
  type RecruitPlanUpsert,
  type RecruitStats,
  type RecruitWorkbench,
} from '../../api/recruitment'
import { executeWorkflowTaskAction, listWorkflowTasks, type WorkflowActionOption, type WorkflowTaskRecord } from '../../api/workflow'

const sourceChannelOptions = ['导师推荐', '实验室官网', '高校宣讲', '朋友同学推荐', '其他']
const genderOptions = ['男', '女']
const maritalStatusOptions = ['未婚', '已婚']
const educationStageOptions = ['硕士', '硕士在读', '本科', '本科在读', '高中']
const familyRelationOptions = ['父亲', '母亲', '兄', '弟', '姐', '妹', '其他']

function createApplicationProfile() {
  return {
    gender: '',
    native_place: '',
    political_status: '',
    marital_status: '未婚',
    religious_belief: '无',
    id_type: '居民身份证',
    mailing_address: '',
  }
}

function createApplicationPreference(order: number, isOptional: boolean) {
  return {
    preference_order: order,
    research_center_name: '',
    advisor_name: '',
    is_optional: isOptional,
  }
}

function createApplicationEducation(order: number) {
  return {
    sort_order: order,
    education_stage: order === 1 ? '硕士' : '',
    school_name: '',
    major_name: '',
    average_score: '',
    gpa: '',
    ranking: '',
    start_month: '',
    end_month: '',
    verifier_name: '',
    verifier_phone: '',
  }
}

function createApplicationPractice() {
  return {
    start_month: '',
    end_month: '',
    organization_name: '',
    position_name: '',
    responsibility_text: '',
    verifier_name: '',
    verifier_phone: '',
  }
}

function createApplicationFamilyMember(relationType = '其他') {
  return {
    member_name: '',
    relation_type: relationType,
    employer_name: '',
    job_title: '',
    contact_phone: '',
  }
}

function createApplicationPersonalStatement() {
  return {
    personal_statement_text: '',
    ai_problem_statement: '',
    ai_industry_opinion: '',
    resume_attachment_url: '',
  }
}

function trimText(value: unknown) {
  return String(value || '').trim()
}

function buildApplicationFormState(row?: RecruitApplicationRecord): RecruitApplicationUpsert {
  return {
    plan_id: row?.plan_id ?? selectedPlanId.value ?? planReferenceList.value[0]?.id ?? 0,
    business_key: row?.business_key || '',
    portal_student_id: row?.portal_student_id ?? null,
    candidate_no: row?.candidate_no || '',
    review_round: row?.review_round || '',
    student_name: row?.student_name || '',
    first_choice: row?.first_choice || '',
    second_choice: row?.second_choice || '',
    gender: row?.gender || '',
    political_status: row?.political_status || '',
    marital_status: row?.marital_status || '未婚',
    religious_belief: row?.religious_belief || '无',
    native_place: row?.native_place || '',
    phone_number: row?.phone_number || '',
    email: row?.email || '',
    mailing_address: row?.mailing_address || '',
    id_type: row?.id_type || '居民身份证',
    id_number: row?.id_number || '',
    graduation_school: row?.graduation_school || '',
    undergraduate_school: row?.undergraduate_school || '',
    accept_adjustment: row?.accept_adjustment || '是',
    undergraduate_average_score: row?.undergraduate_average_score || '',
    undergraduate_gpa: row?.undergraduate_gpa || '',
    undergraduate_rank: row?.undergraduate_rank || '',
    undergraduate_major: row?.undergraduate_major || '',
    graduate_average_score: row?.graduate_average_score || '',
    graduate_gpa: row?.graduate_gpa || '',
    graduate_rank: row?.graduate_rank || '',
    graduate_major: row?.graduate_major || '',
    highest_degree: row?.highest_degree || '硕士',
    intended_field: row?.intended_field || '',
    intended_advisor_name: row?.intended_advisor_name || '',
    discovery_channel: row?.discovery_channel || '',
    source_channel: row?.source_channel || '',
    source_channel_other: row?.source_channel_other || '',
    graduate_school: row?.graduate_school || '',
    overseas_university_name: row?.overseas_university_name || '',
    overseas_master_university_name: row?.overseas_master_university_name || '',
    self_evaluation: row?.self_evaluation || '',
    applied_at: row?.applied_at || '',
    research_problem: row?.research_problem || '',
    research_status_analysis: row?.research_status_analysis || '',
    research_impact: row?.research_impact || '',
    ai_society_impact: row?.ai_society_impact || '',
    dissenting_view: row?.dissenting_view || '',
    family_info: row?.family_info || '',
    education_experience: row?.education_experience || '',
    practice_experience: row?.practice_experience || '',
    personal_statement_text: row?.personal_statement_text || '',
    student_activity_experience: row?.student_activity_experience || '',
    personal_statement_attachment: row?.personal_statement_attachment || '',
    material_list_attachment: row?.material_list_attachment || '',
    supplementary_profile: row?.supplementary_profile || '',
    material_status: row?.material_status || '材料齐全',
    application_status: row?.application_status || '报名已提交',
    reviewer_name: row?.reviewer_name || '',
    final_score: row?.final_score ?? undefined,
    profile: row?.profile ? { ...createApplicationProfile(), ...row.profile } : {
      ...createApplicationProfile(),
      gender: row?.gender || '',
      native_place: row?.native_place || '',
      political_status: row?.political_status || '',
      marital_status: row?.marital_status || '未婚',
      religious_belief: row?.religious_belief || '无',
      id_type: row?.id_type || '居民身份证',
      mailing_address: row?.mailing_address || '',
    },
    preferences: row?.preferences?.length
      ? row.preferences.map((item, index) => ({ ...createApplicationPreference(index + 1, index > 0), ...item, preference_order: index + 1 }))
      : [
          {
            ...createApplicationPreference(1, false),
            research_center_name: row?.first_choice || row?.intended_field || '',
            advisor_name: row?.intended_advisor_name || '',
          },
          ...(row?.second_choice ? [{ ...createApplicationPreference(2, true), research_center_name: row.second_choice }] : []),
        ],
    education_experiences: row?.education_experiences?.length
      ? row.education_experiences.map((item, index) => ({ ...createApplicationEducation(index + 1), ...item, sort_order: index + 1 }))
      : [createApplicationEducation(1)],
    practice_experiences: row?.practice_experiences?.length
      ? row.practice_experiences.map((item) => ({ ...createApplicationPractice(), ...item }))
      : [],
    family_members: row?.family_members?.length
      ? row.family_members.map((item) => ({ ...createApplicationFamilyMember(item.relation_type || '其他'), ...item }))
      : [createApplicationFamilyMember('父亲'), createApplicationFamilyMember('母亲')],
    personal_statement: {
      ...createApplicationPersonalStatement(),
      ...(row?.personal_statement || {}),
      personal_statement_text: row?.personal_statement?.personal_statement_text || row?.personal_statement_text || '',
      ai_problem_statement: row?.personal_statement?.ai_problem_statement || row?.research_problem || '',
      ai_industry_opinion: row?.personal_statement?.ai_industry_opinion || row?.dissenting_view || '',
      resume_attachment_url: row?.personal_statement?.resume_attachment_url || row?.personal_statement_attachment || '',
    },
    declaration: row?.declaration || { has_read_declaration: false },
  }
}
const plans = ref<RecruitPlanRecord[]>([])
const applications = ref<RecruitApplicationRecord[]>([])
const options = ref<RecruitmentOptions>({
  semester_options: [],
  plan_stage_options: [],
  degree_options: [],
  material_status_options: [],
  application_status_options: [],
  intended_field_options: [],
  reviewer_options: [],
  graduation_school_options: [],
})
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
const applicationDetailVisible = ref(false)
const deleteApplicationDialogVisible = ref(false)
const planMode = ref<'create' | 'edit'>('create')
const applicationMode = ref<'create' | 'edit'>('create')
const deletingPlan = ref(false)
const planSubmitting = ref(false)
const applicationSubmitting = ref(false)
const deleteApplicationSubmitting = ref(false)
const importSubmitting = ref(false)
const exportSubmitting = ref(false)
const templateSubmitting = ref(false)
const brochureUploading = ref(false)
const selectedPlanId = ref<number | undefined>()
const editingPlanId = ref<number | null>(null)
const editingApplicationId = ref<number | null>(null)
const deletingApplication = ref<RecruitApplicationRecord | null>(null)
const planReferenceList = ref<RecruitPlanRecord[]>([])
const viewingApplication = ref<RecruitApplicationRecord | null>(null)
const viewingApplicationWorkflowTask = ref<WorkflowTaskRecord | null>(null)
const applicationStatusColors = ref<DictColorMap>({})
const materialStatusColors = ref<DictColorMap>({})
const applicationWorkflowTaskLoading = ref(false)
const applicationWorkflowActionSubmitting = ref(false)

const planFormRef = ref<FormInstance>()
const applicationFormRef = ref<FormInstance>()
const importInputRef = ref<HTMLInputElement | null>(null)
const brochureInputRef = ref<HTMLInputElement | null>(null)

const applicationFilters = reactive({
  keyword: '',
  status: '',
})
const planFilters = reactive({
  keyword: '',
  semester: '',
})

const planForm = reactive<RecruitPlanUpsert>({
  plan_name: '',
  academic_year: String(new Date().getFullYear()),
  semester: '秋',
  brochure_image_url: '',
  plan_description: '',
})

const applicationForm = reactive<RecruitApplicationUpsert>({
  ...buildApplicationFormState(),
})

const planRules: FormRules<RecruitPlanUpsert> = {
  plan_name: [{ required: true, message: '请输入计划名称', trigger: 'blur' }],
  academic_year: [{ required: true, message: '请输入学年', trigger: 'blur' }],
  semester: [{ required: true, message: '请选择学期', trigger: 'change' }],
  plan_description: [{ required: true, message: '请输入计划描述', trigger: 'blur' }],
}

const applicationRules: FormRules<RecruitApplicationUpsert> = {
  plan_id: [{ required: true, message: '请选择招生计划', trigger: 'change' }],
  student_name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  graduation_school: [{ required: true, message: '请输入毕业院校', trigger: 'blur' }],
  highest_degree: [{ required: true, message: '请选择最高学历', trigger: 'change' }],
  intended_field: [{ required: true, message: '请输入研究方向', trigger: 'blur' }],
  material_status: [{ required: true, message: '请选择材料状态', trigger: 'change' }],
  application_status: [{ required: true, message: '请选择申请状态', trigger: 'change' }],
}

const statsCards = computed(() => [
  { label: '招生计划', value: stats.value.plan_count, tone: 'healthy' },
  { label: '可用计划', value: stats.value.open_plan_count, tone: 'attention' },
  { label: '报名申请', value: stats.value.application_total, tone: 'neutral' },
  { label: '待审核', value: stats.value.pending_review_total, tone: 'warning' },
  { label: '预录取', value: stats.value.pre_admit_total, tone: 'healthy' },
])

const selectedPlan = computed(() => plans.value.find((item) => item.id === selectedPlanId.value))
const planPager = useServerPagination()
const applicationPager = useServerPagination()

function applicationTagType(status: string) {
  return resolveDictTagType(status, applicationStatusColors.value)
}

function materialTagType(status: string) {
  return resolveDictTagType(status, materialStatusColors.value)
}

async function loadOverview() {
  const [statsResponse, workbenchResponse, optionsResponse] = await Promise.all([getRecruitmentStats(), getRecruitmentWorkbench(), getRecruitmentOptions()])
  stats.value = statsResponse.data
  workbench.value = workbenchResponse.data
  options.value = optionsResponse.data
  applicationStatusColors.value = buildDictColorMap(optionsResponse.data.application_status_options)
  materialStatusColors.value = buildDictColorMap(optionsResponse.data.material_status_options)
}

function resolveAutoSelectedPlanId(planItems: RecruitPlanRecord[]) {
  return planItems.find((item) => item.application_count > 0)?.id ?? planItems[0]?.id
}

async function loadPlans() {
  plansLoading.value = true
  try {
    const response = await listRecruitmentPlans({
      keyword: planFilters.keyword || undefined,
      semester: planFilters.semester || undefined,
      page: planPager.pagination.currentPage,
      page_size: planPager.pagination.pageSize,
    })
    plans.value = response.data.items
    planPager.sync(response.data.total)
    if (selectedPlanId.value && !plans.value.some((item) => item.id === selectedPlanId.value)) {
      selectedPlanId.value = undefined
    }
    if (!selectedPlanId.value && plans.value.length > 0) {
      selectedPlanId.value = resolveAutoSelectedPlanId(plans.value)
    }
  } finally {
    plansLoading.value = false
  }
}

async function loadPlanReferences() {
  const response = await listRecruitmentPlans({ page: 1, page_size: 1000 })
  planReferenceList.value = response.data.items
}

async function loadApplications() {
  applicationsLoading.value = true
  try {
    const response = await listRecruitmentApplications({
      keyword: applicationFilters.keyword || undefined,
      status: applicationFilters.status || undefined,
      plan_id: selectedPlanId.value,
      page: applicationPager.pagination.currentPage,
      page_size: applicationPager.pagination.pageSize,
    })
    applications.value = response.data.items
    applicationPager.sync(response.data.total)
  } finally {
    applicationsLoading.value = false
  }
}

async function refreshAll() {
  await loadPlans()
  await Promise.all([loadOverview(), loadApplications(), loadPlanReferences()])
}

function resetPlanForm() {
  editingPlanId.value = null
  Object.assign(planForm, {
    plan_name: '',
    academic_year: String(new Date().getFullYear()),
    semester: '秋',
    brochure_image_url: '',
    plan_description: '',
  })
  planFormRef.value?.clearValidate()
}

function resetApplicationForm() {
  editingApplicationId.value = null
  Object.assign(applicationForm, buildApplicationFormState())
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
    brochure_image_url: row.brochure_image_url || '',
    plan_description: row.plan_description || '',
  })
  planDialogVisible.value = true
}

async function handleDeleteSelectedPlan() {
  if (!selectedPlan.value || deletingPlan.value) {
    return
  }
  try {
    await ElMessageBox.confirm(
      `确定删除招生计划“${selectedPlan.value.plan_name}”吗？`,
      '删除招生计划',
      {
        type: 'warning',
        confirmButtonText: '删除',
        cancelButtonText: '取消',
      },
    )
  } catch {
    return
  }

  deletingPlan.value = true
  try {
    const deletedPlanId = selectedPlan.value.id
    await deleteRecruitmentPlan(deletedPlanId)
    ElMessage.success('招生计划已删除')
    if (selectedPlanId.value === deletedPlanId) {
      selectedPlanId.value = undefined
    }
    await refreshAll()
  } catch (error) {
    const message = axios.isAxiosError(error) ? String(error.response?.data?.detail || error.message) : '删除招生计划失败'
    ElMessage.error(message)
  } finally {
    deletingPlan.value = false
  }
}

function openCreateApplicationDialog() {
  applicationMode.value = 'create'
  resetApplicationForm()
  applicationDialogVisible.value = true
}

async function openEditApplicationDialog(row: RecruitApplicationRecord) {
  applicationMode.value = 'edit'
  try {
    const response = await getRecruitmentApplicationDetail(row.id)
    editingApplicationId.value = row.id
    Object.assign(applicationForm, buildApplicationFormState(response.data))
    applicationDialogVisible.value = true
  } catch (error) {
    const message = axios.isAxiosError(error) ? String(error.response?.data?.detail || error.message) : '加载报名申请详情失败'
    ElMessage.error(message)
  }
}

function addPreference() {
  if ((applicationForm.preferences?.length || 0) >= 2) {
    return
  }
  applicationForm.preferences = [...(applicationForm.preferences || []), createApplicationPreference((applicationForm.preferences?.length || 0) + 1, true)]
}

function removePreference(index: number) {
  if (index === 0) {
    return
  }
  applicationForm.preferences?.splice(index, 1)
  applicationForm.preferences?.forEach((item, itemIndex) => {
    item.preference_order = itemIndex + 1
    item.is_optional = itemIndex > 0
  })
}

function addEducation() {
  applicationForm.education_experiences = [...(applicationForm.education_experiences || []), createApplicationEducation((applicationForm.education_experiences?.length || 0) + 1)]
}

function removeEducation(index: number) {
  if ((applicationForm.education_experiences?.length || 0) <= 1) {
    return
  }
  applicationForm.education_experiences?.splice(index, 1)
  applicationForm.education_experiences?.forEach((item, itemIndex) => {
    item.sort_order = itemIndex + 1
  })
}

function addPractice() {
  applicationForm.practice_experiences = [...(applicationForm.practice_experiences || []), createApplicationPractice()]
}

function removePractice(index: number) {
  applicationForm.practice_experiences?.splice(index, 1)
}

function addFamilyMember() {
  applicationForm.family_members = [...(applicationForm.family_members || []), createApplicationFamilyMember()]
}

function removeFamilyMember(index: number) {
  if ((applicationForm.family_members?.length || 0) <= 2) {
    return
  }
  applicationForm.family_members?.splice(index, 1)
}

function syncApplicationLegacyFields() {
  const preferences = (applicationForm.preferences || []).filter((item) => trimText(item.research_center_name))
  applicationForm.first_choice = preferences[0]?.research_center_name || ''
  applicationForm.second_choice = preferences[1]?.research_center_name || ''
  applicationForm.intended_field = preferences[0]?.research_center_name || ''
  applicationForm.intended_advisor_name = preferences[0]?.advisor_name || ''

  const education = (applicationForm.education_experiences || []).filter((item) => trimText(item.school_name))
  applicationForm.graduation_school = education[0]?.school_name || ''
  applicationForm.highest_degree = education[0]?.education_stage || ''

  applicationForm.gender = applicationForm.profile?.gender || ''
  applicationForm.native_place = applicationForm.profile?.native_place || ''
  applicationForm.political_status = applicationForm.profile?.political_status || ''
  applicationForm.marital_status = applicationForm.profile?.marital_status || '未婚'
  applicationForm.religious_belief = applicationForm.profile?.religious_belief || '无'
  applicationForm.id_type = applicationForm.profile?.id_type || '居民身份证'
  applicationForm.mailing_address = applicationForm.profile?.mailing_address || ''
  applicationForm.personal_statement_text = applicationForm.personal_statement?.personal_statement_text || ''
  applicationForm.research_problem = applicationForm.personal_statement?.ai_problem_statement || ''
  applicationForm.dissenting_view = applicationForm.personal_statement?.ai_industry_opinion || ''
  applicationForm.personal_statement_attachment = applicationForm.personal_statement?.resume_attachment_url || ''
  applicationForm.discovery_channel = trimText(applicationForm.source_channel_other) || trimText(applicationForm.source_channel)
}

async function openViewApplicationDetail(row: RecruitApplicationRecord) {
  try {
    const response = await getRecruitmentApplicationDetail(row.id)
    viewingApplication.value = response.data
    applicationDetailVisible.value = true
    await loadViewingApplicationWorkflowTask(response.data.business_key)
  } catch (error) {
    const message = axios.isAxiosError(error) ? String(error.response?.data?.detail || error.message) : '加载报名申请详情失败'
    ElMessage.error(message)
  }
}

async function loadViewingApplicationWorkflowTask(businessKey?: string | null) {
  const normalizedKey = String(businessKey || '').trim()
  if (!normalizedKey) {
    viewingApplicationWorkflowTask.value = null
    return
  }
  applicationWorkflowTaskLoading.value = true
  try {
    const response = await listWorkflowTasks({ page: 1, page_size: 20, module: '招生管理', keyword: normalizedKey })
    viewingApplicationWorkflowTask.value = response.data.items.find((item) => item.business_key === normalizedKey) || null
  } catch (error) {
    const message = axios.isAxiosError(error) ? String(error.response?.data?.detail || error.message) : '加载审批任务失败'
    ElMessage.error(message)
    viewingApplicationWorkflowTask.value = null
  } finally {
    applicationWorkflowTaskLoading.value = false
  }
}

function canReviewApplication(row: RecruitApplicationRecord) {
  return row.application_status === '报名已提交'
}

function applicationMainActions(row: RecruitApplicationRecord) {
  return [
    { key: 'view', label: '查看填报', type: 'info' as const, onClick: openViewApplicationDetail },
    { key: 'review', label: '审批', type: 'primary' as const, disabled: !canReviewApplication(row), onClick: openViewApplicationDetail },
  ]
}

function applicationMoreActions() {
  return [
    { key: 'edit', label: '编辑', type: 'primary' as const, onClick: openEditApplicationDialog },
    { key: 'delete', label: '删除', type: 'danger' as const, onClick: handleDeleteApplication },
  ]
}

async function refreshViewingApplication() {
  if (!viewingApplication.value?.id) {
    return
  }
  const response = await getRecruitmentApplicationDetail(viewingApplication.value.id)
  viewingApplication.value = response.data
  await loadViewingApplicationWorkflowTask(response.data.business_key)
}

async function handleViewingApplicationWorkflowAction(action: WorkflowActionOption) {
  if (!viewingApplicationWorkflowTask.value) {
    ElMessage.warning('当前未找到可执行的审批任务')
    return
  }
  const promptResult = await ElMessageBox.prompt(`请输入“${action.label}”审批意见，可留空。`, '审批处理', {
    inputValue: '',
    inputPlaceholder: '审批意见（可选）',
    confirmButtonText: action.label,
    cancelButtonText: '取消',
  }).catch(() => null)
  if (!promptResult) {
    return
  }
  applicationWorkflowActionSubmitting.value = true
  try {
    await executeWorkflowTaskAction(viewingApplicationWorkflowTask.value.id, {
      action: action.action,
      comment: promptResult.value?.trim() || undefined,
    })
    ElMessage.success(`${action.label}已完成`)
    await Promise.all([refreshAll(), refreshViewingApplication()])
  } catch (error) {
    const message = axios.isAxiosError(error) ? String(error.response?.data?.detail || error.message) : `${action.label}失败`
    ElMessage.error(message)
  } finally {
    applicationWorkflowActionSubmitting.value = false
  }
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

function triggerBrochureUpload() {
  brochureInputRef.value?.click()
}

async function handleBrochureUpload(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) {
    return
  }

  brochureUploading.value = true
  try {
    const response = await uploadRecruitmentBrochureImage(file)
    planForm.brochure_image_url = response.data.url
    ElMessage.success('招生简章图片已上传')
  } catch (error) {
    const message = axios.isAxiosError(error) ? String(error.response?.data?.detail || error.message) : '图片上传失败'
    ElMessage.error(message)
  } finally {
    input.value = ''
    brochureUploading.value = false
  }
}

async function submitApplicationForm() {
  syncApplicationLegacyFields()
  const formInstance = applicationFormRef.value
  if (!formInstance) {
    return
  }

  const isValid = await formInstance.validate().catch(() => false)
  if (!isValid) {
    return
  }

  const idType = trimText(applicationForm.id_type || applicationForm.profile?.id_type)
  const idNumber = trimText(applicationForm.id_number)
  const phoneValidationMessage = getPhoneValidationMessage(applicationForm.phone_number || '')
  if (phoneValidationMessage) {
    ElMessage.warning(phoneValidationMessage)
    return
  }
  const emailValidationMessage = getEmailValidationMessage(applicationForm.email || '')
  if (emailValidationMessage) {
    ElMessage.warning(emailValidationMessage)
    return
  }
  if (idNumber && (!idType || idType.includes('身份证'))) {
    const idValidationMessage = getChinaResidentIdValidationMessage(idNumber)
    if (idValidationMessage) {
      ElMessage.warning(idValidationMessage)
      return
    }
    applicationForm.id_number = normalizeChinaResidentIdNumber(idNumber)
  }
  if (trimText(applicationForm.phone_number)) {
    applicationForm.phone_number = normalizePhoneNumber(applicationForm.phone_number || '')
  }
  if (trimText(applicationForm.email)) {
    applicationForm.email = normalizeEmail(applicationForm.email || '')
  }

  applicationSubmitting.value = true
  try {
    const payload: RecruitApplicationUpsert = {
      ...applicationForm,
      source_channel: trimText(applicationForm.source_channel) || null,
      source_channel_other: trimText(applicationForm.source_channel_other) || null,
      preferences: (applicationForm.preferences || []).filter((item) => trimText(item.research_center_name)).map((item, index) => ({
        ...item,
        preference_order: index + 1,
        is_optional: index > 0,
      })),
      education_experiences: (applicationForm.education_experiences || []).filter((item) => trimText(item.school_name)).map((item, index) => ({
        ...item,
        sort_order: index + 1,
      })),
      practice_experiences: (applicationForm.practice_experiences || []).filter((item) => trimText(item.organization_name)),
      family_members: (applicationForm.family_members || []).filter((item) => trimText(item.member_name)),
      personal_statement: {
        ...(applicationForm.personal_statement || createApplicationPersonalStatement()),
        personal_statement_text: trimText(applicationForm.personal_statement?.personal_statement_text) || null,
        ai_problem_statement: trimText(applicationForm.personal_statement?.ai_problem_statement) || null,
        ai_industry_opinion: trimText(applicationForm.personal_statement?.ai_industry_opinion) || null,
        resume_attachment_url: trimText(applicationForm.personal_statement?.resume_attachment_url) || null,
      },
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

function handleDeleteApplication(row: RecruitApplicationRecord) {
  deletingApplication.value = row
  deleteApplicationDialogVisible.value = true
}

async function submitDeleteApplication() {
  if (!deletingApplication.value) {
    return
  }
  deleteApplicationSubmitting.value = true
  try {
    await deleteRecruitmentApplication(deletingApplication.value.id)
    ElMessage.success('报名申请已删除')
    deleteApplicationDialogVisible.value = false
    deletingApplication.value = null
    await refreshAll()
  } finally {
    deleteApplicationSubmitting.value = false
  }
}

function closeDeleteApplicationDialog() {
  deleteApplicationDialogVisible.value = false
  deletingApplication.value = null
}

function triggerTemplateImport() {
  if (!selectedPlanId.value) {
    ElMessage.warning('请先在左侧选择一个招生计划，再导入模板')
    return
  }
  importInputRef.value?.click()
}

async function handleTemplateImport(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) {
    return
  }
  if (!selectedPlanId.value) {
    ElMessage.warning('请先选择招生计划')
    input.value = ''
    return
  }

  importSubmitting.value = true
  try {
    const response = await importRecruitmentApplications(selectedPlanId.value, file)
    const result = response.data
    if (result.issues.length > 0) {
      const topIssues = result.issues.slice(0, 3).map((item) => `${item.row_number} 行${item.student_name ? ` ${item.student_name}` : ''}：${item.reason}`)
      ElMessage.warning(`成功导入 ${result.imported_count} 条，跳过 ${result.skipped_count} 条。${topIssues.join('；')}`)
    } else {
      ElMessage.success(`已导入 ${result.imported_count} 条报名申请`)
    }
    await refreshAll()
  } catch (error) {
    const message = axios.isAxiosError(error) ? String(error.response?.data?.detail || error.message) : '导入失败'
    ElMessage.error(message)
  } finally {
    input.value = ''
    importSubmitting.value = false
  }
}

async function handleTemplateExport() {
  exportSubmitting.value = true
  try {
    const response = await exportRecruitmentApplications({
      keyword: applicationFilters.keyword || undefined,
      status: applicationFilters.status || undefined,
      plan_id: selectedPlanId.value,
    })
    const blob = new Blob([response.data], {
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    const disposition = String(response.headers['content-disposition'] || '')
    const matched = disposition.match(/filename\*=UTF-8''([^;]+)/)
    link.href = url
    link.download = matched ? decodeURIComponent(matched[1]) : '资料审核名单.xlsx'
    document.body.append(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
    ElMessage.success('资料审核名单已导出')
  } catch (error) {
    const message = axios.isAxiosError(error) ? error.message : '导出失败'
    ElMessage.error(message)
  } finally {
    exportSubmitting.value = false
  }
}

async function handleTemplateDownload() {
  templateSubmitting.value = true
  try {
    const response = await downloadRecruitmentTemplate()
    const blob = new Blob([response.data], {
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    const disposition = String(response.headers['content-disposition'] || '')
    const matched = disposition.match(/filename\*=UTF-8''([^;]+)/)
    link.href = url
    link.download = matched ? decodeURIComponent(matched[1]) : '资料审核名单模板.xlsx'
    document.body.append(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
    ElMessage.success('空白模板已下载')
  } catch (error) {
    const message = axios.isAxiosError(error) ? error.message : '模板下载失败'
    ElMessage.error(message)
  } finally {
    templateSubmitting.value = false
  }
}

async function handlePlanSelection(row: RecruitPlanRecord) {
  selectedPlanId.value = row.id
  applicationPager.reset()
  await loadApplications()
}

async function handleFilterSearch() {
  applicationPager.reset()
  await loadApplications()
}

async function handleFilterReset() {
  applicationFilters.keyword = ''
  applicationFilters.status = ''
  applicationPager.reset()
  await loadApplications()
}

async function handlePlanSearch() {
  planPager.reset()
  await loadPlans()
}

async function handlePlanReset() {
  Object.assign(planFilters, { keyword: '', semester: '' })
  planPager.reset()
  await loadPlans()
}

async function handlePlanPageChange(page: number) {
  planPager.handleCurrentChange(page)
  await loadPlans()
}

async function handlePlanPageSizeChange(size: number) {
  planPager.handleSizeChange(size)
  await loadPlans()
}

async function handleApplicationPageChange(page: number) {
  applicationPager.handleCurrentChange(page)
  await loadApplications()
}

async function handleApplicationPageSizeChange(size: number) {
  applicationPager.handleSizeChange(size)
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
          <h2>计划维护概览</h2>
        </div>
        <div class="header-actions">
          <span class="summary-text" v-if="selectedPlan">当前计划：{{ selectedPlan.plan_name }}</span>
          <el-button v-if="selectedPlan" @click="openEditPlanDialog(selectedPlan)">编辑当前计划</el-button>
          <el-button v-if="selectedPlan" type="danger" plain :loading="deletingPlan" @click="handleDeleteSelectedPlan">删除当前计划</el-button>
          <el-button type="primary" round @click="openCreatePlanDialog">新增招生计划</el-button>
        </div>
      </div>
      <div class="plan-overview-grid">
        <article v-for="plan in workbench.plans.slice(0, 3)" :key="plan.plan_name" class="plan-overview-card">
          <strong>{{ plan.plan_name }}</strong>
          <span>{{ plan.academic_term }}</span>
          <p>{{ plan.plan_description || '暂未填写计划描述' }}</p>
          <small>当前申请 {{ plan.application_count }} 份</small>
        </article>
      </div>
    </section>

    <section class="two-column-grid">
      <article class="section-card">
        <div class="section-card__header compact">
          <div>
            <p class="section-tag">计划矩阵</p>
            <h2>进行中的招生计划</h2>
          </div>
        </div>
        <el-form class="filter-form" :inline="true">
          <el-form-item>
            <el-input v-model="planFilters.keyword" placeholder="计划名称 / 学年学期 / 计划描述" clearable @keyup.enter="handlePlanSearch" />
          </el-form-item>
          <el-form-item>
            <el-select v-model="planFilters.semester" placeholder="全部学期" clearable style="width: 140px">
              <el-option v-for="item in options.semester_options" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handlePlanSearch">查询</el-button>
            <el-button @click="handlePlanReset">重置</el-button>
          </el-form-item>
        </el-form>
        <div class="table-scroll">
          <el-table :data="plans" stripe border v-loading="plansLoading" @row-click="handlePlanSelection">
            <el-table-column prop="plan_name" label="计划名称" min-width="188" show-overflow-tooltip />
            <el-table-column prop="academic_term" label="学年学期" width="110" show-overflow-tooltip />
            <el-table-column label="简章图片" width="110">
              <template #default="scope">
                <img v-if="scope.row.brochure_image_url" :src="scope.row.brochure_image_url" alt="简章图片" class="plan-table-brochure" />
                <span v-else>未上传</span>
              </template>
            </el-table-column>
            <el-table-column prop="plan_description" label="计划描述" min-width="280" show-overflow-tooltip />
            <el-table-column prop="application_count" label="申请数" width="82" />
          </el-table>
        </div>
        <div class="pagination-bar">
          <el-pagination
            :current-page="planPager.pagination.currentPage"
            :page-size="planPager.pagination.pageSize"
            :page-sizes="[10, 20, 50, 100]"
            :total="planPager.pagination.total"
            layout="total, sizes, prev, pager, next"
            @current-change="handlePlanPageChange"
            @size-change="handlePlanPageSizeChange"
          />
        </div>
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
          <el-button :loading="templateSubmitting" @click="handleTemplateDownload">下载空白模板</el-button>
          <el-button :loading="importSubmitting" @click="triggerTemplateImport">模板导入</el-button>
          <el-button :loading="exportSubmitting" @click="handleTemplateExport">导出名单</el-button>
          <el-button type="primary" round @click="openCreateApplicationDialog">新增报名申请</el-button>
        </div>
      </div>

      <input ref="importInputRef" type="file" accept=".xlsx" class="hidden-input" @change="handleTemplateImport" />

      <el-form class="filter-form" :inline="true">
        <el-form-item label="关键字">
            <el-input v-model="applicationFilters.keyword" placeholder="业务编号 / 姓名 / 学校 / 方向" clearable />
        </el-form-item>
        <el-form-item label="申请状态">
          <el-select v-model="applicationFilters.status" placeholder="全部状态" clearable style="width: 180px">
            <el-option v-for="item in options.application_status_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleFilterSearch">查询</el-button>
          <el-button @click="handleFilterReset">重置</el-button>
        </el-form-item>
      </el-form>

      <div class="table-scroll">
        <el-table :data="applications" stripe border v-loading="applicationsLoading">
          <el-table-column prop="business_key" label="业务编号" min-width="150" show-overflow-tooltip />
          <el-table-column prop="student_name" label="姓名" width="92" show-overflow-tooltip />
          <el-table-column prop="first_choice" label="第一志愿" min-width="106" show-overflow-tooltip />
          <el-table-column prop="intended_advisor_name" label="意向导师" width="92" show-overflow-tooltip />
          <el-table-column prop="phone_number" label="电话" width="120" show-overflow-tooltip />
          <el-table-column prop="graduation_school" label="本科院校" min-width="124" show-overflow-tooltip />
          <el-table-column prop="intended_field" label="研究方向" min-width="108" show-overflow-tooltip />
          <el-table-column label="材料状态" width="100">
            <template #default="scope">
              <el-tag :type="materialTagType(scope.row.material_status)">{{ scope.row.material_status }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="申请状态" width="108">
            <template #default="scope">
              <el-tag :type="applicationTagType(scope.row.application_status)">{{ scope.row.application_status }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="reviewer_name" label="审核人" width="92" show-overflow-tooltip />
          <el-table-column prop="final_score" label="得分" width="72" />
          <el-table-column label="操作" width="170" align="left">
            <template #default="scope">
              <TableRowActions :row="scope.row" :main-actions="applicationMainActions(scope.row)" :more-actions="applicationMoreActions()" />
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div class="pagination-bar">
        <el-pagination
          :current-page="applicationPager.pagination.currentPage"
          :page-size="applicationPager.pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="applicationPager.pagination.total"
          layout="total, sizes, prev, pager, next"
          @current-change="handleApplicationPageChange"
          @size-change="handleApplicationPageSizeChange"
        />
      </div>
    </article>

    <el-dialog v-model="planDialogVisible" :title="planMode === 'create' ? '新增招生计划' : '编辑招生计划'" width="680px" destroy-on-close>
      <el-form ref="planFormRef" :model="planForm" :rules="planRules" label-width="96px">
        <input ref="brochureInputRef" type="file" accept="image/*" class="hidden-input" @change="handleBrochureUpload" />
        <div class="dialog-grid dialog-grid--single">
          <el-form-item label="计划名称" prop="plan_name">
            <el-input v-model="planForm.plan_name" placeholder="请输入招生计划名称" />
          </el-form-item>
          <el-form-item label="学年" prop="academic_year">
            <el-input v-model="planForm.academic_year" placeholder="例如 2026" />
          </el-form-item>
          <el-form-item label="学期" prop="semester">
            <el-select v-model="planForm.semester" placeholder="请选择学期">
              <el-option v-for="item in options.semester_options" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
          <el-form-item label="计划描述" prop="plan_description">
            <el-input v-model="planForm.plan_description" type="textarea" :rows="4" placeholder="请输入招生计划描述" />
          </el-form-item>
          <el-form-item label="简章图片">
            <div class="brochure-upload-field">
              <div class="brochure-upload-actions">
                <el-input v-model="planForm.brochure_image_url" placeholder="上传后自动回填图片地址" readonly />
                <el-button :loading="brochureUploading" @click="triggerBrochureUpload">上传图片</el-button>
              </div>
              <div v-if="planForm.brochure_image_url" class="brochure-upload-preview">
                <img :src="planForm.brochure_image_url" alt="招生简章预览" />
              </div>
            </div>
          </el-form-item>
        </div>
      </el-form>
      <template #footer>
        <el-button @click="planDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="planSubmitting" @click="submitPlanForm">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="applicationDialogVisible" :title="applicationMode === 'create' ? '新增报名申请' : '编辑报名申请'" width="1280px" destroy-on-close>
      <el-form ref="applicationFormRef" :model="applicationForm" :rules="applicationRules" label-width="96px">
        <section class="dialog-section">
          <h3 class="dialog-section__title">基础信息</h3>
          <div class="dialog-grid dialog-grid--three">
            <el-form-item label="招生计划" prop="plan_id">
              <el-select v-model="applicationForm.plan_id" placeholder="请选择计划">
                <el-option v-for="item in planReferenceList" :key="item.id" :label="item.plan_name" :value="item.id" />
              </el-select>
            </el-form-item>
            <el-form-item label="业务编号">
              <el-input :model-value="applicationForm.business_key || '保存后自动生成'" disabled />
            </el-form-item>
            <el-form-item label="轮次">
              <el-input v-model="applicationForm.review_round" placeholder="如 2026 秋季第一轮" />
            </el-form-item>
            <el-form-item label="姓名" prop="student_name">
              <el-input v-model="applicationForm.student_name" placeholder="请输入姓名" />
            </el-form-item>
            <el-form-item label="性别">
              <el-select v-model="applicationForm.profile!.gender" placeholder="请选择性别">
                <el-option v-for="item in genderOptions" :key="item" :label="item" :value="item" />
              </el-select>
            </el-form-item>
            <el-form-item label="政治面貌">
              <el-input v-model="applicationForm.profile!.political_status" placeholder="请输入政治面貌" />
            </el-form-item>
            <el-form-item label="电话">
              <el-input v-model="applicationForm.phone_number" placeholder="请输入联系电话" />
            </el-form-item>
            <el-form-item label="邮箱">
              <el-input v-model="applicationForm.email" placeholder="请输入邮箱" />
            </el-form-item>
            <el-form-item label="联系地址" class="grid-span-3">
              <el-input v-model="applicationForm.profile!.mailing_address" placeholder="请输入联系地址" />
            </el-form-item>
            <el-form-item label="籍贯">
              <el-input v-model="applicationForm.profile!.native_place" placeholder="请输入籍贯" />
            </el-form-item>
            <el-form-item label="婚姻状况">
              <el-select v-model="applicationForm.profile!.marital_status" placeholder="请选择婚姻状况">
                <el-option v-for="item in maritalStatusOptions" :key="item" :label="item" :value="item" />
              </el-select>
            </el-form-item>
            <el-form-item label="宗教信仰">
              <el-input v-model="applicationForm.profile!.religious_belief" placeholder="请输入宗教信仰" />
            </el-form-item>
            <el-form-item label="证件类型">
              <el-input v-model="applicationForm.profile!.id_type" placeholder="请输入证件类型" />
            </el-form-item>
            <el-form-item label="证件号码" class="grid-span-2">
              <el-input v-model="applicationForm.id_number" placeholder="请输入证件号码" />
            </el-form-item>
          </div>
        </section>

        <section class="dialog-section">
          <h3 class="dialog-section__title">报名信息</h3>
          <div class="dialog-grid dialog-grid--three">
            <el-form-item label="了解渠道">
              <el-select v-model="applicationForm.source_channel" placeholder="请选择了解渠道">
                <el-option v-for="item in sourceChannelOptions" :key="item" :label="item" :value="item" />
              </el-select>
            </el-form-item>
            <el-form-item label="其他渠道" class="grid-span-2">
              <el-input v-model="applicationForm.source_channel_other" placeholder="选择“其他”时填写补充说明" />
            </el-form-item>
            <el-form-item label="是否接受调剂">
              <el-input v-model="applicationForm.accept_adjustment" placeholder="请输入是否接受调剂" />
            </el-form-item>
            <el-form-item label="申请时间" class="grid-span-2">
              <el-input v-model="applicationForm.applied_at" placeholder="请输入申请时间" />
            </el-form-item>
          </div>
          <div class="record-stack">
            <section v-for="(item, index) in applicationForm.preferences" :key="`preference-${index}`" class="record-card">
              <div class="record-card__header">
                <strong>{{ index === 0 ? '第一志愿' : '第二志愿' }}</strong>
                <el-button v-if="index > 0" link type="danger" @click="removePreference(index)">删除</el-button>
              </div>
              <div class="dialog-grid dialog-grid--three">
                <el-form-item :label="index === 0 ? '志愿研究中心' : '调剂研究中心'" class="grid-span-2">
                  <el-input v-model="item.research_center_name" placeholder="请输入研究中心/研究方向" />
                </el-form-item>
                <el-form-item label="意向导师">
                  <el-select v-model="item.advisor_name" filterable allow-create default-first-option placeholder="请选择或录入导师">
                    <el-option v-for="option in options.reviewer_options" :key="option.value" :label="option.label" :value="option.value" />
                  </el-select>
                </el-form-item>
              </div>
            </section>
          </div>
          <div class="record-actions">
            <el-button plain :disabled="(applicationForm.preferences?.length || 0) >= 2" @click="addPreference">新增第二志愿</el-button>
          </div>
        </section>

        <section class="dialog-section">
          <h3 class="dialog-section__title">教育经历</h3>
          <div class="record-stack">
            <section v-for="(item, index) in applicationForm.education_experiences" :key="`education-${index}`" class="record-card">
              <div class="record-card__header">
                <strong>教育经历 {{ index + 1 }}</strong>
                <el-button v-if="applicationForm.education_experiences!.length > 1" link type="danger" @click="removeEducation(index)">删除</el-button>
              </div>
              <div class="dialog-grid dialog-grid--three">
                <el-form-item label="教育阶段">
                  <el-select v-model="item.education_stage" placeholder="请选择教育阶段">
                    <el-option v-for="stage in educationStageOptions" :key="stage" :label="stage" :value="stage" />
                  </el-select>
                </el-form-item>
                <el-form-item label="开始时间">
                  <el-input v-model="item.start_month" placeholder="如 2021-09" />
                </el-form-item>
                <el-form-item label="结束时间">
                  <el-input v-model="item.end_month" placeholder="如 2024-06" />
                </el-form-item>
                <el-form-item label="院校" class="grid-span-2">
                  <el-input v-model="item.school_name" placeholder="请输入院校名称" />
                </el-form-item>
                <el-form-item label="专业">
                  <el-input v-model="item.major_name" placeholder="请输入专业名称" />
                </el-form-item>
                <el-form-item label="平均分">
                  <el-input v-model="item.average_score" placeholder="请输入平均分" />
                </el-form-item>
                <el-form-item label="绩点">
                  <el-input v-model="item.gpa" placeholder="请输入绩点" />
                </el-form-item>
                <el-form-item label="排名">
                  <el-input v-model="item.ranking" placeholder="请输入排名" />
                </el-form-item>
              </div>
            </section>
          </div>
          <div class="record-actions">
            <el-button plain @click="addEducation">新增教育经历</el-button>
          </div>
        </section>

        <section class="dialog-section">
          <h3 class="dialog-section__title">实践经历</h3>
          <div v-if="!(applicationForm.practice_experiences && applicationForm.practice_experiences.length)" class="empty-inline">当前未填写实践经历，可留空。</div>
          <div class="record-stack">
            <section v-for="(item, index) in applicationForm.practice_experiences" :key="`practice-${index}`" class="record-card">
              <div class="record-card__header">
                <strong>实践经历 {{ index + 1 }}</strong>
                <el-button link type="danger" @click="removePractice(index)">删除</el-button>
              </div>
              <div class="dialog-grid dialog-grid--three">
                <el-form-item label="开始时间">
                  <el-input v-model="item.start_month" placeholder="如 2023-07" />
                </el-form-item>
                <el-form-item label="结束时间">
                  <el-input v-model="item.end_month" placeholder="如 2023-12" />
                </el-form-item>
                <el-form-item label="单位名称">
                  <el-input v-model="item.organization_name" placeholder="请输入单位名称" />
                </el-form-item>
                <el-form-item label="岗位名称">
                  <el-input v-model="item.position_name" placeholder="请输入岗位名称" />
                </el-form-item>
                <el-form-item label="证明人">
                  <el-input v-model="item.verifier_name" placeholder="请输入证明人" />
                </el-form-item>
                <el-form-item label="证明人电话">
                  <el-input v-model="item.verifier_phone" placeholder="请输入证明人电话" />
                </el-form-item>
                <el-form-item label="职责说明" class="grid-span-3">
                  <el-input v-model="item.responsibility_text" type="textarea" :rows="3" placeholder="请输入实践内容、职责与成果" />
                </el-form-item>
              </div>
            </section>
          </div>
          <div class="record-actions">
            <el-button plain @click="addPractice">新增实践经历</el-button>
          </div>
        </section>

        <section class="dialog-section">
          <h3 class="dialog-section__title">家庭情况</h3>
          <div class="dialog-grid dialog-grid--three">
            <section v-for="(item, index) in applicationForm.family_members" :key="`family-${index}`" class="record-card grid-span-3">
              <div class="record-card__header">
                <strong>家庭成员 {{ index + 1 }}</strong>
                <el-button v-if="applicationForm.family_members!.length > 2" link type="danger" @click="removeFamilyMember(index)">删除</el-button>
              </div>
              <div class="dialog-grid dialog-grid--three">
                <el-form-item label="姓名">
                  <el-input v-model="item.member_name" placeholder="请输入姓名" />
                </el-form-item>
                <el-form-item label="关系">
                  <el-select v-model="item.relation_type" placeholder="请选择关系">
                    <el-option v-for="relation in familyRelationOptions" :key="relation" :label="relation" :value="relation" />
                  </el-select>
                </el-form-item>
                <el-form-item label="联系电话">
                  <el-input v-model="item.contact_phone" placeholder="请输入联系电话" />
                </el-form-item>
                <el-form-item label="工作单位">
                  <el-input v-model="item.employer_name" placeholder="请输入工作单位" />
                </el-form-item>
                <el-form-item label="职务" class="grid-span-2">
                  <el-input v-model="item.job_title" placeholder="请输入职务" />
                </el-form-item>
              </div>
            </section>
          </div>
          <div class="record-actions">
            <el-button plain @click="addFamilyMember">新增家庭成员</el-button>
          </div>
        </section>

        <section class="dialog-section">
          <h3 class="dialog-section__title">个人陈述与补充说明</h3>
          <div class="dialog-grid dialog-grid--single">
            <el-form-item label="本人自我评价">
              <el-input v-model="applicationForm.self_evaluation" type="textarea" :rows="3" placeholder="请输入本人自我评价" />
            </el-form-item>
            <el-form-item label="个人陈述">
              <el-input v-model="applicationForm.personal_statement!.personal_statement_text" type="textarea" :rows="4" placeholder="请输入申请动机、研究基础与职业规划" />
            </el-form-item>
            <el-form-item label="AI 关键问题思考">
              <el-input v-model="applicationForm.personal_statement!.ai_problem_statement" type="textarea" :rows="4" placeholder="请输入你关注的 AI 关键问题" />
            </el-form-item>
            <el-form-item label="AI 行业不同观点">
              <el-input v-model="applicationForm.personal_statement!.ai_industry_opinion" type="textarea" :rows="4" placeholder="请输入你对行业议题的不同观点或补充说明" />
            </el-form-item>
            <el-form-item label="个人陈述附件">
              <el-input v-model="applicationForm.personal_statement!.resume_attachment_url" placeholder="请输入简历/个人陈述附件地址" />
            </el-form-item>
            <el-form-item label="研究现状与局限">
              <el-input v-model="applicationForm.research_status_analysis" type="textarea" :rows="3" placeholder="请输入科研进展与局限分析" />
            </el-form-item>
            <el-form-item label="问题解决后的影响">
              <el-input v-model="applicationForm.research_impact" type="textarea" :rows="3" placeholder="请输入对技术与行业的影响判断" />
            </el-form-item>
            <el-form-item label="AI 对社会影响判断">
              <el-input v-model="applicationForm.ai_society_impact" type="textarea" :rows="3" placeholder="请输入对 AI 影响场景的判断" />
            </el-form-item>
            <el-form-item label="学生活动经历">
              <el-input v-model="applicationForm.student_activity_experience" type="textarea" :rows="3" placeholder="请输入学生活动、论文、获奖等补充说明" />
            </el-form-item>
            <el-form-item label="补充简介">
              <el-input v-model="applicationForm.supplementary_profile" type="textarea" :rows="3" placeholder="请输入额外补充信息" />
            </el-form-item>
          </div>
        </section>

        <section class="dialog-section">
          <h3 class="dialog-section__title">审核与管理信息</h3>
          <div class="dialog-grid dialog-grid--three">
            <el-form-item label="资料审核" prop="material_status">
              <el-select v-model="applicationForm.material_status" placeholder="请选择资料审核状态">
                <el-option v-for="item in options.material_status_options" :key="item.value" :label="item.label" :value="item.value" />
              </el-select>
            </el-form-item>
            <el-form-item label="申请状态" prop="application_status">
              <el-select v-model="applicationForm.application_status" placeholder="请选择申请状态">
                <el-option v-for="item in options.application_status_options" :key="item.value" :label="item.label" :value="item.value" />
              </el-select>
            </el-form-item>
            <el-form-item label="审核人">
              <el-select v-model="applicationForm.reviewer_name" filterable allow-create default-first-option placeholder="请选择审核人">
                <el-option v-for="item in options.reviewer_options" :key="item.value" :label="item.label" :value="item.value" />
              </el-select>
            </el-form-item>
            <el-form-item label="材料得分">
              <el-input-number v-model="applicationForm.final_score" :min="0" :max="100" :precision="1" controls-position="right" />
            </el-form-item>
            <el-form-item label="材料清单附件" class="grid-span-2">
              <el-input v-model="applicationForm.material_list_attachment" placeholder="请输入材料清单附件地址" />
            </el-form-item>
          </div>
        </section>
      </el-form>
      <template #footer>
        <el-button @click="applicationDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="applicationSubmitting" @click="submitApplicationForm">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="deleteApplicationDialogVisible" title="删除确认" width="560px" destroy-on-close @closed="closeDeleteApplicationDialog">
      <div v-if="deletingApplication" class="dialog-form delete-application-dialog">
        <p class="delete-application-dialog__lead">确定删除这条报名申请吗？删除后不可恢复。</p>
        <div class="delete-application-dialog__summary">
          <div>
            <span class="delete-application-dialog__label">姓名</span>
            <strong>{{ deletingApplication.student_name }}</strong>
          </div>
          <div>
            <span class="delete-application-dialog__label">业务编号</span>
            <strong>{{ deletingApplication.business_key || '未生成' }}</strong>
          </div>
          <div>
            <span class="delete-application-dialog__label">第一志愿</span>
            <strong>{{ deletingApplication.first_choice || '未填写' }}</strong>
          </div>
          <div>
            <span class="delete-application-dialog__label">申请状态</span>
            <strong>{{ deletingApplication.application_status || '未填写' }}</strong>
          </div>
        </div>
      </div>
      <template #footer>
        <el-button @click="closeDeleteApplicationDialog">取消</el-button>
        <el-button type="danger" :loading="deleteApplicationSubmitting" @click="submitDeleteApplication">确认删除</el-button>
      </template>
    </el-dialog>

    <RecruitmentApplicationReviewDrawer
      v-model="applicationDetailVisible"
      :application="viewingApplication"
      :workflow-task="viewingApplicationWorkflowTask"
      :workflow-task-loading="applicationWorkflowTaskLoading"
      :action-loading="applicationWorkflowActionSubmitting"
      @execute-action="handleViewingApplicationWorkflowAction"
    />
  </section>
</template>

<style scoped>
.content-stack,
.stats-grid,
.two-column-grid {
  display: grid;
  gap: 14px;
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
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 18px 44px rgba(14, 40, 88, 0.07);
}

.section-card {
  padding: 16px;
  min-width: 0;
}

.stat-card {
  padding: 14px 16px;
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
  margin-top: 6px;
  color: #12284d;
  font-size: 24px;
}

.section-card__header {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
  margin-bottom: 12px;
}

.section-card__header.compact {
  margin-bottom: 10px;
}

.section-tag,
.section-card h2,
.task-list p,
.summary-text {
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

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.table-scroll {
  width: 100%;
  min-width: 0;
  overflow-x: auto;
}

.table-scroll :deep(.el-table) {
  width: 100%;
  min-width: 0;
}

.summary-text {
  color: #60718f;
  font-size: 12px;
}

.filter-form {
  margin-bottom: 12px;
}

.delete-application-dialog {
  display: grid;
  gap: 16px;
}

.delete-application-dialog__lead {
  margin: 0;
  color: #475569;
  line-height: 1.7;
}

.delete-application-dialog__summary {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  padding: 16px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  background: #f8fafc;
}

.delete-application-dialog__label {
  display: block;
  margin-bottom: 6px;
  color: #909399;
  font-size: 12px;
}

.delete-application-dialog__summary strong {
  color: #303133;
  font-size: 14px;
  word-break: break-word;
}

.task-list {
  display: grid;
  gap: 8px;
  list-style: none;
  padding: 0;
  margin: 0;
}

.task-list li {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
  padding: 10px 12px;
  border-radius: 14px;
  background: linear-gradient(135deg, rgba(245, 248, 255, 0.98), rgba(252, 244, 221, 0.92));
}

.task-list strong {
  color: #12315e;
  font-size: 14px;
}

.task-list p {
  margin-top: 4px;
  color: #60718f;
  font-size: 12px;
}

.plan-overview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 14px;
}

.plan-overview-card {
  display: grid;
  gap: 8px;
  padding: 16px 18px;
  border-radius: 16px;
  border: 1px solid rgba(18, 50, 95, 0.08);
  background: linear-gradient(135deg, rgba(245, 248, 255, 0.96), rgba(255, 249, 235, 0.9));
}

.plan-overview-card strong {
  color: #12315e;
}

.plan-overview-card span,
.plan-overview-card small {
  color: #60718f;
  font-size: 12px;
}

.plan-overview-card p {
  margin: 0;
  color: #334e75;
  font-size: 13px;
  line-height: 1.6;
}

.plan-table-brochure {
  display: block;
  width: 64px;
  height: 40px;
  object-fit: cover;
  border-radius: 8px;
}

.dialog-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 4px 18px;
}

.dialog-grid--three {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.dialog-grid--single {
  grid-template-columns: 1fr;
}

.brochure-upload-field {
  display: grid;
  gap: 12px;
  width: 100%;
}

.brochure-upload-actions {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 12px;
  align-items: center;
}

.brochure-upload-preview {
  width: 100%;
  max-width: 280px;
  overflow: hidden;
  border-radius: 16px;
  border: 1px solid rgba(18, 50, 95, 0.12);
  background: rgba(246, 249, 255, 0.72);
}

.brochure-upload-preview img {
  display: block;
  width: 100%;
  max-height: 220px;
  object-fit: cover;
}

.grid-span-2 {
  grid-column: span 2;
}

.grid-span-3 {
  grid-column: span 3;
}

.dialog-section,
.detail-section {
  margin-bottom: 18px;
}

.record-stack {
  display: grid;
  gap: 12px;
}

.record-card {
  padding: 12px;
  border: 1px solid rgba(18, 50, 95, 0.08);
  border-radius: 16px;
  background: rgba(246, 249, 255, 0.7);
}

.record-card__header,
.record-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.record-card__header {
  margin-bottom: 10px;
}

.record-card__header strong {
  color: #12315e;
  font-size: 13px;
}

.record-actions {
  margin-top: 10px;
}

.empty-inline {
  padding: 10px 12px;
  border-radius: 14px;
  color: #60718f;
  background: rgba(246, 249, 255, 0.72);
}

.dialog-section__title {
  margin: 0 0 10px;
  color: #18355d;
  font-size: 14px;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px 14px;
}

.detail-record-stack {
  display: grid;
  gap: 12px;
}

.detail-record-card {
  padding: 12px;
  border: 1px solid rgba(18, 50, 95, 0.08);
  border-radius: 16px;
  background: rgba(246, 249, 255, 0.7);
}

.detail-record-card__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-bottom: 10px;
}

.detail-record-card__header strong {
  color: #12315e;
  font-size: 13px;
}

.detail-item {
  display: grid;
  gap: 4px;
  padding: 10px 12px;
  border: 1px solid rgba(18, 50, 95, 0.08);
  border-radius: 14px;
  background: rgba(246, 249, 255, 0.72);
}

.detail-item__label {
  color: #6e819d;
  font-size: 12px;
}

.detail-item__value {
  color: #12315e;
  font-size: 13px;
  line-height: 1.5;
  word-break: break-word;
}

.detail-item--full {
  grid-column: 1 / -1;
}

.detail-attachment-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.detail-attachment-actions--stacked {
  margin-top: 10px;
}

.detail-attachment-link,
.detail-attachment-download {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 36px;
  padding: 0 12px;
  border-radius: 10px;
  border: 1px solid rgba(28, 78, 146, 0.12);
  background: rgba(240, 246, 255, 0.96);
  color: #1c4e92;
  text-decoration: none;
}

.detail-attachment-download {
  border: none;
  cursor: pointer;
}

.detail-attachment-link span,
.detail-attachment-download span {
  line-height: 1.4;
  word-break: break-word;
}

.detail-text-list {
  display: grid;
  gap: 10px;
}

.detail-text-card {
  padding: 12px 14px;
  border: 1px solid rgba(18, 50, 95, 0.08);
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.92);
}

.detail-text-card h4,
.detail-text-card p {
  margin: 0;
}

.detail-text-card h4 {
  color: #18355d;
  font-size: 13px;
}

.detail-text-card p {
  margin-top: 8px;
  color: #4e6381;
  line-height: 1.7;
  white-space: pre-wrap;
}

.hidden-input {
  display: none;
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

  .brochure-upload-actions {
    grid-template-columns: 1fr;
  }

  .detail-grid {
    grid-template-columns: 1fr;
  }

  .grid-span-2,
  .grid-span-3 {
    grid-column: auto;
  }
}
</style>
