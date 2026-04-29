<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

import {
  changePortalStudentPassword,
  clearPortalToken,
  getPortalProfile,
  getPortalProfileOptions,
  getPortalToken,
  listPortalPlans,
  listPortalTeams,
  savePortalApplicationDraft,
  submitPortalApplication,
  uploadPortalAttachment,
  type PortalAchievementRecordItem,
  type PortalAttachmentCategory,
  type PortalApplicantProfileData,
  type PortalApplicationDeclarationData,
  type PortalApplicationPreferenceItem,
  type PortalApplicationUpsert,
  type PortalEducationExperienceItem,
  type PortalEnglishProficiencyItem,
  type PortalFamilyMemberItem,
  type PortalPersonalStatementData,
  type PortalPasswordChangeRequest,
  type PortalPlanRecord,
  type PortalPracticeExperienceItem,
  type PortalStudentRecord,
  type PortalTeamRecord,
} from '../../api/portal'
import type { SelectOption } from '../../api/common'
import { resolveRequestError, showPortalAlert } from '../../utils/portalAlerts'

const router = useRouter()
const initializing = ref(true)
const savingDraft = ref(false)
const submitting = ref(false)
const profileDialogVisible = ref(false)
const profileSubmitting = ref(false)
const student = ref<PortalStudentRecord | null>(null)
const plans = ref<PortalPlanRecord[]>([])
const teams = ref<PortalTeamRecord[]>([])
const politicalStatusOptions = ref<SelectOption[]>([])
const ethnicGroupOptions = ref<SelectOption[]>([])
const selectedPlanId = ref<number | null>(null)
const activeSectionId = ref('plan-section')
const navElement = ref<HTMLElement | null>(null)
const navTranslateY = ref(0)
const showBackToTop = ref(false)
const quickNavOpen = ref(false)
let sectionObserver: IntersectionObserver | null = null
const navBaseTop = 96
const navMaxTranslate = 360
const attachmentUploading = reactive<Record<string, boolean>>({})
const profileForm = reactive<PortalPasswordChangeRequest & { confirm_password: string }>({
  current_password: '',
  new_password: '',
  confirm_password: '',
})

type SectionItem = {
  id: string
  label: string
  caption: string
}

type SectionGroup = {
  id: string
  label: string
  caption: string
  items: string[]
}

type PortalSectionStatus = {
  id: string
  label: string
  completed: boolean
  status: 'not-started' | 'in-progress' | 'completed'
}

const sourceChannelOptions = ['导师推荐', '实验室官网', '高校宣讲', '朋友同学推荐', '其他']
const genderOptions = ['男', '女']
const idTypeOptions = ['居民身份证', '护照', '港澳居民来往内地通行证']
const educationStageOptions = ['硕士', '硕士在读', '本科', '本科在读', '高中']
const englishExamOptions = ['CET-4', 'CET-6', 'IELTS', 'TOEFL', '其他']
const familyRelationOptions = ['父亲', '母亲', '兄', '弟', '姐', '妹', '其他']
const achievementTypeOptions = ['论文发表', '科研项目', '学生活动', '获奖经历']
const defaultPoliticalStatusOptions: SelectOption[] = [
  { label: '中共党员', value: '中共党员' },
  { label: '中共预备党员', value: '中共预备党员' },
  { label: '共青团员', value: '共青团员' },
  { label: '民革党员', value: '民革党员' },
  { label: '民盟盟员', value: '民盟盟员' },
  { label: '民建会员', value: '民建会员' },
  { label: '民进会员', value: '民进会员' },
  { label: '农工党党员', value: '农工党党员' },
  { label: '致公党党员', value: '致公党党员' },
  { label: '九三学社社员', value: '九三学社社员' },
  { label: '台盟盟员', value: '台盟盟员' },
  { label: '无党派人士', value: '无党派人士' },
  { label: '群众', value: '群众' },
]
const defaultEthnicGroupOptions: SelectOption[] = [
  '汉族', '蒙古族', '回族', '藏族', '维吾尔族', '苗族', '彝族', '壮族', '布依族', '朝鲜族', '满族', '侗族', '瑶族', '白族', '土家族',
  '哈尼族', '哈萨克族', '傣族', '黎族', '傈僳族', '佤族', '畲族', '高山族', '拉祜族', '水族', '东乡族', '纳西族', '景颇族',
  '柯尔克孜族', '土族', '达斡尔族', '仫佬族', '羌族', '布朗族', '撒拉族', '毛南族', '仡佬族', '锡伯族', '阿昌族', '普米族',
  '塔吉克族', '怒族', '乌孜别克族', '俄罗斯族', '鄂温克族', '德昂族', '保安族', '裕固族', '京族', '塔塔尔族', '独龙族', '鄂伦春族',
  '赫哲族', '门巴族', '珞巴族', '基诺族',
].map((value) => ({ label: value, value }))
const certificateAttachmentAccept = '.pdf,.png,.jpg,.jpeg,.webp'
const profilePhotoAttachmentAccept = '.png,.jpg,.jpeg,.webp'
const resumeAttachmentAccept = '.pdf,.doc,.docx'

type EducationAttachmentField = 'transcript' | 'degree_certificate'

const sectionItems: SectionItem[] = [
  { id: 'plan-section', label: '当前计划', caption: '系统默认展示最新批次' },
  { id: 'basic-section', label: '基本信息', caption: '身份与联系信息' },
  { id: 'application-section', label: '报名信息', caption: '来源渠道与志愿选择' },
  { id: 'education-section', label: '教育经历', caption: '多段学习背景' },
  { id: 'practice-section', label: '实践经历', caption: '项目、实习与科研训练' },
  { id: 'english-section', label: '英语能力', caption: '英语考试与成绩' },
  { id: 'family-section', label: '家庭情况', caption: '父母及家庭成员信息' },
  { id: 'achievement-section', label: '论文及获奖', caption: '成果与奖励记录' },
  { id: 'statement-section', label: '个人陈述', caption: '申请动机与提交确认' },
]

const sectionGroups: SectionGroup[] = [
  {
    id: 'workflow-group',
    label: '申请流程',
    caption: '计划确认与报名核心信息',
    items: ['plan-section', 'basic-section', 'application-section'],
  },
  {
    id: 'archive-group',
    label: '档案信息',
    caption: '经历、家庭、成果与陈述',
    items: ['education-section', 'practice-section', 'english-section', 'family-section', 'achievement-section', 'statement-section'],
  },
]

const expandedSections = ref<Record<string, boolean>>({
  'plan-section': true,
  'basic-section': true,
  'application-section': true,
  'education-section': true,
  'practice-section': false,
  'english-section': false,
  'family-section': true,
  'achievement-section': false,
  'statement-section': true,
})

const expandedGroups = ref<Record<string, boolean>>({
  'workflow-group': true,
  'archive-group': true,
})

function createProfile(): PortalApplicantProfileData {
  return {
    full_name_pinyin: '',
    profile_photo_url: '',
    gender: '',
    birth_date: '',
    ethnic_group: '',
    native_place: '',
    political_status: '',
    marital_status: '',
    religious_belief: '',
    id_type: '居民身份证',
    mailing_address: '',
    emergency_contact_name: '',
    emergency_contact_phone: '',
  }
}

function createPreference(order: number, isOptional: boolean): PortalApplicationPreferenceItem {
  return {
    preference_order: order,
    research_center_name: '',
    advisor_name: '',
    is_optional: isOptional,
  }
}

function createEducation(order: number): PortalEducationExperienceItem {
  return {
    sort_order: order,
    education_stage: order === 1 ? '硕士' : '',
    start_month: '',
    end_month: '',
    school_name: '',
    major_name: '',
    average_score: '',
    gpa: '',
    ranking: '',
    verifier_name: '',
    verifier_phone: '',
    transcript_attachment_url: '',
    degree_certificate_attachment_url: '',
  }
}

function createPractice(): PortalPracticeExperienceItem {
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

function createEnglish(): PortalEnglishProficiencyItem {
  return {
    exam_name: '',
    score_text: '',
    certificate_attachment_url: '',
  }
}

function createFamilyMember(relationType = '其他'): PortalFamilyMemberItem {
  return {
    member_name: '',
    relation_type: relationType,
    employer_name: '',
    job_title: '',
    contact_phone: '',
  }
}

function createAchievement(): PortalAchievementRecordItem {
  return {
    achievement_type: '',
    paper_title: '',
    author_order: '',
    journal_or_conference: '',
    publish_or_index_month: '',
    award_name: '',
    awarding_organization: '',
    award_level: '',
    award_year: '',
    responsibility_text: '',
  }
}

function createPersonalStatement(): PortalPersonalStatementData {
  return {
    personal_statement_text: '',
    ai_problem_statement: '',
    ai_industry_opinion: '',
    resume_attachment_url: '',
  }
}

function createDeclaration(): PortalApplicationDeclarationData {
  return {
    has_read_declaration: false,
    declaration_text: '我已同意并仔细阅读使用条款和隐私政策。',
    progress_snapshot: null,
  }
}

function createEmptyForm(): PortalApplicationUpsert {
  return {
    plan_id: 0,
    profile: createProfile(),
    source_channel: '',
    source_channel_other: '',
    preferences: [createPreference(1, false)],
    education_experiences: [createEducation(1)],
    practice_experiences: [],
    english_proficiencies: [],
    family_members: [createFamilyMember('父亲'), createFamilyMember('母亲')],
    achievement_records: [],
    personal_statement: createPersonalStatement(),
    declaration: createDeclaration(),
    graduation_school: '',
    highest_degree: '',
    intended_field: '',
    english_level: '',
    family_info: '',
    education_experience: '',
    practice_experience: '',
    recommendation_notes: '',
    personal_statement_text: '',
    signed_agreement: false,
    selected_team_name: '',
    selected_advisor_name: '',
    self_evaluation: '',
  }
}

const form = reactive<PortalApplicationUpsert>(createEmptyForm())

function parseLegacyList<T>(value: string | null | undefined): T[] {
  if (!value) {
    return []
  }
  try {
    const parsed = JSON.parse(value)
    return Array.isArray(parsed) ? parsed : []
  } catch {
    return []
  }
}

function normalizePreferenceOrders() {
  const preferences = form.preferences || []
  preferences.forEach((item, index) => {
    item.preference_order = index + 1
    item.is_optional = index > 0
  })
}

function trimText(value: string | null | undefined) {
  return String(value || '').trim()
}

function advisorsForCenter(centerName: string) {
  return teams.value.find((item) => item.team_name === centerName)?.advisor_names || []
}

function handlePreferenceCenterChange(item: PortalApplicationPreferenceItem) {
  const advisors = advisorsForCenter(item.research_center_name)
  if (!advisors.includes(item.advisor_name || '')) {
    item.advisor_name = ''
  }
}

function buildAttachmentUploadKey(section: string, index: number | string, field: string) {
  return `${section}-${index}-${field}`
}

function isAttachmentUploading(key: string) {
  return Boolean(attachmentUploading[key])
}

async function uploadAttachmentAndResolveUrl(file: File, category: PortalAttachmentCategory, successMessage: string) {
  const response = await uploadPortalAttachment(file, category)
  ElMessage.success(successMessage)
  return response.data
}

async function handleEducationAttachmentUpload(index: number, field: EducationAttachmentField, event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) {
    return
  }

  const key = buildAttachmentUploadKey('education', index, field)
  attachmentUploading[key] = true
  try {
    const category: PortalAttachmentCategory = field === 'transcript' ? 'education_transcript' : 'education_degree_certificate'
    const attachment = await uploadAttachmentAndResolveUrl(file, category, field === 'transcript' ? '成绩单附件已上传' : '学位证附件已上传')
    const current = form.education_experiences?.[index]
    if (current) {
      if (field === 'transcript') {
        current.transcript_attachment_url = attachment.url
        current.transcript_attachment_name = attachment.file_name
      } else {
        current.degree_certificate_attachment_url = attachment.url
        current.degree_certificate_attachment_name = attachment.file_name
      }
    }
  } catch (error) {
    await showPortalAlert(resolveRequestError(error, '附件上传失败'), '附件上传失败', 'error')
  } finally {
    attachmentUploading[key] = false
    input.value = ''
  }
}

