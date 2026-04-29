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

type EducationAttachmentField = 'transcript' | 'degree_certificate' | 'graduation_certificate'

const sourceChannelOptions = [
  '高校老师推荐',
  '学长学姐推荐',
  '上海人工智能实验室官网',
  '上海人工智能实验室公众号',
  '浦江书院小红书',
  '上海人工智能实验室小红书',
  '其他',
]
const genderOptions = ['男', '女']
const idTypeOptions = ['居民身份证', '护照', '港澳居民来往内地通行证']
const educationStageOptionsByOrder: Record<number, string[]> = {
  1: ['高中毕业'],
  2: ['本科在读', '本科毕业'],
  3: ['硕士在读', '硕士毕业'],
}
const englishExamOptions = ['CET-6', 'IELTS', 'TOEFL', '其他']
const familyRelationOptions = ['父亲', '母亲', '兄', '弟', '姐', '妹', '其他']
const achievementTypeOptions = ['论文发表', '获奖经历']
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
const achievementAwardAttachmentAccept = '.pdf,.png,.jpg,.jpeg,.webp'
const profilePhotoAttachmentAccept = '.png,.jpg,.jpeg,.webp'
const idCardCollageAttachmentAccept = '.jpg,.jpeg'
const resumeAttachmentAccept = '.pdf,.doc,.docx'
const supportingMaterialAttachmentAccept = '.zip,.pdf,.doc,.docx,.png,.jpg,.jpeg,.webp'
const declarationReminderText = '本表及证明材料仅作为申请上海人工智能实验室联培博士项目的参考依据，并承诺提交材料的所有内容均真实、准确、完整。所提供的材料中如有任何不实信息，将被取消录取资格。'

