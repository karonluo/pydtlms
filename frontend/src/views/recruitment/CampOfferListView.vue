<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import { MoreFilled, Promotion, Check, CircleClose, EditPen, ArrowDown, ArrowUp } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'

import { getRecruitmentOptions, getRecruitmentPortalApplicationDetail, type RecruitPortalApplicationDetail, type RecruitmentOptions } from '../../api/recruitment'
import { useServerPagination } from '../../composables/useServerPagination'
import {
  createCampOffer,
  deleteCampOffer,
  deleteOfferTemplate,
  exportCampOffers,
  fetchOfferTemplatePreview,
  getCampOfferStats,
  acceptCampOffer,
  declineCampOffer,
  importCampOffers,
  importHackathonScores,
  markCampOfferPending,
  listCampOffers,
  listOfferTemplates,
  listRecruitmentPlans,
  sendCampOfferNotification,
  updateCampOffer,
  uploadOfferTemplate,
  type CampOfferNotificationSendResponse,
  type CampOfferRecord,
  type CampOfferStats,
  type HackathonScoreImportResult,
  type CampOfferUpsert,
  type OfferTemplateRecord,
  type RecruitPlanRecord,
} from '../../api/recruitment'
import { listCenters } from '../../api/students'
import { listDictData, type DictDataRecord } from '../../api/system'
import { useAuthStore } from '../../stores/auth'
import RecruitmentPortalApplicationDrawer from '../../components/recruitment/RecruitmentPortalApplicationDrawer.vue'

type OfferTemplateId = string | number

type ScoreOp = "eq" | "ne" | "gt" | "ge" | "lt" | "le"

type FilterState = {
  keyword: string
  plan_id: number | null
  is_sent_mail: '' | 'true' | 'false'
  is_agree: '' | 'true' | 'false'
  first_choice_advisor: string
  first_choice_team: string
  first_choice_score_op: '' | ScoreOp
  first_choice_score: number | null
  second_choice_advisor: string
  second_choice_team: string
  second_choice_score_op: '' | ScoreOp
  second_choice_score: number | null
}


type DialogMode = 'create' | 'edit'

const loading = ref(false)
const saving = ref(false)
const importing = ref(false)
const exporting = ref(false)
const statsLoading = ref(false)
const campOfferStats = ref<CampOfferStats | null>(null)
const filterCollapsed = ref(false)

function toggleFilterCollapsed() {
  filterCollapsed.value = !filterCollapsed.value
}
const dialogVisible = ref(false)
const dialogMode = ref<DialogMode>('create')
const currentOfferId = ref<number | null>(null)
const offers = ref<CampOfferRecord[]>([])
const plans = ref<RecruitPlanRecord[]>([])
const selectedOfferIds = ref<number[]>([])
const sortBy = ref<string>('')
const sortOrder = ref<'asc' | 'desc'>('desc')

const notifyDialogVisible = ref(false)
const notifySubmitting = ref(false)
const notifyResult = ref<CampOfferNotificationSendResponse | null>(null)

const authStore = useAuthStore()
const roleSet = computed(() => new Set(authStore.roles || []))
// 2026-07-03: 白名单用户(平台管理员 + 书院管理员), 只有他们可见'评分导入'等写操作按钮
const isWhiteListUser = computed(() => roleSet.value.has('platform_admin') || roleSet.value.has('AILABMGT'))

// 2026-07-04: 判断一行入营名单是否已导入「夏令营评分/评语」。
// 规则: hackathon_score 和 hackathon_comments 都不为空 (即不 NULL 不空字符串) 时返回 true。
// 用于控制 录取/不录取/待定 3 个按钮的可见性: 未导入评分的行不允许操作。
function rowHasHackathonEvaluation(row: CampOfferRecord | null | undefined): boolean {
  if (!row) return false
  const score = row.hackathon_score
  const comment = row.hackathon_comments
  const scoreFilled = score !== null && score !== undefined && !Number.isNaN(score)
  const commentFilled = typeof comment === 'string' && comment.trim().length > 0
  return scoreFilled && commentFilled
}

// 2026-07-04: 操作列宽度自适应。
// 计算策略: 遍历当前页 offers, 统计每行可见的按钮数量, 取最大者, 加上间距/padding。
//   - 每个按钮: 100px (中文文本宽度估算, 例如 "查看学生详情" / "录取")
//   - 按钮间距: 8px
//   - 下拉/更多: 80px
//   - 列内 padding: 24px (左右各 12px)
//   - 最小宽度 100, 最大宽度 540
const ACTIONS_BUTTON_WIDTH = 100
const ACTIONS_DROPDOWN_WIDTH = 80
const ACTIONS_BUTTON_GAP = 8
const ACTIONS_COLUMN_PADDING = 24
const ACTIONS_COLUMN_MIN_WIDTH = 100
const ACTIONS_COLUMN_MAX_WIDTH = 360

function computeRowActionButtonCount(row: CampOfferRecord): number {
  // 与模板内的 v-if 保持一致
  let count = 0
  // "查看学生详情" 永远可见
  count += 1
  // 录取/不录取/待定
  if (row.can_change_accepted && rowHasHackathonEvaluation(row)) {
    count += 3
  }
  return count
}

function computeRowHasDropdown(row: CampOfferRecord): boolean {
  // 当 3 个操作按钮不显示时, 才显示 "更多" dropdown
  return !(row.can_change_accepted && rowHasHackathonEvaluation(row))
}

const actionsColumnWidth = computed(() => {
  if (!Array.isArray(offers.value) || offers.value.length === 0) {
    return ACTIONS_COLUMN_MIN_WIDTH
  }
  let maxButtons = 0
  let anyHasDropdown = false
  for (const row of offers.value) {
    const cnt = computeRowActionButtonCount(row)
    if (cnt > maxButtons) maxButtons = cnt
    if (computeRowHasDropdown(row)) anyHasDropdown = true
  }
  // 宽度 = 按钮总和 + 间距*(按钮数-1) + dropdown + padding
  const buttonArea = maxButtons * ACTIONS_BUTTON_WIDTH
  const gap = maxButtons > 1 ? (maxButtons - 1) * ACTIONS_BUTTON_GAP : 0
  const dropdown = anyHasDropdown ? ACTIONS_DROPDOWN_WIDTH : 0
  // dropdown 与最后一个按钮之间再加一个 gap
  const dropdownGap = anyHasDropdown ? ACTIONS_BUTTON_GAP : 0
  let total = buttonArea + gap + dropdown + dropdownGap + ACTIONS_COLUMN_PADDING
  if (total < ACTIONS_COLUMN_MIN_WIDTH) total = ACTIONS_COLUMN_MIN_WIDTH
  if (total > ACTIONS_COLUMN_MAX_WIDTH) total = ACTIONS_COLUMN_MAX_WIDTH
  return total
})

// 2026-07-01 黑客松入取状态字典选项
const hackathonAcceptedOptions = ref<{ label: string; value: string; colorType: string }[]>([])
async function loadHackathonAcceptedDict() {
  try {
    const response = await listDictData({ dict_type: 'hackathon_accepted_status', status: '启用', page_size: 1000 })
    hackathonAcceptedOptions.value = (response.data.items || [])
      .map((item: DictDataRecord) => ({
        label: item.label,
        value: item.value,
        colorType: item.color_type || 'info',
      }))
      .sort((a, b) => {
        // 待录取(value='') 排第一；其余按 sort_order 升序
        if (a.value === '') return -1
        if (b.value === '') return 1
        return 0
      })
  } catch (error) {
    // 字典加载失败不阻塞主流程
    console.warn('加载黑客松入取状态字典失败:', error)
  }
}

// 2026-07-06: 录取学校字典选项 (字典类型 admission_offered_school)
const admissionOfferedSchoolOptions = ref<{ label: string; value: string }[]>([])
async function loadAdmissionOfferedSchoolDict() {
  try {
    const response = await listDictData({ dict_type: 'admission_offered_school', status: '启用', page_size: 1000 })
    // 服务端 listDictData 已按 sort_order 升序返回，前端不再二次排序
    admissionOfferedSchoolOptions.value = (response.data.items || [])
      .map((item: DictDataRecord) => ({ label: item.label, value: item.value }))
  } catch (error) {
    // 字典加载失败不阻塞主流程
    console.warn('加载录取学校字典失败:', error)
  }
}
function getAcceptedOption(value: string | null | undefined) {
  if (!value) return { label: '待录取', value: '', colorType: 'info' }
  // 1) 优先从字典查找
  const fromDict = hackathonAcceptedOptions.value.find((item) => item.value === value)
  if (fromDict) return fromDict
  // 2) 字典未命中 (字典未加载完成 / 字典缺失该 value) 时, 用前端硬编码兜底
  //    2026-07-04: 避免出现英文 accepted_pending_send 等原始 value 直接显示在列表中
  const fallbackMap: Record<string, { label: string; colorType: string }> = {
    declined: { label: '未录取', colorType: 'danger' },
    pending: { label: '待定', colorType: 'warning' },
    accepted_pending_send: { label: '录取未发送', colorType: 'success' },
    accepted_sent: { label: '录取已发送', colorType: 'success' },
    accepted_confirmed: { label: '录取已确认', colorType: 'success' },
    accepted_rejected: { label: '录取已拒绝', colorType: 'danger' },
  }
  const fallback = fallbackMap[value]
  if (fallback) return { label: fallback.label, value, colorType: fallback.colorType }
  // 3) 实在找不到, 才显示原始 value
  return { label: value, value, colorType: 'info' }
}