async function handleEnglishAttachmentUpload(index: number, event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) {
    return
  }

  const key = buildAttachmentUploadKey('english', index, 'certificate')
  attachmentUploading[key] = true
  try {
    const attachment = await uploadAttachmentAndResolveUrl(file, 'english_certificate', '英语证明附件已上传')
    const current = form.english_proficiencies?.[index]
    if (current) {
      current.certificate_attachment_url = attachment.url
      current.certificate_attachment_name = attachment.file_name
    }
  } catch (error) {
    await showPortalAlert(resolveRequestError(error, '附件上传失败'), '附件上传失败', 'error')
  } finally {
    attachmentUploading[key] = false
    input.value = ''
  }
}

async function handleResumeAttachmentUpload(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) {
    return
  }

  const key = buildAttachmentUploadKey('statement', 0, 'resume')
  attachmentUploading[key] = true
  try {
    const attachment = await uploadAttachmentAndResolveUrl(file, 'resume', '个人简历已上传')
    if (form.personal_statement) {
      form.personal_statement.resume_attachment_url = attachment.url
      form.personal_statement.resume_attachment_name = attachment.file_name
    }
  } catch (error) {
    await showPortalAlert(resolveRequestError(error, '附件上传失败'), '附件上传失败', 'error')
  } finally {
    attachmentUploading[key] = false
    input.value = ''
  }
}

async function handleProfilePhotoUpload(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) {
    return
  }

  const key = buildAttachmentUploadKey('profile', 0, 'photo')
  attachmentUploading[key] = true
  try {
    const attachment = await uploadAttachmentAndResolveUrl(file, 'profile_photo', '个人照片已上传')
    if (form.profile) {
      form.profile.profile_photo_url = attachment.url
    }
  } catch (error) {
    await showPortalAlert(resolveRequestError(error, '个人照片上传失败'), '个人照片上传失败', 'error')
  } finally {
    attachmentUploading[key] = false
    input.value = ''
  }
}

const selectedPlan = computed(() => plans.value.find((item) => item.id === selectedPlanId.value) || null)
const primaryPreference = computed(() => (form.preferences && form.preferences[0] ? form.preferences[0] : null))
const navFloatingStyle = computed(() => ({
  top: `${navBaseTop}px`,
  transform: `translateY(${navTranslateY.value}px)`,
}))
const canAddPreference = computed(() => (form.preferences?.length || 0) < 2)

function updateNavFloatingPosition() {
  const nav = navElement.value
  const section = document.getElementById(activeSectionId.value)
  if (!nav || !section) {
    navTranslateY.value = 0
    return
  }

  const viewportHeight = window.innerHeight
  const navHeight = nav.offsetHeight
  const sectionRect = section.getBoundingClientRect()
  const sectionAnchor = sectionRect.top + Math.min(sectionRect.height * 0.3, 120)
  const targetAnchor = Math.min(viewportHeight * 0.72, Math.max(viewportHeight * 0.32, sectionAnchor))
  const desiredTranslate = targetAnchor - navBaseTop - navHeight * 0.34

  navTranslateY.value = Math.max(0, Math.min(navMaxTranslate, Math.round(desiredTranslate)))
}

function updateActiveSectionByScroll() {
  const anchorLine = Math.max(180, window.innerHeight * 0.34)
  let closestSectionId = activeSectionId.value
  let closestDistance = Number.POSITIVE_INFINITY

  for (const item of sectionItems) {
    const element = document.getElementById(item.id)
    if (!element) {
      continue
    }

    const rect = element.getBoundingClientRect()
    const distance = Math.abs(rect.top - anchorLine)
    if (distance < closestDistance) {
      closestDistance = distance
      closestSectionId = item.id
    }
  }

  activeSectionId.value = closestSectionId
}