function createProfile(): PortalApplicantProfileData {
  return {
    full_name_pinyin: '',
    profile_photo_url: '',
    id_card_collage_url: '',
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

function createEducation(order: number, stage = ''): PortalEducationExperienceItem {
  return {
    sort_order: order,
    education_stage: stage,
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
    graduation_certificate_attachment_url: '',
  }
}

function createDefaultEducationExperiences(): PortalEducationExperienceItem[] {
  return [createEducation(1, '高中毕业')]
}

function ensureEducationExperienceShape(items?: Array<Partial<PortalEducationExperienceItem>> | null) {
  const normalized = (items || []).slice(0, 3).map((item, index) => ({
    ...createEducation(index + 1),
    ...item,
    sort_order: index + 1,
  }))

  if (!normalized.length) {
    normalized.push(createEducation(1, '高中毕业'))
  }

  if (!trimText(normalized[0]?.education_stage) || trimText(normalized[0]?.education_stage) !== '高中毕业') {
    normalized[0].education_stage = '高中毕业'
  }

  return normalized
}

function isHighSchoolStage(stage: string | null | undefined) {
  return trimText(stage) === '高中毕业'
}

function isCurrentEducationStage(stage: string | null | undefined) {
  return trimText(stage).endsWith('在读')
}

function recommendedNextEducationStage(items?: PortalEducationExperienceItem[] | null) {
  const currentItems = items || []
  if (currentItems.length <= 1) {
    return '本科在读'
  }
  if (currentItems.length === 2 && trimText(currentItems[1]?.education_stage) === '本科毕业') {
    return '硕士在读'
  }
  return ''
}

function getEducationStageOptions(index: number) {
  return educationStageOptionsByOrder[index + 1] || []
}

function getEducationAddBlockedMessage(items?: PortalEducationExperienceItem[] | null) {
  const currentItems = items || []
  if (currentItems.length >= 3) {
    return '教育经历最多填写 3 条'
  }
  if (currentItems.length <= 1) {
    return ''
  }

  const secondStage = trimText(currentItems[1]?.education_stage)
  if (secondStage === '本科在读') {
    return '最后一条教育经历当前为“本科在读”，请先改为“本科毕业”，再填写硕士相关经历'
  }
  if (secondStage !== '本科毕业') {
    return '新增教育经历3前，请先将教育经历2的教育阶段填写为“本科毕业”'
  }
  return ''
}

function normalizeEducationWhenStageChanges(item: PortalEducationExperienceItem) {
  if (!trimText(item.education_stage).endsWith('毕业')) {
    item.degree_certificate_attachment_url = ''
    item.degree_certificate_attachment_name = ''
    item.graduation_certificate_attachment_url = ''
    item.graduation_certificate_attachment_name = ''
  }

  if (!isHighSchoolStage(item.education_stage)) {
    return
  }
  item.major_name = ''
  item.average_score = ''
  item.gpa = ''
  item.ranking = ''
}

function getCompletedEducationExperiences(items?: PortalEducationExperienceItem[] | null) {
  return (items || []).filter((item) => trimText(item.education_stage) && trimText(item.school_name))
}

function validateEducationRules(items?: PortalEducationExperienceItem[] | null) {
  const orderedItems = [...(items || [])].sort((left, right) => left.sort_order - right.sort_order)
  const firstItem = orderedItems[0]
  if (!firstItem || trimText(firstItem.education_stage) !== '高中毕业') {
    return '教育经历1的教育阶段必须为“高中毕业”'
  }

  const secondItem = orderedItems[1]
  if (!secondItem || !trimText(secondItem.education_stage) || !trimText(secondItem.school_name)) {
    return '教育经历2必须完整填写，且教育阶段应为“本科在读”或“本科毕业”'
  }
  if (!['本科在读', '本科毕业'].includes(trimText(secondItem.education_stage))) {
    return '教育经历2必须完整填写，且教育阶段应为“本科在读”或“本科毕业”'
  }

  const thirdItem = orderedItems[2]
  const thirdItemStarted = Boolean(
    thirdItem
    && (
      trimText(thirdItem.education_stage)
      || trimText(thirdItem.school_name)
      || trimText(thirdItem.start_month)
      || trimText(thirdItem.end_month)
    ),
  )
  if (thirdItemStarted) {
    if (trimText(secondItem.education_stage) !== '本科毕业') {
      return '填写教育经历3前，教育经历2的教育阶段应为“本科毕业”'
    }
    if (!['硕士在读', '硕士毕业'].includes(trimText(thirdItem?.education_stage))) {
      return '教育经历3的教育阶段应为“硕士在读”或“硕士毕业”'
    }
  }

  for (const [index, item] of orderedItems.entries()) {
    const stage = trimText(item.education_stage)
    if (!stage) {
      continue
    }
    const missingFields: string[] = []
    if (!trimText(item.start_month)) {
      missingFields.push('开始年月')
    }
    if (!isCurrentEducationStage(stage) && !trimText(item.end_month)) {
      missingFields.push('结束年月')
    }
    if (!trimText(item.school_name)) {
      missingFields.push('就读学校')
    }
    if (!trimText(item.verifier_name)) {
      missingFields.push('证明人姓名')
    }
    if (!trimText(item.verifier_phone)) {
      missingFields.push('证明人手机')
    }
    if (!isHighSchoolStage(stage)) {
      if (!trimText(item.major_name)) {
        missingFields.push('就读专业')
      }
      if (!trimText(item.average_score)) {
        missingFields.push('期间平均成绩')
      }
      if (!trimText(item.gpa)) {
        missingFields.push('期间绩点')
      }
      if (!trimText(item.ranking)) {
        missingFields.push('成绩排名')
      }
      if (!trimText(item.transcript_attachment_url)) {
        missingFields.push('成绩单附件')
      }
      if (stage.endsWith('毕业')) {
        if (!trimText(item.degree_certificate_attachment_url)) {
          missingFields.push('学位证附件')
        }
        if (!trimText(item.graduation_certificate_attachment_url)) {
          missingFields.push('毕业证附件')
        }
      }
    }
    if (missingFields.length) {
      return `教育经历${index + 1}以下字段必填：${missingFields.join('、')}`
    }
  }

  const stages = orderedItems.map((item) => trimText(item.education_stage)).filter(Boolean)
  const hasBachelorGraduate = stages.includes('本科毕业')
  const hasBachelorCurrent = stages.includes('本科在读')
  const hasMasterStage = stages.includes('硕士在读') || stages.includes('硕士毕业')

  if (hasBachelorGraduate && !hasMasterStage) {
    return '填写“本科毕业”时，必须同时填写“硕士在读”或“硕士毕业”教育经历'
  }
  if (hasBachelorCurrent && hasMasterStage) {
    return '填写“本科在读”时，不能同时填写“硕士在读”或“硕士毕业”教育经历'
  }
  return ''
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

function practiceItemHasContent(item: PortalPracticeExperienceItem) {
  return Boolean(
    trimText(item.start_month)
    || trimText(item.end_month)
    || trimText(item.organization_name)
    || trimText(item.position_name)
    || trimText(item.responsibility_text)
    || trimText(item.verifier_name)
    || trimText(item.verifier_phone),
  )
}

function ensurePracticeExperienceShape(items?: Array<Partial<PortalPracticeExperienceItem>> | null) {
  const normalized = (items || [])
    .map((item) => ({ ...createPractice(), ...item }))
    .filter((item) => practiceItemHasContent(item))
    .slice(0, 2)

  return normalized
}

function validatePracticeRules(items?: PortalPracticeExperienceItem[] | null) {
  const meaningfulItems = (items || []).filter((item) => practiceItemHasContent(item))
  if (meaningfulItems.length > 2) {
    return '实践经历最多填写 2 条'
  }

  for (let index = 0; index < meaningfulItems.length; index += 1) {
    const item = meaningfulItems[index]
    if (!trimText(item.verifier_name)) {
      return `实践经历${index + 1}必须填写证明人姓名`
    }
    if (!trimText(item.verifier_phone)) {
      return `实践经历${index + 1}必须填写证明人手机`
    }
    if (!trimText(item.start_month) && !trimText(item.end_month)) {
      continue
    }

    const missingFields: string[] = []
    if (!trimText(item.start_month)) {
      missingFields.push('开始年月')
    }
    if (!trimText(item.end_month)) {
      missingFields.push('结束年月')
    }
    if (!trimText(item.organization_name)) {
      missingFields.push('实习实践/工作单位')
    }
    if (!trimText(item.position_name)) {
      missingFields.push('岗位')
    }
    if (!trimText(item.verifier_name)) {
      missingFields.push('证明人姓名')
    }
    if (!trimText(item.verifier_phone)) {
      missingFields.push('证明人手机')
    }
    if (missingFields.length) {
      return `实践经历${index + 1}填写了开始年月或结束年月时，除职责外其余字段均必填：缺少${missingFields.join('、')}`
    }
  }

  return ''
}

function createEnglish(): PortalEnglishProficiencyItem {
  return {
    exam_name: '',
    score_text: '',
    certificate_attachment_url: '',
  }
}

function englishItemHasContent(item: PortalEnglishProficiencyItem) {
  return Boolean(
    trimText(item.exam_name)
    || trimText(item.score_text)
    || trimText(item.certificate_attachment_url)
    || trimText(item.certificate_attachment_name),
  )
}

function ensureEnglishProficiencyShape(items?: Array<Partial<PortalEnglishProficiencyItem>> | null) {
  const normalized = (items || [])
    .map((item) => ({ ...createEnglish(), ...item }))
    .filter((item) => englishItemHasContent(item))

  return normalized.length ? normalized : [createEnglish()]
}

function validateEnglishRules(items?: PortalEnglishProficiencyItem[] | null, requireAtLeastOne = true) {
  const meaningfulItems = (items || []).filter((item) => englishItemHasContent(item))

  if (requireAtLeastOne && !meaningfulItems.length) {
    return '请至少完整填写一条英语能力，并上传英语证明附件'
  }

  for (let index = 0; index < meaningfulItems.length; index += 1) {
    const item = meaningfulItems[index]
    if (trimText(item.exam_name) === 'CET-4') {
      return '英语能力不再支持填写“CET-4”，请改填 CET-6、IELTS、TOEFL 或其他英语考试成绩'
    }
    if (!trimText(item.exam_name)) {
      return `英语能力${index + 1}请先选择英语考试名称`
    }
    if (!trimText(item.certificate_attachment_url)) {
      return `英语能力${index + 1}必须上传英语证明附件`
    }
  }

  return ''
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

function familyMemberHasContent(item: PortalFamilyMemberItem) {
  return Boolean(
    trimText(item.member_name)
    || trimText(item.employer_name)
    || trimText(item.job_title)
    || trimText(item.contact_phone),
  )
}

function hasCompletedParentFamilyMember(items?: PortalFamilyMemberItem[] | null) {
  return Boolean(
    (items || []).find(
      (item) => ['父亲', '母亲'].includes(trimText(item.relation_type)) && trimText(item.member_name),
    ),
  )
}

function validateFamilyRules(items?: PortalFamilyMemberItem[] | null) {
  if (!hasCompletedParentFamilyMember(items)) {
    return '父母信息至少填写一方'
  }

  return ''
}

function createAchievement(): PortalAchievementRecordItem {
  return {
    achievement_type: '',
    achievement_month: '',
    paper_title: '',
    author_order: '',
    journal_or_conference: '',
    publish_or_index_month: '',
    award_name: '',
    award_rank: '',
    award_certificate_attachment_url: '',
    award_certificate_attachment_name: '',
    awarding_organization: '',
    award_level: '',
    award_year: '',
    description_text: '',
    responsibility_text: '',
  }
}

function normalizeAchievementItem(item?: Partial<PortalAchievementRecordItem> | null): PortalAchievementRecordItem {
  const normalized = {
    ...createAchievement(),
    ...item,
  }
  normalized.achievement_month = trimText(normalized.achievement_month) || trimText(normalized.publish_or_index_month)
  normalized.award_rank = trimText(normalized.award_rank) || trimText(normalized.award_level)
  normalized.description_text = trimText(normalized.description_text) || trimText(normalized.responsibility_text)
  return normalized
}

function achievementItemHasContent(item: PortalAchievementRecordItem) {
  return Boolean(
    trimText(item.achievement_type)
    || trimText(item.achievement_month)
    || trimText(item.paper_title)
    || trimText(item.author_order)
    || trimText(item.journal_or_conference)
    || trimText(item.publish_or_index_month)
    || trimText(item.award_name)
    || trimText(item.award_rank)
    || trimText(item.award_certificate_attachment_url)
    || trimText(item.awarding_organization)
    || trimText(item.award_level)
    || trimText(item.award_year)
    || trimText(item.description_text)
    || trimText(item.responsibility_text),
  )
}

function ensureAchievementRecordShape(items?: Array<Partial<PortalAchievementRecordItem>> | null) {
  return (items || [])
    .map((item) => normalizeAchievementItem(item))
    .filter((item) => achievementItemHasContent(item))
    .slice(0, 4)
}

function validateAchievementRules(items?: PortalAchievementRecordItem[] | null) {
  const meaningfulItems = (items || [])
    .map((item) => normalizeAchievementItem(item))
    .filter((item) => achievementItemHasContent(item))

  if (meaningfulItems.length > 4) {
    return '成果经历最多填写 4 条'
  }

  for (let index = 0; index < meaningfulItems.length; index += 1) {
    const item = meaningfulItems[index]
    const rowLabel = `成果经历${index + 1}`
    const achievementType = trimText(item.achievement_type)
    if (!achievementType) {
      return `${rowLabel}请先选择类型`
    }
    if (!achievementTypeOptions.includes(achievementType)) {
      return `${rowLabel}仅支持填写“论文发表”或“获奖经历”`
    }

    if (achievementType === '论文发表') {
      const missingFields: string[] = []
      if (!trimText(item.achievement_month)) {
        missingFields.push('日期')
      }
      if (!trimText(item.paper_title)) {
        missingFields.push('论文名称')
      }
      if (!trimText(item.author_order)) {
        missingFields.push('作者序位')
      }
      if (!trimText(item.journal_or_conference)) {
        missingFields.push('期刊名称')
      }
      if (!trimText(item.description_text)) {
        missingFields.push('描述')
      }
      if (missingFields.length) {
        return `${rowLabel}为论文发表时，以下字段必填：${missingFields.join('、')}`
      }
    }

    if (achievementType === '获奖经历') {
      const missingFields: string[] = []
      if (!trimText(item.achievement_month)) {
        missingFields.push('日期')
      }
      if (!trimText(item.award_name)) {
        missingFields.push('奖项名称')
      }
      if (!trimText(item.award_rank)) {
        missingFields.push('获奖名次')
      }
      if (!trimText(item.award_certificate_attachment_url)) {
        missingFields.push('获奖证明')
      }
      if (!trimText(item.description_text)) {
        missingFields.push('描述')
      }
      if (missingFields.length) {
        return `${rowLabel}为获奖经历时，以下字段必填：${missingFields.join('、')}`
      }
    }
  }

  return ''
}

function createPersonalStatement(): PortalPersonalStatementData {
  return {
    personal_statement_text: '',
    ai_problem_statement: '',
    ai_industry_opinion: '',
    resume_attachment_url: '',
    resume_attachment_name: '',
    supporting_material_attachment_url: '',
    supporting_material_attachment_name: '',
  }
}

function personalStatementLength(text: string | null | undefined) {
  return trimText(text).replace(/\s+/g, '').length
}

function buildPersonalStatementSummary(personalStatement?: PortalPersonalStatementData | null) {
  return trimText(personalStatement?.personal_statement_text)
}

function validatePersonalStatementRules(personalStatement?: PortalPersonalStatementData | null, requireComplete = false) {
  if (!requireComplete) {
    return ''
  }

  const statementText = buildPersonalStatementSummary(personalStatement)
  if (!statementText) {
    return '请填写个人陈述第 1 题'
  }

  const length = personalStatementLength(statementText)
  if (length < 800 || length > 1200) {
    return '个人陈述第 1 题总字数需控制在 800-1200 字'
  }
  if (!trimText(personalStatement?.resume_attachment_url)) {
    return '请先上传个人简历附件'
  }

  return ''
}

function createDeclaration(): PortalApplicationDeclarationData {
  return {
    has_read_declaration: false,
    declaration_text: declarationReminderText,
    progress_snapshot: null,
  }
}

function createEmptyForm(): PortalApplicationUpsert {
  return {
    plan_id: 0,
    profile: createProfile(),
    source_channel: '',
    source_channel_other: '',
    preferences: [createPreference(1, false), createPreference(2, true)],
    education_experiences: createDefaultEducationExperiences(),
    practice_experiences: [],
    english_proficiencies: [createEnglish()],
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

function ensureTwoPreferences(items?: Array<Partial<PortalApplicationPreferenceItem>> | null) {
  const normalized = (items || []).slice(0, 2).map((item, index) => ({
    ...createPreference(index + 1, index > 0),
    ...item,
    preference_order: index + 1,
    is_optional: index > 0,
  }))

  while (normalized.length < 2) {
    normalized.push(createPreference(normalized.length + 1, normalized.length > 0))
  }

  return normalized
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
    const category: PortalAttachmentCategory = field === 'transcript'
      ? 'education_transcript'
      : field === 'degree_certificate'
        ? 'education_degree_certificate'
        : 'education_graduation_certificate'
    const attachment = await uploadAttachmentAndResolveUrl(
      file,
      category,
      field === 'transcript'
        ? '成绩单附件已上传'
        : field === 'degree_certificate'
          ? '学位证附件已上传'
          : '毕业证附件已上传',
    )
    const current = form.education_experiences?.[index]
    if (current) {
      if (field === 'transcript') {
        current.transcript_attachment_url = attachment.url
        current.transcript_attachment_name = attachment.file_name
      } else if (field === 'degree_certificate') {
        current.degree_certificate_attachment_url = attachment.url
        current.degree_certificate_attachment_name = attachment.file_name
      } else {
        current.graduation_certificate_attachment_url = attachment.url
        current.graduation_certificate_attachment_name = attachment.file_name
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

async function handleAchievementAwardAttachmentUpload(index: number, event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) {
    return
  }

  const key = buildAttachmentUploadKey('achievement', index, 'award-certificate')
  attachmentUploading[key] = true
  try {
    const attachment = await uploadAttachmentAndResolveUrl(file, 'achievement_award_certificate', '获奖证明已上传')
    const current = form.achievement_records?.[index]
    if (current) {
      current.award_certificate_attachment_url = attachment.url
      current.award_certificate_attachment_name = attachment.file_name
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

async function handleSupportingMaterialAttachmentUpload(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) {
    return
  }

  const key = buildAttachmentUploadKey('statement', 0, 'supporting-material')
  attachmentUploading[key] = true
  try {
    const attachment = await uploadAttachmentAndResolveUrl(file, 'supporting_material', '其他支撑材料已上传')
    if (form.personal_statement) {
      form.personal_statement.supporting_material_attachment_url = attachment.url
      form.personal_statement.supporting_material_attachment_name = attachment.file_name
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

async function handleIdCardCollageUpload(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) {
    return
  }

  const key = buildAttachmentUploadKey('profile', 0, 'id-card-collage')
  attachmentUploading[key] = true
  try {
    const attachment = await uploadAttachmentAndResolveUrl(file, 'id_card_collage', '身份证拼图已上传')
    if (form.profile) {
      form.profile.id_card_collage_url = attachment.url
    }
  } catch (error) {
    await showPortalAlert(resolveRequestError(error, '身份证拼图上传失败'), '身份证拼图上传失败', 'error')
  } finally {
    attachmentUploading[key] = false
    input.value = ''
  }
}

const primaryPreference = computed(() => (form.preferences && form.preferences[0] ? form.preferences[0] : null))

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
      id_card_collage_url: profile.profile?.id_card_collage_url || '',
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
    preferences: ensureTwoPreferences(
      draft?.preferences?.length
        ? draft.preferences.map((item) => ({
            research_center_name: item.research_center_name || '',
            advisor_name: item.advisor_name || '',
          }))
        : [
            {
              research_center_name: profile.selected_team_name || '',
              advisor_name: profile.selected_advisor_name || '',
            },
          ],
    ),
    education_experiences: ensureEducationExperienceShape(
      draft?.education_experiences?.length
        ? draft.education_experiences.map((item) => ({ ...item }))
        : fallbackEducation.length
          ? fallbackEducation.map((item) => ({ ...item }))
          : createDefaultEducationExperiences(),
    ),
    practice_experiences: ensurePracticeExperienceShape(
      draft?.practice_experiences?.length
        ? draft.practice_experiences.map((item) => ({ ...item }))
        : fallbackPractice.length
          ? fallbackPractice.map((item) => ({ ...item }))
          : null,
    ),
    english_proficiencies: ensureEnglishProficiencyShape(
      draft?.english_proficiencies?.length
        ? draft.english_proficiencies.map((item) => ({ ...item }))
        : profile.english_level
          ? [{ ...createEnglish(), exam_name: profile.english_level }]
          : null,
    ),
    family_members: draft?.family_members?.length
      ? draft.family_members.map((item) => ({ ...createFamilyMember(item.relation_type || '其他'), ...item }))
      : fallbackFamily.length
        ? fallbackFamily.map((item) => ({ ...createFamilyMember(item.relation_type || '其他'), ...item }))
        : [createFamilyMember('父亲'), createFamilyMember('母亲')],
    achievement_records: ensureAchievementRecordShape(
      draft?.achievement_records?.length
        ? draft.achievement_records.map((item) => ({ ...item }))
        : fallbackAchievements.map((item) => ({ ...item })),
    ),
    personal_statement: {
      ...createPersonalStatement(),
      ...draft?.personal_statement,
      personal_statement_text: draft?.personal_statement?.personal_statement_text || profile.personal_statement_text || '',
    },
    declaration: {
      ...createDeclaration(),
      ...draft?.declaration,
      has_read_declaration: draft?.declaration?.has_read_declaration ?? Boolean(profile.signed_agreement),
      declaration_text: createDeclaration().declaration_text,
    },
  })

  normalizePreferenceOrders()
}

function choosePlan(planId: number) {
  selectedPlanId.value = planId
  form.plan_id = planId
}

async function addEducation() {
  const blockedMessage = getEducationAddBlockedMessage(form.education_experiences)
  if (blockedMessage) {
    await showPortalAlert(blockedMessage, '教育经历提醒', 'warning')
    return
  }
  form.education_experiences = [
    ...(form.education_experiences || []),
    createEducation((form.education_experiences?.length || 0) + 1, recommendedNextEducationStage(form.education_experiences)),
  ]
}

async function removeEducation(index: number) {
  if (index <= 0) {
    await showPortalAlert('默认高中毕业记录不可删除', '教育经历提醒', 'warning')
    return
  }
  if ((form.education_experiences?.length || 0) <= 1) {
    await showPortalAlert('教育经历至少保留 1 条', '教育经历提醒', 'warning')
    return
  }
  form.education_experiences?.splice(index, 1)
  form.education_experiences?.forEach((item, itemIndex) => {
    item.sort_order = itemIndex + 1
  })
}

function handleEducationStageChange(item: PortalEducationExperienceItem) {
  normalizeEducationWhenStageChanges(item)
}

async function addPractice() {
  if ((form.practice_experiences?.length || 0) >= 2) {
    await showPortalAlert(
      '实践经历最多填写 2 条。\n若有更多经历，请通过上传个人简历附件的方式进行详细说明。',
      '实践经历提醒',
      'warning',
    )
    return
  }
  form.practice_experiences = [...(form.practice_experiences || []), createPractice()]
}

async function removePractice(index: number) {
  form.practice_experiences?.splice(index, 1)
}

function addEnglish() {
  form.english_proficiencies = [...(form.english_proficiencies || []), createEnglish()]
}

async function removeEnglish(index: number) {
  if ((form.english_proficiencies?.length || 0) <= 1) {
    await showPortalAlert('英语能力至少保留 1 条', '英语能力提醒', 'warning')
    return
  }
  form.english_proficiencies?.splice(index, 1)
}

function addFamilyMember() {
  form.family_members = [...(form.family_members || []), createFamilyMember()]
}

function removeFamilyMember(index: number) {
  if (index <= 0) {
    return
  }
  form.family_members?.splice(index, 1)
}

async function addAchievement() {
  if ((form.achievement_records?.length || 0) >= 4) {
    await showPortalAlert(
      '成果经历最多填写 4 条。\n若有更多成果，请通过上传个人简历附件的方式进行详细说明。',
      '成果经历提醒',
      'warning',
    )
    return
  }
  form.achievement_records = [...(form.achievement_records || []), createAchievement()]
}

function handleAchievementTypeChange(index: number) {
  const current = form.achievement_records?.[index]
  if (!current) {
    return
  }

  const achievementType = trimText(current.achievement_type)
  current.achievement_month = trimText(current.achievement_month) || trimText(current.publish_or_index_month)
  current.description_text = trimText(current.description_text) || trimText(current.responsibility_text)

  if (achievementType === '论文发表') {
    current.award_name = ''
    current.award_rank = ''
    current.award_certificate_attachment_url = ''
    current.award_certificate_attachment_name = ''
    current.awarding_organization = ''
    current.award_level = ''
    current.award_year = ''
    return
  }

  if (achievementType === '获奖经历') {
    current.paper_title = ''
    current.author_order = ''
    current.journal_or_conference = ''
  }
}

function removeAchievement(index: number) {
  form.achievement_records?.splice(index, 1)
}

function buildProgressSnapshot() {
  return {
    preference_count: (form.preferences || []).filter((item) => trimText(item.research_center_name)).length,
    education_count: (form.education_experiences || []).filter((item) => trimText(item.school_name)).length,
    practice_count: (form.practice_experiences || []).filter((item) => practiceItemHasContent(item)).length,
    english_count: (form.english_proficiencies || []).filter((item) => englishItemHasContent(item)).length,
    family_count: (form.family_members || []).filter((item) => familyMemberHasContent(item)).length,
    achievement_count: (form.achievement_records || []).filter((item) => achievementItemHasContent(normalizeAchievementItem(item))).length,
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
    || trimText(profileData.profile_photo_url)
    || trimText(profileData.id_card_collage_url),
  )
  const basicCompleted = Boolean(
    trimText(profileData.full_name_pinyin)
    && trimText(profileData.gender)
    && trimText(profileData.ethnic_group)
    && trimText(profileData.political_status)
    && trimText(profileData.mailing_address)
    && trimText(profileData.emergency_contact_name)
    && trimText(profileData.emergency_contact_phone)
    && trimText(profileData.profile_photo_url)
    && trimText(profileData.id_card_collage_url),
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
  const completedEducationItems = getCompletedEducationExperiences(educationItems)
  const educationCompleted = completedEducationItems.length >= 2 && !validateEducationRules(educationItems)

  const practiceItems = form.practice_experiences || []
  const practiceStarted = practiceItems.some((item) => practiceItemHasContent(item))
  const practiceCompleted = practiceStarted && !validatePracticeRules(practiceItems)

  const englishItems = form.english_proficiencies || []
  const englishStarted = englishItems.some((item) => englishItemHasContent(item))
  const englishCompleted = !validateEnglishRules(englishItems)

  const familyItems = form.family_members || []
  const familyStarted = familyItems.some((item) => familyMemberHasContent(item))
  const familyCompleted = !validateFamilyRules(familyItems)

  const achievementItems = form.achievement_records || []
  const achievementStarted = achievementItems.some((item) => achievementItemHasContent(normalizeAchievementItem(item)))
  const achievementCompleted = achievementStarted && !validateAchievementRules(achievementItems)

  const statementText = trimText(form.personal_statement?.personal_statement_text)
  const statementStarted = Boolean(
    statementText
    || trimText(form.personal_statement?.ai_problem_statement)
    || trimText(form.personal_statement?.ai_industry_opinion)
    || trimText(form.personal_statement?.resume_attachment_url)
    || trimText(form.personal_statement?.supporting_material_attachment_url)
    || form.declaration?.has_read_declaration,
  )
  const statementCompleted = statementStarted && !validatePersonalStatementRules(form.personal_statement, true)

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
    createStatus('practice-section', '实践经历', practiceStarted, practiceCompleted),
    createStatus('english-section', '英语能力', englishStarted, englishCompleted),
    createStatus('family-section', '家庭情况', familyStarted, familyCompleted),
    createStatus('achievement-section', '成果经历', achievementStarted, achievementCompleted),
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
      degree_certificate_attachment_url: isHighSchoolStage(item.education_stage) ? null : trimText(item.degree_certificate_attachment_url) || null,
      graduation_certificate_attachment_url: isHighSchoolStage(item.education_stage) ? null : trimText(item.graduation_certificate_attachment_url) || null,
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
    .filter((item) => practiceItemHasContent(item))

  const englishProficiencies = (form.english_proficiencies || [])
    .map((item) => ({
      ...item,
      exam_name: trimText(item.exam_name),
      score_text: trimText(item.score_text) || null,
      certificate_attachment_url: trimText(item.certificate_attachment_url) || null,
    }))
    .filter((item) => englishItemHasContent(item))

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
    .map((item) => normalizeAchievementItem(item))
    .map((item) => {
      const achievementType = trimText(item.achievement_type)
      const achievementMonth = trimText(item.achievement_month) || null
      const descriptionText = trimText(item.description_text) || null
      return {
        ...item,
        achievement_type: achievementType,
        achievement_month: achievementMonth,
        paper_title: achievementType === '论文发表' ? trimText(item.paper_title) || null : null,
        author_order: achievementType === '论文发表' ? trimText(item.author_order) || null : null,
        journal_or_conference: achievementType === '论文发表' ? trimText(item.journal_or_conference) || null : null,
        publish_or_index_month: achievementType === '论文发表' ? achievementMonth : null,
        award_name: achievementType === '获奖经历' ? trimText(item.award_name) || null : null,
        award_rank: achievementType === '获奖经历' ? trimText(item.award_rank) || null : null,
        award_certificate_attachment_url: achievementType === '获奖经历' ? trimText(item.award_certificate_attachment_url) || null : null,
        award_certificate_attachment_name: achievementType === '获奖经历' ? trimText(item.award_certificate_attachment_name) || null : null,
        awarding_organization: null,
        award_level: achievementType === '获奖经历' ? trimText(item.award_rank) || null : null,
        award_year: achievementType === '获奖经历' && achievementMonth ? achievementMonth.slice(0, 4) : null,
        description_text: descriptionText,
        responsibility_text: descriptionText,
      }
    })
    .filter((item) => item.achievement_type)

  const primaryPreferenceItem = orderedPreferences[0]
  const primaryEducationItem = orderedEducation[0]
  const declaration = {
    ...(form.declaration || createDeclaration()),
    has_read_declaration: Boolean(form.declaration?.has_read_declaration),
    declaration_text: createDeclaration().declaration_text,
    progress_snapshot: buildProgressSnapshot(),
  }

  return {
    plan_id: selectedPlanId.value || form.plan_id || 0,
    profile: {
      ...profileData,
      full_name_pinyin: trimText(profileData.full_name_pinyin) || null,
      profile_photo_url: trimText(profileData.profile_photo_url) || null,
      id_card_collage_url: trimText(profileData.id_card_collage_url) || null,
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
      personal_statement_text: buildPersonalStatementSummary(form.personal_statement) || null,
      ai_problem_statement: trimText(form.personal_statement?.ai_problem_statement) || null,
      ai_industry_opinion: trimText(form.personal_statement?.ai_industry_opinion) || null,
      resume_attachment_url: trimText(form.personal_statement?.resume_attachment_url) || null,
      resume_attachment_name: trimText(form.personal_statement?.resume_attachment_name) || null,
      supporting_material_attachment_url: trimText(form.personal_statement?.supporting_material_attachment_url) || null,
      supporting_material_attachment_name: trimText(form.personal_statement?.supporting_material_attachment_name) || null,
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
    material_list_attachment: trimText(form.personal_statement?.supporting_material_attachment_url) || null,
    personal_statement_text: buildPersonalStatementSummary(form.personal_statement) || null,
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
  if (!trimText(form.profile?.id_card_collage_url)) {
    await showPortalAlert('请先上传身份证拼图后再提交申请表', '提交受阻', 'warning')
    return
  }
  const primary = primaryPreference.value
  if (!trimText(primary?.research_center_name)) {
    await showPortalAlert('请至少选择第一志愿研究中心', '提交受阻', 'warning')
    return
  }
  const completedEducationItems = getCompletedEducationExperiences(form.education_experiences)
  if (completedEducationItems.length < 2) {
    await showPortalAlert('请至少完整填写两条教育经历', '提交受阻', 'warning')
    return
  }
  const educationRuleMessage = validateEducationRules(form.education_experiences)
  if (educationRuleMessage) {
    await showPortalAlert(educationRuleMessage, '提交受阻', 'warning')
    return
  }
  const practiceRuleMessage = validatePracticeRules(form.practice_experiences)
  if (practiceRuleMessage) {
    await showPortalAlert(practiceRuleMessage, '提交受阻', 'warning')
    return
  }
  const englishRuleMessage = validateEnglishRules(form.english_proficiencies)
  if (englishRuleMessage) {
    await showPortalAlert(englishRuleMessage, '提交受阻', 'warning')
    return
  }
  const familyRuleMessage = validateFamilyRules(form.family_members)
  if (familyRuleMessage) {
    await showPortalAlert(familyRuleMessage, '提交受阻', 'warning')
    return
  }
  const personalStatementRuleMessage = validatePersonalStatementRules(form.personal_statement, true)
  if (personalStatementRuleMessage) {
    await showPortalAlert(personalStatementRuleMessage, '提交受阻', 'warning')
    return
  }
  const achievementRuleMessage = validateAchievementRules(form.achievement_records)
  if (achievementRuleMessage) {
    await showPortalAlert(achievementRuleMessage, '提交受阻', 'warning')
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
    await showPortalAlert(
      [
        '报名申请提交成功。',
        response.data.application_business_key ? `业务编号：${response.data.application_business_key}` : '',
        response.data.application_status ? `当前状态：${response.data.application_status}` : '',
        response.data.student?.submitted_at ? `提交时间：${response.data.student.submitted_at}` : '',
      ].filter(Boolean).join('\n'),
      '提交成功',
      'success',
    )
  } catch (error) {
    await showPortalAlert(resolveRequestError(error, '提交失败'), '提交失败', 'error')
  } finally {
    submitting.value = false
  }
}

async function saveDraft(showSuccess = true) {
  const educationRuleMessage = validateEducationRules(form.education_experiences)
  if (educationRuleMessage) {
    await showPortalAlert(educationRuleMessage, '草稿保存受阻', 'warning')
    return false
  }
  const practiceRuleMessage = validatePracticeRules(form.practice_experiences)
  if (practiceRuleMessage) {
    await showPortalAlert(practiceRuleMessage, '草稿保存受阻', 'warning')
    return false
  }
  const familyRuleMessage = validateFamilyRules(form.family_members)
  if (familyRuleMessage) {
    await showPortalAlert(familyRuleMessage, '草稿保存受阻', 'warning')
    return false
  }
  const achievementRuleMessage = validateAchievementRules(form.achievement_records)
  if (achievementRuleMessage) {
    await showPortalAlert(achievementRuleMessage, '草稿保存受阻', 'warning')
    return false
  }
  savingDraft.value = true
  try {
    const response = await savePortalApplicationDraft(buildSubmitPayload())
    student.value = response.data.student
    if (showSuccess) {
      await showPortalAlert(response.data.message || '报名草稿已保存，可稍后继续填写。', '保存成功', 'success')
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
        :id-card-collage-attachment-accept="idCardCollageAttachmentAccept"
        :is-attachment-uploading="isAttachmentUploading"
        :build-attachment-upload-key="buildAttachmentUploadKey"
        :handle-profile-photo-upload="handleProfilePhotoUpload"
        :handle-id-card-collage-upload="handleIdCardCollageUpload"
      />

      <PortalApplicationSection
        v-else-if="activeSectionId === 'application-section'"
        :form="form"
        :teams="teams"
        :source-channel-options="sourceChannelOptions"
        :advisors-for-center="advisorsForCenter"
        :handle-preference-center-change="handlePreferenceCenterChange"
      />

      <PortalEducationSection
        v-else-if="activeSectionId === 'education-section'"
        :form="form"
        :get-education-stage-options="getEducationStageOptions"
        :certificate-attachment-accept="certificateAttachmentAccept"
        :is-attachment-uploading="isAttachmentUploading"
        :build-attachment-upload-key="buildAttachmentUploadKey"
        :handle-education-attachment-upload="handleEducationAttachmentUpload"
        :handle-education-stage-change="handleEducationStageChange"
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
        :achievement-award-attachment-accept="achievementAwardAttachmentAccept"
        :is-attachment-uploading="isAttachmentUploading"
        :build-attachment-upload-key="buildAttachmentUploadKey"
        :add-achievement="addAchievement"
        :handle-achievement-type-change="handleAchievementTypeChange"
        :handle-achievement-award-attachment-upload="handleAchievementAwardAttachmentUpload"
        :remove-achievement="removeAchievement"
      />

      <PortalStatementSection
        v-else-if="activeSectionId === 'statement-section'"
        :form="form"
        :declaration-reminder-text="declarationReminderText"
        :resume-attachment-accept="resumeAttachmentAccept"
        :supporting-material-attachment-accept="supportingMaterialAttachmentAccept"
        :is-attachment-uploading="isAttachmentUploading"
        :build-attachment-upload-key="buildAttachmentUploadKey"
        :handle-resume-attachment-upload="handleResumeAttachmentUpload"
        :handle-supporting-material-attachment-upload="handleSupportingMaterialAttachmentUpload"
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