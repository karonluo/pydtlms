<script setup lang="ts">
import axios from 'axios'
import { computed, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { useRoute } from 'vue-router'
import TableRowActions from '../../components/table/TableRowActions.vue'
import RecruitmentPortalApplicationDrawer from '../../components/recruitment/RecruitmentPortalApplicationDrawer.vue'
import { buildDictColorMap, resolveDictTagType, type DictColorMap } from '../../utils/dictTag'
import { getEmailValidationMessage, getPhoneValidationMessage, normalizeEmail, normalizePhoneNumber } from '../../utils/contactValidation'
import { getChinaResidentIdValidationMessage, normalizeChinaResidentIdNumber } from '../../utils/chinaResidentId'
import { useServerPagination } from '../../composables/useServerPagination'
import { useAuthStore } from '../../stores/auth'
import {
  confirmInitialScreening,
  createRecruitmentApplication,
  createRecruitmentPlan,
  deleteRecruitmentPlan,
  deleteRecruitmentApplication,
  downloadRecruitmentTemplate,
  exportRecruitmentApplications,
  getRecruitmentApplicationDetail,
  getRecruitmentPortalApplicationDetail,
  getRecruitmentOptions,
  getRecruitmentStats,
  getRecruitmentWorkbench,
  importRecruitmentApplications,
  listInitialScreeningConfirmationApplications,
  listRecruitmentApplications,
  listRecruitmentPlans,
  rescoreAdvisorScreeningSubmittedApplication,
  submitAdvisorScreeningBatch,
  uploadRecruitmentBrochureImage,
  updateRecruitmentApplication,
  updateRecruitmentPlan,
  type AdvisorScreeningBatchSubmitRequest,
  type InitialScreeningConfirmationRequest,
  type RecruitApplicationRecord,
  type RecruitPortalApplicationDetail,
  type RecruitApplicationUpsert,
  type RecruitmentOptions,
  type RecruitPlanRecord,
  type RecruitPlanUpsert,
  type RecruitStats,
  type RecruitWorkbench,
} from '../../api/recruitment'
import { executeWorkflowTaskAction, listWorkflowTasks, type WorkflowActionOption, type WorkflowTaskRecord } from '../../api/workflow'
import {
  listAdvisorScreeningPendingApplications,
  listAdvisorScreeningSubmittedApplications,
  type AdvisorScreeningSubmittedApplicationRecord,
} from '../../api/recruitment'

const sourceChannelOptions = ['导师推荐', '实验室官网', '高校宣讲', '朋友同学推荐', '其他']
const genderOptions = ['男', '女']
const maritalStatusOptions = ['未婚', '已婚']
const educationStageOptions = ['硕士', '硕士在读', '本科', '本科在读', '高中']
const familyRelationOptions = ['父亲', '母亲', '兄', '弟', '姐', '妹', '其他']
const route = useRoute()
const authStore = useAuthStore()
const viewportWidth = ref(typeof window === 'undefined' ? 1440 : window.innerWidth)

const updateViewportWidth = () => {
  viewportWidth.value = window.innerWidth
}

const ADVISOR_SCREENING_DEFAULT_STATUSES = ['待导师初筛', '待导师初筛-第一志愿', '待导师初筛-第二志愿', '待初筛确认', '报名终止']
const INITIAL_SCREENING_DEFAULT_STATUSES = ['待初筛确认']
const PLAN_SECTION_DEFAULT_STATUSES = ['报名已提交', '待背景评估', '待导师初筛-第一志愿', '待导师初筛-第二志愿', '待初筛确认', '入营面试', '报名终止']
const ADVISOR_SCREENING_PASS_SCORE = 80
const ADVISOR_SCREENING_QUERY_STATUS = 'advisor_screening_pending'
const RECRUITMENT_STATUS_QUERY_MAP: Record<string, string> = {
  报名已提交: 'submitted',
  待审核: 'submitted',
  驳回重填: 'returned',
  不录取: 'rejected',
  报名终止: 'terminated',
  资格审核通过: 'qualified',
  待背景评估: 'background_review',
  待导师初筛: 'initial_screening',
  '待导师初筛-第一志愿': 'initial_screening_first',
  '待导师初筛-第二志愿': 'initial_screening_second',
  待初筛确认: 'initial_screening_confirmation',
  入营面试: 'camp_interview',
  结果公布: 'result_published',
  材料评分中: 'scoring',
  面试完成: 'interviewed',
  预录取: 'pre_admitted',
  同意录取: 'admitted',
}

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

type InitialScreeningConfirmationApplicationRow = RecruitApplicationRecord & {
  application_id?: number
  student_id?: number
  full_name?: string
}

function getApplicationRowId(row: RecruitApplicationRecord) {
  return row.id || (row as InitialScreeningConfirmationApplicationRow).application_id || 0
}

function normalizeInitialScreeningApplicationRows(rows: RecruitApplicationRecord[]) {
  return rows.map((item) => {
    const row = item as InitialScreeningConfirmationApplicationRow
    return {
      ...item,
      id: item.id || row.application_id || 0,
      portal_student_id: item.portal_student_id ?? row.student_id ?? null,
      business_key: item.business_key || row.candidate_no || '',
      student_name: item.student_name || row.full_name || '',
    }
  }) as RecruitApplicationRecord[]
}

function normalizeRecruitmentStatusForQuery(status: string | undefined | null) {
  return String(status || '')
    .split(',')
    .map((item) => trimText(item))
    .filter(Boolean)
    .map((item) => RECRUITMENT_STATUS_QUERY_MAP[item] || item)
    .join(',')
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
  advisor_options: [],
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
const viewingApplication = ref<RecruitPortalApplicationDetail | null>(null)
const viewingApplicationWorkflowTask = ref<WorkflowTaskRecord | null>(null)
const applicationStatusColors = ref<DictColorMap>({})
const materialStatusColors = ref<DictColorMap>({})
const applicationWorkflowTaskLoading = ref(false)
const applicationWorkflowActionSubmitting = ref(false)
const applicationWorkflowCommentDialogVisible = ref(false)
const initialScreeningBatchConfirmDialogVisible = ref(false)
const pendingViewingApplicationWorkflowAction = ref<WorkflowActionOption | null>(null)
const applicationWorkflowComment = ref('')
const selectedAdvisorScreeningIds = ref<number[]>([])
const selectedInitialScreeningIds = ref<number[]>([])
const advisorScreeningBatchConfirmDialogVisible = ref(false)
const advisorScreeningDrafts = reactive<Record<number, { advisor_score?: number }>>({})
const initialScreeningDrafts = reactive<Record<number, { result: 'passed' | 'rejected'; comment: string }>>({})

const planFormRef = ref<FormInstance>()
const applicationFormRef = ref<FormInstance>()
const importInputRef = ref<HTMLInputElement | null>(null)
const brochureInputRef = ref<HTMLInputElement | null>(null)

const applicationFilters = reactive({
  keyword: '',
  status: '',
  advisor_names: [] as string[],
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

const currentSection = computed(() => String(route.meta.section || 'plans'))
const isPlanSection = computed(() => currentSection.value === 'plans')
const isAdvisorScreeningSection = computed(() => currentSection.value === 'advisor-screening')
const isInitialScreeningSection = computed(() => currentSection.value === 'initial-screening-confirmation')
const isScreeningSection = computed(() => isAdvisorScreeningSection.value || isInitialScreeningSection.value)
const isCompactApplicationTable = computed(() => viewportWidth.value < 1480)
const showTopStatsPanel = computed(() => !isAdvisorScreeningSection.value)
const showIntendedAdvisorColumn = computed(() => !isScreeningSection.value)
const showMaterialStatusColumn = computed(() => !isScreeningSection.value)
const showApplicationStatusColumn = computed(() => !isScreeningSection.value)
const showPhoneColumn = computed(() => !isScreeningSection.value && !isCompactApplicationTable.value)
const showReviewerColumn = computed(() => !isScreeningSection.value && !isCompactApplicationTable.value)
const showApplicationPagination = computed(() => !isAdvisorScreeningSection.value)
const advisorScreeningTab = ref<'pending' | 'submitted'>('pending')
const advisorScreeningSubmittedLoading = ref(false)
const advisorScreeningSubmittedRows = ref<AdvisorScreeningSubmittedApplicationRecord[]>([])
const advisorScreeningSubmittedPagination = useServerPagination()
const advisorScreeningPendingRows = ref<RecruitApplicationRecord[]>([])
const advisorScreeningSubmittedFilters = reactive({
  keyword: '',
})
const advisorScreeningRescoreDialogVisible = ref(false)
const advisorScreeningRescoreSubmitting = ref(false)
const advisorScreeningRescoreTarget = ref<AdvisorScreeningSubmittedApplicationRecord | null>(null)
const advisorScreeningRescoreNoticeDialogVisible = ref(false)
const advisorScreeningRescoreNotice = ref<{ title: string; message: string; type: 'success' | 'warning' | 'error' | 'info' } | null>(null)
const advisorScreeningRescoreNoticeDialogTitle = computed(() => advisorScreeningRescoreNotice.value?.title || '提示')
const isAdvisorScreeningPendingTab = computed(() => isAdvisorScreeningSection.value && advisorScreeningTab.value === 'pending')
const isAdvisorScreeningSubmittedTab = computed(() => isAdvisorScreeningSection.value && advisorScreeningTab.value === 'submitted')
const applicationActionColumnWidth = computed(() => {
  if (isInitialScreeningSection.value) {
    return isCompactApplicationTable.value ? 136 : 150
  }
  return isCompactApplicationTable.value ? 150 : 170
})
const roleSet = computed(() => new Set(authStore.roles))
const canAccessAdvisorScreeningSection = computed(() => ['advisor', 'platform_admin'].some((role) => roleSet.value.has(role)))
const canAccessInitialScreeningSection = computed(() => ['AILABMGT', 'academy_admin', 'platform_admin'].some((role) => roleSet.value.has(role)))
const canAccessCurrentSection = computed(() => {
  if (isAdvisorScreeningSection.value) {
    return canAccessAdvisorScreeningSection.value
  }
  if (isInitialScreeningSection.value) {
    return canAccessInitialScreeningSection.value
  }
  return true
})
const canWriteRecruitment = computed(() => {
  const permissionSet = new Set(authStore.permissions)
  return permissionSet.has('*') || permissionSet.has('recruitment:write')
})
const canOperateAdvisorScreening = computed(() => canWriteRecruitment.value && canAccessAdvisorScreeningSection.value)
const canOperateInitialScreening = computed(() => canWriteRecruitment.value && canAccessInitialScreeningSection.value)

const applicationSectionTag = computed(() => {
  if (isAdvisorScreeningSection.value) {
    return '导师初筛'
  }
  if (isInitialScreeningSection.value) {
    return '初筛确认'
  }
  return '报名申请管理'
})

const applicationSectionTitle = computed(() => {
  if (isAdvisorScreeningSection.value) {
    return '导师初筛工作台'
  }
  if (isInitialScreeningSection.value) {
    return '初筛确认工作台'
  }
  return '申请池'
})

const applicationSectionSummary = computed(() => {
  if (isAdvisorScreeningSection.value) {
    const tabLabel = advisorScreeningTab.value === 'submitted' ? '已提交' : '待提交'
    return selectedPlan.value ? `当前计划：${selectedPlan.value.plan_name}，当前标签：${tabLabel}` : `当前标签：${tabLabel}`
  }
  if (isInitialScreeningSection.value) {
    return selectedPlan.value ? `当前计划：${selectedPlan.value.plan_name}，默认展示待初筛确认申请` : '默认展示待初筛确认申请'
  }
  return selectedPlan.value ? `已筛选计划：${selectedPlan.value.plan_name}，默认展示注册学生中“报名已提交”及后续环节` : '默认展示注册学生中“报名已提交”及后续环节'
})

const applicationStatusOptions = computed(() => {
  if (isPlanSection.value) {
    return options.value.application_status_options.filter((item) => PLAN_SECTION_DEFAULT_STATUSES.includes(String(item.value || '')))
  }
  if (isAdvisorScreeningSection.value) {
    return options.value.application_status_options.filter((item) => ADVISOR_SCREENING_DEFAULT_STATUSES.includes(String(item.value || '')))
  }
  if (isInitialScreeningSection.value) {
    return options.value.application_status_options.filter((item) => INITIAL_SCREENING_DEFAULT_STATUSES.includes(String(item.value || '')))
  }
  return options.value.application_status_options
})

const selectedAdvisorScreeningRows = computed(() => {
  return advisorScreeningTableRows.value.filter((item) => selectedAdvisorScreeningIds.value.includes(item.id))
})

const advisorBatchSubmitSummary = computed(() => {
  return selectedAdvisorScreeningRows.value.map((item) => {
    const draft = advisorScreeningDrafts[item.id]
    return {
      application_id: item.id,
      business_key: item.business_key,
      student_name: item.student_name,
      advisor_score: draft?.advisor_score,
      result: resolveAdvisorScreeningAutoResult(draft?.advisor_score),
    }
  })
})

const advisorBatchMissingScoreRows = computed(() => {
  return selectedAdvisorScreeningRows.value.filter((item) => {
    const draft = advisorScreeningDrafts[item.id]
    const score = Number(draft?.advisor_score)
    return draft?.advisor_score === undefined || Number.isNaN(score) || score < 0 || score > 100
  })
})

const advisorBatchLockedRows = computed(() => {
  return selectedAdvisorScreeningRows.value.filter((item) => isAdvisorScreeningLocked(item))
})

const advisorBatchMixedScreeningRounds = computed(() => {
  return selectedAdvisorScreeningRows.value.length > 0 && new Set(selectedAdvisorScreeningRows.value.map((item) => String(item.advisor_screening_round || '').trim()).filter(Boolean)).size > 1
})

const advisorBatchCanSubmit = computed(() => {
  return isAdvisorScreeningPendingTab.value && advisorBatchSubmitSummary.value.length > 0 && advisorBatchMissingScoreRows.value.length === 0 && advisorBatchLockedRows.value.length === 0 && !advisorBatchMixedScreeningRounds.value
})

const selectedInitialScreeningRows = computed(() => {
  return applications.value.filter((item) => selectedInitialScreeningIds.value.includes(item.id))
})

const advisorScreeningTableRows = computed(() => {
  return applications.value.filter((item) => !isAdvisorScreeningLocked(item))
})

function resolveAdvisorScreeningAutoResult(score?: number | null) {
  if (score === undefined || score === null || Number.isNaN(Number(score))) {
    return null
  }
  return Number(score) >= ADVISOR_SCREENING_PASS_SCORE ? 'passed' : 'rejected'
}

function formatAdvisorScreeningRound(round?: string | null) {
  return String(round || '').trim() === 'second_choice' ? '第二志愿' : '第一志愿'
}

function formatAdvisorScreeningAutoResult(score?: number | null) {
  const result = resolveAdvisorScreeningAutoResult(score)
  if (result === 'passed') {
    return '自动通过'
  }
  if (result === 'rejected') {
    return '自动不通过'
  }
  return '待判定'
}

function resolveAdvisorScreeningResultTagType(score?: number | null) {
  const result = resolveAdvisorScreeningAutoResult(score)
  if (result === 'passed') {
    return 'success'
  }
  if (result === 'rejected') {
    return 'danger'
  }
  return 'info'
}

const effectiveApplicationStatusFilter = computed(() => {
  if (applicationFilters.status) {
    return normalizeRecruitmentStatusForQuery(applicationFilters.status)
  }
  if (isPlanSection.value) {
    return normalizeRecruitmentStatusForQuery(PLAN_SECTION_DEFAULT_STATUSES.join(','))
  }
  if (isAdvisorScreeningSection.value) {
    return ADVISOR_SCREENING_QUERY_STATUS
  }
  if (isInitialScreeningSection.value) {
    return normalizeRecruitmentStatusForQuery(INITIAL_SCREENING_DEFAULT_STATUSES.join(','))
  }
  return undefined
})

const selectedPlan = computed(() => plans.value.find((item) => item.id === selectedPlanId.value))
const planPager = useServerPagination()
const applicationPager = useServerPagination()

function applicationTagType(status: string) {
  return resolveDictTagType(status, applicationStatusColors.value)
}

function formatInitialScreeningScore(score?: number | null, fallback = '') {
  if (score === null || score === undefined) {
    return fallback
  }
  return String(score)
}

function materialTagType(status: string) {
  return resolveDictTagType(status, materialStatusColors.value)
}

function portalApplicationFormStatusTagType(status: string) {
  if (status === '已填写报名') {
    return 'success'
  }
  if (status === '驳回重填') {
    return 'warning'
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
  if (status === '驳回重填') {
    return 'danger'
  }
  return 'info'
}

function portalAccountStatusTagType(status: string | null | undefined) {
  return status === '停用' ? 'danger' : 'success'
}

function resolvePortalApplicationFormStatus(row: RecruitApplicationRecord) {
  if (row.application_status === '驳回重填') {
    return '驳回重填'
  }
  if (row.portal_student_id) {
    return '已填写报名'
  }
  return '未填写报名'
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
  return planItems[0]?.id
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
  if (!canAccessCurrentSection.value) {
    applications.value = []
    applicationPager.sync(0)
    selectedAdvisorScreeningIds.value = []
    selectedInitialScreeningIds.value = []
    return
  }
  applicationsLoading.value = true
  try {
    if (isAdvisorScreeningSection.value) {
      applications.value = []
      applicationPager.sync(0)
      selectedAdvisorScreeningIds.value = []
      if (advisorScreeningTab.value === 'pending') {
        await loadAdvisorScreeningPendingRows()
      }
    } else if (isInitialScreeningSection.value) {
      if (selectedPlanId.value === undefined) {
        applications.value = []
        applicationPager.sync(0)
        selectedInitialScreeningIds.value = []
        return
      }
      const response = await listInitialScreeningConfirmationApplications({
        keyword: applicationFilters.keyword || undefined,
        plan_id: selectedPlanId.value,
        advisor_names: applicationFilters.advisor_names.length ? applicationFilters.advisor_names.join(',') : undefined,
        page: applicationPager.pagination.currentPage,
        page_size: applicationPager.pagination.pageSize,
      })
      applications.value = normalizeInitialScreeningApplicationRows(response.data.items)
      applicationPager.sync(response.data.total)
    } else {
      const response = await listRecruitmentApplications({
        keyword: applicationFilters.keyword || undefined,
        status: effectiveApplicationStatusFilter.value,
        portal_student_only: isPlanSection.value || undefined,
        advisor_names: applicationFilters.advisor_names.length ? applicationFilters.advisor_names.join(',') : undefined,
        plan_id: selectedPlanId.value,
        page: 1,
        page_size: applicationPager.pagination.pageSize,
      })
      applications.value = response.data.items
      applicationPager.sync(response.data.total)
    }
    if (!isAdvisorScreeningSection.value) {
      selectedAdvisorScreeningIds.value = []
    }
    if (isInitialScreeningSection.value) {
      syncInitialScreeningDrafts(applications.value)
      selectedInitialScreeningIds.value = selectedInitialScreeningIds.value.filter((id) => applications.value.some((item) => item.id === id))
    } else {
      selectedInitialScreeningIds.value = []
    }
  } finally {
    applicationsLoading.value = false
  }
}

const advisorScreeningVisibleRows = computed(() => {
  if (!isAdvisorScreeningSection.value) {
    return applications.value
  }
  return advisorScreeningTab.value === 'submitted' ? applications.value : advisorScreeningPendingRows.value
})

function handleAdvisorScreeningTabChange(tab: 'pending' | 'submitted') {
  advisorScreeningTab.value = tab
  if (tab === 'pending') {
    selectedAdvisorScreeningIds.value = []
    void loadAdvisorScreeningPendingRows()
    return
  }
  if (tab === 'submitted') {
    selectedAdvisorScreeningIds.value = []
    void loadAdvisorScreeningSubmittedRows()
  }
}

async function loadAdvisorScreeningPendingRows() {
  if (!isAdvisorScreeningSection.value || advisorScreeningTab.value !== 'pending') {
    advisorScreeningPendingRows.value = []
    applications.value = []
    return
  }
  applicationsLoading.value = true
  try {
    const response = await listAdvisorScreeningPendingApplications({
      keyword: applicationFilters.keyword || undefined,
    })
    advisorScreeningPendingRows.value = response.data.map((item) => ({
      id: item.application_id,
      student_name: item.full_name,
      business_key: item.business_key || '',
      candidate_no: item.candidate_no,
      first_choice: item.first_choice || '',
      first_choice_id: item.first_choice_id ?? null,
      first_choice_screening_submitted_at: item.first_choice_screening_submitted_at || null,
      first_choice_screening_score: item.first_choice_screening_score ?? null,
      second_choice: item.second_choice || '',
      second_choice_id: item.second_choice_id ?? null,
      second_choice_screening_submitted_at: item.second_choice_screening_submitted_at || null,
      second_choice_screening_score: item.second_choice_screening_score ?? null,
      advisor_screening_round: item.choice_name === '第二志愿' ? 'second_choice' : 'first_choice',
      application_status: item.choice_name === '第二志愿' ? 'initial_screening_second' : 'initial_screening_first',
      advisor_screening_status: 'pending',
      intended_advisor_name: item.first_choice || '',
    } as RecruitApplicationRecord))
    applications.value = advisorScreeningPendingRows.value
    syncAdvisorScreeningDrafts(applications.value)
  } finally {
    applicationsLoading.value = false
  }
}

async function handleAdvisorScreeningPendingSearch() {
  selectedAdvisorScreeningIds.value = []
  await loadAdvisorScreeningPendingRows()
}

async function handleAdvisorScreeningPendingReset() {
  applicationFilters.keyword = ''
  selectedAdvisorScreeningIds.value = []
  await loadAdvisorScreeningPendingRows()
}

async function loadAdvisorScreeningSubmittedRows() {
  if (!isAdvisorScreeningSection.value || advisorScreeningTab.value !== 'submitted') {
    advisorScreeningSubmittedRows.value = []
    advisorScreeningSubmittedPagination.sync(0)
    return
  }
  advisorScreeningSubmittedLoading.value = true
  try {
    const response = await listAdvisorScreeningSubmittedApplications({
      keyword: advisorScreeningSubmittedFilters.keyword || undefined,
      page: advisorScreeningSubmittedPagination.pagination.currentPage,
      page_size: advisorScreeningSubmittedPagination.pagination.pageSize,
    })
    advisorScreeningSubmittedRows.value = response.data.items
    advisorScreeningSubmittedPagination.sync(response.data.total)
  } finally {
    advisorScreeningSubmittedLoading.value = false
  }
}

function formatSubmittedDateTime(value?: string | null) {
  const normalized = String(value || '').trim()
  if (!normalized) {
    return '-'
  }
  return normalized.replace('T', ' ').slice(0, 19)
}

function handleAdvisorScreeningSubmittedSearch() {
  advisorScreeningSubmittedPagination.pagination.currentPage = 1
  void loadAdvisorScreeningSubmittedRows()
}

function handleAdvisorScreeningSubmittedReset() {
  advisorScreeningSubmittedFilters.keyword = ''
  advisorScreeningSubmittedPagination.pagination.currentPage = 1
  void loadAdvisorScreeningSubmittedRows()
}

async function openAdvisorScreeningSubmittedDetail(row: AdvisorScreeningSubmittedApplicationRecord) {
  try {
    const applicationId = row.application_id
    const response = await getRecruitmentPortalApplicationDetail(applicationId)
    viewingApplication.value = response.data
    applicationDetailVisible.value = true
    await loadViewingApplicationWorkflowTask(response.data.business_key)
  } catch (error) {
    const message = axios.isAxiosError(error) ? String(error.response?.data?.detail || error.message) : '加载报名申请详情失败'
    ElMessage.error(message)
  }
}

function advisorScreeningSubmittedActions() {
  return [
    { key: 'view', label: '查看详情', type: 'info' as const, onClick: openAdvisorScreeningSubmittedDetail },
    { key: 'rescore', label: '重新评分', type: 'warning' as const, onClick: handleAdvisorScreeningSubmittedRescore },
  ]
}

async function handleAdvisorScreeningSubmittedRescore(row: AdvisorScreeningSubmittedApplicationRecord) {
  advisorScreeningRescoreTarget.value = row
  advisorScreeningRescoreDialogVisible.value = true
}

function closeAdvisorScreeningRescoreDialog() {
  if (advisorScreeningRescoreSubmitting.value) {
    return
  }
  advisorScreeningRescoreDialogVisible.value = false
  advisorScreeningRescoreTarget.value = null
}

function showAdvisorScreeningRescoreNotice(message: string, type: 'success' | 'warning' | 'error' | 'info' = 'info', title?: string) {
  advisorScreeningRescoreNotice.value = {
    title: title || (type === 'success' ? '操作成功' : type === 'warning' ? '提醒' : type === 'error' ? '操作失败' : '提示'),
    message,
    type,
  }
  advisorScreeningRescoreNoticeDialogVisible.value = true
}

async function submitAdvisorScreeningRescore() {
  const target = advisorScreeningRescoreTarget.value
  if (!target) {
    return
  }
  advisorScreeningRescoreSubmitting.value = true
  try {
    await rescoreAdvisorScreeningSubmittedApplication(target.application_id)
    advisorScreeningRescoreDialogVisible.value = false
    advisorScreeningRescoreTarget.value = null
    showAdvisorScreeningRescoreNotice(`${target.full_name} 的已提交记录已回退到导师初筛。`, 'success', '重新评分完成')
    await loadAdvisorScreeningSubmittedRows()
  } catch (error) {
    const message = axios.isAxiosError(error)
      ? String(error.response?.data?.detail || error.message)
      : '重新评分失败'
    showAdvisorScreeningRescoreNotice(message, 'error', '重新评分失败')
  } finally {
    advisorScreeningRescoreSubmitting.value = false
  }
}

function resolveAdvisorExistingScore(row: RecruitApplicationRecord) {
  if (row.advisor_screening_round === 'second_choice') {
    return row.second_choice_screening_score ?? undefined
  }
  return row.first_choice_screening_score ?? undefined
}

function syncAdvisorScreeningDrafts(rows: RecruitApplicationRecord[]) {
  const activeIds = new Set(rows.map((item) => item.id))
  Object.keys(advisorScreeningDrafts).forEach((key) => {
    if (!activeIds.has(Number(key))) {
      delete advisorScreeningDrafts[Number(key)]
    }
  })
  rows.forEach((item) => {
    if (!advisorScreeningDrafts[item.id]) {
      advisorScreeningDrafts[item.id] = {
        advisor_score: resolveAdvisorExistingScore(item),
      }
    }
  })
}

function syncInitialScreeningDrafts(rows: RecruitApplicationRecord[]) {
  const activeIds = new Set(rows.map((item) => item.id))
  Object.keys(initialScreeningDrafts).forEach((key) => {
    if (!activeIds.has(Number(key))) {
      delete initialScreeningDrafts[Number(key)]
    }
  })
  rows.forEach((item) => {
    if (!initialScreeningDrafts[item.id]) {
      initialScreeningDrafts[item.id] = {
        result: item.initial_screening_result === 'rejected' ? 'rejected' : 'passed',
        comment: '',
      }
    }
  })
}

function handleApplicationSelectionChange(rows: RecruitApplicationRecord[]) {
  const ids = rows.map((item) => item.id)
  if (isAdvisorScreeningSection.value) {
    selectedAdvisorScreeningIds.value = ids
    return
  }
  if (isInitialScreeningSection.value) {
    selectedInitialScreeningIds.value = ids
  }
}

function isAdvisorScreeningLocked(row: RecruitApplicationRecord) {
  if (row.application_status === '报名终止') {
    return true
  }
  if (row.advisor_screening_status === 'submitted') {
    return true
  }
  if (String(row.advisor_screening_round || '').trim() === 'second_choice') {
    return Boolean(row.second_choice_screening_batch_id || row.second_choice_screening_submitted_at)
  }
  return Boolean(row.first_choice_screening_batch_id || row.first_choice_screening_submitted_at)
}

function isInitialScreeningLocked(row: RecruitApplicationRecord) {
  return row.initial_screening_status === 'confirmed' || Boolean(row.initial_screening_confirmed_at)
}

function openInitialScreeningBatchConfirmDialog() {
  initialScreeningBatchConfirmDialogVisible.value = true
}

function closeInitialScreeningBatchConfirmDialog() {
  initialScreeningBatchConfirmDialogVisible.value = false
}

function openAdvisorBatchSubmitDialog() {
  if (!canOperateAdvisorScreening.value) {
    ElMessage.warning('当前账号只有查看权限，无法提交导师初筛')
    return
  }
  if (!selectedAdvisorScreeningIds.value.length) {
    ElMessage.warning('请先勾选至少一条导师初筛记录')
    return
  }
  if (advisorBatchMixedScreeningRounds.value) {
    ElMessage.warning('批量提交仅支持同一志愿轮次，请只勾选第一志愿或第二志愿记录')
    return
  }
  advisorScreeningBatchConfirmDialogVisible.value = true
}

function closeAdvisorBatchSubmitDialog() {
  advisorScreeningBatchConfirmDialogVisible.value = false
}

async function submitAdvisorBatchScreening() {
  if (advisorBatchMixedScreeningRounds.value) {
    ElMessage.warning('批量提交仅支持同一志愿轮次，请只勾选第一志愿或第二志愿记录')
    return
  }
  applicationWorkflowActionSubmitting.value = true
  const payload = {
    signature_base64: '',
    items: selectedAdvisorScreeningRows.value.map((row) => ({
      application_id: row.id,
      advisor_score: Number(advisorScreeningDrafts[row.id]?.advisor_score),
    })),
  }
  try {
    await submitAdvisorScreeningBatch(payload)
    advisorScreeningBatchConfirmDialogVisible.value = false
    ElMessage.success('导师初筛批量提交成功')
    await Promise.all([refreshAll(), reloadViewingApplicationDetail()])
    selectedAdvisorScreeningIds.value = []
  } catch (error) {
    console.error('导师初筛批量提交失败', { payload, error })
    const message = axios.isAxiosError(error)
      ? String(error.response?.data?.detail || error.message)
      : '导师初筛批量提交失败'
    ElMessage.error(message)
  } finally {
    applicationWorkflowActionSubmitting.value = false
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
    const applicationId = getApplicationRowId(row)
    const response = await getRecruitmentApplicationDetail(applicationId)
    editingApplicationId.value = applicationId
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
  const preferences = (applicationForm.preferences || []).filter((item) => trimText(item.advisor_name))
  applicationForm.first_choice = preferences[0]?.advisor_name || ''
  applicationForm.second_choice = preferences[1]?.advisor_name || ''
  applicationForm.intended_field = preferences[0]?.advisor_name || ''
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
    const applicationId = getApplicationRowId(row)
    const response = await getRecruitmentPortalApplicationDetail(applicationId)
    viewingApplication.value = response.data
    applicationDetailVisible.value = true
    await loadViewingApplicationWorkflowTask(response.data.business_key)
  } catch (error) {
    const message = axios.isAxiosError(error) ? String(error.response?.data?.detail || error.message) : '加载报名申请详情失败'
    ElMessage.error(message)
  }
}

async function reloadViewingApplicationDetail() {
  if (!viewingApplication.value?.application_id) {
    return
  }
  const response = await getRecruitmentPortalApplicationDetail(viewingApplication.value.application_id)
  viewingApplication.value = response.data
  await loadViewingApplicationWorkflowTask(response.data.business_key)
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
  if (isAdvisorScreeningSection.value) {
    return false
  }
  if (isInitialScreeningSection.value) {
    return canOperateInitialScreening.value && INITIAL_SCREENING_DEFAULT_STATUSES.includes(row.application_status) && !isInitialScreeningLocked(row)
  }
  if (!canWriteRecruitment.value && isScreeningSection.value) {
    return false
  }
  return row.application_status === '报名已提交'
}

function resolveApplicationActionLabel() {
  if (isAdvisorScreeningSection.value) {
    return '查看填报'
  }
  return '审批'
}

function applicationMainActions(row: RecruitApplicationRecord) {
  if (isAdvisorScreeningSection.value) {
    return [
      { key: 'view', label: '查看填报', type: 'info' as const, onClick: openViewApplicationDetail },
    ]
  }
  return [
    { key: 'view', label: '查看填报', type: 'info' as const, onClick: openViewApplicationDetail },
    ...(isInitialScreeningSection.value
      ? []
      : [{ key: 'review', label: resolveApplicationActionLabel(), type: 'primary' as const, disabled: !canReviewApplication(row), onClick: openViewApplicationDetail }]),
  ]
}

function applicationMoreActions() {
  if (isScreeningSection.value) {
    return []
  }
  return [
    { key: 'edit', label: '编辑', type: 'primary' as const, onClick: openEditApplicationDialog },
    { key: 'delete', label: '删除', type: 'danger' as const, onClick: handleDeleteApplication },
  ]
}

async function handleViewingApplicationWorkflowAction(action: WorkflowActionOption) {
  if (!viewingApplicationWorkflowTask.value) {
    ElMessage.warning('当前未找到可执行的审批任务')
    return
  }
  pendingViewingApplicationWorkflowAction.value = action
  applicationWorkflowComment.value = ''
  applicationWorkflowCommentDialogVisible.value = true
}

async function submitApplicationWorkflowCommentDialog() {
  if (!viewingApplicationWorkflowTask.value || !pendingViewingApplicationWorkflowAction.value) {
    return
  }
  const currentAction = pendingViewingApplicationWorkflowAction.value
  applicationWorkflowActionSubmitting.value = true
  try {
    await executeWorkflowTaskAction(viewingApplicationWorkflowTask.value.id, {
      action: currentAction.action,
      comment: applicationWorkflowComment.value.trim() || undefined,
    })
    applicationWorkflowCommentDialogVisible.value = false
    applicationDetailVisible.value = false
    viewingApplication.value = null
    viewingApplicationWorkflowTask.value = null
    ElMessage.success(`${currentAction.label}已完成`)
    try {
      await refreshAll()
    } catch (refreshError) {
      const refreshMessage = axios.isAxiosError(refreshError)
        ? String(refreshError.response?.data?.detail || refreshError.message)
        : '列表刷新失败，请手动刷新页面'
      ElMessage.warning(`操作已完成，但${refreshMessage}`)
    }
  } catch (error) {
    const message = axios.isAxiosError(error)
      ? String(error.response?.data?.detail || error.message)
      : `${currentAction.label}失败`
    ElMessage.error(message)
  } finally {
    applicationWorkflowActionSubmitting.value = false
  }
}

async function handleAdvisorScreeningSubmit(payload: AdvisorScreeningBatchSubmitRequest) {
  applicationWorkflowActionSubmitting.value = true
  try {
    await submitAdvisorScreeningBatch(payload)
    ElMessage.success('导师初筛已提交')
    await Promise.all([refreshAll(), reloadViewingApplicationDetail()])
  } catch (error) {
    console.error('导师初筛提交失败', { payload, error })
    const message = axios.isAxiosError(error)
      ? String(error.response?.data?.detail || error.message)
      : '导师初筛提交失败'
    ElMessage.error(message)
  } finally {
    applicationWorkflowActionSubmitting.value = false
  }
}

async function handleInitialScreeningConfirmation(payload: InitialScreeningConfirmationRequest) {
  if (!viewingApplication.value?.application_id) {
    ElMessage.warning('当前未找到申请记录')
    return
  }
  applicationWorkflowActionSubmitting.value = true
  try {
    await confirmInitialScreening(viewingApplication.value.application_id, payload)
    ElMessage.success('初筛确认已提交')
    await Promise.all([refreshAll(), reloadViewingApplicationDetail()])
  } catch (error) {
    const message = axios.isAxiosError(error)
      ? String(error.response?.data?.detail || error.message)
      : '初筛确认提交失败'
    ElMessage.error(message)
  } finally {
    applicationWorkflowActionSubmitting.value = false
  }
}

async function submitInitialScreeningBatch() {
  if (!canOperateInitialScreening.value) {
    ElMessage.warning('当前账号只有查看权限，无法提交初筛确认')
    return
  }
  if (!selectedInitialScreeningIds.value.length) {
    ElMessage.warning('请先勾选至少一条初筛确认记录')
    return
  }
  for (const row of selectedInitialScreeningRows.value) {
    if (isInitialScreeningLocked(row)) {
      ElMessage.warning(`${row.student_name} 已完成初筛确认，不能重复提交`)
      return
    }
    if (!initialScreeningDrafts[row.id]) {
      ElMessage.warning(`请先确认 ${row.student_name} 的确认结论`)
      return
    }
  }

  applicationWorkflowActionSubmitting.value = true
  try {
    const results = await Promise.allSettled(
      selectedInitialScreeningRows.value.map((row) =>
        confirmInitialScreening(row.id, {
          result: initialScreeningDrafts[row.id].result,
          comment: initialScreeningDrafts[row.id].comment.trim() || undefined,
        }),
      ),
    )
    const failedResults = results.filter((item): item is PromiseRejectedResult => item.status === 'rejected')
    const successCount = results.length - failedResults.length

    await Promise.all([refreshAll(), reloadViewingApplicationDetail()])
    selectedInitialScreeningIds.value = []

    if (!failedResults.length) {
      ElMessage.success(`初筛确认已批量提交，共 ${successCount} 条`)
      return
    }

    const firstError = failedResults[0]?.reason
    const failureMessage = axios.isAxiosError(firstError)
      ? String(firstError.response?.data?.detail || firstError.message)
      : '部分初筛确认提交失败'

    if (successCount > 0) {
      ElMessage.warning(`已成功提交 ${successCount} 条，另有 ${failedResults.length} 条失败：${failureMessage}`)
      return
    }

    ElMessage.error(failureMessage)
  } catch (error) {
    const message = axios.isAxiosError(error)
      ? String(error.response?.data?.detail || error.message)
      : '初筛确认批量提交失败'
    ElMessage.error(message)
  } finally {
    initialScreeningBatchConfirmDialogVisible.value = false
    applicationWorkflowActionSubmitting.value = false
  }
}

async function confirmInitialScreeningBatch() {
  if (!canOperateInitialScreening.value) {
    ElMessage.warning('当前账号只有查看权限，无法提交初筛确认')
    return
  }
  if (!selectedInitialScreeningIds.value.length) {
    ElMessage.warning('请先勾选至少一条初筛确认记录')
    return
  }
  initialScreeningBatchConfirmDialogVisible.value = false
  await submitInitialScreeningBatch()
}

function resetApplicationWorkflowCommentDialog() {
  pendingViewingApplicationWorkflowAction.value = null
  applicationWorkflowComment.value = ''
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
      preferences: (applicationForm.preferences || []).filter((item) => trimText(item.advisor_name)).map((item, index) => ({
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
      status: effectiveApplicationStatusFilter.value,
      portal_student_only: isPlanSection.value || undefined,
      advisor_names: applicationFilters.advisor_names.length ? applicationFilters.advisor_names.join(',') : undefined,
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
  applicationFilters.advisor_names = []
  applicationPager.reset()
  await loadApplications()
}

watch(
  () => currentSection.value,
  () => {
    applicationFilters.keyword = ''
    applicationFilters.status = ''
    applicationFilters.advisor_names = []
    advisorScreeningTab.value = 'pending'
    selectedAdvisorScreeningIds.value = []
    selectedInitialScreeningIds.value = []
    applicationPager.reset()
    void loadApplications()
  },
)

watch(
  () => advisorScreeningTab.value,
  () => {
    if (!isAdvisorScreeningSection.value) {
      return
    }
    if (advisorScreeningTab.value === 'pending') {
      selectedAdvisorScreeningIds.value = []
      void loadAdvisorScreeningPendingRows()
      return
    }
    if (isAdvisorScreeningSubmittedTab.value) {
      selectedAdvisorScreeningIds.value = []
      void loadAdvisorScreeningSubmittedRows()
      return
    }
    selectedAdvisorScreeningIds.value = selectedAdvisorScreeningIds.value.filter((id) => advisorScreeningTableRows.value.some((item) => item.id === id))
  },
)

watch(
  () => [advisorScreeningSubmittedPagination.pagination.currentPage, advisorScreeningSubmittedPagination.pagination.pageSize],
  () => {
    if (isAdvisorScreeningSubmittedTab.value) {
      void loadAdvisorScreeningSubmittedRows()
    }
  },
)
async function handlePlanSearch() {
  planPager.reset()
  await loadPlans()
}

onBeforeUnmount(() => {
  window.removeEventListener('resize', updateViewportWidth)
})

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
  if (isAdvisorScreeningSection.value) {
    return
  }
  applicationPager.handleCurrentChange(page)
  await loadApplications()
}

async function handleApplicationPageSizeChange(size: number) {
  if (isAdvisorScreeningSection.value) {
    return
  }
  applicationPager.handleSizeChange(size)
  await loadApplications()
}

onMounted(() => {
  updateViewportWidth()
  window.addEventListener('resize', updateViewportWidth)
  void refreshAll()
})
</script>

<template>
  <section class="content-stack">
    <section v-if="showTopStatsPanel" class="stats-grid">
      <article v-for="card in statsCards" :key="card.label" class="stat-card" :data-tone="card.tone">
        <p>{{ card.label }}</p>
        <strong>{{ card.value }}</strong>
      </article>
    </section>

    <section v-if="isPlanSection" class="section-card">
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

    <section v-if="isPlanSection" class="two-column-grid">
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
          <p class="section-tag">{{ applicationSectionTag }}</p>
          <h2>{{ applicationSectionTitle }}</h2>
        </div>
        <div class="header-actions">
          <span class="summary-text">{{ applicationSectionSummary }}</span>
          <el-tag v-if="isScreeningSection && !canAccessCurrentSection" type="danger" effect="light">当前角色无权访问该初筛页面</el-tag>
          <el-tag v-else-if="isScreeningSection && ((isAdvisorScreeningSection && !canOperateAdvisorScreening) || (isInitialScreeningSection && !canOperateInitialScreening))" type="info" effect="light">当前账号仅可查看，不能提交</el-tag>
          <template v-if="isPlanSection">
            <el-button :loading="templateSubmitting" @click="handleTemplateDownload">下载空白模板</el-button>
            <el-button :loading="importSubmitting" @click="triggerTemplateImport">模板导入</el-button>
            <el-button :loading="exportSubmitting" @click="handleTemplateExport">导出名单</el-button>
            <el-button type="primary" round @click="openCreateApplicationDialog">新增报名申请</el-button>
          </template>
          <el-button v-if="false">
            导出当前清单
          </el-button>
        </div>
      </div>

      <input v-if="isPlanSection" ref="importInputRef" type="file" accept=".xlsx" class="hidden-input" @change="handleTemplateImport" />

      <el-form v-if="!isAdvisorScreeningSection" class="filter-form" :inline="true">
        <el-form-item label="关键字">
          <el-input v-model="applicationFilters.keyword" placeholder="业务编号 / 姓名 / 学校 / 方向" clearable />
        </el-form-item>
        <el-form-item label="申请状态">
          <el-select v-model="applicationFilters.status" placeholder="全部状态" clearable style="width: 180px">
            <el-option v-for="item in applicationStatusOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="导师">
          <el-select v-model="applicationFilters.advisor_names" multiple collapse-tags collapse-tags-tooltip clearable filterable placeholder="全部导师" style="width: 280px">
            <el-option v-for="item in options.advisor_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleFilterSearch">查询</el-button>
          <el-button @click="handleFilterReset">重置</el-button>
        </el-form-item>
      </el-form>

      <div v-if="!canAccessCurrentSection" class="empty-inline">当前角色不在该页面的处理范围内。导师仅可见“导师初筛”，书院管理员仅可见“初筛确认”。</div>

      <div v-if="isAdvisorScreeningSection && canAccessCurrentSection" class="advisor-screening-tabs">
        <el-tabs :model-value="advisorScreeningTab" class="advisor-screening-tabs__nav" @tab-change="handleAdvisorScreeningTabChange">
          <el-tab-pane label="待提交" name="pending" />
          <el-tab-pane label="已提交" name="submitted" />
        </el-tabs>
        <div v-if="isAdvisorScreeningPendingTab" class="advisor-screening-pending-panel">
          <el-form inline :model="applicationFilters" class="advisor-screening-pending-panel__filter">
            <el-form-item label="关键字">
              <el-input v-model="applicationFilters.keyword" placeholder="请输入报名号或学生姓名" clearable @keyup.enter="handleAdvisorScreeningPendingSearch" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleAdvisorScreeningPendingSearch">查询</el-button>
              <el-button @click="handleAdvisorScreeningPendingReset">重置</el-button>
            </el-form-item>
          </el-form>
        </div>
        <div v-if="isAdvisorScreeningPendingTab" class="advisor-screening-floating-action">
          <el-button type="primary" size="large" round :disabled="!selectedAdvisorScreeningIds.length || !canOperateAdvisorScreening" :loading="applicationWorkflowActionSubmitting" @click="openAdvisorBatchSubmitDialog">
            批量提交
          </el-button>
          <span class="advisor-screening-floating-action__hint">已勾选 {{ selectedAdvisorScreeningIds.length }} 条</span>
        </div>
      </div>

      <div v-if="canAccessCurrentSection" class="table-scroll">
        <el-table
          v-if="!isAdvisorScreeningSubmittedTab"
          :data="isAdvisorScreeningSection ? advisorScreeningVisibleRows : applications"
          stripe
          border
          v-loading="applicationsLoading"
          @selection-change="handleApplicationSelectionChange"
        >
          <el-table-column
            v-if="(isAdvisorScreeningSection && isAdvisorScreeningPendingTab) || isInitialScreeningSection"
            type="selection"
            width="48"
            :selectable="(row: RecruitApplicationRecord) => isAdvisorScreeningSection ? canOperateAdvisorScreening && !isAdvisorScreeningLocked(row) : canOperateInitialScreening && !isInitialScreeningLocked(row)"
          />
          <el-table-column v-if="isPlanSection" prop="candidate_no" label="报名号" width="126" show-overflow-tooltip />
          <el-table-column v-else prop="business_key" label="业务编号" min-width="132" show-overflow-tooltip />
          <el-table-column prop="student_name" label="姓名" width="96" show-overflow-tooltip />
          <el-table-column v-if="isPlanSection" prop="phone_number" label="手机号" width="128" show-overflow-tooltip />
          <el-table-column v-if="isPlanSection" prop="email" label="邮箱" min-width="180" show-overflow-tooltip />
          <el-table-column v-if="isPlanSection" label="账号状态" width="96" align="center">
            <template #default="scope">
              <el-tag :type="portalAccountStatusTagType(scope.row.account_status)">{{ scope.row.account_status || '启用' }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column v-if="isPlanSection" label="报名状态" width="110" align="center">
            <template #default="scope">
              <el-tag :type="portalApplicationFormStatusTagType(resolvePortalApplicationFormStatus(scope.row))">{{ resolvePortalApplicationFormStatus(scope.row) }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column v-if="isPlanSection" prop="selected_plan_name" label="招生计划" min-width="160" show-overflow-tooltip />
          <el-table-column v-if="isPlanSection" label="申请流转状态" width="130" align="center">
            <template #default="scope">
              <el-tag :type="portalRecruitmentStatusTagType(scope.row.application_status)">{{ scope.row.application_status || '未提交' }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column v-if="isPlanSection" prop="registered_at" label="注册时间" width="160" show-overflow-tooltip />
          <el-table-column v-if="isInitialScreeningSection" prop="second_choice" label="第二志愿" min-width="92" show-overflow-tooltip />
          <el-table-column v-if="showIntendedAdvisorColumn && !isPlanSection" prop="intended_advisor_name" label="意向导师" width="88" show-overflow-tooltip />
          <el-table-column v-if="showPhoneColumn && !isPlanSection" prop="phone_number" label="电话" width="112" show-overflow-tooltip />
          <el-table-column v-if="showMaterialStatusColumn && !isPlanSection" label="材料状态" width="92">
            <template #default="scope">
              <el-tag :type="materialTagType(scope.row.material_status)">{{ scope.row.material_status }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column v-if="showApplicationStatusColumn && !isPlanSection" label="申请状态" width="100">
            <template #default="scope">
              <el-tag :type="applicationTagType(scope.row.application_status)">{{ scope.row.application_status }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column v-if="isAdvisorScreeningSection" label="初筛轮次" width="92" show-overflow-tooltip>
            <template #default="scope">
              {{ formatAdvisorScreeningRound(scope.row.advisor_screening_round) }}
            </template>
          </el-table-column>
          <el-table-column v-if="isAdvisorScreeningSection" label="提交状态" width="90">
            <template #default="scope">
              <el-tag :type="isAdvisorScreeningLocked(scope.row) ? 'info' : 'warning'">{{ isAdvisorScreeningLocked(scope.row) ? '已提交' : '待提交' }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column v-if="isAdvisorScreeningSection" label="导师评分" width="118">
            <template #default="scope">
              <el-input-number v-model="advisorScreeningDrafts[scope.row.id].advisor_score" :min="0" :max="100" :precision="2" :step="1" size="small" style="width: 100%" :disabled="advisorScreeningTab === 'submitted' || !canOperateAdvisorScreening || isAdvisorScreeningLocked(scope.row)" />
            </template>
          </el-table-column>
          <el-table-column v-if="isAdvisorScreeningSection" label="自动结论" min-width="112">
            <template #default="scope">
              <el-tag :type="resolveAdvisorScreeningResultTagType(advisorScreeningDrafts[scope.row.id]?.advisor_score)">
                {{ formatAdvisorScreeningAutoResult(advisorScreeningDrafts[scope.row.id]?.advisor_score) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column v-if="isInitialScreeningSection" prop="first_choice_screening_score" label="第一志愿分数" width="120" show-overflow-tooltip>
            <template #default="scope">
              {{ formatInitialScreeningScore(scope.row.first_choice_screening_score, '等待初筛') }}
            </template>
          </el-table-column>
          <el-table-column v-if="isInitialScreeningSection" prop="second_choice_screening_score" label="第二志愿分数" width="120" show-overflow-tooltip>
            <template #default="scope">
              {{ formatInitialScreeningScore(scope.row.second_choice_screening_score) }}
            </template>
          </el-table-column>
          <el-table-column v-if="isInitialScreeningSection" prop="initial_screening_result" label="确认结果" width="90" show-overflow-tooltip />
          <el-table-column v-if="isInitialScreeningSection" label="确认状态" width="90">
            <template #default="scope">
              <el-tag :type="isInitialScreeningLocked(scope.row) ? 'info' : 'warning'">{{ isInitialScreeningLocked(scope.row) ? '已确认' : '待确认' }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column v-if="isInitialScreeningSection" label="确认结论" min-width="148">
            <template #default="scope">
              <el-radio-group v-model="initialScreeningDrafts[scope.row.id].result" size="small" :disabled="!canOperateInitialScreening || isInitialScreeningLocked(scope.row)">
                <el-radio value="passed">通过</el-radio>
                <el-radio value="rejected">不通过</el-radio>
              </el-radio-group>
            </template>
          </el-table-column>
          <el-table-column v-if="isInitialScreeningSection" label="确认意见" min-width="180">
            <template #default="scope">
              <el-input v-model="initialScreeningDrafts[scope.row.id].comment" maxlength="200" show-word-limit placeholder="请输入确认意见，可选" :disabled="!canOperateInitialScreening || isInitialScreeningLocked(scope.row)" />
            </template>
          </el-table-column>
          <el-table-column v-if="showReviewerColumn && !isPlanSection" prop="reviewer_name" label="审核人" width="88" show-overflow-tooltip />
          <el-table-column :label="isAdvisorScreeningSection ? '查看' : isScreeningSection ? '处理' : '操作'" :width="applicationActionColumnWidth" align="center">
            <template #default="scope">
              <TableRowActions class="table-row-actions--centered" :row="scope.row" :main-actions="applicationMainActions(scope.row)" :more-actions="applicationMoreActions()" />
            </template>
          </el-table-column>
        </el-table>

        <div v-if="isAdvisorScreeningSubmittedTab" class="advisor-screening-submitted-panel">
          <el-form inline :model="advisorScreeningSubmittedFilters" class="advisor-screening-submitted-panel__filter">
            <el-form-item label="关键字">
              <el-input v-model="advisorScreeningSubmittedFilters.keyword" clearable placeholder="请输入报名号或学生姓名" @keyup.enter="handleAdvisorScreeningSubmittedSearch" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleAdvisorScreeningSubmittedSearch">查询</el-button>
              <el-button @click="handleAdvisorScreeningSubmittedReset">重置</el-button>
            </el-form-item>
          </el-form>
          <div class="advisor-screening-submitted-panel__summary">已提交页签仅展示导师已提交的初筛记录，支持按报名号和学生姓名检索。</div>
        </div>

        <el-table v-if="isAdvisorScreeningSubmittedTab" :data="advisorScreeningSubmittedRows" stripe border v-loading="advisorScreeningSubmittedLoading">
          <el-table-column prop="candidate_no" label="报名号" min-width="132" show-overflow-tooltip />
          <el-table-column prop="choice_name" label="志愿" width="92" show-overflow-tooltip />
          <el-table-column prop="full_name" label="姓名" width="96" show-overflow-tooltip />
          <el-table-column label="分数" width="80" align="center">
            <template #default="scope">
              {{ scope.row.choice_name === '第二志愿' ? (scope.row.second_choice_screening_score ?? '-') : (scope.row.first_choice_screening_score ?? '-') }}
            </template>
          </el-table-column>
          <el-table-column label="结论" width="96" align="center">
            <template #default="scope">
              <el-tag :type="scope.row.is_passed === '通过' ? 'success' : 'danger'">
                {{ scope.row.is_passed || '-' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="提交时间" min-width="180">
            <template #default="scope">
              {{ formatSubmittedDateTime(scope.row.first_choice_screening_submitted_at || scope.row.second_choice_screening_submitted_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150" align="center">
            <template #default="scope">
              <TableRowActions class="table-row-actions--centered" :row="scope.row" :main-actions="advisorScreeningSubmittedActions()" :more-actions="[]" />
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div v-if="showApplicationPagination" class="pagination-bar">
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
      <div v-if="isAdvisorScreeningSubmittedTab" class="pagination-bar">
        <el-pagination
          v-model:current-page="advisorScreeningSubmittedPagination.pagination.currentPage"
          v-model:page-size="advisorScreeningSubmittedPagination.pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="advisorScreeningSubmittedPagination.pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
        />
      </div>

      <el-dialog
        v-model="advisorScreeningRescoreDialogVisible"
        title="重新评分确认"
        width="620px"
        destroy-on-close
        class="recruitment-confirm-dialog"
        :close-on-click-modal="!advisorScreeningRescoreSubmitting"
        :close-on-press-escape="!advisorScreeningRescoreSubmitting"
        :show-close="!advisorScreeningRescoreSubmitting"
        @closed="closeAdvisorScreeningRescoreDialog"
      >
        <div v-if="advisorScreeningRescoreTarget" class="dialog-form reset-password-dialog management-confirm-dialog">
          <p class="management-confirm-dialog__lead">确定将 {{ advisorScreeningRescoreTarget.full_name }} 的已提交记录回退到导师初筛并重新评分吗？</p>
          <div class="management-confirm-dialog__summary reset-password-summary dialog-summary-shell">
            <div>
              <span class="management-confirm-dialog__label">报名号</span>
              <strong>{{ advisorScreeningRescoreTarget.candidate_no }}</strong>
            </div>
            <div>
              <span class="management-confirm-dialog__label">志愿</span>
              <strong>{{ advisorScreeningRescoreTarget.choice_name || '-' }}</strong>
            </div>
            <div>
              <span class="management-confirm-dialog__label">学生姓名</span>
              <strong>{{ advisorScreeningRescoreTarget.full_name }}</strong>
            </div>
            <div>
              <span class="management-confirm-dialog__label">当前分数</span>
              <strong>
                {{ advisorScreeningRescoreTarget.choice_name === '第二志愿'
                  ? (advisorScreeningRescoreTarget.second_choice_screening_score ?? '-')
                  : (advisorScreeningRescoreTarget.first_choice_screening_score ?? '-') }}
              </strong>
            </div>
            <div style="grid-column: span 2;">
              <span class="management-confirm-dialog__label">提醒</span>
              <strong>执行后将把该学生回退到导师初筛环节，请确认后再继续。</strong>
            </div>
          </div>
        </div>
        <template #footer>
          <el-button :disabled="advisorScreeningRescoreSubmitting" @click="closeAdvisorScreeningRescoreDialog">取消</el-button>
          <el-button type="primary" :loading="advisorScreeningRescoreSubmitting" @click="submitAdvisorScreeningRescore">确认重新评分</el-button>
        </template>
      </el-dialog>

      <el-dialog v-model="advisorScreeningRescoreNoticeDialogVisible" :title="advisorScreeningRescoreNoticeDialogTitle" width="520px" destroy-on-close>
        <el-result v-if="advisorScreeningRescoreNotice" :icon="advisorScreeningRescoreNotice.type" :title="advisorScreeningRescoreNotice.title" :sub-title="advisorScreeningRescoreNotice.message" />
        <template #footer>
          <el-button type="primary" @click="advisorScreeningRescoreNoticeDialogVisible = false">确定</el-button>
        </template>
      </el-dialog>

      <div v-if="isInitialScreeningSection" class="advisor-batch-toolbar">
        <div class="advisor-batch-toolbar__summary">
          <strong>已勾选 {{ selectedInitialScreeningIds.length }} 条待确认记录</strong>
          <span>请先在表格中选择通过或不通过，并补充确认意见后，再统一提交初筛确认。</span>
        </div>
        <el-button type="primary" :disabled="!selectedInitialScreeningIds.length || !canOperateInitialScreening" :loading="applicationWorkflowActionSubmitting" @click="openInitialScreeningBatchConfirmDialog">
          批量确认提交
        </el-button>
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
                <el-form-item :label="index === 0 ? '第一志愿导师' : '第二志愿导师'" class="grid-span-2">
                  <el-input v-model="item.advisor_name" placeholder="请输入导师姓名" />
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
      <div v-if="deletingApplication" class="dialog-form reset-password-dialog delete-application-dialog">
        <p class="delete-application-dialog__lead">确定删除这条报名申请吗？删除后不可恢复。</p>
        <div class="delete-application-dialog__summary reset-password-summary dialog-summary-shell">
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

    <RecruitmentPortalApplicationDrawer
      v-model="applicationDetailVisible"
      :detail="viewingApplication"
      :workflow-task="isAdvisorScreeningSection ? null : viewingApplicationWorkflowTask"
      :enable-screening-tools="!isAdvisorScreeningSection"
      :hide-preference-details="isAdvisorScreeningSection"
      :workflow-task-loading="isAdvisorScreeningSection ? false : applicationWorkflowTaskLoading"
      :action-loading="applicationWorkflowActionSubmitting"
      @execute-action="handleViewingApplicationWorkflowAction"
      @submit-advisor-screening="handleAdvisorScreeningSubmit"
      @confirm-initial-screening="handleInitialScreeningConfirmation"
    />

    <el-dialog
      v-model="applicationWorkflowCommentDialogVisible"
      :title="pendingViewingApplicationWorkflowAction ? pendingViewingApplicationWorkflowAction.label : '审批处理'"
      width="640px"
      destroy-on-close
      @closed="resetApplicationWorkflowCommentDialog"
    >
      <div class="dialog-form reset-password-dialog workflow-comment-dialog">
        <p class="workflow-comment-dialog__hint">请输入审批意见，可留空后直接提交。</p>
        <el-input
          v-model="applicationWorkflowComment"
          type="textarea"
          :rows="5"
          maxlength="500"
          show-word-limit
          placeholder="审批意见（可选）"
        />
      </div>
      <template #footer>
        <el-button @click="applicationWorkflowCommentDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="applicationWorkflowActionSubmitting" @click="submitApplicationWorkflowCommentDialog">
          {{ pendingViewingApplicationWorkflowAction?.label || '确认' }}
        </el-button>
      </template>
    </el-dialog>

    <el-dialog
      v-model="advisorScreeningBatchConfirmDialogVisible"
      title="批量提交确认"
      width="640px"
      destroy-on-close
      class="recruitment-confirm-dialog"
      :close-on-click-modal="!applicationWorkflowActionSubmitting"
      :close-on-press-escape="!applicationWorkflowActionSubmitting"
      :show-close="!applicationWorkflowActionSubmitting"
      @closed="closeAdvisorBatchSubmitDialog"
    >
      <div v-if="advisorBatchSubmitSummary.length" class="dialog-form reset-password-dialog management-confirm-dialog">
        <p class="management-confirm-dialog__lead">将一次性提交 {{ advisorBatchSubmitSummary.length }} 条导师初筛记录，确认后立即生效。</p>
        <div class="management-confirm-dialog__summary reset-password-summary dialog-summary-shell">
          <div>
            <span class="management-confirm-dialog__label">已选数量</span>
            <strong>{{ advisorBatchSubmitSummary.length }}</strong>
          </div>
          <div>
            <span class="management-confirm-dialog__label">判定规则</span>
            <strong>80 分及以上通过</strong>
          </div>
          <div style="grid-column: span 2;">
            <span class="management-confirm-dialog__label">提醒</span>
            <strong>提交后将同步更新导师初筛结果，请再次核对分数。</strong>
          </div>
        </div>
        <div class="management-confirm-dialog__summary reset-password-summary dialog-summary-shell">
          <div v-for="item in advisorBatchSubmitSummary" :key="item.application_id">
            <span class="management-confirm-dialog__label">{{ item.student_name }}</span>
            <strong>{{ item.business_key }} / {{ item.advisor_score ?? '未填写' }} / {{ formatAdvisorScreeningAutoResult(item.advisor_score) }}</strong>
          </div>
        </div>
        <div v-if="advisorBatchMissingScoreRows.length" class="management-confirm-dialog__summary management-confirm-dialog__summary--warning reset-password-summary dialog-summary-shell">
          <div style="grid-column: span 2;">
            <span class="management-confirm-dialog__label">未填写分数</span>
            <strong>以下记录还没有填写分数，不能提交：</strong>
          </div>
          <div v-for="item in advisorBatchMissingScoreRows" :key="item.id">
            <span class="management-confirm-dialog__label">{{ item.student_name }}</span>
            <strong>{{ item.business_key }}</strong>
          </div>
        </div>
        <div v-if="advisorBatchLockedRows.length" class="management-confirm-dialog__summary management-confirm-dialog__summary--warning reset-password-summary dialog-summary-shell">
          <div style="grid-column: span 2;">
            <span class="management-confirm-dialog__label">已提交记录</span>
            <strong>以下记录已经完成导师初筛提交，不能重复操作：</strong>
          </div>
          <div v-for="item in advisorBatchLockedRows" :key="item.id">
            <span class="management-confirm-dialog__label">{{ item.student_name }}</span>
            <strong>{{ item.business_key }}</strong>
          </div>
        </div>
        <p class="management-confirm-dialog__hint">
          <span v-if="advisorBatchMissingScoreRows.length || advisorBatchLockedRows.length">请先处理上面的提示项后再提交。</span>
          <span v-else>确认后操作将立即生效，请再次核对上面的分数与判定结果。</span>
        </p>
      </div>
      <template #footer>
        <el-button :disabled="applicationWorkflowActionSubmitting" @click="closeAdvisorBatchSubmitDialog">取消</el-button>
        <el-button type="primary" :loading="applicationWorkflowActionSubmitting" :disabled="!advisorBatchCanSubmit" @click="submitAdvisorBatchScreening">确认提交</el-button>
      </template>
    </el-dialog>

    <el-dialog
      v-model="initialScreeningBatchConfirmDialogVisible"
      title="批量确认提交"
      width="640px"
      destroy-on-close
      class="recruitment-confirm-dialog"
      :close-on-click-modal="!applicationWorkflowActionSubmitting"
      :close-on-press-escape="!applicationWorkflowActionSubmitting"
      :show-close="!applicationWorkflowActionSubmitting"
      @closed="closeInitialScreeningBatchConfirmDialog"
    >
      <div v-if="selectedInitialScreeningRows.length" class="dialog-form reset-password-dialog initial-screening-batch-dialog">
        <p class="initial-screening-batch-dialog__lead">将一次性提交 {{ selectedInitialScreeningRows.length }} 条初筛确认记录，确认后立即生效。</p>
        <div class="initial-screening-batch-dialog__summary reset-password-summary dialog-summary-shell">
          <div>
            <span class="initial-screening-batch-dialog__label">已选数量</span>
            <strong>{{ selectedInitialScreeningRows.length }}</strong>
          </div>
          <div>
            <span class="initial-screening-batch-dialog__label">操作说明</span>
            <strong>请先在表格里选择通过/不通过并填写意见</strong>
          </div>
          <div>
            <span class="initial-screening-batch-dialog__label">提醒</span>
            <strong>确认后将立即提交初筛结果，请再次核对</strong>
          </div>
        </div>
        <div class="initial-screening-batch-dialog__summary reset-password-summary dialog-summary-shell">
          <div v-for="item in selectedInitialScreeningRows" :key="item.id">
            <span class="initial-screening-batch-dialog__label">{{ item.student_name }}</span>
            <strong>{{ item.business_key }} / {{ item.initial_screening_result || '待确认' }}</strong>
          </div>
        </div>
        <p class="initial-screening-batch-dialog__hint">确认后操作将立即生效，请再次核对上面的确认结论与意见。</p>
      </div>
      <template #footer>
        <el-button :disabled="applicationWorkflowActionSubmitting" @click="closeInitialScreeningBatchConfirmDialog">取消</el-button>
        <el-button type="primary" :loading="applicationWorkflowActionSubmitting" @click="confirmInitialScreeningBatch">确认提交</el-button>
      </template>
    </el-dialog>
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

.workflow-comment-dialog {
  display: grid;
  gap: 16px;
}

.workflow-comment-dialog__hint {
  margin: 0;
  color: #606266;
  line-height: 1.7;
}

.delete-application-dialog__lead {
  margin: 0;
  color: #475569;
  line-height: 1.7;
}

.delete-application-dialog__summary {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
  padding: 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #f8fafc;
}

.dialog-summary-shell {
  box-shadow: none;
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

.table-row-actions--centered {
  justify-content: center;
}

.advisor-screening-tabs {
  display: grid;
  gap: 12px;
  margin-bottom: 8px;
}

.advisor-screening-tabs__nav :deep(.el-tabs__header) {
  margin: 0;
}

.advisor-screening-submitted-tag {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 28px;
  padding: 0 10px;
  border-radius: 999px;
  background: #eef2ff;
  color: #3b82f6;
  font-size: 12px;
  font-weight: 600;
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

.advisor-screening-floating-action {
  position: fixed;
  top: 108px;
  right: 24px;
  z-index: 40;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  border: 1px solid rgba(18, 50, 95, 0.12);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 12px 30px rgba(18, 50, 95, 0.14);
  backdrop-filter: blur(10px);
}

.advisor-screening-floating-action__hint {
  color: var(--el-text-color-secondary);
  font-size: 12px;
  white-space: nowrap;
}

@media (max-width: 1280px) {
  .advisor-screening-floating-action {
    top: auto;
    bottom: 20px;
    right: 16px;
    left: 16px;
    justify-content: space-between;
    border-radius: 18px;
  }
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

.advisor-batch-toolbar {
  display: flex;
  justify-content: space-between;
  gap: 14px;
  align-items: center;
  margin-top: 14px;
  padding: 14px 16px;
  border: 1px dashed rgba(18, 50, 95, 0.18);
  border-radius: 16px;
  background: linear-gradient(135deg, rgba(245, 248, 255, 0.96), rgba(255, 249, 235, 0.92));
}

.advisor-batch-toolbar__summary {
  display: grid;
  gap: 4px;
}

.advisor-batch-toolbar__summary strong {
  color: #12315e;
}

.advisor-batch-toolbar__summary span {
  color: #60718f;
  font-size: 12px;
}

.advisor-screening-submitted-panel {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 8px 0 4px;
}

.advisor-screening-submitted-panel__filter {
  gap: 12px;
}

.advisor-screening-submitted-panel__summary {
  color: #60718f;
  font-size: 12px;
}

.advisor-screening-rescore-dialog {
  display: grid;
  gap: 16px;
}

.advisor-screening-rescore-dialog__lead {
  margin: 0;
  color: #475569;
  line-height: 1.7;
}

.advisor-screening-rescore-notice {
  display: grid;
  gap: 12px;
}

.signature-batch-dialog {
  display: grid;
  gap: 14px;
}

.signature-batch-dialog__hint {
  margin: 0;
  color: #4e6381;
  line-height: 1.7;
}

.advisor-signature-canvas {
  width: 100%;
  height: 240px;
  border: 1px dashed rgba(28, 78, 146, 0.24);
  border-radius: 16px;
  background: #ffffff;
  touch-action: none;
}

.signature-batch-dialog__actions {
  display: flex;
  justify-content: flex-end;
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
  .header-actions,
  .advisor-batch-toolbar {
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