function syncFloatingUi() {
  showBackToTop.value = window.scrollY > 420
  updateActiveSectionByScroll()
  updateNavFloatingPosition()
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function toggleQuickNav() {
  quickNavOpen.value = !quickNavOpen.value
}

function closeQuickNav() {
  quickNavOpen.value = false
}

function isSectionExpanded(sectionId: string) {
  return expandedSections.value[sectionId] !== false
}

function isGroupExpanded(groupId: string) {
  return expandedGroups.value[groupId] !== false
}

function applyProfile(profile: PortalStudentRecord) {
  const draft = profile.application_draft
  const fallbackEducation = parseLegacyList<PortalEducationExperienceItem>(profile.education_experience)
  const fallbackPractice = parseLegacyList<PortalPracticeExperienceItem>(profile.practice_experience)
  const fallbackFamily = parseLegacyList<PortalFamilyMemberItem>(profile.family_info)
  const fallbackAchievements = parseLegacyList<PortalAchievementRecordItem>(profile.recommendation_notes)

  selectedPlanId.value = draft?.selected_plan_id || profile.selected_plan_id || null

  Object.assign(form, createEmptyForm(), {
    plan_id: selectedPlanId.value || 0,
    profile: {
      ...createProfile(),
      ...profile.profile,
      profile_photo_url: profile.profile?.profile_photo_url || '',
      gender: profile.profile?.gender || profile.gender || '',
      birth_date: profile.profile?.birth_date || profile.birth_date || '',
      ethnic_group: profile.profile?.ethnic_group || profile.ethnic_group || '',
      native_place: profile.profile?.native_place || profile.native_place || '',
      political_status: profile.profile?.political_status || profile.political_status || '',
      marital_status: profile.profile?.marital_status || profile.marital_status || '',
      religious_belief: profile.profile?.religious_belief || profile.religious_belief || '',
      id_type: profile.profile?.id_type || profile.id_type || '居民身份证',
      mailing_address: profile.profile?.mailing_address || profile.mailing_address || '',
    },
    source_channel: draft?.source_channel || '',
    source_channel_other: draft?.source_channel_other || '',
    preferences: draft?.preferences?.length
      ? draft.preferences.map((item, index) => ({
          preference_order: index + 1,
          research_center_name: item.research_center_name || '',
          advisor_name: item.advisor_name || '',
          is_optional: index > 0,
        }))
      : [
          {
            preference_order: 1,
            research_center_name: profile.selected_team_name || '',
            advisor_name: profile.selected_advisor_name || '',
            is_optional: false,
          },
        ],
    education_experiences: draft?.education_experiences?.length
      ? draft.education_experiences.map((item, index) => ({ ...createEducation(index + 1), ...item, sort_order: index + 1 }))
      : fallbackEducation.length
        ? fallbackEducation.map((item, index) => ({ ...createEducation(index + 1), ...item, sort_order: index + 1 }))
        : [createEducation(1)],
    practice_experiences: draft?.practice_experiences?.length
      ? draft.practice_experiences.map((item) => ({ ...createPractice(), ...item }))
      : fallbackPractice.map((item) => ({ ...createPractice(), ...item })),
    english_proficiencies: draft?.english_proficiencies?.length
      ? draft.english_proficiencies.map((item) => ({ ...createEnglish(), ...item }))
      : profile.english_level
        ? [{ ...createEnglish(), exam_name: profile.english_level }]
        : [],
    family_members: draft?.family_members?.length
      ? draft.family_members.map((item) => ({ ...createFamilyMember(item.relation_type || '其他'), ...item }))
      : fallbackFamily.length
        ? fallbackFamily.map((item) => ({ ...createFamilyMember(item.relation_type || '其他'), ...item }))
        : [createFamilyMember('父亲'), createFamilyMember('母亲')],
    achievement_records: draft?.achievement_records?.length
      ? draft.achievement_records.map((item) => ({ ...createAchievement(), ...item }))
      : fallbackAchievements.map((item) => ({ ...createAchievement(), ...item })),
    personal_statement: {
      ...createPersonalStatement(),
      ...draft?.personal_statement,
      personal_statement_text: draft?.personal_statement?.personal_statement_text || profile.personal_statement_text || '',
    },
    declaration: {
      ...createDeclaration(),
      ...draft?.declaration,
      has_read_declaration: draft?.declaration?.has_read_declaration ?? Boolean(profile.signed_agreement),
    },
  })

  normalizePreferenceOrders()
}

function choosePlan(planId: number) {
  selectedPlanId.value = planId
  form.plan_id = planId
}

function addPreference() {
  if (!canAddPreference.value) {
    return
  }
  form.preferences = [...(form.preferences || []), createPreference((form.preferences?.length || 0) + 1, true)]
  normalizePreferenceOrders()
}

function removePreference(index: number) {
  if (!form.preferences || index === 0) {
    return
  }
  form.preferences.splice(index, 1)
  normalizePreferenceOrders()
}

function addEducation() {
  form.education_experiences = [...(form.education_experiences || []), createEducation((form.education_experiences?.length || 0) + 1)]
}

function removeEducation(index: number) {
  if ((form.education_experiences?.length || 0) <= 1) {
    return
  }
  form.education_experiences?.splice(index, 1)
  form.education_experiences?.forEach((item, itemIndex) => {
    item.sort_order = itemIndex + 1
  })
}

function addPractice() {
  form.practice_experiences = [...(form.practice_experiences || []), createPractice()]
}

function removePractice(index: number) {
  form.practice_experiences?.splice(index, 1)
}

function addEnglish() {
  form.english_proficiencies = [...(form.english_proficiencies || []), createEnglish()]
}

function removeEnglish(index: number) {
  form.english_proficiencies?.splice(index, 1)
}

function addFamilyMember() {
  form.family_members = [...(form.family_members || []), createFamilyMember()]
}

function removeFamilyMember(index: number) {
  if ((form.family_members?.length || 0) <= 2) {
    return
  }
  form.family_members?.splice(index, 1)
}

function addAchievement() {
  form.achievement_records = [...(form.achievement_records || []), createAchievement()]
}

function removeAchievement(index: number) {
  form.achievement_records?.splice(index, 1)
}

function scrollToSection(sectionId: string) {
  closeQuickNav()
  activeSectionId.value = sectionId
  expandedSections.value = { ...expandedSections.value, [sectionId]: true }
  const parentGroup = sectionGroups.find((group) => group.items.includes(sectionId))
  if (parentGroup) {
    expandedGroups.value = { ...expandedGroups.value, [parentGroup.id]: true }
  }
  nextTick(() => {
    const sectionElement = document.getElementById(sectionId)
    if (!sectionElement) {
      return
    }
    const headerOffset = 104
    const top = window.scrollY + sectionElement.getBoundingClientRect().top - headerOffset
    window.scrollTo({ top: Math.max(0, top), behavior: 'smooth' })
  })
}

function toggleSection(sectionId: string) {
  expandedSections.value = { ...expandedSections.value, [sectionId]: !isSectionExpanded(sectionId) }
  nextTick(() => updateNavFloatingPosition())
}

function toggleGroup(groupId: string) {
  expandedGroups.value = { ...expandedGroups.value, [groupId]: !isGroupExpanded(groupId) }
  nextTick(() => updateNavFloatingPosition())
}

function mountSectionObserver() {
  sectionObserver?.disconnect()
  sectionObserver = new IntersectionObserver(
    (entries) => {
      const visibleEntry = entries
        .filter((entry) => entry.isIntersecting)
        .sort((left, right) => right.intersectionRatio - left.intersectionRatio)[0]
      if (visibleEntry?.target?.id) {
        activeSectionId.value = visibleEntry.target.id
      }
    },
    {
      rootMargin: '-18% 0px -52% 0px',
      threshold: [0.2, 0.45, 0.7],
    },
  )
  for (const item of sectionItems) {
    const element = document.getElementById(item.id)
    if (element) {
      sectionObserver.observe(element)
    }
  }
}

function buildProgressSnapshot() {
  return {
    preference_count: (form.preferences || []).filter((item) => trimText(item.research_center_name)).length,
    education_count: (form.education_experiences || []).filter((item) => trimText(item.school_name)).length,
    practice_count: (form.practice_experiences || []).filter((item) => trimText(item.organization_name)).length,
    english_count: (form.english_proficiencies || []).filter((item) => trimText(item.exam_name)).length,
    family_count: (form.family_members || []).filter((item) => trimText(item.member_name)).length,
    achievement_count: (form.achievement_records || []).filter((item) => trimText(item.achievement_type)).length,
  }
}

function buildSectionStatuses(): PortalSectionStatus[] {
  const profileData = form.profile || createProfile()
  const basicStarted = Boolean(
    trimText(profileData.full_name_pinyin)
    || trimText(profileData.gender)
    || trimText(profileData.ethnic_group)
    || trimText(profileData.political_status)
    || trimText(profileData.mailing_address)
    || trimText(profileData.emergency_contact_name)
    || trimText(profileData.emergency_contact_phone)
    || trimText(profileData.profile_photo_url),
  )
  const basicCompleted = Boolean(
    trimText(profileData.full_name_pinyin)
    && trimText(profileData.gender)
    && trimText(profileData.ethnic_group)
    && trimText(profileData.political_status)
    && trimText(profileData.mailing_address)
    && trimText(profileData.emergency_contact_name)
    && trimText(profileData.emergency_contact_phone)
    && trimText(profileData.profile_photo_url),
  )

  const firstPreference = primaryPreference.value
  const applicationStarted = Boolean(
    trimText(form.source_channel)
    || trimText(form.source_channel_other)
    || trimText(firstPreference?.research_center_name)
    || trimText(firstPreference?.advisor_name),
  )
  const applicationCompleted = Boolean(trimText(firstPreference?.research_center_name))

  const educationItems = form.education_experiences || []
  const educationCompleted = educationItems.some((item) => trimText(item.education_stage) && trimText(item.school_name))

  const practiceItems = form.practice_experiences || []
  const practiceCompleted = practiceItems.some((item) => trimText(item.organization_name))

  const englishItems = form.english_proficiencies || []
  const englishCompleted = englishItems.some((item) => trimText(item.exam_name))

  const familyItems = form.family_members || []
  const familyStarted = familyItems.some((item) => trimText(item.member_name) || trimText(item.relation_type))
  const father = familyItems.find((item) => item.relation_type === '父亲' && trimText(item.member_name))
  const mother = familyItems.find((item) => item.relation_type === '母亲' && trimText(item.member_name))
  const familyCompleted = Boolean(father && mother)

  const achievementItems = form.achievement_records || []
  const achievementCompleted = achievementItems.some((item) => trimText(item.achievement_type))

  const statementText = trimText(form.personal_statement?.personal_statement_text)
  const statementStarted = Boolean(
    statementText
    || trimText(form.personal_statement?.ai_problem_statement)
    || trimText(form.personal_statement?.ai_industry_opinion)
    || trimText(form.personal_statement?.resume_attachment_url)
    || form.declaration?.has_read_declaration,
  )
  const statementCompleted = Boolean(statementText)

  const createStatus = (id: string, label: string, started: boolean, completed: boolean): PortalSectionStatus => ({
    id,
    label,
    completed,
    status: completed ? 'completed' : started ? 'in-progress' : 'not-started',
  })

  return [
    createStatus('basic-section', '基本信息', basicStarted, basicCompleted),
    createStatus('application-section', '报名信息', applicationStarted, applicationCompleted),
    createStatus('education-section', '教育经历', educationCompleted, educationCompleted),
    createStatus('practice-section', '实践经历', practiceCompleted, practiceCompleted),
    createStatus('english-section', '英语语言能力', englishCompleted, englishCompleted),
    createStatus('family-section', '家庭情况', familyStarted, familyCompleted),
    createStatus('achievement-section', '论文发表及获奖经历', achievementCompleted, achievementCompleted),
    createStatus('statement-section', '个人陈述', statementStarted, statementCompleted),
  ]
}

function buildSubmitPayload(): PortalApplicationUpsert {
  const profileData = form.profile || createProfile()
  const orderedPreferences = (form.preferences || [])
    .map((item, index) => ({
      preference_order: index + 1,
      research_center_name: trimText(item.research_center_name),
      advisor_name: trimText(item.advisor_name) || null,
      is_optional: index > 0,
    }))
    .filter((item) => item.research_center_name)

  const orderedEducation = (form.education_experiences || [])
    .map((item, index) => ({
      ...item,
      sort_order: index + 1,
      education_stage: trimText(item.education_stage),
      school_name: trimText(item.school_name),
      major_name: trimText(item.major_name) || null,
      average_score: trimText(item.average_score) || null,
      gpa: trimText(item.gpa) || null,
      ranking: trimText(item.ranking) || null,
      verifier_name: trimText(item.verifier_name) || null,
      verifier_phone: trimText(item.verifier_phone) || null,
      start_month: trimText(item.start_month) || null,
      end_month: trimText(item.end_month) || null,
      transcript_attachment_url: trimText(item.transcript_attachment_url) || null,
      degree_certificate_attachment_url: trimText(item.degree_certificate_attachment_url) || null,
    }))
    .filter((item) => item.education_stage && item.school_name)

  const practiceExperiences = (form.practice_experiences || [])
    .map((item) => ({
      ...item,
      organization_name: trimText(item.organization_name),
      position_name: trimText(item.position_name) || null,
      responsibility_text: trimText(item.responsibility_text) || null,
      verifier_name: trimText(item.verifier_name) || null,
      verifier_phone: trimText(item.verifier_phone) || null,
      start_month: trimText(item.start_month) || null,
      end_month: trimText(item.end_month) || null,
    }))
    .filter((item) => item.organization_name)

  const englishProficiencies = (form.english_proficiencies || [])
    .map((item) => ({
      ...item,
      exam_name: trimText(item.exam_name),
      score_text: trimText(item.score_text) || null,
      certificate_attachment_url: trimText(item.certificate_attachment_url) || null,
    }))
    .filter((item) => item.exam_name)

  const familyMembers = (form.family_members || [])
    .map((item) => ({
      ...item,
      member_name: trimText(item.member_name),
      relation_type: trimText(item.relation_type),
      employer_name: trimText(item.employer_name) || null,
      job_title: trimText(item.job_title) || null,
      contact_phone: trimText(item.contact_phone) || null,
    }))
    .filter((item) => item.member_name && item.relation_type)

  const achievementRecords = (form.achievement_records || [])
    .map((item) => ({
      ...item,
      achievement_type: trimText(item.achievement_type),
      paper_title: trimText(item.paper_title) || null,
      author_order: trimText(item.author_order) || null,
      journal_or_conference: trimText(item.journal_or_conference) || null,
      publish_or_index_month: trimText(item.publish_or_index_month) || null,
      award_name: trimText(item.award_name) || null,
      awarding_organization: trimText(item.awarding_organization) || null,
      award_level: trimText(item.award_level) || null,
      award_year: trimText(item.award_year) || null,
      responsibility_text: trimText(item.responsibility_text) || null,
    }))
    .filter((item) => item.achievement_type)

  const primaryPreferenceItem = orderedPreferences[0]
  const primaryEducationItem = orderedEducation[0]
  const declaration = {
    ...(form.declaration || createDeclaration()),
    has_read_declaration: Boolean(form.declaration?.has_read_declaration),
    declaration_text: trimText(form.declaration?.declaration_text) || createDeclaration().declaration_text,
    progress_snapshot: buildProgressSnapshot(),
  }

  return {
    plan_id: selectedPlanId.value || form.plan_id || 0,
    profile: {
      ...profileData,
      full_name_pinyin: trimText(profileData.full_name_pinyin) || null,
      profile_photo_url: trimText(profileData.profile_photo_url) || null,
      gender: trimText(profileData.gender) || null,
      birth_date: trimText(profileData.birth_date) || null,
      ethnic_group: trimText(profileData.ethnic_group) || null,
      native_place: trimText(profileData.native_place) || null,
      political_status: trimText(profileData.political_status) || null,
      marital_status: trimText(profileData.marital_status) || null,
      religious_belief: trimText(profileData.religious_belief) || null,
      id_type: trimText(profileData.id_type) || null,
      mailing_address: trimText(profileData.mailing_address) || null,
      emergency_contact_name: trimText(profileData.emergency_contact_name) || null,
      emergency_contact_phone: trimText(profileData.emergency_contact_phone) || null,
    },
    source_channel: trimText(form.source_channel) || null,
    source_channel_other: trimText(form.source_channel_other) || null,
    preferences: orderedPreferences,
    education_experiences: orderedEducation,
    practice_experiences: practiceExperiences,
    english_proficiencies: englishProficiencies,
    family_members: familyMembers,
    achievement_records: achievementRecords,
    personal_statement: {
      ...(form.personal_statement || createPersonalStatement()),
      personal_statement_text: trimText(form.personal_statement?.personal_statement_text) || null,
      ai_problem_statement: trimText(form.personal_statement?.ai_problem_statement) || null,
      ai_industry_opinion: trimText(form.personal_statement?.ai_industry_opinion) || null,
      resume_attachment_url: trimText(form.personal_statement?.resume_attachment_url) || null,
    },
    declaration,
    gender: trimText(profileData.gender) || null,
    birth_date: trimText(profileData.birth_date) || null,
    ethnic_group: trimText(profileData.ethnic_group) || null,
    native_place: trimText(profileData.native_place) || null,
    marital_status: trimText(profileData.marital_status) || null,
    religious_belief: trimText(profileData.religious_belief) || null,
    id_type: trimText(profileData.id_type) || null,
    mailing_address: trimText(profileData.mailing_address) || null,
    graduation_school: primaryEducationItem?.school_name || '',
    highest_degree: primaryEducationItem?.education_stage || '',
    intended_field: primaryPreferenceItem?.research_center_name || '',
    political_status: trimText(profileData.political_status) || null,
    english_level: englishProficiencies[0]?.exam_name || null,
    personal_statement_text: trimText(form.personal_statement?.personal_statement_text) || null,
    signed_agreement: declaration.has_read_declaration,
    selected_team_name: primaryPreferenceItem?.research_center_name || '',
    selected_advisor_name: primaryPreferenceItem?.advisor_name || null,
    self_evaluation: trimText(form.personal_statement?.ai_industry_opinion) || null,
  }
}

async function submitForm() {
  if (!selectedPlanId.value) {
    await showPortalAlert('当前暂无可提交的招生计划', '提交受阻', 'warning')
    return
  }

  if (!trimText(form.profile?.profile_photo_url)) {
    await showPortalAlert('请先上传个人照片后再提交申请表', '提交受阻', 'warning')
    return
  }

  const primary = primaryPreference.value
  if (!trimText(primary?.research_center_name)) {
    await showPortalAlert('请至少选择第一志愿研究中心', '提交受阻', 'warning')
    return
  }

  const firstEducation = (form.education_experiences || []).find((item) => trimText(item.education_stage) && trimText(item.school_name))
  if (!firstEducation) {
    await showPortalAlert('请至少填写一条教育经历', '提交受阻', 'warning')
    return
  }

  const familyMembers = form.family_members || []
  const father = familyMembers.find((item) => item.relation_type === '父亲' && trimText(item.member_name))
  const mother = familyMembers.find((item) => item.relation_type === '母亲' && trimText(item.member_name))
  if (!father || !mother) {
    await showPortalAlert('请完整填写父亲和母亲信息', '提交受阻', 'warning')
    return
  }

  if (trimText(form.source_channel) === '其他' && !trimText(form.source_channel_other)) {
    await showPortalAlert('选择“其他”来源时，请补充说明', '提交受阻', 'warning')
    return
  }

  if (!form.declaration?.has_read_declaration) {
    await showPortalAlert('请先确认提交声明', '提交受阻', 'warning')
    return
  }

  submitting.value = true
  try {
    const response = await submitPortalApplication(buildSubmitPayload())
    student.value = response.data.student
    applyProfile(response.data.student)
    ElMessage.success(`申请已提交，业务编号 ${response.data.application_business_key}`)
  } catch (error) {
    await showPortalAlert(resolveRequestError(error, '提交失败'), '提交失败', 'error')
  } finally {
    submitting.value = false
  }
}

async function saveDraft(showSuccess = true) {
  savingDraft.value = true
  try {
    const response = await savePortalApplicationDraft(buildSubmitPayload())
    student.value = response.data.student
    applyProfile(response.data.student)
    if (showSuccess) {
      ElMessage.success(response.data.message || '草稿已保存')
    }
    return true
  } catch (error) {
    await showPortalAlert(resolveRequestError(error, '草稿保存失败'), '草稿保存失败', 'error')
    return false
  } finally {
    savingDraft.value = false
  }
}

function resetProfileForm() {
  profileForm.current_password = ''
  profileForm.new_password = ''
  profileForm.confirm_password = ''
}

function openProfileDialog() {
  resetProfileForm()
  profileDialogVisible.value = true
}

async function submitProfilePasswordChange() {
  if (!profileForm.current_password.trim()) {
    await showPortalAlert('请输入当前密码', '修改密码', 'warning')
    return
  }
  if (!profileForm.new_password.trim()) {
    await showPortalAlert('请输入新密码', '修改密码', 'warning')
    return
  }
  if (profileForm.new_password.trim().length < 6) {
    await showPortalAlert('新密码长度不能少于 6 位', '修改密码', 'warning')
    return
  }
  if (profileForm.new_password !== profileForm.confirm_password) {
    await showPortalAlert('两次输入的新密码不一致', '修改密码', 'warning')
    return
  }
  profileSubmitting.value = true
  try {
    const response = await changePortalStudentPassword({
      current_password: profileForm.current_password,
      new_password: profileForm.new_password,
    })
    profileDialogVisible.value = false
    resetProfileForm()
    ElMessage.success(response.data.message)
  } catch (error) {
    await showPortalAlert(resolveRequestError(error, '密码修改失败'), '密码修改失败', 'error')
  } finally {
    profileSubmitting.value = false
  }
}

function logoutPortal() {
  clearPortalToken()
  void router.replace('/portal')
}

watch(
  () => form.source_channel,
  (value) => {
    if (trimText(value) !== '其他') {
      form.source_channel_other = ''
    }
  },
)

watch(activeSectionId, () => {
  void nextTick(() => updateNavFloatingPosition())
})

onMounted(async () => {
  window.addEventListener('scroll', syncFloatingUi, { passive: true })
  window.addEventListener('resize', syncFloatingUi)

  if (!getPortalToken()) {
    await router.replace('/portal')
    return
  }

  try {
    const [profileResponse, planResponse, teamResponse, optionsResult] = await Promise.allSettled([
      getPortalProfile(),
      listPortalPlans(),
      listPortalTeams(),
      getPortalProfileOptions(),
    ])
    if (profileResponse.status !== 'fulfilled') {
      throw profileResponse.reason
    }
    if (planResponse.status !== 'fulfilled') {
      throw planResponse.reason
    }
    if (teamResponse.status !== 'fulfilled') {
      throw teamResponse.reason
    }

    student.value = profileResponse.value.data
    plans.value = planResponse.value.data.items
    teams.value = teamResponse.value.data.items
    if (optionsResult.status === 'fulfilled') {
      politicalStatusOptions.value = optionsResult.value.data.political_status_options
      ethnicGroupOptions.value = optionsResult.value.data.ethnic_group_options
    } else {
      politicalStatusOptions.value = defaultPoliticalStatusOptions
      ethnicGroupOptions.value = defaultEthnicGroupOptions
    }
    applyProfile(profileResponse.value.data)
    if (!selectedPlanId.value && plans.value[0]) {
      choosePlan(plans.value[0].id)
    }
  } catch (error) {
    clearPortalToken()
    await showPortalAlert(resolveRequestError(error, '门户信息加载失败，请重新登录。'), '进入失败', 'error')
    await router.replace('/portal')
  } finally {
    initializing.value = false
    await nextTick()
    mountSectionObserver()
    syncFloatingUi()
  }
})

onBeforeUnmount(() => {
  sectionObserver?.disconnect()
  window.removeEventListener('scroll', syncFloatingUi)
  window.removeEventListener('resize', syncFloatingUi)
})

defineExpose({
  saveDraft,
  getSectionStatuses: buildSectionStatuses,
  getSavingDraft: () => savingDraft.value,
})
</script>

<template>
  <div class="portal-application-shell">
    <div class="application-ambient application-ambient--left"></div>
    <div class="application-ambient application-ambient--right"></div>
    <header class="application-header">
      <div class="application-header__brand">
        <div class="brand-logo">SAIL</div>
        <div>
          <strong>上海人工智能实验室</strong>
          <span>Shanghai Artificial Intelligence Laboratory</span>
        </div>
      </div>
      <div class="application-header__user">
        <span>{{ student?.account_status || '启用' }}</span>
        <strong>{{ student?.full_name || '考生' }}</strong>
        <button type="button" @click="openProfileDialog">个人空间</button>
        <button type="button" @click="logoutPortal">退出</button>
      </div>
    </header>

    <main class="application-page" v-if="!initializing">
      <section class="application-notice">
        <div class="application-notice__meta">
          <p>报名开始时间：2025-10-27 13:20</p>
          <p>报名截止时间：2026-05-31 23:59</p>
        </div>
        <span>系统已默认展示最新招生计划。请直接继续完善学生档案、研究中心志愿、教育经历与个人陈述，整体填写版式保持原门户模式。</span>
      </section>

      <section class="application-layout">
        <aside ref="navElement" class="application-nav" :style="navFloatingStyle">
          <div class="application-nav__heading">
            <span>档案导航</span>
            <strong>申请表分段填写</strong>
          </div>
          <section v-for="group in sectionGroups" :key="group.id" class="application-nav__group">
            <button type="button" class="application-nav__group-toggle" @click="toggleGroup(group.id)">
              <span class="application-nav__group-copy">
                <strong>{{ group.label }}</strong>
                <small>{{ group.caption }}</small>
              </span>
              <span class="application-nav__group-icon" :class="{ 'application-nav__group-icon--expanded': isGroupExpanded(group.id) }" aria-hidden="true"></span>
            </button>
            <div v-show="isGroupExpanded(group.id)" class="application-nav__group-items">
              <button
                v-for="sectionId in group.items"
                :key="sectionId"
                type="button"
                class="application-nav__item"
                :class="{ 'application-nav__item--active': activeSectionId === sectionId }"
                @click="scrollToSection(sectionId)"
              >
                <span class="application-nav__index">{{ String(sectionItems.findIndex((item) => item.id === sectionId) + 1).padStart(2, '0') }}</span>
                <span class="application-nav__copy">
                  <strong>{{ sectionItems.find((item) => item.id === sectionId)?.label }}</strong>
                  <small>{{ sectionItems.find((item) => item.id === sectionId)?.caption }}</small>
                </span>
              </button>
            </div>
          </section>
          <div class="application-nav__status">
            <span>当前申请人</span>
            <strong>{{ student?.full_name || '考生' }}</strong>
            <small>{{ selectedPlan?.plan_name || '尚未选定计划' }}</small>
          </div>
        </aside>

        <section class="application-content">
          <article id="plan-section" class="application-panel" :class="{ 'application-panel--collapsed': !isSectionExpanded('plan-section') }">
            <button type="button" class="panel-toggle" @click="toggleSection('plan-section')">
              <span class="panel-toggle__copy">
                <small>STEP 01</small>
                <strong>当前招生计划</strong>
                <span>系统默认展示最新计划，无需学生手动选择</span>
              </span>
              <span class="panel-toggle__action">{{ isSectionExpanded('plan-section') ? '收起' : '展开' }}</span>
              <span class="panel-toggle__icon" :class="{ 'panel-toggle__icon--expanded': isSectionExpanded('plan-section') }" aria-hidden="true"></span>
            </button>
            <div v-show="isSectionExpanded('plan-section')" class="panel-body">
              <div v-if="selectedPlan" class="portal-plan-spotlight">
                <div class="portal-plan-spotlight__badge">最新招生计划</div>
                <div class="portal-plan-spotlight__copy">
                  <strong>{{ selectedPlan.plan_name }}</strong>
                  <p>{{ selectedPlan.summary || '当前计划暂未填写计划介绍，请联系招生管理员补充。' }}</p>
                </div>
              </div>
              <div v-else class="portal-plan-empty">
                当前暂无可展示的招生计划，请联系招生管理员开放最新计划。
              </div>
            </div>
          </article>

          <article id="basic-section" class="application-panel" :class="{ 'application-panel--collapsed': !isSectionExpanded('basic-section') }">
            <button type="button" class="panel-toggle" @click="toggleSection('basic-section')">
              <span class="panel-toggle__copy">
                <small>STEP 02</small>
                <strong>基本信息</strong>
                <span>用于确认身份、联系方式与基础背景</span>
              </span>
              <span class="panel-toggle__action">{{ isSectionExpanded('basic-section') ? '收起' : '展开' }}</span>
              <span class="panel-toggle__icon" :class="{ 'panel-toggle__icon--expanded': isSectionExpanded('basic-section') }" aria-hidden="true"></span>
            </button>
            <div v-show="isSectionExpanded('basic-section')" class="panel-body">
              <div class="profile-photo-card">
                <div class="profile-photo-card__preview">
                  <img v-if="form.profile!.profile_photo_url" :src="form.profile!.profile_photo_url" alt="个人证件照片预览" />
                  <div v-else class="profile-photo-card__empty">请上传个人证件照片</div>
                </div>
                <div class="profile-photo-card__content">
                  <div class="profile-photo-card__copy">
                    <strong>个人照片</strong>
                    <span>建议使用身份证照片比例，作为报名资料随个人信息一并提交。</span>
                  </div>
                  <div class="upload-field upload-field--compact">
                    <div class="upload-field__controls">
                      <input
                        class="upload-file-input"
                        type="file"
                        :disabled="isAttachmentUploading(buildAttachmentUploadKey('profile', 0, 'photo'))"
                        :accept="profilePhotoAttachmentAccept"
                        @change="handleProfilePhotoUpload"
                      />
                    </div>
                    <small class="upload-field__hint">{{ isAttachmentUploading(buildAttachmentUploadKey('profile', 0, 'photo')) ? '上传中...' : '支持 JPG/PNG/WEBP，建议尺寸接近身份证照片，单张不超过 1MB' }}</small>
                  </div>
                </div>
              </div>
              <div class="form-grid form-grid--three">
                <label><span>姓名</span><input :value="student?.full_name || ''" disabled /></label>
                <label><span>姓名拼音</span><input v-model="form.profile!.full_name_pinyin" placeholder="请输入姓名拼音" /></label>
                <label><span>性别</span><select v-model="form.profile!.gender"><option value="">请选择</option><option v-for="item in genderOptions" :key="item" :value="item">{{ item }}</option></select></label>
                <label>
                  <span>民族</span>
                  <select v-model="form.profile!.ethnic_group">
                    <option value="">请选择</option>
                    <option v-for="item in ethnicGroupOptions" :key="item.value" :value="item.value">{{ item.label }}</option>
                  </select>
                </label>
                <label>
                  <span>政治面貌</span>
                  <select v-model="form.profile!.political_status">
                    <option value="">请选择</option>
                    <option v-for="item in politicalStatusOptions" :key="item.value" :value="item.value">{{ item.label }}</option>
                  </select>
                </label>
                <label><span>籍贯</span><input v-model="form.profile!.native_place" placeholder="请输入籍贯" /></label>
                <label><span>证件类型</span><select v-model="form.profile!.id_type"><option v-for="item in idTypeOptions" :key="item" :value="item">{{ item }}</option></select></label>
                <label><span>证件号码</span><input :value="student?.id_number || ''" disabled /></label>
                <label><span>邮箱</span><input :value="student?.email || ''" disabled /></label>
                <label><span>手机号码</span><input :value="student?.phone_number || ''" disabled /></label>
                <label><span>紧急联系人姓名</span><input v-model="form.profile!.emergency_contact_name" placeholder="请输入紧急联系人姓名" /></label>
                <label><span>紧急联系人手机</span><input v-model="form.profile!.emergency_contact_phone" placeholder="请输入紧急联系人手机" /></label>
                <label class="form-field form-field--full"><span>通讯地址</span><input v-model="form.profile!.mailing_address" placeholder="请输入通讯地址" /></label>
              </div>
            </div>
          </article>

          <article id="application-section" class="application-panel" :class="{ 'application-panel--collapsed': !isSectionExpanded('application-section') }">
            <button type="button" class="panel-toggle" @click="toggleSection('application-section')">
              <span class="panel-toggle__copy">
                <small>STEP 03</small>
                <strong>报名信息</strong>
                <span>填写获知渠道、研究中心志愿和导师选择</span>
              </span>
              <span class="panel-toggle__action">{{ isSectionExpanded('application-section') ? '收起' : '展开' }}</span>
              <span class="panel-toggle__icon" :class="{ 'panel-toggle__icon--expanded': isSectionExpanded('application-section') }" aria-hidden="true"></span>
            </button>
            <div v-show="isSectionExpanded('application-section')" class="panel-body">
              <div class="form-grid form-grid--three">
                <label>
                  <span>了解项目方式</span>
                  <select v-model="form.source_channel">
                    <option value="">请选择</option>
                    <option v-for="item in sourceChannelOptions" :key="item" :value="item">{{ item }}</option>
                  </select>
                </label>
                <label v-if="form.source_channel === '其他'">
                  <span>其他说明</span>
                  <input v-model="form.source_channel_other" placeholder="请补充获知渠道" />
                </label>
              </div>

              <div class="record-toolbar">
                <div>
                  <strong>研究中心志愿</strong>
                  <span>默认保留第一志愿，可追加第二志愿。</span>
                </div>
                <button type="button" class="secondary-button" :disabled="!canAddPreference" @click="addPreference">添加第二志愿</button>
              </div>
              <div class="record-list">
                <section v-for="(item, index) in form.preferences" :key="`preference-${index}`" class="record-card">
                  <div class="record-card__header">
                    <div>
                      <strong>第 {{ item.preference_order }} 志愿</strong>
                      <span>{{ index === 0 ? '必填' : '选填' }}</span>
                    </div>
                    <button v-if="index > 0" type="button" class="tertiary-button" @click="removePreference(index)">删除</button>
                  </div>
                  <div class="form-grid form-grid--three">
                    <label>
                      <span>研究中心</span>
                      <select v-model="item.research_center_name" @change="handlePreferenceCenterChange(item)">
                        <option value="">请选择研究中心</option>
                        <option v-for="team in teams" :key="team.id" :value="team.team_name">{{ team.team_name }}</option>
                      </select>
                    </label>
                    <label>
                      <span>意向导师</span>
                      <select v-model="item.advisor_name">
                        <option value="">请选择导师</option>
                        <option v-for="advisor in advisorsForCenter(item.research_center_name)" :key="advisor" :value="advisor">{{ advisor }}</option>
                      </select>
                    </label>
                  </div>
                </section>
              </div>
            </div>
          </article>

          <article id="education-section" class="application-panel" :class="{ 'application-panel--collapsed': !isSectionExpanded('education-section') }">
            <button type="button" class="panel-toggle" @click="toggleSection('education-section')">
              <span class="panel-toggle__copy">
                <small>STEP 04</small>
                <strong>教育经历</strong>
                <span>请按最高学历到高中的顺序填写</span>
              </span>
              <span class="panel-toggle__action">{{ isSectionExpanded('education-section') ? '收起' : '展开' }}</span>
              <span class="panel-toggle__icon" :class="{ 'panel-toggle__icon--expanded': isSectionExpanded('education-section') }" aria-hidden="true"></span>
            </button>
            <div v-show="isSectionExpanded('education-section')" class="panel-body">
              <div class="record-toolbar">
                <div>
                  <strong>教育经历列表</strong>
                  <span>至少填写一条，建议按“硕士/本科/高中”依次补全。</span>
                </div>
                <button type="button" class="secondary-button" @click="addEducation">新增教育经历</button>
              </div>
              <div class="record-list">
                <section v-for="(item, index) in form.education_experiences" :key="`education-${index}`" class="record-card">
                  <div class="record-card__header">
                    <div>
                      <strong>教育经历 {{ index + 1 }}</strong>
                      <span>用于派生最高学历与毕业院校</span>
                    </div>
                    <button v-if="form.education_experiences!.length > 1" type="button" class="tertiary-button" @click="removeEducation(index)">删除</button>
                  </div>
                  <div class="form-grid form-grid--three">
                    <label><span>教育阶段</span><select v-model="item.education_stage"><option value="">请选择</option><option v-for="stage in educationStageOptions" :key="stage" :value="stage">{{ stage }}</option></select></label>
                    <label><span>开始年月</span><input v-model="item.start_month" type="month" /></label>
                    <label><span>结束年月</span><input v-model="item.end_month" type="month" /></label>
                    <label><span>就读学校</span><input v-model="item.school_name" placeholder="请输入就读学校" /></label>
                    <label><span>就读专业</span><input v-model="item.major_name" placeholder="请输入就读专业" /></label>
                    <label><span>期间平均成绩</span><input v-model="item.average_score" placeholder="如 88.5" /></label>
                    <label><span>期间绩点</span><input v-model="item.gpa" placeholder="如 3.7/4.0" /></label>
                    <label><span>成绩排名</span><input v-model="item.ranking" placeholder="如 5/120" /></label>
                    <label><span>证明人姓名</span><input v-model="item.verifier_name" placeholder="请输入证明人姓名" /></label>
                    <label><span>证明人手机</span><input v-model="item.verifier_phone" placeholder="请输入证明人手机" /></label>
                  </div>
                  <div class="upload-grid">
                    <div class="upload-field">
                      <span class="upload-field__label">成绩单附件</span>
                      <div class="upload-field__controls">
                        <input :value="item.transcript_attachment_url || ''" readonly placeholder="未上传时可留空" />
                        <input
                          class="upload-file-input"
                          type="file"
                          :disabled="isAttachmentUploading(buildAttachmentUploadKey('education', index, 'transcript'))"
                          :accept="certificateAttachmentAccept"
                          @change="handleEducationAttachmentUpload(index, 'transcript', $event)"
                        />
                      </div>
                      <small class="upload-field__hint">{{ isAttachmentUploading(buildAttachmentUploadKey('education', index, 'transcript')) ? '上传中...' : '支持 PDF/JPG/PNG/WEBP，单个文件不超过 20MB' }}</small>
                    </div>
                    <div class="upload-field">
                      <span class="upload-field__label">学位证附件</span>
                      <div class="upload-field__controls">
                        <input :value="item.degree_certificate_attachment_url || ''" readonly placeholder="未上传时可留空" />
                        <input
                          class="upload-file-input"
                          type="file"
                          :disabled="isAttachmentUploading(buildAttachmentUploadKey('education', index, 'degree_certificate'))"
                          :accept="certificateAttachmentAccept"
                          @change="handleEducationAttachmentUpload(index, 'degree_certificate', $event)"
                        />
                      </div>
                      <small class="upload-field__hint">{{ isAttachmentUploading(buildAttachmentUploadKey('education', index, 'degree_certificate')) ? '上传中...' : '支持 PDF/JPG/PNG/WEBP，单个文件不超过 20MB' }}</small>
                    </div>
                  </div>
                </section>
              </div>
            </div>
          </article>

          <article id="practice-section" class="application-panel" :class="{ 'application-panel--collapsed': !isSectionExpanded('practice-section') }">
            <button type="button" class="panel-toggle" @click="toggleSection('practice-section')">
              <span class="panel-toggle__copy">
                <small>STEP 05</small>
                <strong>实践经历</strong>
                <span>该部分非必填，可补充项目、实习与科研训练</span>
              </span>
              <span class="panel-toggle__action">{{ isSectionExpanded('practice-section') ? '收起' : '展开' }}</span>
              <span class="panel-toggle__icon" :class="{ 'panel-toggle__icon--expanded': isSectionExpanded('practice-section') }" aria-hidden="true"></span>
            </button>
            <div v-show="isSectionExpanded('practice-section')" class="panel-body">
              <div class="record-toolbar">
                <div>
                  <strong>实践经历列表</strong>
                  <span>可填写项目、实习、工程实践或工作经历。</span>
                </div>
                <button type="button" class="secondary-button" @click="addPractice">新增实践经历</button>
              </div>
              <div v-if="!(form.practice_experiences && form.practice_experiences.length)" class="empty-state">当前未填写实践经历，可跳过。</div>
              <div v-else class="record-list">
                <section v-for="(item, index) in form.practice_experiences" :key="`practice-${index}`" class="record-card">
                  <div class="record-card__header">
                    <div><strong>实践经历 {{ index + 1 }}</strong><span>非必填</span></div>
                    <button type="button" class="tertiary-button" @click="removePractice(index)">删除</button>
                  </div>
                  <div class="form-grid form-grid--three">
                    <label><span>开始年月</span><input v-model="item.start_month" type="month" /></label>
                    <label><span>结束年月</span><input v-model="item.end_month" type="month" /></label>
                    <label><span>实习实践/工作单位</span><input v-model="item.organization_name" placeholder="请输入实习实践/工作单位" /></label>
                    <label><span>岗位</span><input v-model="item.position_name" placeholder="请输入岗位" /></label>
                    <label><span>证明人姓名</span><input v-model="item.verifier_name" placeholder="请输入证明人姓名" /></label>
                    <label><span>证明人手机</span><input v-model="item.verifier_phone" placeholder="请输入证明人手机" /></label>
                    <label class="form-field form-field--full"><span>职责</span><textarea v-model="item.responsibility_text" rows="4" placeholder="请输入职责、项目内容或实践成果" /></label>
                  </div>
                </section>
              </div>
            </div>
          </article>

          <article id="english-section" class="application-panel" :class="{ 'application-panel--collapsed': !isSectionExpanded('english-section') }">
            <button type="button" class="panel-toggle" @click="toggleSection('english-section')">
              <span class="panel-toggle__copy">
                <small>STEP 06</small>
                <strong>英语语言能力</strong>
                <span>支持填写多条英语考试记录</span>
              </span>
              <span class="panel-toggle__action">{{ isSectionExpanded('english-section') ? '收起' : '展开' }}</span>
              <span class="panel-toggle__icon" :class="{ 'panel-toggle__icon--expanded': isSectionExpanded('english-section') }" aria-hidden="true"></span>
            </button>
            <div v-show="isSectionExpanded('english-section')" class="panel-body">
              <div class="record-toolbar">
                <div>
                  <strong>英语能力列表</strong>
                  <span>可填写 CET、IELTS、TOEFL 等成绩。</span>
                </div>
                <button type="button" class="secondary-button" @click="addEnglish">新增英语成绩</button>
              </div>
              <div v-if="!(form.english_proficiencies && form.english_proficiencies.length)" class="empty-state">当前未填写英语成绩，可后续补充。</div>
              <div v-else class="record-list">
                <section v-for="(item, index) in form.english_proficiencies" :key="`english-${index}`" class="record-card">
                  <div class="record-card__header">
                    <div><strong>英语成绩 {{ index + 1 }}</strong><span>支持多条</span></div>
                    <button type="button" class="tertiary-button" @click="removeEnglish(index)">删除</button>
                  </div>
                  <div class="form-grid form-grid--three">
                    <label><span>英语考试名称</span><select v-model="item.exam_name"><option value="">请选择</option><option v-for="exam in englishExamOptions" :key="exam" :value="exam">{{ exam }}</option></select></label>
                    <label><span>成绩</span><input v-model="item.score_text" placeholder="请输入成绩" /></label>
                  </div>
                  <div class="upload-grid upload-grid--single">
                    <div class="upload-field">
                      <span class="upload-field__label">英语证明附件</span>
                      <div class="upload-field__controls">
                        <input :value="item.certificate_attachment_url || ''" readonly placeholder="未上传时可留空" />
                        <input
                          class="upload-file-input"
                          type="file"
                          :disabled="isAttachmentUploading(buildAttachmentUploadKey('english', index, 'certificate'))"
                          :accept="certificateAttachmentAccept"
                          @change="handleEnglishAttachmentUpload(index, $event)"
                        />
                      </div>
                      <small class="upload-field__hint">{{ isAttachmentUploading(buildAttachmentUploadKey('english', index, 'certificate')) ? '上传中...' : '支持 PDF/JPG/PNG/WEBP，单个文件不超过 20MB' }}</small>
                    </div>
                  </div>
                </section>
              </div>
            </div>
          </article>

          <article id="family-section" class="application-panel" :class="{ 'application-panel--collapsed': !isSectionExpanded('family-section') }">
            <button type="button" class="panel-toggle" @click="toggleSection('family-section')">
              <span class="panel-toggle__copy">
                <small>STEP 07</small>
                <strong>家庭情况</strong>
                <span>父母信息必填，兄弟姐妹可按需补充</span>
              </span>
              <span class="panel-toggle__action">{{ isSectionExpanded('family-section') ? '收起' : '展开' }}</span>
              <span class="panel-toggle__icon" :class="{ 'panel-toggle__icon--expanded': isSectionExpanded('family-section') }" aria-hidden="true"></span>
            </button>
            <div v-show="isSectionExpanded('family-section')" class="panel-body">
              <div class="record-toolbar">
                <div>
                  <strong>家庭成员</strong>
                  <span>父亲与母亲信息请完整填写，其他成员可补充。</span>
                </div>
                <button type="button" class="secondary-button" @click="addFamilyMember">新增家庭成员</button>
              </div>
              <div class="record-list">
                <section v-for="(item, index) in form.family_members" :key="`family-${index}`" class="record-card">
                  <div class="record-card__header">
                    <div><strong>家庭成员 {{ index + 1 }}</strong><span>{{ item.relation_type || '请选择关系' }}</span></div>
                    <button v-if="form.family_members!.length > 2" type="button" class="tertiary-button" @click="removeFamilyMember(index)">删除</button>
                  </div>
                  <div class="form-grid form-grid--three">
                    <label><span>与本人关系</span><select v-model="item.relation_type"><option value="">请选择</option><option v-for="relation in familyRelationOptions" :key="relation" :value="relation">{{ relation }}</option></select></label>
                    <label><span>姓名</span><input v-model="item.member_name" placeholder="请输入姓名" /></label>
                    <label><span>联系电话</span><input v-model="item.contact_phone" placeholder="请输入联系电话" /></label>
                    <label><span>工作单位</span><input v-model="item.employer_name" placeholder="请输入工作单位" /></label>
                    <label><span>职务</span><input v-model="item.job_title" placeholder="请输入职务" /></label>
                  </div>
                </section>
              </div>
            </div>
          </article>

          <article id="achievement-section" class="application-panel" :class="{ 'application-panel--collapsed': !isSectionExpanded('achievement-section') }">
            <button type="button" class="panel-toggle" @click="toggleSection('achievement-section')">
              <span class="panel-toggle__copy">
                <small>STEP 08</small>
                <strong>论文发表及获奖经历</strong>
                <span>该部分非必填，可补充论文、科研或获奖成果</span>
              </span>
              <span class="panel-toggle__action">{{ isSectionExpanded('achievement-section') ? '收起' : '展开' }}</span>
              <span class="panel-toggle__icon" :class="{ 'panel-toggle__icon--expanded': isSectionExpanded('achievement-section') }" aria-hidden="true"></span>
            </button>
            <div v-show="isSectionExpanded('achievement-section')" class="panel-body">
              <div class="record-toolbar">
                <div>
                  <strong>成果记录</strong>
                  <span>支持论文、科研项目、学生活动和获奖经历。</span>
                </div>
                <button type="button" class="secondary-button" @click="addAchievement">新增成果记录</button>
              </div>
              <div v-if="!(form.achievement_records && form.achievement_records.length)" class="empty-state">当前未填写论文或获奖经历，可留空提交。</div>
              <div v-else class="record-list">
                <section v-for="(item, index) in form.achievement_records" :key="`achievement-${index}`" class="record-card">
                  <div class="record-card__header">
                    <div><strong>成果记录 {{ index + 1 }}</strong><span>非必填</span></div>
                    <button type="button" class="tertiary-button" @click="removeAchievement(index)">删除</button>
                  </div>
                  <div class="form-grid form-grid--three">
                    <label><span>类型</span><select v-model="item.achievement_type"><option value="">请选择</option><option v-for="type in achievementTypeOptions" :key="type" :value="type">{{ type }}</option></select></label>
                    <label><span>论文名称</span><input v-model="item.paper_title" placeholder="论文发表时填写" /></label>
                    <label><span>作者序位</span><input v-model="item.author_order" placeholder="如 第一作者" /></label>
                    <label><span>期刊/会议名称</span><input v-model="item.journal_or_conference" placeholder="请输入期刊或会议名称" /></label>
                    <label><span>发表/收录日期（年月）</span><input v-model="item.publish_or_index_month" type="month" /></label>
                    <label><span>奖项名称</span><input v-model="item.award_name" placeholder="获奖时填写" /></label>
                    <label><span>颁发机构</span><input v-model="item.awarding_organization" placeholder="请输入颁发机构" /></label>
                    <label><span>获奖等级</span><input v-model="item.award_level" placeholder="如 全国一等奖" /></label>
                    <label><span>获奖年份</span><input v-model="item.award_year" placeholder="如 2025" /></label>
                    <label class="form-field form-field--full"><span>职责内容</span><textarea v-model="item.responsibility_text" rows="4" placeholder="请输入成果说明、职责或获奖背景" /></label>
                  </div>
                </section>
              </div>
            </div>
          </article>

          <article id="statement-section" class="application-panel" :class="{ 'application-panel--collapsed': !isSectionExpanded('statement-section') }">
            <button type="button" class="panel-toggle" @click="toggleSection('statement-section')">
              <span class="panel-toggle__copy">
                <small>STEP 09</small>
                <strong>个人陈述与提交确认</strong>
                <span>填写个人陈述、AI 问题思考并完成声明确认</span>
              </span>
              <span class="panel-toggle__action">{{ isSectionExpanded('statement-section') ? '收起' : '展开' }}</span>
              <span class="panel-toggle__icon" :class="{ 'panel-toggle__icon--expanded': isSectionExpanded('statement-section') }" aria-hidden="true"></span>
            </button>
            <div v-show="isSectionExpanded('statement-section')" class="panel-body">
              <div class="form-grid form-grid--three">
                <label class="form-field form-field--full"><span>个人陈述</span><textarea v-model="form.personal_statement!.personal_statement_text" rows="6" placeholder="请输入申请动机、研究基础与职业规划" /></label>
                <label class="form-field form-field--full"><span>AI 关键问题思考</span><textarea v-model="form.personal_statement!.ai_problem_statement" rows="5" placeholder="请输入你关注的 AI 关键问题" /></label>
                <label class="form-field form-field--full"><span>AI 行业不同观点</span><textarea v-model="form.personal_statement!.ai_industry_opinion" rows="5" placeholder="请输入你对行业议题的不同观点或补充说明" /></label>
              </div>
              <div class="upload-grid upload-grid--single">
                <div class="upload-field">
                  <span class="upload-field__label">个人简历附件</span>
                  <div class="upload-field__controls">
                    <input :value="form.personal_statement!.resume_attachment_url || ''" readonly placeholder="支持 PDF / Word 简历" />
                    <input
                      class="upload-file-input"
                      type="file"
                      :disabled="isAttachmentUploading(buildAttachmentUploadKey('statement', 0, 'resume'))"
                      :accept="resumeAttachmentAccept"
                      @change="handleResumeAttachmentUpload"
                    />
                  </div>
                  <small class="upload-field__hint">{{ isAttachmentUploading(buildAttachmentUploadKey('statement', 0, 'resume')) ? '上传中...' : '支持 PDF/DOC/DOCX，单个文件不超过 20MB' }}</small>
                </div>
              </div>
              <div class="section-note section-note--muted">
                <strong>附件上传</strong>
                <span>已支持简历、成绩单、学位证和英语证明上传；后续如需扩展更多材料类型，再继续补充材料清单归档。</span>
              </div>
              <label class="agreement-row">
                <input v-model="form.declaration!.has_read_declaration" type="checkbox" />
                <span>{{ form.declaration!.declaration_text || '我已同意并仔细阅读使用条款和隐私政策。' }}</span>
              </label>
              <div class="submit-row">
                <button type="button" class="primary-button" :disabled="submitting" @click="submitForm">提交申请表</button>
                <span>最近提交时间：{{ student?.application_draft?.submitted_at || student?.submitted_at || '尚未提交' }}</span>
              </div>
            </div>
          </article>
        </section>
      </section>

      <div class="floating-action-stack">
        <button type="button" class="floating-action-button floating-action-button--directory" @click="toggleQuickNav">
          <span class="floating-action-button__icon floating-action-button__icon--directory" aria-hidden="true"></span>
          <span>目录</span>
        </button>
        <button v-if="showBackToTop" type="button" class="floating-action-button floating-action-button--primary" @click="scrollToTop">
          <span class="floating-action-button__icon floating-action-button__icon--up" aria-hidden="true"></span>
          <span>回到顶部</span>
        </button>
      </div>

      <div v-if="quickNavOpen" class="quick-nav-overlay" @click="closeQuickNav"></div>
      <aside v-if="quickNavOpen" class="quick-nav-panel">
        <div class="quick-nav-panel__header">
          <div>
            <span>快捷目录</span>
            <strong>跳转到目标章节</strong>
          </div>
          <button type="button" class="quick-nav-panel__close" @click="closeQuickNav">关闭</button>
        </div>
        <div class="quick-nav-panel__body">
          <section v-for="group in sectionGroups" :key="`quick-${group.id}`" class="quick-nav-group">
            <span class="quick-nav-group__title">{{ group.label }}</span>
            <button
              v-for="sectionId in group.items"
              :key="`quick-${sectionId}`"
              type="button"
              class="quick-nav-item"
              :class="{ 'quick-nav-item--active': activeSectionId === sectionId }"
              @click="scrollToSection(sectionId)"
            >
              <span class="quick-nav-item__index">{{ String(sectionItems.findIndex((item) => item.id === sectionId) + 1).padStart(2, '0') }}</span>
              <span class="quick-nav-item__copy">
                <strong>{{ sectionItems.find((item) => item.id === sectionId)?.label }}</strong>
                <small>{{ sectionItems.find((item) => item.id === sectionId)?.caption }}</small>
              </span>
            </button>
          </section>
        </div>
      </aside>
    </main>

    <el-dialog v-model="profileDialogVisible" title="个人空间" width="480px" destroy-on-close>
      <div class="profile-dialog">
        <div class="profile-dialog__summary">
          <div>
            <span>当前账号</span>
            <strong>{{ student?.full_name || '考生' }}</strong>
          </div>
          <div>
            <span>登录方式</span>
            <strong>{{ student?.phone_number || student?.email || '-' }}</strong>
          </div>
          <div>
            <span>账号状态</span>
            <strong>{{ student?.account_status || '启用' }}</strong>
          </div>
        </div>
        <div class="profile-dialog__form">
          <label>
            <span>当前密码</span>
            <input v-model="profileForm.current_password" type="password" placeholder="请输入当前密码" />
          </label>
          <label>
            <span>新密码</span>
            <input v-model="profileForm.new_password" type="password" placeholder="请输入新密码" />
          </label>
          <label>
            <span>确认新密码</span>
            <input v-model="profileForm.confirm_password" type="password" placeholder="请再次输入新密码" />
          </label>
        </div>
      </div>
      <template #footer>
        <div class="profile-dialog__footer">
          <button type="button" class="secondary-button" @click="profileDialogVisible = false">取消</button>
          <button type="button" class="primary-button" :disabled="profileSubmitting" @click="submitProfilePasswordChange">
            {{ profileSubmitting ? '保存中...' : '保存新密码' }}
          </button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.portal-application-shell {
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
  overflow-y: visible;
  font-family: 'Microsoft YaHei', 'Microsoft YaHei UI', sans-serif;
  background:
    radial-gradient(circle at top left, rgba(78, 129, 255, 0.18), transparent 28%),
    radial-gradient(circle at right 20%, rgba(35, 210, 255, 0.18), transparent 26%),
    linear-gradient(180deg, #eef4ff 0%, #f7faff 44%, #edf3fb 100%);
  color: #23344d;
}

.application-ambient {
  position: absolute;
  width: 420px;
  height: 420px;
  border-radius: 50%;
  filter: blur(90px);
  opacity: 0.42;
  pointer-events: none;
}

.application-ambient--left {
  top: -140px;
  left: -120px;
  background: rgba(52, 116, 255, 0.28);
}

.application-ambient--right {
  top: 120px;
  right: -160px;
  background: rgba(42, 209, 201, 0.24);
}

.application-header {
  position: relative;
  z-index: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 18px 32px;
  background: linear-gradient(90deg, #071a64, #1f2ea3 48%, #2818ab 100%);
  color: #fff;
  box-shadow: 0 18px 54px rgba(9, 26, 92, 0.26);
}

.application-header__brand,
.application-header__user {
  display: flex;
  align-items: center;
  gap: 14px;
}

.application-header__brand strong,
.application-header__brand span {
  display: block;
}

.application-header__brand span {
  font-size: 12px;
  opacity: 0.74;
}

.brand-logo {
  width: 72px;
  height: 46px;
  display: grid;
  place-items: center;
  border-radius: 12px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.18), rgba(255, 255, 255, 0.08));
  font-weight: 700;
  border: 1px solid rgba(255, 255, 255, 0.22);
}

.application-header__user button,
.primary-button,
.secondary-button,
.tertiary-button,
.application-nav button,
.plan-pick-card {
  cursor: pointer;
}

.application-header__user button,
.primary-button,
.secondary-button {
  border: none;
  border-radius: 12px;
}

.application-header__user button {
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.12);
  color: #fff;
}