// 学生填报详情弹窗（复用 /recruitment/registered-students 同款组件）
const portalApplicationDetailVisible = ref(false)
const portalViewingApplication = ref<RecruitPortalApplicationDetail | null>(null)
const portalApplicationDetailLoading = ref(false)
const notifyForm = reactive({
  template_id: 'first' as OfferTemplateId,
  simulate: false,
  simulate_recipient: '',
})
const offerTemplates = ref<OfferTemplateRecord[]>([])
const offerTemplatesLoading = ref(false)
const offerTemplateUploading = ref(false)
const previewDialogVisible = ref(false)
const previewLoading = ref(false)
const previewHtml = ref('')
const previewTitle = ref('')

const currentTemplateRecord = computed<OfferTemplateRecord | null>(() => {
  if (notifyForm.template_id === '' || notifyForm.template_id === null || notifyForm.template_id === undefined) {
    return null
  }
  return offerTemplates.value.find((item) => String(item.id) === String(notifyForm.template_id)) || null
})
const currentTemplateHint = computed(() => {
  const record = currentTemplateRecord.value
  if (!record) {
    return '请先选择一个邮件模板'
  }
  if (record.source === 'builtin') {
    return '系统内置模板 - ' + record.filename
  }
  return '自定义上传 - ' + record.filename
})
const builtinTemplateOptions = computed(() =>
  offerTemplates.value
    .filter((item) => item.source === 'builtin')
    .sort((a) => (a.builtin_key === 'first' ? -1 : 1))
    .map((item) => ({ id: item.id, label: '预置 - ' + item.filename, filename: item.filename }))
)

const uploadedTemplateOptions = computed(() =>
  offerTemplates.value
    .filter((item) => item.source === 'uploaded')
    .map((item) => ({ id: item.id, label: '自定义 - ' + item.filename, filename: item.filename }))
)

const filters = reactive<FilterState>({
  keyword: '',
  plan_id: null,
  is_sent_mail: '',
  is_agree: '',
  first_choice_advisor: '',
  first_choice_team: '',
  first_choice_score_op: '',
  first_choice_score: null,
  second_choice_advisor: '',
  second_choice_team: '',
  second_choice_score_op: '',
  second_choice_score: null,
})

const scoreOpOptions: { label: string; value: ScoreOp }[] = [
  { label: "=", value: "eq" },
  { label: "!=", value: "ne" },
  { label: ">", value: "gt" },
  { label: ">=", value: "ge" },
  { label: "<", value: "lt" },
  { label: "<=", value: "le" },
]

const teamOptions = ref<{ label: string; value: string }[]>([])
const teamOptionsLoading = ref(false)

const formRef = ref<FormInstance>()
const formModel = reactive<CampOfferUpsert>({
  candidate_no: '',
  plan_id: null,
  is_sent_mail: false,
  is_agree: null,
  reason: '',
  student_offer_submitted_at: '',
  // 2026-07-01 黑客松夏令营专用字段
  hackathon_score: null,
  hackathon_comments: '',
  accepted: null,
  // 2026-07-06: 录取学校
  admission_offered_school: '',
})

const formRules: FormRules<CampOfferUpsert> = {
  candidate_no: [{ required: true, message: '请输入报名号', trigger: 'blur' }],
}

const pager = useServerPagination(10)

const planOptions = computed(() => plans.value.map((item) => ({ label: item.plan_name, value: item.id })))

const agreeOptions = [
  { label: '全部', value: '' },
  { label: '同意', value: 'true' },
  { label: '不同意', value: 'false' },
]

const mailOptions = [
  { label: '全部', value: '' },
  { label: '已发', value: 'true' },
  { label: '未发', value: 'false' },
]

const dialogTitle = computed(() => (dialogMode.value === 'create' ? '新增入营名单' : '编辑入营名单'))

type CampOfferKpi = {
  key: 'sent_mail' | 'agreed' | 'declined' | 'unsigned'
  title: string
  status: 'healthy' | 'attention' | 'warning'
  icon: unknown
}

const KPI_DEFINITIONS: CampOfferKpi[] = [
  { key: 'sent_mail', title: '已发邮件', status: 'healthy', icon: Promotion },
  { key: 'agreed', title: '已同意', status: 'healthy', icon: Check },
  { key: 'declined', title: '不同意', status: 'attention', icon: CircleClose },
  { key: 'unsigned', title: '未签署', status: 'warning', icon: EditPen },
]

const kpiCards = computed(() =>
  KPI_DEFINITIONS.map((card) => {
    const stats = campOfferStats.value
    const fallback = statsLoading.value ? '…' : '0'
    return {
      ...card,
      value: stats ? String(stats[card.key] ?? 0) : fallback,
    }
  })
)

async function openCampOfferPortalApplicationDetail(row: CampOfferRecord) {
  if (!row.recruitment_application_id) {
    ElMessage.warning('该入营记录未关联报名详情')
    return
  }
  portalApplicationDetailLoading.value = true
  try {
    const response = await getRecruitmentPortalApplicationDetail(row.recruitment_application_id)
    portalViewingApplication.value = response.data
    portalApplicationDetailVisible.value = true
  } catch (error) {
    const message = axios.isAxiosError(error)
      ? String(error.response?.data?.detail || error.message)
      : '加载填报详情失败'
    ElMessage.error(message)
  } finally {
    portalApplicationDetailLoading.value = false
  }
}

function extractErrorMessage(error: any, fallback: string): string {
  if (axios.isAxiosError(error)) {
    const data = error.response?.data as { detail?: unknown } | undefined
    const detail = data?.detail
    if (typeof detail === 'string' && detail.trim()) {
      return detail
    }
    if (Array.isArray(detail) && detail.length) {
      const first = detail[0] as { msg?: string; loc?: unknown[] }
      const loc = Array.isArray(first?.loc) ? first.loc.join('.') : ''
      const msg = first?.msg || ''
      if (msg && loc) return `${loc}: ${msg}`
      if (msg) return msg
      return JSON.stringify(detail)
    }
    if (detail && typeof detail === 'object') {
      try {
        return JSON.stringify(detail)
      } catch {
        return fallback
      }
    }
    if (error.message) {
      return error.message
    }
  } else if (error?.message) {
    return String(error.message)
  }
  return fallback
}

function normalizeBooleanFilter(value: '' | 'true' | 'false'): boolean | undefined {
  if (value === 'true') {
    return true
  }
  if (value === 'false') {
    return false
  }
  return undefined
}

function formatDateTime(value?: string | null): string {
  const text = String(value || '').trim()
  if (!text) {
    return '-'
  }
  const normalized = text.includes('T') ? text : text.replace(' ', 'T')
  const date = new Date(normalized)
  if (Number.isNaN(date.getTime())) {
    return text
  }
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  const seconds = String(date.getSeconds()).padStart(2, '0')
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
}

function parseDateTimeInput(value?: string | null): string {
  const text = String(value || '').trim()
  if (!text) {
    return ''
  }
  return text.slice(0, 19)
}

function resetForm() {
  formModel.candidate_no = ''
  formModel.plan_id = null
  formModel.is_sent_mail = false
  formModel.is_agree = null
  formModel.reason = ''
  formModel.student_offer_submitted_at = ''
  // 2026-07-01 黑客松夏令营字段重置
  formModel.hackathon_score = null
  formModel.hackathon_comments = ''
  formModel.accepted = null
  // 2026-07-06: 录取学校
  formModel.admission_offered_school = ''
  currentOfferId.value = null
}

async function fetchPlans() {
  try {
    const response = await listRecruitmentPlans({ page: 1, page_size: 500 })
    plans.value = response.data.items || []
  } catch (error: any) {
    ElMessage.error(error?.message || '加载招生计划失败')
  }
}

const advisorOptions = ref<{ label: string; value: string }[]>([])
const advisorOptionsLoading = ref(false)
let recruitmentOptionsCache: RecruitmentOptions | null = null

async function fetchAdvisorOptions() {
  advisorOptionsLoading.value = true
  try {
    if (!recruitmentOptionsCache) {
      const response = await getRecruitmentOptions()
      recruitmentOptionsCache = response.data
    }
    advisorOptions.value = (recruitmentOptionsCache.advisor_options || []).map(
      (item) => ({ label: item.label, value: String(item.value) }),
    )
  } catch (error: any) {
    ElMessage.error(error?.message || '加载导师列表失败')
  } finally {
    advisorOptionsLoading.value = false
  }
}

