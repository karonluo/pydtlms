<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

import {
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
  type PortalPlanRecord,
  type PortalPracticeExperienceItem,
  type PortalStudentRecord,
  type PortalTeamRecord,
} from '../../../api/portal'
import type { SelectOption } from '../../../api/common'
import { resolveRequestError, showPortalAlert } from '../../../utils/portalAlerts'
import PortalApplicationSection from './sections/PortalApplicationSection.vue'
import PortalAchievementSection from './sections/PortalAchievementSection.vue'
import PortalBasicSection from './sections/PortalBasicSection.vue'
import PortalEducationSection from './sections/PortalEducationSection.vue'
import PortalEnglishSection from './sections/PortalEnglishSection.vue'
import PortalFamilySection from './sections/PortalFamilySection.vue'
import PortalPracticeSection from './sections/PortalPracticeSection.vue'
import PortalStatementSection from './sections/PortalStatementSection.vue'

const props = defineProps<{
  activeSectionId: string
}>()

const router = useRouter()
const initializing = ref(true)
const savingDraft = ref(false)
const submitting = ref(false)
const student = ref<PortalStudentRecord | null>(null)
const plans = ref<PortalPlanRecord[]>([])
const teams = ref<PortalTeamRecord[]>([])
const politicalStatusOptions = ref<SelectOption[]>([])
const ethnicGroupOptions = ref<SelectOption[]>([])
const selectedPlanId = ref<number | null>(null)
const attachmentUploading = reactive<Record<string, boolean>>({})

type PortalSectionStatus = {
  id: string
  label: string
  completed: boolean
  status: 'not-started' | 'in-progress' | 'completed'
}

type EducationAttachmentField = 'transcript' | 'degree_certificate'

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
  return response.data.url
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
    const url = await uploadAttachmentAndResolveUrl(file, category, field === 'transcript' ? '成绩单附件已上传' : '学位证附件已上传')
    const current = form.education_experiences?.[index]
    if (current) {
      if (field === 'transcript') {
        current.transcript_attachment_url = url
      } else {
        current.degree_certificate_attachment_url = url
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
    const url = await uploadAttachmentAndResolveUrl(file, 'english_certificate', '英语证明附件已上传')
    const current = form.english_proficiencies?.[index]
    if (current) {
      current.certificate_attachment_url = url
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
    const url = await uploadAttachmentAndResolveUrl(file, 'resume', '个人简历已上传')
    if (form.personal_statement) {
      form.personal_statement.resume_attachment_url = url
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
    const url = await uploadAttachmentAndResolveUrl(file, 'profile_photo', '个人照片已上传')
    if (form.profile) {
      form.profile.profile_photo_url = url
    }
  } catch (error) {
    await showPortalAlert(resolveRequestError(error, '个人照片上传失败'), '个人照片上传失败', 'error')
  } finally {
    attachmentUploading[key] = false
    input.value = ''
  }
}

const primaryPreference = computed(() => (form.preferences && form.preferences[0] ? form.preferences[0] : null))
const canAddPreference = computed(() => (form.preferences?.length || 0) < 2)

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

watch(
  () => form.source_channel,
  (value) => {
    if (trimText(value) !== '其他') {
      form.source_channel_other = ''
    }
  },
)

onMounted(async () => {
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
  }
})

defineExpose({
  saveDraft,
  getSectionStatuses: buildSectionStatuses,
  getSavingDraft: () => savingDraft.value,
})
</script>

<template>
  <div class="portal-v2-form-shell">
    <div v-if="initializing" class="portal-v2-form-loading">正在加载申请表...</div>

    <template v-else>
      <PortalBasicSection
        v-if="activeSectionId === 'basic-section'"
        :form="form"
        :student="student"
        :gender-options="genderOptions"
        :ethnic-group-options="ethnicGroupOptions"
        :political-status-options="politicalStatusOptions"
        :id-type-options="idTypeOptions"
        :profile-photo-attachment-accept="profilePhotoAttachmentAccept"
        :is-attachment-uploading="isAttachmentUploading"
        :build-attachment-upload-key="buildAttachmentUploadKey"
        :handle-profile-photo-upload="handleProfilePhotoUpload"
      />

      <PortalApplicationSection
        v-else-if="activeSectionId === 'application-section'"
        :form="form"
        :teams="teams"
        :source-channel-options="sourceChannelOptions"
        :can-add-preference="canAddPreference"
        :add-preference="addPreference"
        :remove-preference="removePreference"
        :advisors-for-center="advisorsForCenter"
        :handle-preference-center-change="handlePreferenceCenterChange"
      />

      <PortalEducationSection
        v-else-if="activeSectionId === 'education-section'"
        :form="form"
        :education-stage-options="educationStageOptions"
        :certificate-attachment-accept="certificateAttachmentAccept"
        :is-attachment-uploading="isAttachmentUploading"
        :build-attachment-upload-key="buildAttachmentUploadKey"
        :handle-education-attachment-upload="handleEducationAttachmentUpload"
        :add-education="addEducation"
        :remove-education="removeEducation"
      />

      <PortalEnglishSection
        v-else-if="activeSectionId === 'english-section'"
        :form="form"
        :english-exam-options="englishExamOptions"
        :certificate-attachment-accept="certificateAttachmentAccept"
        :is-attachment-uploading="isAttachmentUploading"
        :build-attachment-upload-key="buildAttachmentUploadKey"
        :handle-english-attachment-upload="handleEnglishAttachmentUpload"
        :add-english="addEnglish"
        :remove-english="removeEnglish"
      />

      <PortalPracticeSection
        v-else-if="activeSectionId === 'practice-section'"
        :form="form"
        :add-practice="addPractice"
        :remove-practice="removePractice"
      />

      <PortalFamilySection
        v-else-if="activeSectionId === 'family-section'"
        :form="form"
        :family-relation-options="familyRelationOptions"
        :add-family-member="addFamilyMember"
        :remove-family-member="removeFamilyMember"
      />

      <PortalAchievementSection
        v-else-if="activeSectionId === 'achievement-section'"
        :form="form"
        :achievement-type-options="achievementTypeOptions"
        :add-achievement="addAchievement"
        :remove-achievement="removeAchievement"
      />

      <PortalStatementSection
        v-else-if="activeSectionId === 'statement-section'"
        :form="form"
        :resume-attachment-accept="resumeAttachmentAccept"
        :is-attachment-uploading="isAttachmentUploading"
        :build-attachment-upload-key="buildAttachmentUploadKey"
        :handle-resume-attachment-upload="handleResumeAttachmentUpload"
        :submit-form="submitForm"
        :submitting="submitting"
      />

      <div v-else class="portal-v2-form-placeholder">该章节正在拆分中，下一步补入独立组件。</div>
    </template>
  </div>
</template>

<style scoped>
.portal-v2-form-shell {
  min-width: 0;
}

.portal-v2-form-loading,
.portal-v2-form-placeholder {
  display: grid;
  place-items: center;
  min-height: 420px;
  padding: 32px;
  border-radius: 24px;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.94), rgba(248, 251, 255, 0.96));
  color: #4d6384;
  font-size: 15px;
}
</style>