.profile-dialog {
  display: grid;
  gap: 18px;
}

.profile-dialog__summary {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
  padding: 14px 16px;
  border-radius: 16px;
  background: linear-gradient(135deg, rgba(16, 56, 165, 0.08), rgba(64, 170, 255, 0.12));
}

.profile-dialog__summary span,
.profile-dialog__form span {
  display: block;
  margin-bottom: 6px;
  font-size: 12px;
  color: #6c7b93;
}

.profile-dialog__summary strong {
  display: block;
  color: #19315e;
}

.profile-dialog__form {
  display: grid;
  gap: 14px;
}

.profile-dialog__form input {
  width: 100%;
  padding: 11px 12px;
  border-radius: 12px;
  border: 1px solid rgba(25, 49, 94, 0.14);
  background: #fff;
}

.profile-dialog__footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.application-page {
  position: relative;
  z-index: 1;
  padding: 20px 24px 36px;
}

.application-notice {
  display: grid;
  gap: 10px;
  padding: 14px 18px;
  margin-bottom: 12px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.72);
  border: 1px solid rgba(108, 138, 196, 0.16);
  backdrop-filter: blur(10px);
  color: #415473;
}

.application-notice__meta {
  display: flex;
  gap: 18px;
  flex-wrap: wrap;
}