async function fetchTeamOptions() {
  teamOptionsLoading.value = true
  try {
    const response = await listCenters({ page: 1, page_size: 500 })
    teamOptions.value = (response.data.items || []).map(
      (item) => ({ label: item.center_name, value: item.center_name }),
    )
  } catch (error: any) {
    ElMessage.error(error?.message || '加载中心列表失败')
  } finally {
    teamOptionsLoading.value = false
  }
}

function buildFilterParams() {
  return {
    keyword: filters.keyword || undefined,
    plan_id: typeof filters.plan_id === 'number' ? filters.plan_id : undefined,
    is_sent_mail: normalizeBooleanFilter(filters.is_sent_mail),
    is_agree: normalizeBooleanFilter(filters.is_agree),
    first_choice_advisor: filters.first_choice_advisor || undefined,
    first_choice_team: filters.first_choice_team || undefined,
    first_choice_score_op:
      filters.first_choice_score_op && filters.first_choice_score !== null
        ? filters.first_choice_score_op
        : undefined,
    first_choice_score:
      filters.first_choice_score_op && filters.first_choice_score !== null
        ? filters.first_choice_score
        : undefined,
    second_choice_advisor: filters.second_choice_advisor || undefined,
    second_choice_team: filters.second_choice_team || undefined,
    second_choice_score_op:
      filters.second_choice_score_op && filters.second_choice_score !== null
        ? filters.second_choice_score_op
        : undefined,
    second_choice_score:
      filters.second_choice_score_op && filters.second_choice_score !== null
        ? filters.second_choice_score
        : undefined,
  }
}

async function fetchCampOfferStats() {
  statsLoading.value = true
  try {
    const response = await getCampOfferStats(buildFilterParams())
    campOfferStats.value = response.data
  } catch (error: any) {
    // Stats are non-critical; surface a console warning but do not
    // interrupt the rest of the page.
    // eslint-disable-next-line no-console
    console.warn('加载入营名单统计失败', error)
  } finally {
    statsLoading.value = false
  }
}