.application-notice p,
.application-notice span {
  margin: 0;
}

.application-layout {
  display: grid;
  grid-template-columns: 228px minmax(0, 1fr);
  gap: 20px;
  align-items: start;
}

.application-nav,
.application-panel {
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.78);
  box-shadow: 0 20px 48px rgba(65, 88, 135, 0.1);
  backdrop-filter: blur(14px);
  border: 1px solid rgba(119, 144, 192, 0.12);
}

.application-nav {
  position: sticky;
  display: grid;
  gap: 10px;
  padding: 14px;
  transition: top 0.28s ease, transform 0.28s ease;
}

@media (prefers-reduced-motion: reduce) {
  .application-nav {
    transition: none;
  }
}

.application-nav__group {
  display: grid;
  gap: 8px;
}

.application-nav__group-toggle {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
  width: 100%;
  padding: 14px 16px;
  border: none;
  border-radius: 18px;
  text-align: left;
  background: linear-gradient(180deg, rgba(228, 237, 252, 0.96), rgba(244, 248, 255, 0.94));
  color: #19385f;
}

.application-nav__group-copy {
  display: grid;
  gap: 4px;
}

.application-nav__group-copy strong {
  font-size: 15px;
}

.application-nav__group-copy small {
  color: #6b7e9b;
}

.application-nav__group-icon {
  position: relative;
  width: 14px;
  height: 14px;
  flex: 0 0 auto;
}

.application-nav__group-icon::before,
.application-nav__group-icon::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 9px;
  height: 2px;
  border-radius: 999px;
  background: #1d4f8e;
  transform-origin: center;
  transition: transform 0.22s ease;
}

.application-nav__group-icon::before {
  transform: translate(-64%, -50%) rotate(45deg);
}

.application-nav__group-icon::after {
  transform: translate(-12%, -50%) rotate(-45deg);
}

.application-nav__group-icon--expanded::before {
  transform: translate(-64%, -50%) rotate(-45deg);
}

.application-nav__group-icon--expanded::after {
  transform: translate(-12%, -50%) rotate(45deg);
}

.application-nav__group-items {
  display: grid;
  gap: 8px;
  padding-left: 10px;
  border-left: 1px dashed rgba(65, 103, 164, 0.24);
}

.application-nav__heading,
.application-nav__status {
  display: grid;
  gap: 4px;
  padding: 14px 16px;
  border-radius: 18px;
  background: linear-gradient(180deg, rgba(233, 241, 255, 0.92), rgba(247, 250, 255, 0.88));
}

.application-nav__heading span,
.application-nav__status span {
  color: #6a7d99;
  font-size: 12px;
}