async function fetchOffers() {
  loading.value = true
  try {
    const response = await listCampOffers({
      ...buildFilterParams(),
      sort_by: sortBy.value || undefined,
      sort_order: sortBy.value ? sortOrder.value : undefined,
      page: pager.pagination.currentPage,
      page_size: pager.pagination.pageSize,
    })
    offers.value = response.data.items || []
    pager.sync(response.data.total || 0)
  } catch (error: any) {
    ElMessage.error(error?.message || '加载入营名单失败')
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  pager.pagination.currentPage = 1
  void fetchOffers()
  void fetchCampOfferStats()
}

function handleResetFilters() {
  filters.keyword = ''
  filters.plan_id = null
  filters.is_sent_mail = ''
  filters.is_agree = ''
  filters.first_choice_advisor = ''
  filters.first_choice_team = ''
  filters.first_choice_score_op = ''
  filters.first_choice_score = null
  filters.second_choice_advisor = ''
  filters.second_choice_team = ''
  filters.second_choice_score_op = ''
  filters.second_choice_score = null
  pager.pagination.currentPage = 1
  void fetchOffers()
}

function handleOfferSelectionChange(selection: CampOfferRecord[]) {
  selectedOfferIds.value = selection.map((item) => item.id)
}

async function handleOfferSortChange({ prop, order }: { prop: string | null; order: 'ascending' | 'descending' | null }) {
  if (!prop || !order) {
    sortBy.value = ''
    sortOrder.value = 'desc'
  } else {
    sortBy.value = prop
    sortOrder.value = order === 'ascending' ? 'asc' : 'desc'
  }
  pager.pagination.currentPage = 1
  await fetchOffers()
}


function resetNotifyDialog() {
  notifyResult.value = null
  notifyForm.template_id = 'first'
  notifyForm.simulate = false
  notifyForm.simulate_recipient = ''
}

async function fetchOfferTemplates() {
  offerTemplatesLoading.value = true
  try {
    const response = await listOfferTemplates()
    offerTemplates.value = response.data.items || []
  } catch (error: any) {
    ElMessage.error(error?.message || '加载邮件模板失败')
  } finally {
    offerTemplatesLoading.value = false
  }
}

function resolveChoiceFromTemplateId(id: OfferTemplateId): 'first' | 'second' {
  const record = offerTemplates.value.find((item) => String(item.id) === String(id))
  if (record?.builtin_key === 'second') {
    return 'second'
  }
  return 'first'
}

async function handleUploadTemplate(file: File): Promise<boolean> {
  if (!file) {
    return false
  }
  const lowerName = file.name.toLowerCase()
  if (!(lowerName.endsWith('.md') || lowerName.endsWith('.markdown'))) {
    ElMessage.error('仅支持上传 .md / .markdown 文件')
    return false
  }
  if (file.size > 1024 * 1024) {
    ElMessage.error('模板文件大小不能超过 1 MB')
    return false
  }
  offerTemplateUploading.value = true
  try {
    const response = await uploadOfferTemplate(file)
    ElMessage.success('模板已上传')
    await fetchOfferTemplates()
    notifyForm.template_id = response.data.id
  } catch (error: any) {
    ElMessage.error(extractErrorMessage(error, '上传失败'))
  } finally {
    offerTemplateUploading.value = false
  }
  return false
}

async function handlePreviewTemplate() {
  const record = currentTemplateRecord.value
  if (!record) {
    ElMessage.warning('请先选择要预览的模板')
    return
  }
  previewDialogVisible.value = true
  previewLoading.value = true
  previewTitle.value = record.display_name
  previewHtml.value = ''
  try {
    const response = await fetchOfferTemplatePreview(record.id)
    previewHtml.value = String(response.data || '')
  } catch (error: any) {
    previewDialogVisible.value = false
    ElMessage.error(extractErrorMessage(error, '预览失败'))
  } finally {
    previewLoading.value = false
  }
}

async function handleDeleteTemplateById(id: string | number) {
  const record = offerTemplates.value.find((item) => String(item.id) === String(id))
  if (!record || record.source !== "uploaded") {
    return
  }
  try {
    await ElMessageBox.confirm(
      `确定要删除自定义模板 “${record.display_name}” 吗？删除后无法恢复。`,
      "删除确认",
      { type: "warning", confirmButtonText: "删除", cancelButtonText: "取消" },
    )
  } catch {
    return
  }
  try {
    await deleteOfferTemplate(record.id)
    ElMessage.success("模板已删除")
    await fetchOfferTemplates()
    if (String(notifyForm.template_id) === String(record.id)) {
      notifyForm.template_id = "first"
    }
  } catch (error: any) {
    ElMessage.error(extractErrorMessage(error, "删除失败"))
  }
}

// ------------------------------------------------------------------
// 2026-07-03: 黑客松入取状态变更 (录取/不录取/待定) - 二次确认 + 调用 API + 刷新
// ------------------------------------------------------------------
/** 操作列"录取/不录取/待定"的统一入口 (带 ElMessageBox 二次确认)。
 *  action: 'accept' | 'decline' | 'pending"
 *  服务端使用 3 个独立端点，前端也按 action 区分提示文案与状态值。
 */
async function confirmAndChangeAccepted(row: CampOfferRecord, action: 'accept' | 'decline' | 'pending') {
  if (!row || !row.id) {
    ElMessage.warning('记录无效，无法操作')
    return
  }
  // 2026-07-04: 二次确认对话框样式, 仿照上传图标的效果 (信息卡片 + 黄色提示条)
  // 标题: 颜色方块图标 + 标题文字
  // 信息卡片: 学生姓名 + 评分(按动作配色) + 评语
  // 黄色提示条: 提示动作后果
  // 主按钮: 按动作语义配色
  interface ActionStyle {
    title: string
    iconColor: string
    iconChar: string
    iconTextColor: string
    scoreColor: string
    tipText: string
    confirmText: string
    confirmButtonColor: string
    successMsg: string
    apiCall: (id: number) => Promise<unknown>
  }
  const actionStyles: Record<typeof action, ActionStyle> = {
    accept: {
      title: "确认录取",
      iconColor: "#e1f3d8",
      iconChar: "✓",
      iconTextColor: "#67c23a",
      scoreColor: "#409eff",
      tipText: "确认后该学生将被标记为「录取」状态。",
      confirmText: "确认录取",
      confirmButtonColor: "#67c23a",
      successMsg: "已录取",
      apiCall: (id) => acceptCampOffer(id),
    },
    decline: {
      title: "确认不录取",
      iconColor: "#fde2e2",
      iconChar: "×",
      iconTextColor: "#f56c6c",
      scoreColor: "#f56c6c",
      tipText: "确认后该学生将被标记为「不录取」状态, 此操作不可撤销。",
      confirmText: "确认不录取",
      confirmButtonColor: "#f56c6c",
      successMsg: "已标记不录取",
      apiCall: (id) => declineCampOffer(id),
    },
    pending: {
      title: "确认为待定",
      iconColor: "#fdf6d8",
      iconChar: "□",
      iconTextColor: "#e6a23c",
      scoreColor: "#e6a23c",
      tipText: "确认后该学生将被标记为「待定」状态, 后续可再次操作。",
      confirmText: "确认为待定",
      confirmButtonColor: "#e6a23c",
      successMsg: "已标记待定",
      apiCall: (id) => markCampOfferPending(id),
    },
  }
  const cfg = actionStyles[action]
  const candidate = String(row.candidate_no || "").trim() || "该学生"
  const studentName = String(row.student_name || "").trim() || candidate
  const score = row.hackathon_score !== null && row.hackathon_score !== undefined ? row.hackathon_score : "-"
  const comment = String(row.hackathon_comments || "").trim() || "暂无评语"
  function escapeHtml(s: string): string {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;")
  }
  const messageHtml = `
    <div class="camp-offer-confirm">
      <div class="camp-offer-confirm__header">
        <span class="camp-offer-confirm__icon" style="background: ${cfg.iconColor}; color: ${cfg.iconTextColor};">${cfg.iconChar}</span>
        <span class="camp-offer-confirm__heading">${escapeHtml(cfg.title)}</span>
      </div>
      <div class="camp-offer-confirm__card">
        <div class="camp-offer-confirm__name">${escapeHtml(studentName)}</div>
        <div class="camp-offer-confirm__divider"></div>
        <div class="camp-offer-confirm__row">
          <span class="camp-offer-confirm__label">夏令营评分</span>
          <span class="camp-offer-confirm__score" style="color: ${cfg.scoreColor};">${escapeHtml(String(score))}</span>
        </div>
        <div class="camp-offer-confirm__row camp-offer-confirm__row--block">
          <span class="camp-offer-confirm__label">夏令营评语</span>
          <span class="camp-offer-confirm__comment">${escapeHtml(comment)}</span>
        </div>
      </div>
      <div class="camp-offer-confirm__tip">⚠  ${escapeHtml(cfg.tipText)}</div>
    </div>
  `
  try {
    await ElMessageBox.confirm(
      messageHtml,
      cfg.title,
      {
        confirmButtonText: cfg.confirmText,
        cancelButtonText: "取消",
        confirmButtonClass: "el-button--custom-" + action,
        dangerouslyUseHTMLString: true,
        customClass: "camp-offer-confirm-box camp-offer-confirm-box--" + action,
      },
    )
  } catch {
    // 用户取消
    return
  }
  try {
    await cfg.apiCall(Number(row.id))
    ElMessage.success(`${cfg.successMsg} (${candidate})`)
    // 刷新当前页
    await fetchOffers()
    await fetchCampOfferStats()
  } catch (error: any) {
    const message = axios.isAxiosError(error)
      ? String(error.response?.data?.detail || error.message)
      : '操作失败'
    ElMessage.error(message)
  }
}

/** 操作列"更多"下拉 (目前只有删除) 的命令处理。 */
function runMoreAction(key: string, row: CampOfferRecord) {
  if (key === 'delete') {
    void handleDelete(row)
  }
}

// ------------------------------------------------------------------
// ------------------------------------------------------------------
// 2026-07-03: 黑客松夏令营专用工具栏按钮
// - 评分导入: 已对接后端 (通过 手机号+邮箱 联合匹配, 仅更新 hackathon_score/comments)
// - 上传录取学校 / 发送录取通知: 后续实现
// ------------------------------------------------------------------

// 评分导入 弹窗状态
const hackathonImportDialogVisible = ref(false)
const hackathonImportFile = ref<File | null>(null)
const hackathonImporting = ref(false)
const hackathonImportResult = ref<HackathonScoreImportResult | null>(null)
const hackathonImportFileInputRef = ref<HTMLInputElement | null>(null)

// 触发文件选择: 通过隐藏的 input[type=file]
function onHackathonScoreImport() {
  hackathonImportResult.value = null
  hackathonImportFile.value = null
  hackathonImportDialogVisible.value = true
}

function onHackathonImportFileChange(event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files && target.files[0] ? target.files[0] : null
  hackathonImportFile.value = file
  // 重置 input, 允许同名文件再次选择
  if (target) target.value = ''
}

async function submitHackathonImport() {
  if (!hackathonImportFile.value) {
    ElMessage.warning('请先选择 Excel 文件')
    return
  }
  hackathonImporting.value = true
  try {
    const response = await importHackathonScores(hackathonImportFile.value)
    hackathonImportResult.value = response.data
    const r = response.data
    if (r.matched_count > 0) {
      ElMessage.success(`评分导入完成: 匹配 ${r.matched_count} 行, 未匹配 ${r.unmatched_count} 行`)
      // 刷新列表
      pager.pagination.currentPage = 1
      await fetchOffers()
    } else if (r.total_rows === 0) {
      ElMessage.warning('Excel 文件中没有可导入的数据行')
    } else {
      ElMessage.warning('评分导入完成: 无任何匹配行, 请检查手机号/邮箱是否正确')
    }
  } catch (error: any) {
    ElMessage.error(error?.response?.data?.detail || error?.message || '评分导入失败')
  } finally {
    hackathonImporting.value = false
  }
}

function onHackathonUploadSchools() {
  // 占位: 后续将对接 '上传录取学校' 后端端点
  ElMessage.info('上传录取学校功能待后续实现')
}

function onHackathonSendNotification() {
  // 占位: 后续将对接 '发送录取通知' 后端端点 (录取通知书发送)
  ElMessage.info('发送录取通知功能待后续实现')
}


function openNotifyDialog() {
  if (!selectedOfferIds.value.length) {
    ElMessage.warning('请先勾选要发送通知的入营名单')
    return
  }
  resetNotifyDialog()
  notifyDialogVisible.value = true
}

async function submitNotifyDialog() {
  const candidateNos = offers.value
    .filter((item) => selectedOfferIds.value.includes(item.id))
    .map((item) => String(item.candidate_no || '').trim())
    .filter((value) => value)
  if (!candidateNos.length) {
    ElMessage.warning('所选记录缺少报名号，无法发送通知')
    return
  }
  if (notifyForm.simulate && !notifyForm.simulate_recipient.trim()) {
    ElMessage.warning('请填写模拟收件邮箱')
    return
  }
  notifySubmitting.value = true
  try {
    const response = await sendCampOfferNotification({
      candidate_nos: candidateNos,
      choice: resolveChoiceFromTemplateId(notifyForm.template_id),
      template_id: notifyForm.template_id,
      simulate: notifyForm.simulate,
      simulate_recipient: notifyForm.simulate ? notifyForm.simulate_recipient.trim() : null,
    })
    notifyResult.value = response.data
    ElMessage.success(response.data.message || '通知邮件已发送')
    await fetchOffers()
  } catch (error: any) {
    ElMessage.error(extractErrorMessage(error, '发送失败'))
  } finally {
    notifySubmitting.value = false
  }
}

function handlePageChange(page: number) {
  pager.handleCurrentChange(page)
  void fetchOffers()
}

function handlePageSizeChange(size: number) {
  pager.handleSizeChange(size)
  void fetchOffers()
}

function openCreateDialog() {
  dialogMode.value = 'create'
  resetForm()
  dialogVisible.value = true
}

function openEditDialog(row: CampOfferRecord) {
  dialogMode.value = 'edit'
  currentOfferId.value = row.id
  formModel.candidate_no = row.candidate_no || ''
  formModel.plan_id = row.plan_id || null
  formModel.is_sent_mail = Boolean(row.is_sent_mail)
  formModel.is_agree = row.is_agree ?? null
  formModel.reason = row.reason || ''
  formModel.student_offer_submitted_at = parseDateTimeInput(row.student_offer_submitted_at)
  // 2026-07-01 黑客松夏令营字段回填
  formModel.hackathon_score = typeof row.hackathon_score === 'number' ? row.hackathon_score : null
  formModel.hackathon_comments = row.hackathon_comments || ''
  formModel.accepted = row.accepted || null
  // 2026-07-06: 录取学校
  formModel.admission_offered_school = row.admission_offered_school || ''
  dialogVisible.value = true
}

async function submitDialog() {
  if (!formRef.value) {
    return
  }
  try {
    await formRef.value.validate()
  } catch {
    return
  }

  saving.value = true
  try {
    const payload: CampOfferUpsert = {
      candidate_no: String(formModel.candidate_no || '').trim(),
      plan_id: formModel.plan_id ?? null,
      is_sent_mail: Boolean(formModel.is_sent_mail),
      is_agree: formModel.is_agree,
      reason: String(formModel.reason || '').trim() || null,
      student_offer_submitted_at: String(formModel.student_offer_submitted_at || '').trim() || null,
      // 2026-07-03: 黑客松夏令营字段, 之前漏传导致后端写库为 NULL
      hackathon_score: formModel.hackathon_score === null || formModel.hackathon_score === undefined ? null : Number(formModel.hackathon_score),
      hackathon_comments: String(formModel.hackathon_comments || '').trim() || null,
      accepted: formModel.accepted || null,
      // 2026-07-06: 录取学校
      admission_offered_school: String(formModel.admission_offered_school || '').trim() || null,
    }

    if (dialogMode.value === 'create') {
      await createCampOffer(payload)
      ElMessage.success('新增成功')
    } else {
      if (!currentOfferId.value) {
        throw new Error('缺少记录 ID')
      }
      await updateCampOffer(currentOfferId.value, payload)
      ElMessage.success('更新成功')
    }
    dialogVisible.value = false
    pager.pagination.currentPage = 1
    await fetchOffers()
  } catch (error: any) {
    ElMessage.error(error?.message || '保存失败')
  } finally {
    saving.value = false
  }
}

async function handleDelete(row: CampOfferRecord) {
  try {
    await ElMessageBox.confirm(
      `确定删除报名号 ${row.candidate_no || '-'} 的入营名单记录吗？`,
      '删除确认',
      {
        type: 'warning',
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
      },
    )
    await deleteCampOffer(row.id)
    ElMessage.success('删除成功')
    await fetchOffers()
  } catch (error: any) {
    if (error === 'cancel' || error === 'close') {
      return
    }
    ElMessage.error(error?.message || '删除失败')
  }
}

async function handleImportUpload(file: File): Promise<boolean> {
  importing.value = true
  try {
    const response = await importCampOffers(file, filters.plan_id ?? undefined)
    const message = `导入完成：成功 ${response.data.imported_count} 条，跳过 ${response.data.skipped_count} 条`
    ElMessage.success(message)
    if (response.data.issues?.length) {
      const firstIssue = response.data.issues[0]
      ElMessage.warning(`首条跳过原因：第 ${firstIssue.row_number} 行，${firstIssue.reason}`)
    }
    pager.pagination.currentPage = 1
    await fetchOffers()
  } catch (error: any) {
    ElMessage.error(error?.message || '导入失败')
  } finally {
    importing.value = false
  }
  return false
}

function normalizeBooleanFilterForExport(value: '' | 'true' | 'false'): boolean | undefined {
  if (value === 'true') return true
  if (value === 'false') return false
  return undefined
}

async function handleExportList() {
  exporting.value = true
  try {
    const response = await exportCampOffers({
      keyword: filters.keyword || undefined,
      plan_id: typeof filters.plan_id === 'number' ? filters.plan_id : undefined,
      is_sent_mail: normalizeBooleanFilterForExport(filters.is_sent_mail),
      is_agree: normalizeBooleanFilterForExport(filters.is_agree),
      first_choice_advisor: filters.first_choice_advisor || undefined,
      first_choice_team: filters.first_choice_team || undefined,
      first_choice_score_op:
        filters.first_choice_score_op && filters.first_choice_score !== null
          ? filters.first_choice_score_op
          : undefined,
      first_choice_score:
        filters.first_choice_score_op && filters.first_choice_score !== null
          ? filters.first_choice_score
          : undefined,
      second_choice_advisor: filters.second_choice_advisor || undefined,
      second_choice_team: filters.second_choice_team || undefined,
      second_choice_score_op:
        filters.second_choice_score_op && filters.second_choice_score !== null
          ? filters.second_choice_score_op
          : undefined,
      second_choice_score:
        filters.second_choice_score_op && filters.second_choice_score !== null
          ? filters.second_choice_score
          : undefined,
    })
    const blob = response.data instanceof Blob
      ? response.data
      : new Blob([response.data as any], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
    const downloadUrl = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = downloadUrl
    const disposition = response.headers?.['content-disposition'] || ''
    const match = disposition.match(/filename\*=UTF-8\'\'([^;]+)/i)
    link.download = decodeURIComponent((match && match[1]) || '入营名单.xlsx')
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(downloadUrl)
    ElMessage.success('已导出当前筛选的全部入营名单')
  } catch (error: any) {
    ElMessage.error(extractErrorMessage(error, '导出失败'))
  } finally {
    exporting.value = false
  }
}

onMounted(async () => {
  // 2026-07-01 加载黑客松入取状态字典(不阻塞主流程)
  void loadHackathonAcceptedDict()
  // 2026-07-06: 加载录取学校字典(不阻塞主流程)
  void loadAdmissionOfferedSchoolDict()
  await fetchPlans()
  await fetchAdvisorOptions()
  await fetchTeamOptions()
  await fetchOfferTemplates()
  await fetchCampOfferStats()
  await fetchOffers()
})
</script>

<template>
  <section class="camp-offer-page">
    <header class="camp-offer-page__header">
      <div class="camp-offer-page__title">
        <p class="camp-offer-page__tag">招生管理 / 初筛管理</p>
        <h2>入营名单</h2>
      </div>
      <div class="camp-offer-kpi-strip">
        <div
          v-for="card in kpiCards"
          :key="card.key"
          class="camp-offer-kpi-tile"
          :data-status="card.status"
          :title="card.title"
        >
          <el-icon class="camp-offer-kpi-tile__icon">
            <component :is="card.icon" />
          </el-icon>
          <span class="camp-offer-kpi-tile__value">{{ card.value }}</span>
          <span class="camp-offer-kpi-tile__label">{{ card.title }}</span>
        </div>
      </div>
      <div class="camp-offer-page__actions">
        <template v-if="isWhiteListUser">
          <el-upload
            :show-file-list="false"
            accept=".xlsx,.xls"
            :before-upload="handleImportUpload"
            :disabled="importing"
          >
            <el-button :loading="importing" type="success" plain>上传导入</el-button>
          </el-upload>
          <el-button type="warning" plain :disabled="!selectedOfferIds.length" @click="openNotifyDialog">发送通知邮件</el-button>
          <el-button type="primary" @click="openCreateDialog">新增记录</el-button>
        </template>
      </div>
    </header>
    <el-card shadow="never" class="filter-card" :class="{ 'is-collapsed': filterCollapsed }">
      <div class="filter-card__head">
        <span class="filter-card__title">筛选条件</span>
        <el-button text class="filter-card__toggle" @click="toggleFilterCollapsed">
          <span>{{ filterCollapsed ? '展开' : '收起' }}</span>
          <el-icon class="filter-card__toggle-icon">
            <component :is="filterCollapsed ? ArrowDown : ArrowUp" />
          </el-icon>
        </el-button>
      </div>
      <el-form v-show="!filterCollapsed" label-width="80px" class="filter-form">
        <div class="filter-row filter-row--primary">
          <el-form-item label="报名号/姓名" class="filter-row__item">
            <el-input v-model="filters.keyword" placeholder="报名号/姓名" clearable @keyup.enter="handleSearch" />
          </el-form-item>
          <el-form-item label="招生计划" class="filter-row__item">
            <el-select v-model="filters.plan_id" placeholder="招生计划" clearable>
              <el-option v-for="item in planOptions" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
          <el-form-item label="是否已发邮件" class="filter-row__item">
            <el-select v-model="filters.is_sent_mail" placeholder="是否已发邮件">
              <el-option v-for="item in mailOptions" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
          <el-form-item label="是否同意" class="filter-row__item">
            <el-select v-model="filters.is_agree" placeholder="是否同意">
              <el-option v-for="item in agreeOptions" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
        </div>
        <div class="filter-row filter-row--choice">
          <el-form-item v-if="isWhiteListUser" label="第一志愿导师" class="filter-row__item">
            <el-select
              v-model="filters.first_choice_advisor"
              placeholder="第一志愿导师"
              clearable
              filterable
              :loading="advisorOptionsLoading"
            >
              <el-option v-for="item in advisorOptions" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
          <el-form-item v-if="isWhiteListUser" label="第一志愿中心" class="filter-row__item">
            <el-select
              v-model="filters.first_choice_team"
              placeholder="第一志愿中心"
              clearable
              filterable
              :loading="teamOptionsLoading"
            >
              <el-option v-for="item in teamOptions" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
          <el-form-item label="第一志愿分数" class="filter-row__item">
            <div class="filter-score">
              <el-select v-model="filters.first_choice_score_op" placeholder="op" clearable class="filter-score__op">
                <el-option v-for="item in scoreOpOptions" :key="item.value" :label="item.label" :value="item.value" />
              </el-select>
              <el-input-number
                v-model="filters.first_choice_score"
                placeholder="分数"
                :min="0"
                :max="1000"
                :step="1"
                controls-position="right"
                class="filter-score__value"
              />
            </div>
          </el-form-item>
        </div>
        <div class="filter-row filter-row--choice">
          <el-form-item v-if="isWhiteListUser" label="第二志愿导师" class="filter-row__item">
            <el-select
              v-model="filters.second_choice_advisor"
              placeholder="第二志愿导师"
              clearable
              filterable
              :loading="advisorOptionsLoading"
            >
              <el-option v-for="item in advisorOptions" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
          <el-form-item v-if="isWhiteListUser" label="第二志愿中心" class="filter-row__item">
            <el-select
              v-model="filters.second_choice_team"
              placeholder="第二志愿中心"
              clearable
              filterable
              :loading="teamOptionsLoading"
            >
              <el-option v-for="item in teamOptions" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
          <el-form-item label="第二志愿分数" class="filter-row__item">
            <div class="filter-score">
              <el-select v-model="filters.second_choice_score_op" placeholder="op" clearable class="filter-score__op">
                <el-option v-for="item in scoreOpOptions" :key="item.value" :label="item.label" :value="item.value" />
              </el-select>
              <el-input-number
                v-model="filters.second_choice_score"
                placeholder="分数"
                :min="0"
                :max="1000"
                :step="1"
                controls-position="right"
                class="filter-score__value"
              />
            </div>
          </el-form-item>
        </div>
      </el-form>
      <div v-show="!filterCollapsed" class="filter-actions">
        <el-button type="primary" @click="handleSearch">查询</el-button>
        <el-button @click="handleResetFilters">重置</el-button>
      </div>
    </el-card>

    <el-card shadow="never" class="table-card">
      <!--
        2026-07-03 需求: 列表工具栏 (放在 el-card 顶部, 紧贴表格上方)
        - 左侧 (左对齐): 黑客松夏令营专用按钮 (评分导入 / 上传录取学校 / 发送录取通知)
          仅 isWhiteListUser (平台管理员+书院管理员) 时显示 (其他角色无写操作权限)
        - 右侧 (右对齐): 导出清单 (对所有角色可见)
      -->
      <div class="table-card__toolbar">
        <div class="table-card__toolbar-left" v-if="isWhiteListUser">
          <el-button type="primary" plain @click="onHackathonScoreImport">评分导入</el-button>
          <el-button type="success" plain @click="onHackathonUploadSchools">上传录取学校</el-button>
          <el-button type="warning" plain @click="onHackathonSendNotification">发送录取通知</el-button>
        </div>
        <div class="table-card__toolbar-right">
          <el-button :loading="exporting" type="primary" plain @click="handleExportList">导出清单</el-button>
        </div>
      </div>
      <el-table :data="offers" v-loading="loading" border @selection-change="handleOfferSelectionChange" @sort-change="handleOfferSortChange">
        <el-table-column type="index" label="序号" width="64" align="center">
          <template #default="scope">
            {{ (pager.pagination.currentPage - 1) * pager.pagination.pageSize + scope.$index + 1 }}
          </template>
        </el-table-column>
        <el-table-column type="selection" width="44" />
        <el-table-column prop="plan_name" label="计划名称" min-width="180" show-overflow-tooltip />
        <el-table-column prop="candidate_no" label="报名号" min-width="140" />
        <!-- 2026-07-06: 录取学校 (dtlms_plan_offer.admission_offered_school) -->
        <el-table-column prop="admission_offered_school" label="录取学校" min-width="140" show-overflow-tooltip>
          <template #default="{ row }">
            <span v-if="row.admission_offered_school">{{ row.admission_offered_school }}</span>
            <span v-else class="text-muted">-</span>
          </template>
        </el-table-column>
        <el-table-column prop="student_name" label="学生姓名" min-width="120" show-overflow-tooltip />
        <!-- 2026-07-01 黑客松夏令营专用列 -->
        <el-table-column prop="hackathon_score" label="夏令营评分" min-width="110" align="center">
          <template #default="{ row }">
            <span v-if="row.hackathon_score !== null && row.hackathon_score !== undefined">{{ row.hackathon_score }}</span>
            <span v-else class="text-muted">-</span>
          </template>
        </el-table-column>
        <el-table-column prop="hackathon_comments" label="夏令营评语" min-width="180" show-overflow-tooltip />
        <el-table-column label="入取状态" min-width="120" align="center">
          <template #default="{ row }">
            <el-tag :type="getAcceptedOption(row.accepted).colorType as any" disable-transitions>
              {{ getAcceptedOption(row.accepted).label }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="是否同意" min-width="100" align="center">
          <template #default="{ row }">
            <el-tag v-if="row.is_agree === true" type="success">同意</el-tag>
            <el-tag v-else-if="row.is_agree === false" type="danger">不同意</el-tag>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="已发邮件" min-width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="row.is_sent_mail ? 'success' : 'info'">{{ row.is_sent_mail ? '是' : '否' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="first_choice_advisor_name" label="第一志愿导师" min-width="120" show-overflow-tooltip />
        <el-table-column prop="first_choice_advisor_team_name" label="第一志愿中心" min-width="160" show-overflow-tooltip />
        <el-table-column prop="first_choice_screening_score" label="第一志愿分数" width="120" sortable="custom" align="center">
          <template #default="{ row }">
            {{ row.first_choice_screening_score ?? '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="second_choice_advisor_name" label="第二志愿导师" min-width="120" show-overflow-tooltip />
        <el-table-column prop="second_choice_advisor_team_name" label="第二志愿中心" min-width="160" show-overflow-tooltip />
        <el-table-column prop="second_choice_screening_score" label="第二志愿分数" width="120" sortable="custom" align="center">
          <template #default="{ row }">
            {{ row.second_choice_screening_score ?? '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="student_email" label="学生邮箱" min-width="180" show-overflow-tooltip />
        <el-table-column prop="student_phone" label="学生手机号" min-width="140" show-overflow-tooltip />
        <el-table-column label="学生提交日期" min-width="170">
          <template #default="{ row }">{{ formatDateTime(row.student_offer_submitted_at) }}</template>
        </el-table-column>
        <!--
          2026-07-04: 操作列宽度按可见按钮数量自适应 (actionsColumnWidth); 仅显示必要按钮。
          - 查看学生详情: 所有人可见，点击后弹窗显示 portal 详情
          - 编辑: 仅非 advisor 角色可见
          - 录取/不录取/待定: 仅 can_change_accepted=True 且 rowHasHackathonEvaluation(row)=True (hackathon_score 和 hackathon_comments 都不为空) 时可见, 否则隐藏. 2026-07-04 新增: 未导入评分的行不允许操作.
          - 删除: 移到"更多"下拉菜单，仅非 advisor 角色可见
        -->
        <el-table-column label="操作" :width="actionsColumnWidth" fixed="right" align="right">
          <template #default="{ row }">
            <div class="table-row-actions" @click.stop>
              <el-button link size="small" type="info" @click.stop="openCampOfferPortalApplicationDetail(row)">
                查看学生详情
              </el-button>
              <!-- 2026-07-03 修正: 录取/不录取/待定 按钮独立于 isWhiteListUser, 让中心负责人也能看到 (后端 SQL 已用 is_center_leader 守卫) -->
              <el-button
                v-if="row.can_change_accepted && rowHasHackathonEvaluation(row)"
                link
                size="small"
                type="success"
                @click.stop="confirmAndChangeAccepted(row, 'accept')"
              >
                录取
              </el-button>
              <el-button
                v-if="row.can_change_accepted && rowHasHackathonEvaluation(row)"
                link
                size="small"
                type="danger"
                @click.stop="confirmAndChangeAccepted(row, 'decline')"
              >
                不录取
              </el-button>
              <el-button
                v-if="row.can_change_accepted && rowHasHackathonEvaluation(row)"
                link
                size="small"
                type="warning"
                @click.stop="confirmAndChangeAccepted(row, 'pending')"
              >
                待定
              </el-button>

              <!-- 仅白名单用户 (书院管理员/平台管理员) 可见: 编辑 + 更多/删除 -->
              <template v-if="isWhiteListUser">
                <el-button link size="small" type="primary" @click.stop="openEditDialog(row)">
                  编辑
                </el-button>
                <el-dropdown v-if="!(row.can_change_accepted && rowHasHackathonEvaluation(row))" trigger="click" @command="(key: string) => runMoreAction(key, row)">
                  <el-button link size="small" type="primary" @click.stop>
                    更多
                    <el-icon><MoreFilled /></el-icon>
                  </el-button>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item command="delete" class="is-danger">删除</el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </template>
            </div>
          </template>
        </el-table-column>
      </el-table>

      <div class="table-footer">
        <el-pagination
          background
          layout="total, sizes, prev, pager, next, jumper"
          :total="pager.pagination.total"
          :current-page="pager.pagination.currentPage"
          :page-size="pager.pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          @current-change="handlePageChange"
          @size-change="handlePageSizeChange"
        />
      </div>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="640px" destroy-on-close>
      <el-form ref="formRef" :model="formModel" :rules="formRules" label-width="110px" class="dialog-form">
        <div class="dialog-grid">
          <el-form-item label="报名号" prop="candidate_no">
            <el-input v-model="formModel.candidate_no" placeholder="请输入报名号" />
          </el-form-item>
          <el-form-item label="招生计划">
            <el-select v-model="formModel.plan_id" placeholder="不填默认最新计划" clearable>
              <el-option v-for="item in planOptions" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
          <el-form-item label="是否已发邮件">
            <el-switch v-model="formModel.is_sent_mail" />
          </el-form-item>
          <el-form-item label="是否同意">
            <el-select v-model="formModel.is_agree" clearable placeholder="请选择">
              <el-option :value="true" label="同意" />
              <el-option :value="false" label="不同意" />
            </el-select>
          </el-form-item>
          <el-form-item label="学生提交日期" class="dialog-grid--full">
            <el-input
              v-model="formModel.student_offer_submitted_at"
              placeholder="格式：YYYY-MM-DD HH:mm:ss"
            />
          </el-form-item>
          <!-- 2026-07-01 黑客松夏令营专用字段 -->
          <el-form-item label="夏令营评分" class="dialog-grid--full">
            <el-input-number
              v-model="formModel.hackathon_score"
              :min="0"
              :max="100"
              :step="0.01"
              :precision="2"
              placeholder="0~100，2 位小数"
              style="width: 200px"
              clearable
            />
          </el-form-item>
          <el-form-item label="夏令营评语" class="dialog-grid--full">
            <el-input
              v-model="formModel.hackathon_comments"
              type="textarea"
              :rows="3"
              maxlength="500"
              show-word-limit
              placeholder="可选，限 500 字以内"
            />
          </el-form-item>
          <el-form-item label="入取状态" class="dialog-grid--full">
            <el-select v-model="formModel.accepted" clearable placeholder="请选择入取状态(可选)" style="width: 100%">
              <el-option
                v-for="item in hackathonAcceptedOptions"
                :key="item.value || 'empty'"
                :label="item.label"
                :value="item.value || null"
              />
            </el-select>
          </el-form-item>
          <!-- 2026-07-06: 录取学校 (字典 admission_offered_school) -->
          <el-form-item label="录取学校" class="dialog-grid--full">
            <el-select
              v-model="formModel.admission_offered_school"
              clearable
              filterable
              placeholder="请选择录取学校(可选)"
              style="width: 100%"
            >
              <el-option
                v-for="item in admissionOfferedSchoolOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="原因" class="dialog-grid--full">
            <el-input v-model="formModel.reason" type="textarea" :rows="3" maxlength="300" show-word-limit />
          </el-form-item>
        </div>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="submitDialog">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog
      v-model="notifyDialogVisible"
      title="发送通知邮件"
      width="640px"
      destroy-on-close
      :close-on-click-modal="false"
    >
      <div v-if="!notifyResult" class="notify-form">
        <p class="notify-form__lead">
          将向已选择的 {{ selectedOfferIds.length }} 条入营名单发送通知邮件。
        </p>
        <el-form label-width="110px" class="dialog-form">
          <el-form-item label="邮件模板" class="dialog-grid--full">
            <div class="notify-template-picker">
              <div class="offer-template-section">
                <div class="offer-template-section__title">预置模板</div>
                <el-radio-group v-model="notifyForm.template_id" class="offer-template-radios">
                  <el-radio
                    v-for="item in builtinTemplateOptions"
                    :key="String(item.id)"
                    :value="item.id"
                    :label="item.label"
                    border
                    class="offer-template-radio"
                  >
                    <span class="offer-template-radio__filename">{{ item.filename }}</span>
                  </el-radio>
                </el-radio-group>
              </div>

              <div v-if="isWhiteListUser" class="offer-template-section">
                <div class="offer-template-section__title">上传模板</div>
                <el-radio-group
                  v-if="uploadedTemplateOptions.length"
                  v-model="notifyForm.template_id"
                  class="offer-template-radios"
                >
                  <el-radio
                    v-for="item in uploadedTemplateOptions"
                    :key="String(item.id)"
                    :value="item.id"
                    border
                    class="offer-template-radio"
                  >
                    <span class="offer-template-radio__filename">{{ item.filename }}</span>
                    <el-button
                      type="danger"
                      link
                      class="offer-template-radio__delete"
                      @click.stop.prevent="handleDeleteTemplateById(item.id)"
                    >删除</el-button>
                  </el-radio>
                </el-radio-group>
                <div v-else class="offer-template-empty">尚未上传任何模板</div>
                <el-upload
                  :show-file-list="false"
                  :before-upload="handleUploadTemplate"
                  accept=".md,.markdown"
                  style="display: inline-flex; margin-top: 6px"
                >
                  <el-button :loading="offerTemplateUploading" plain>上传 .md</el-button>
                </el-upload>
              </div>

              <div class="offer-template-actions">
                <el-button :disabled="!currentTemplateRecord" @click="handlePreviewTemplate">预览</el-button>
                <span class="notify-form__hint">{{ currentTemplateHint }}</span>
              </div>
            </div>
          </el-form-item>
          <el-form-item label="是否模拟发送">
            <el-switch v-model="notifyForm.simulate" />
          </el-form-item>
          <el-form-item v-if="notifyForm.simulate" label="模拟收件邮箱" class="dialog-grid--full">
            <el-input v-model="notifyForm.simulate_recipient" placeholder="请输入模拟收件邮箱" />
          </el-form-item>
        </el-form>
      </div>
      <div v-else class="notify-result">
        <p class="notify-result__summary">
          {{ notifyResult.message }}
        </p>
        <p v-if="notifyResult.simulate" class="notify-result__hint">
          模拟发送：实际收件人 = {{ notifyResult.simulate_recipient || notifyForm.simulate_recipient }}
        </p>
        <p v-if="notifyResult.template_path" class="notify-result__hint">
          使用模板：{{ notifyResult.template_path }}<span v-if="notifyForm.template_id">（来自 {{ currentTemplateHint }}）</span>
        </p>
        <el-table :data="notifyResult.results" border size="small" max-height="320">
          <el-table-column prop="candidate_no" label="报名号" min-width="120" />
          <el-table-column prop="email" label="收件邮箱" min-width="180" show-overflow-tooltip />
          <el-table-column label="状态" width="90" align="center">
            <template #default="{ row }">
              <el-tag :type="row.status === 'sent' ? 'success' : 'danger'">
                {{ row.status === 'sent' ? '成功' : (row.status === 'missing' ? '未找到' : '失败') }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="error" label="错误信息" min-width="180" show-overflow-tooltip />
        </el-table>
      </div>
      <template #footer>
        <template v-if="!notifyResult">
          <el-button @click="notifyDialogVisible = false">取消</el-button>
          <el-button type="primary" :loading="notifySubmitting" @click="submitNotifyDialog">确认发送</el-button>
        </template>
        <template v-else>
          <el-button type="primary" @click="notifyDialogVisible = false">关闭</el-button>
        </template>
      </template>
    </el-dialog>

    <el-dialog
      v-model="previewDialogVisible"
      :title="`邮件模板预览 - ${previewTitle}`"
      width="720px"
      destroy-on-close
      :close-on-click-modal="false"
    >
      <div v-loading="previewLoading" class="offer-preview-wrapper">
        <p class="offer-preview-hint">
          预览中的占位符（如 <code>{candidate_no}</code>、<code>{student_name}</code>、<code>{first_choice}</code>、<code>{second_choice}</code>）会被替换为示例数据，发送时会使用真实候选人数据。
        </p>
        <div v-if="previewHtml" class="offer-preview" v-html="previewHtml"></div>
      </div>
      <template #footer>
        <el-button @click="previewDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>

    <!-- 2026-07-03: 黑客松夏令营「评分导入」弹窗
         - 限制: 仅白名单用户 (平台管理员 + 书院管理员) 可见
         - 表头: 学生手机号 / 学生邮箱 / 夏令营评分 / 夏令营评语
         - 匹配: 手机号+邮箱 联合匹配入营名单
         - 结果: 显示 matched / unmatched / issues 明细
    -->
    <el-dialog v-model="hackathonImportDialogVisible" title="夏令营评分导入" width="640px" destroy-on-close>
      <el-alert
        title="导入说明"
        type="info"
        :closable="false"
        show-icon
      >
        <template #default>
          <div>Excel 表头必须包含: 学生手机号 / 学生邮箱 / 夏令营评分 / 夏令营评语</div>
          <div>匹配规则: 学生的手机号 + 邮箱 联合匹配入营名单</div>
          <div>写入字段: 仅更新 <b>夏令营评分</b> / <b>夏令营评语</b> 两列, 不影响其他字段</div>
          <div>未匹配的行: 跳过并在下方报告, 不会报错</div>
        </template>
      </el-alert>
      <div style="margin: 16px 0;">
        <input
          ref="hackathonImportFileInputRef"
          type="file"
          accept=".xlsx,.xls"
          style="display: none"
          @change="onHackathonImportFileChange"
        />
        <el-button @click="() => hackathonImportFileInputRef?.click()">选择文件</el-button>
        <span style="margin-left: 12px; color: #909399;" v-if="hackathonImportFile">
          已选择: {{ hackathonImportFile.name }} ({{ (hackathonImportFile.size / 1024).toFixed(1) }} KB)
        </span>
        <span style="margin-left: 12px; color: #909399;" v-else>未选择文件</span>
      </div>

      <div v-if="hackathonImportResult" class="hackathon-import-result">
        <el-divider content-position="left">导入结果</el-divider>
        <el-descriptions :column="3" border size="small">
          <el-descriptions-item label="总行数">{{ hackathonImportResult.total_rows }}</el-descriptions-item>
          <el-descriptions-item label="匹配成功">
            <el-tag type="success">{{ hackathonImportResult.matched_count }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="未匹配">
            <el-tag :type="hackathonImportResult.unmatched_count > 0 ? 'warning' : 'info'">
              {{ hackathonImportResult.unmatched_count }}
            </el-tag>
          </el-descriptions-item>
        </el-descriptions>
        <div v-if="hackathonImportResult.issues.length" style="margin-top: 12px;">
          <div style="font-weight: 600; margin-bottom: 6px;">问题明细 ({{ hackathonImportResult.issues.length }} 条)</div>
          <el-table :data="hackathonImportResult.issues" size="small" border max-height="240">
            <el-table-column prop="row_number" label="行号" width="80" align="center" />
            <el-table-column prop="phone" label="手机号" width="140" />
            <el-table-column prop="email" label="邮箱" min-width="180" show-overflow-tooltip />
            <el-table-column prop="reason" label="原因" min-width="200" show-overflow-tooltip />
          </el-table>
        </div>
      </div>

      <template #footer>
        <el-button @click="hackathonImportDialogVisible = false">关闭</el-button>
        <el-button
          type="primary"
          :loading="hackathonImporting"
          :disabled="!hackathonImportFile"
          @click="submitHackathonImport"
        >开始导入</el-button>
      </template>
    </el-dialog>

    <!-- 学生填报详情弹窗（复用 /recruitment/registered-students 同款组件） -->
    <RecruitmentPortalApplicationDrawer
      v-model="portalApplicationDetailVisible"
      :detail="portalViewingApplication"
    />
  </section>
</template>

<style scoped>
.camp-offer-page {
  display: grid;
  gap: 12px;
}

.camp-offer-page__header {
  display: grid;
  /* 3 columns: title (left) | KPI strip (center, flexes) | actions (right) */
  grid-template-columns: auto 1fr auto;
  align-items: center;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #ffffff;
  padding: 14px 16px;
  gap: 16px;
}

.camp-offer-page__tag {
  margin: 0;
  color: #909399;
  font-size: 12px;
}

.camp-offer-page__header h2 {
  margin: 6px 0 0;
  color: #303133;
}

.camp-offer-page__actions {
  display: flex;
  gap: 10px;
}

.filter-card,
.table-card {
  border-radius: 8px;
}

/* Reduce el-table row height by 5px: shrink the row's height
   and pull the cell padding in. Applies to the main offers
   table only (the notify-result table uses size="small"). */
.table-card :deep(.el-table__row),
.table-card :deep(.el-table__row td) {
  height: 40px;
  padding-top: 2px;
  padding-bottom: 2px;
}

.filter-card__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
  gap: 8px;
  height: 25px;
}

/* Collapsed state: hide head bottom margin, drop card body padding
   so the total card height is exactly 45px. */
.filter-card.is-collapsed {
  --el-card-padding: 0 16px;
}

.filter-card.is-collapsed :deep(.el-card__body) {
  padding-top: 10px;
  padding-bottom: 10px;
}

.filter-card.is-collapsed .filter-card__head {
  margin-bottom: 0;
  height: 25px;
}

.filter-card__title {
  color: var(--text-subtle);
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.filter-card__toggle {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
}

.filter-card__toggle-icon {
  font-size: 14px;
  transition: transform 0.15s ease-in-out;
}

.camp-offer-kpi-strip {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  min-width: 0;
  flex-wrap: wrap;
  align-self: center;
  justify-self: center;
  height: 100%;
}

.camp-offer-kpi-tile {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  height: 32px;
  min-width: 132px;
  padding: 0 12px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  background: #ffffff;
  box-sizing: border-box;
  font-size: 13px;
  line-height: 1;
  white-space: nowrap;
}

.camp-offer-kpi-tile__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  border-radius: 6px;
  font-size: 14px;
  color: #ffffff;
  background: var(--brand);
}

.camp-offer-kpi-tile[data-status="attention"] .camp-offer-kpi-tile__icon {
  background: #f2a531;
}

.camp-offer-kpi-tile[data-status="warning"] .camp-offer-kpi-tile__icon {
  background: #ea725b;
}

.camp-offer-kpi-tile__value {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-main);
  min-width: 18px;
  text-align: center;
}

.camp-offer-kpi-tile__label {
  color: var(--text-subtle);
  font-size: 13px;
}

.filter-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-width: 0;
  width: 100%;
  box-sizing: border-box;
}

/* Each filter row is a 4-column grid. Empty trailing cells still occupy
   their column so controls line up vertically across rows. */
.filter-row {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  column-gap: 10px;
  row-gap: 10px;
  min-width: 0;
  width: 100%;
  box-sizing: border-box;
}

.filter-row--primary,
.filter-row--choice {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.filter-row__item {
  margin-bottom: 0;
  min-width: 0;
}

/* Each cell is a label (left) + control (right) with a 10px gap. The
   label is a fixed 92px wide so all labels line up; the control is a
   fixed 200px wide so every control in the same row is identical. */
.filter-form :deep(.el-form-item) {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 10px;
  margin: 0;
  min-width: 0;
  height: 32px;
  box-sizing: border-box;
}

.filter-form :deep(.el-form-item__label) {
  width: 80px;
  min-width: 80px;
  max-width: 80px;
  flex: 0 0 80px;
  text-align: left;
  justify-content: flex-start;
  white-space: nowrap;
  padding: 0;
  margin: 0;
  height: 32px;
  line-height: 32px;
  box-sizing: border-box;
  display: flex;
  align-items: center;
}

.filter-form :deep(.el-form-item__content) {
  display: flex;
  align-items: center;
  width: 200px;
  min-width: 0;
  max-width: 200px;
  flex: 0 0 200px;
  height: 32px;
  box-sizing: border-box;
}

/* Every control is exactly 200px wide inside the content cell. */
.filter-form :deep(.el-form-item__content > .el-input),
.filter-form :deep(.el-form-item__content > .el-select),
.filter-form :deep(.el-form-item__content > .el-input-number),
.filter-form :deep(.el-form-item__content > .filter-score) {
  width: 200px !important;
  flex: 0 0 200px;
  min-width: 200px;
  max-width: 200px;
}

/* OP+score combined is exactly 200px, matching one text field. */
.filter-score {
  display: flex;
  align-items: center;
  gap: 5px;
  width: 200px;
  min-width: 200px;
  max-width: 200px;
  box-sizing: border-box;
}

/* OP select: ~2x the width of one operator symbol. */
.filter-score__op {
  width: 60px;
  flex: 0 0 60px;
  min-width: 60px;
  max-width: 60px;
}

.filter-score__op :deep(.el-select__wrapper) {
  min-width: 0;
  width: 100%;
  padding-left: 4px;
  padding-right: 4px;
}

.filter-score__value {
  flex: 1 1 auto;
  min-width: 0;
  width: 135px;
  margin-left: 0;
}

.filter-score__value :deep(.el-input-number) {
  width: 100%;
  min-width: 0;
}

.filter-score__value :deep(.el-input-number .el-input-number__decrease),
.filter-score__value :deep(.el-input-number .el-input-number__increase) {
  width: 20px;
}



.filter-actions {
  margin-top: 10px;
  display: flex;
  gap: 8px;
}

.table-footer {
  margin-top: 12px;
  display: flex;
  justify-content: flex-end;
}

.dialog-form {
  padding-top: 4px;
}

.dialog-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  column-gap: 12px;
}

.dialog-grid--full {
  grid-column: 1 / -1;
}

@media (max-width: 960px) {
  .camp-offer-page__header {
    align-items: flex-start;
    flex-direction: column;
    gap: 10px;
  }

  .filter-row--primary,
  .filter-row--choice {
    grid-template-columns: 1fr;
  }

  .dialog-grid {
    grid-template-columns: 1fr;
  }
}

.notify-template-picker {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.offer-template-section {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.offer-template-section__title {
  color: #606266;
  font-size: 13px;
  font-weight: 600;
}

.offer-template-radios {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.offer-template-radio {
  margin-right: 0 !important;
  width: 100%;
  padding: 6px 12px;
}

.offer-template-radio__filename {
  margin-left: 6px;
  color: #303133;
}

.offer-template-radio__delete {
  margin-left: 8px;
  padding: 0;
}

.offer-template-empty {
  color: #909399;
  font-size: 12px;
  padding: 4px 0;
}

.offer-template-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-top: 4px;
  border-top: 1px dashed #e5e7eb;
}

.offer-template-actions .notify-form__hint {
  flex: 1;
  text-align: right;
}


.offer-preview-wrapper {
  min-height: 240px;
}

.offer-preview-hint {
  color: #909399;
  font-size: 12px;
  margin: 0 0 12px;
}

.offer-preview-hint code {
  background: #f1f5f9;
  padding: 1px 6px;
  border-radius: 4px;
  font-size: 12px;
}

.offer-preview {
  max-height: 60vh;
  overflow: auto;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 16px 20px;
  background: #ffffff;
}

.offer-preview :deep(h1) {
  font-size: 22px;
  margin-top: 0;
}
.offer-preview :deep(h2) {
  font-size: 18px;
}
.offer-preview :deep(p) {
  line-height: 1.7;
}
/* 2026-07-03: 列表上方工具栏 (左: 黑客松按钮组, 右: 导出清单) */
.table-card__toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}
.table-card__toolbar-left {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}
.table-card__toolbar-right {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-left: auto;
}



/* 二次确认对话框样式已迁到全局 src/style.css（ElMessageBox portal 到 body，scoped/:deep 都不生效） */

</style>