.application-nav__heading strong,
.application-nav__status strong {
  color: #163258;
}

.application-nav__status small {
  color: #7385a0;
}

.application-nav__item {
  position: relative;
  display: grid;
  grid-template-columns: 44px minmax(0, 1fr);
  gap: 12px;
  align-items: center;
  padding: 14px 12px 14px 16px;
  border: none;
  border-radius: 16px;
  text-align: left;
  background: linear-gradient(180deg, rgba(244, 248, 255, 0.98), rgba(237, 243, 252, 0.94));
  color: #395173;
  transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
}

.application-nav__item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 12px;
  bottom: 12px;
  width: 4px;
  border-radius: 999px;
  background: transparent;
  transition: background 0.2s ease, box-shadow 0.2s ease;
}

.application-nav__item:hover {
  transform: translateX(2px);
  box-shadow: 0 12px 26px rgba(42, 79, 142, 0.12);
}

.application-nav__item--active {
  background: linear-gradient(135deg, #113c78, #1a5aa8 62%, #32ace2);
  color: #fff;
  box-shadow: 0 18px 34px rgba(20, 64, 127, 0.24);
}

.application-nav__item--active::before {
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(181, 235, 255, 0.92));
  box-shadow: 0 0 18px rgba(146, 229, 255, 0.72);
}

.application-nav__index {
  display: grid;
  place-items: center;
  width: 44px;
  height: 44px;
  border-radius: 14px;
  background: rgba(17, 56, 112, 0.08);
  font-size: 13px;
  font-weight: 700;
}

.application-nav__item--active .application-nav__index {
  background: rgba(255, 255, 255, 0.16);
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.12);
}

.application-nav__copy {
  display: grid;
  gap: 3px;
}

.application-nav__copy strong {
  font-size: 14px;
}

.application-nav__copy small {
  color: inherit;
  opacity: 0.72;
}

.floating-action-stack {
  position: fixed;
  right: 28px;
  bottom: 28px;
  z-index: 12;
  display: grid;
  gap: 12px;
}

.floating-action-button {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  min-height: 48px;
  padding: 0 16px;
  border: none;
  border-radius: 999px;
  cursor: pointer;
}

.floating-action-button--primary {
  background: linear-gradient(135deg, #113c78, #1b5eb2 58%, #2ba7e2);
  color: #fff;
  font-size: 14px;
  font-weight: 700;
  box-shadow: 0 18px 34px rgba(20, 64, 127, 0.24);
}

.floating-action-button--directory {
  background: rgba(255, 255, 255, 0.94);
  color: #163258;
  font-size: 14px;
  font-weight: 700;
  box-shadow: 0 18px 34px rgba(65, 88, 135, 0.16);
  border: 1px solid rgba(119, 144, 192, 0.2);
}

.floating-action-button__icon {
  position: relative;
  width: 14px;
  height: 14px;
  flex: 0 0 auto;
}

.floating-action-button__icon::before,
.floating-action-button__icon::after,
.floating-action-button__icon--directory span {
  content: '';
  position: absolute;
  background: currentColor;
}

.floating-action-button__icon--up::before,
.floating-action-button__icon--up::after {
  top: 4px;
  width: 9px;
  height: 2px;
  border-radius: 999px;
}

.floating-action-button__icon--up::before {
  left: 0;
  transform: rotate(-45deg);
}

.floating-action-button__icon--up::after {
  right: 0;
  transform: rotate(45deg);
}

.floating-action-button__icon--directory::before,
.floating-action-button__icon--directory::after {
  left: 1px;
  width: 12px;
  height: 2px;
  border-radius: 999px;
}

.floating-action-button__icon--directory::before {
  top: 3px;
}

.floating-action-button__icon--directory::after {
  top: 9px;
}

.floating-action-button__icon--directory {
  box-shadow: inset 0 -1px 0 currentColor;
}

.quick-nav-overlay {
  position: fixed;
  inset: 0;
  z-index: 13;
  background: rgba(10, 23, 59, 0.22);
  backdrop-filter: blur(4px);
}

.quick-nav-panel {
  position: fixed;
  right: 28px;
  bottom: 96px;
  z-index: 14;
  width: min(360px, calc(100vw - 32px));
  max-height: min(68vh, 560px);
  display: grid;
  grid-template-rows: auto minmax(0, 1fr);
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.96);
  border: 1px solid rgba(119, 144, 192, 0.2);
  box-shadow: 0 24px 60px rgba(31, 55, 102, 0.24);
  overflow: hidden;
}

.quick-nav-panel__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 14px 18px 10px;
  background: linear-gradient(180deg, rgba(236, 243, 255, 0.96), rgba(255, 255, 255, 0.92));
}

.quick-nav-panel__header span {
  display: block;
  color: #7083a0;
  font-size: 11px;
}

.quick-nav-panel__header strong {
  display: block;
  color: #173459;
  font-size: 16px;
}

.quick-nav-panel__close {
  border: none;
  background: transparent;
  color: #1b5aa8;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
}

.quick-nav-panel__body {
  overflow-y: auto;
  padding: 8px 12px 12px;
  display: grid;
  gap: 10px;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.quick-nav-panel__body::-webkit-scrollbar {
  display: none;
}

.quick-nav-group {
  display: grid;
  gap: 6px;
}

.quick-nav-group__title {
  color: #72839f;
  font-size: 11px;
  font-weight: 700;
  padding: 0 6px;
}

.quick-nav-item {
  display: grid;
  grid-template-columns: 34px minmax(0, 1fr);
  gap: 10px;
  align-items: center;
  width: 100%;
  padding: 10px 12px;
  border: none;
  border-radius: 14px;
  background: linear-gradient(180deg, rgba(244, 248, 255, 0.98), rgba(237, 243, 252, 0.94));
  text-align: left;
  color: #395173;
  cursor: pointer;
}

.quick-nav-item--active {
  background: linear-gradient(135deg, #113c78, #1a5aa8 62%, #32ace2);
  color: #fff;
  box-shadow: 0 18px 34px rgba(20, 64, 127, 0.24);
}

.quick-nav-item__index {
  display: grid;
  place-items: center;
  width: 34px;
  height: 34px;
  border-radius: 10px;
  background: rgba(17, 56, 112, 0.08);
  font-size: 12px;
  font-weight: 700;
}

.quick-nav-item--active .quick-nav-item__index {
  background: rgba(255, 255, 255, 0.16);
}

.quick-nav-item__copy {
  display: grid;
  gap: 1px;
}

.quick-nav-item__copy strong {
  font-size: 13px;
  line-height: 1.2;
}

.quick-nav-item__copy small {
  color: inherit;
  opacity: 0.72;
  font-size: 11px;
  line-height: 1.25;
}

.application-content {
  display: grid;
  gap: 18px;
}

.application-panel {
  padding: 22px;
  scroll-margin-top: 112px;
}

.application-panel--collapsed {
  padding-bottom: 16px;
}

.panel-toggle {
  display: flex;
  width: 100%;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 0;
  border: none;
  background: transparent;
  text-align: left;
  color: inherit;
}

.panel-toggle__copy {
  display: grid;
  gap: 4px;
}

.panel-toggle__copy small {
  color: #6b83a6;
  font-size: 12px;
  letter-spacing: 0.1em;
}

.panel-toggle__copy strong {
  font-size: 22px;
  color: #173459;
}

.panel-toggle__copy span {
  color: #6a7a91;
  font-size: 12px;
}

.panel-toggle__action {
  margin-left: auto;
  color: #597293;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.04em;
}

.panel-toggle__icon {
  position: relative;
  width: 18px;
  height: 18px;
  flex: 0 0 auto;
}

.panel-toggle__icon::before,
.panel-toggle__icon::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 10px;
  height: 2px;
  border-radius: 999px;
  background: #1d4f8e;
  transition: transform 0.22s ease;
}

.panel-toggle__icon::before {
  left: 1px;
  transform: translateY(-50%) rotate(45deg);
}

.panel-toggle__icon::after {
  right: 1px;
  transform: translateY(-50%) rotate(-45deg);
}

.panel-toggle__icon--expanded::before {
  transform: translateY(-50%) rotate(-45deg);
}

.panel-toggle__icon--expanded::after {
  transform: translateY(-50%) rotate(45deg);
}

.panel-body {
  display: grid;
  gap: 18px;
  margin-top: 18px;
  width: 100%;
}

.profile-photo-card {
  display: grid;
  grid-template-columns: 168px minmax(0, 1fr);
  gap: 18px;
  padding: 18px;
  border-radius: 20px;
  border: 1px solid rgba(116, 141, 184, 0.16);
  background: linear-gradient(180deg, rgba(251, 253, 255, 0.98), rgba(244, 248, 255, 0.94));
  box-shadow: 0 14px 32px rgba(82, 107, 150, 0.08);
}

.profile-photo-card__preview {
  width: 168px;
  height: 212px;
  border-radius: 18px;
  overflow: hidden;
  background: linear-gradient(180deg, rgba(236, 244, 255, 0.88), rgba(247, 250, 255, 0.94));
  border: 1px solid rgba(125, 148, 191, 0.18);
  display: grid;
  place-items: center;
}

.profile-photo-card__preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.profile-photo-card__empty {
  padding: 16px;
  text-align: center;
  color: #6f7f97;
  font-size: 13px;
  line-height: 1.6;
}

.profile-photo-card__content {
  display: grid;
  gap: 12px;
  align-content: start;
}

.profile-photo-card__copy {
  display: grid;
  gap: 6px;
}

.profile-photo-card__copy strong {
  color: #173459;
}

.profile-photo-card__copy span {
  color: #697d99;
  font-size: 13px;
}

.plan-pick-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 18px 36px rgba(79, 111, 163, 0.12);
}

.plan-pick-card--active {
  border-color: #173f7b;
  background: linear-gradient(180deg, rgba(23, 63, 123, 0.08), rgba(32, 113, 190, 0.08));
  box-shadow: 0 0 0 3px rgba(20, 61, 118, 0.1), 0 18px 34px rgba(33, 72, 132, 0.14);
}

.plan-pick-card span,
.plan-pick-card small {
  display: block;
  margin-top: 8px;
  color: #6d7c91;
}
.brochure-preview {
  display: grid;
  grid-template-columns: minmax(220px, 320px) minmax(0, 1fr);
  gap: 18px;
  margin-top: 18px;
}

.brochure-preview__media,
.brochure-preview__content {
  min-width: 0;
}
.brochure-preview__placeholder {
  width: 100%;
  min-height: 220px;
  border-radius: 20px;
  background: #f0f4fb;
}

.portal-plan-spotlight {
  position: relative;
  overflow: hidden;
  display: grid;
  gap: 18px;
  padding: 26px 28px;
  border-radius: 24px;
  border: 1px solid rgba(31, 84, 156, 0.14);
  background:
    radial-gradient(circle at top right, rgba(90, 186, 255, 0.22), transparent 28%),
    linear-gradient(135deg, rgba(17, 49, 110, 0.96), rgba(24, 78, 150, 0.92) 54%, rgba(46, 177, 232, 0.84));
  box-shadow: 0 24px 56px rgba(22, 63, 125, 0.18);
}

.portal-plan-spotlight::after {
  content: '';
  position: absolute;
  inset: auto -36px -48px auto;
  width: 180px;
  height: 180px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.08);
}

.portal-plan-spotlight__badge {
  position: relative;
  z-index: 1;
  display: inline-flex;
  width: fit-content;
  padding: 7px 12px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.16);
  color: rgba(255, 255, 255, 0.92);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.06em;
}

.portal-plan-spotlight__copy {
  position: relative;
  z-index: 1;
  display: grid;
  gap: 12px;
}

.portal-plan-spotlight__copy strong {
  font-size: 28px;
  line-height: 1.25;
  color: #fff;
}

.portal-plan-spotlight__copy p {
  margin: 0;
  max-width: 760px;
  color: rgba(236, 245, 255, 0.9);
  line-height: 1.9;
  font-size: 15px;
}

.portal-plan-empty {
  padding: 18px 20px;
  border-radius: 18px;
  border: 1px dashed rgba(115, 138, 177, 0.34);
  background: rgba(255, 255, 255, 0.72);
  color: #5c6f8f;
}

label {
  display: grid;
  gap: 8px;
  color: #41536d;
  font-size: 14px;
}

input,
select,
textarea {
  width: 100%;
  min-height: 48px;
  padding: 12px 14px;
  border-radius: 14px;
  border: 1px solid #d9e3f1;
  background: rgba(250, 252, 255, 0.96);
  color: #23344d;
  font: inherit;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.6);
}

input:focus,
select:focus,
textarea:focus {
  outline: none;
  border-color: #2a83d7;
  box-shadow: 0 0 0 4px rgba(42, 131, 215, 0.12);
}

textarea {
  min-height: 120px;
  resize: vertical;
}

.record-toolbar {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: center;
  gap: 16px;
  padding: 12px 14px;
  border-radius: 18px;
  background: rgba(240, 246, 255, 0.86);
  width: 100%;
}

.record-toolbar div {
  display: grid;
  gap: 4px;
}

.record-toolbar strong,
.section-note strong,
.record-card__header strong,
.empty-state {
  color: #173459;
}

.record-toolbar span,
.section-note span,
.record-card__header span {
  color: #697d99;
  font-size: 13px;
}

.record-list {
  display: grid;
  gap: 14px;
  width: 100%;
}

.record-card {
  display: grid;
  gap: 16px;
  padding: 18px;
  border-radius: 20px;
  border: 1px solid rgba(116, 141, 184, 0.16);
  background: linear-gradient(180deg, rgba(251, 253, 255, 0.98), rgba(244, 248, 255, 0.94));
  box-shadow: 0 14px 32px rgba(82, 107, 150, 0.08);
  width: 100%;
}

.record-card__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.record-card__header div {
  display: grid;
  gap: 4px;
}

.form-grid {
  display: grid;
  gap: 14px;
  align-items: start;
}

.form-grid--three {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.form-grid--two {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.form-field--full {
  grid-column: 1 / -1;
}

.upload-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
  width: 100%;
}

.upload-grid .upload-field {
  grid-column: span 2;
}

.upload-grid--single {
  grid-template-columns: 1fr;
}

.upload-grid--single .upload-field {
  grid-column: 1 / -1;
}

.upload-field {
  display: grid;
  gap: 8px;
  padding: 14px;
  border-radius: 16px;
  background: rgba(247, 250, 255, 0.92);
  border: 1px solid rgba(125, 148, 191, 0.16);
}

.upload-field--compact {
  padding: 0;
  border: none;
  background: transparent;
}

.upload-field__label {
  color: #173459;
  font-size: 13px;
  font-weight: 700;
}

.upload-field__controls {
  display: grid;
  gap: 10px;
}

.upload-file-input {
  min-height: 46px;
  padding: 10px 12px;
  background: rgba(255, 255, 255, 0.94);
}

.upload-field__hint {
  color: #6f7f97;
  font-size: 12px;
}

.section-note {
  display: grid;
  gap: 4px;
  padding: 12px 14px;
  border-radius: 16px;
  background: rgba(236, 244, 255, 0.82);
  border: 1px solid rgba(125, 148, 191, 0.16);
}

.section-note--muted {
  background: rgba(247, 250, 255, 0.88);
}

.empty-state {
  padding: 16px 18px;
  border-radius: 18px;
  background: rgba(248, 251, 255, 0.96);
  border: 1px dashed rgba(125, 148, 191, 0.28);
}

.secondary-button {
  min-height: 40px;
  padding: 0 14px;
  background: linear-gradient(180deg, #edf4ff, #dceafe);
  color: #194b8b;
  font-weight: 700;
}

.secondary-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.tertiary-button {
  padding: 0;
  border: none;
  background: transparent;
  color: #b84a58;
  font-weight: 700;
}

.agreement-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 10px;
  color: #41536d;
  line-height: 1.5;
}

.agreement-row input {
  width: 18px;
  min-width: 18px;
  height: 18px;
  min-height: 18px;
  margin: 0;
  padding: 0;
  border-radius: 5px;
  box-shadow: none;
}

.agreement-row span {
  display: inline-flex;
  align-items: center;
  min-height: 18px;
}

.submit-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-top: 18px;
}

.submit-row span {
  color: #6e7b90;
  font-size: 13px;
}

.primary-button {
  min-height: 46px;
  padding: 0 22px;
  background: linear-gradient(135deg, #154383, #144b93 58%, #2eb1e8);
  color: #fff;
  font-weight: 700;
  box-shadow: 0 16px 30px rgba(23, 74, 140, 0.24);
}

@media (max-width: 1180px) {
  .profile-photo-card,
  .form-grid--three,
  .form-grid--two,
  .upload-grid,
  .portal-plan-spotlight {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .upload-grid .upload-field,
  .upload-grid--single .upload-field {
    grid-column: span 1;
  }

  .application-layout {
    grid-template-columns: 1fr;
  }

  .application-nav {
    position: static;
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .application-nav__group {
    grid-column: span 1;
  }

  .application-nav__heading,
  .application-nav__status {
    grid-column: 1 / -1;
  }
}

@media (max-width: 720px) {
  .form-grid--three,
  .form-grid--two,
  .upload-grid,
  .profile-photo-card,
  .portal-plan-spotlight {
    grid-template-columns: 1fr;
  }

  .upload-grid .upload-field,
  .upload-grid--single .upload-field {
    grid-column: 1 / -1;
  }

  .application-header,
  .submit-row,
  .record-toolbar,
  .record-card__header {
    flex-direction: column;
    align-items: flex-start;
  }

  .application-page {
    padding: 14px;
  }

  .application-nav {
    grid-template-columns: 1fr;
  }

  .profile-dialog__summary {
    grid-template-columns: 1fr;
  }

  .portal-plan-spotlight {
    padding: 20px 18px;
  }

  .portal-plan-spotlight__copy strong {
    font-size: 22px;
  }
}
</style>