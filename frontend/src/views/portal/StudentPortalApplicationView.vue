<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import { useRouter } from 'vue-router'

import {
  clearPortalToken,
  getPortalProfile,
  getPortalToken,
  listPortalPlans,
  listPortalTeams,
  submitPortalApplication,
  type PortalApplicationUpsert,
  type PortalPlanRecord,
  type PortalStudentRecord,
  type PortalTeamRecord,
} from '../../api/portal'

const router = useRouter()
const initializing = ref(true)
const submitting = ref(false)
const student = ref<PortalStudentRecord | null>(null)
const plans = ref<PortalPlanRecord[]>([])
const teams = ref<PortalTeamRecord[]>([])
const selectedPlanId = ref<number | null>(null)
const selectedTeamName = ref('')
const activeSectionId = ref('plan-section')
const navElement = ref<HTMLElement | null>(null)
const navTranslateY = ref(0)
const showBackToTop = ref(false)
const quickNavOpen = ref(false)
let sectionObserver: IntersectionObserver | null = null
const navBaseTop = 96
const navMaxTranslate = 360

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

const sectionItems: SectionItem[] = [
  { id: 'plan-section', label: '选择计划', caption: '确认批次与简章' },
  { id: 'basic-section', label: '基本信息', caption: '身份与联系信息' },
  { id: 'application-section', label: '报名信息', caption: '志愿与团队选择' },
  { id: 'education-section', label: '教育经历', caption: '本科硕士培养背景' },
  { id: 'practice-section', label: '实践经历', caption: '项目与科研训练' },
  { id: 'family-section', label: '家庭情况', caption: '成长环境补充说明' },
  { id: 'statement-section', label: '个人陈述', caption: '申请动机与承诺' },
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
    caption: '经历、家庭与个人陈述',
    items: ['education-section', 'practice-section', 'family-section', 'statement-section'],
  },
]

const expandedSections = ref<Record<string, boolean>>({
  'plan-section': true,
  'basic-section': true,
  'application-section': true,
  'education-section': false,
  'practice-section': false,
  'family-section': false,
  'statement-section': true,
})

const expandedGroups = ref<Record<string, boolean>>({
  'workflow-group': true,
  'archive-group': true,
})

const progressSteps = [
  { index: '01', label: '填写申请表' },
  { index: '02', label: '资格初审' },
  { index: '03', label: '状态确认' },
  { index: '04', label: '综合面试' },
  { index: '05', label: '预录取' },
  { index: '06', label: '结果发布' },
]

const form = reactive<PortalApplicationUpsert>({
  plan_id: 0,
  gender: '',
  birth_date: '',
  ethnic_group: '',
  native_place: '',
  marital_status: '',
  religious_belief: '',
  id_type: '居民身份证',
  mailing_address: '',
  graduation_school: '',
  highest_degree: '硕士',
  intended_field: '',
  political_status: '',
  english_level: '',
  family_info: '',
  education_experience: '',
  practice_experience: '',
  personal_profile: '',
  recommendation_notes: '',
  personal_statement_text: '',
  signed_agreement: false,
  selected_team_name: '',
  selected_advisor_name: '',
  self_evaluation: '',
})

const selectedPlan = computed(() => plans.value.find((item) => item.id === selectedPlanId.value) || null)
const selectedTeam = computed(() => teams.value.find((item) => item.team_name === selectedTeamName.value) || null)
const advisorOptions = computed(() => selectedTeam.value?.advisor_names || [])
const navFloatingStyle = computed(() => {
  return {
    top: `${navBaseTop}px`,
    transform: `translateY(${navTranslateY.value}px)`,
  }
})

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
  selectedPlanId.value = profile.selected_plan_id || null
  selectedTeamName.value = profile.selected_team_name || ''
  Object.assign(form, {
    plan_id: profile.selected_plan_id || 0,
    gender: profile.gender || '',
    birth_date: profile.birth_date || '',
    ethnic_group: profile.ethnic_group || '',
    native_place: profile.native_place || '',
    marital_status: profile.marital_status || '',
    religious_belief: profile.religious_belief || '',
    id_type: profile.id_type || '居民身份证',
    mailing_address: profile.mailing_address || '',
    graduation_school: profile.graduation_school || '',
    highest_degree: profile.highest_degree || '硕士',
    intended_field: profile.intended_field || '',
    political_status: profile.political_status || '',
    english_level: profile.english_level || '',
    family_info: profile.family_info || '',
    education_experience: profile.education_experience || '',
    practice_experience: profile.practice_experience || '',
    personal_profile: profile.personal_profile || '',
    recommendation_notes: profile.recommendation_notes || '',
    personal_statement_text: profile.personal_statement_text || '',
    signed_agreement: Boolean(profile.signed_agreement),
    selected_team_name: profile.selected_team_name || '',
    selected_advisor_name: profile.selected_advisor_name || '',
    self_evaluation: profile.self_evaluation || '',
  })
}

function choosePlan(planId: number) {
  selectedPlanId.value = planId
  form.plan_id = planId
}

function chooseTeam(teamName: string) {
  selectedTeamName.value = teamName
  form.selected_team_name = teamName
  form.selected_advisor_name = teams.value.find((item) => item.team_name === teamName)?.lead_advisor_name || ''
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
  expandedSections.value = {
    ...expandedSections.value,
    [sectionId]: !isSectionExpanded(sectionId),
  }

  nextTick(() => {
    updateNavFloatingPosition()
  })
}

function toggleGroup(groupId: string) {
  expandedGroups.value = {
    ...expandedGroups.value,
    [groupId]: !isGroupExpanded(groupId),
  }

  nextTick(() => {
    updateNavFloatingPosition()
  })
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

async function submitForm() {
  if (!selectedPlanId.value) {
    ElMessage.warning('请先选择招生计划')
    return
  }
  if (!form.selected_team_name) {
    ElMessage.warning('请选择导师团队')
    return
  }
  if (!form.signed_agreement) {
    ElMessage.warning('请先确认签署报名表')
    return
  }

  submitting.value = true
  try {
    const response = await submitPortalApplication({ ...form, plan_id: selectedPlanId.value })
    student.value = response.data.student
    applyProfile(response.data.student)
    ElMessage.success(`申请已提交，业务编号 ${response.data.application_business_key}`)
  } catch (error) {
    const detail = axios.isAxiosError(error) ? String(error.response?.data?.detail || '提交失败') : '提交失败'
    ElMessage.error(detail)
  } finally {
    submitting.value = false
  }
}

function logoutPortal() {
  clearPortalToken()
  void router.replace('/portal')
}

onMounted(async () => {
  if (!getPortalToken()) {
    await router.replace('/portal')
    return
  }

  try {
    const [profileResponse, planResponse, teamResponse] = await Promise.all([
      getPortalProfile(),
      listPortalPlans(),
      listPortalTeams(),
    ])
    student.value = profileResponse.data
    plans.value = planResponse.data.items
    teams.value = teamResponse.data.items
    applyProfile(profileResponse.data)
    if (!selectedPlanId.value && plans.value[0]) {
      choosePlan(plans.value[0].id)
    }
  } catch {
    clearPortalToken()
    await router.replace('/portal')
  } finally {
    initializing.value = false
    await nextTick()
    mountSectionObserver()
    syncFloatingUi()
  }
})

watch(activeSectionId, () => {
  void nextTick(() => {
    updateNavFloatingPosition()
  })
})

onBeforeUnmount(() => {
  sectionObserver?.disconnect()
  window.removeEventListener('scroll', syncFloatingUi)
  window.removeEventListener('resize', syncFloatingUi)
})

onMounted(() => {
  window.addEventListener('scroll', syncFloatingUi, { passive: true })
  window.addEventListener('resize', syncFloatingUi)
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
        <span>官网</span>
        <strong>{{ student?.full_name || '考生' }}</strong>
        <button type="button" @click="logoutPortal">退出</button>
      </div>
    </header>

    <main class="application-page" v-if="!initializing">
      <section class="application-notice">
        <div class="application-notice__meta">
          <p>报名开始时间：2025-10-27 13:20</p>
          <p>报名截止时间：2026-05-31 23:59</p>
        </div>
        <span>请先锁定招生计划，再逐段完成学生档案、导师团队志愿与个人陈述。系统将自动保存当前已提交信息。</span>
      </section>

      <section class="progress-bar">
        <div v-for="(step, index) in progressSteps" :key="step.index" class="progress-step" :class="{ 'progress-step--active': index === 0 }">
          <span class="progress-step__index">{{ step.index }}</span>
          <strong class="progress-step__label">{{ step.label }}</strong>
        </div>
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
                <strong>选择招生计划</strong>
                <span>登录后请选择一个正在开放的招生计划</span>
              </span>
              <span class="panel-toggle__action">{{ isSectionExpanded('plan-section') ? '收起' : '展开' }}</span>
              <span class="panel-toggle__icon" :class="{ 'panel-toggle__icon--expanded': isSectionExpanded('plan-section') }" aria-hidden="true"></span>
            </button>
            <div v-show="isSectionExpanded('plan-section')" class="panel-body">
            <div class="plan-pick-grid">
              <button
                v-for="plan in plans"
                :key="plan.id"
                type="button"
                class="plan-pick-card"
                :class="{ 'plan-pick-card--active': plan.id === selectedPlanId }"
                @click="choosePlan(plan.id)"
              >
                <strong>{{ plan.plan_name }}</strong>
                <span>{{ plan.academic_term }} · {{ plan.current_stage }}</span>
                <small>{{ plan.target_quota }} 个名额 / {{ plan.interview_group_count }} 个面试组</small>
              </button>
            </div>
            <div class="brochure-preview" v-if="selectedPlan">
              <div class="brochure-preview__media">
                <img v-if="selectedPlan.brochure_image_url" :src="selectedPlan.brochure_image_url" :alt="selectedPlan.plan_name" />
                <div v-else class="brochure-preview__placeholder">当前计划未上传招生简章图片</div>
              </div>
              <div class="brochure-preview__content">
                <div class="brochure-chip">当前选择计划</div>
                <strong>{{ selectedPlan.plan_name }}</strong>
                <p>{{ selectedPlan.summary }}</p>
                <dl class="brochure-meta">
                  <div><dt>学期</dt><dd>{{ selectedPlan.academic_term }}</dd></div>
                  <div><dt>阶段</dt><dd>{{ selectedPlan.current_stage }}</dd></div>
                  <div><dt>名额</dt><dd>{{ selectedPlan.target_quota }}</dd></div>
                  <div><dt>面试组</dt><dd>{{ selectedPlan.interview_group_count }}</dd></div>
                </dl>
              </div>
            </div>
            </div>
          </article>

          <article id="basic-section" class="application-panel" :class="{ 'application-panel--collapsed': !isSectionExpanded('basic-section') }">
            <button type="button" class="panel-toggle" @click="toggleSection('basic-section')">
              <span class="panel-toggle__copy">
                <small>STEP 02</small>
                <strong>基本信息(必填)</strong>
                <span>用于确认身份、联系方式与基础背景</span>
              </span>
              <span class="panel-toggle__action">{{ isSectionExpanded('basic-section') ? '收起' : '展开' }}</span>
              <span class="panel-toggle__icon" :class="{ 'panel-toggle__icon--expanded': isSectionExpanded('basic-section') }" aria-hidden="true"></span>
            </button>
            <div v-show="isSectionExpanded('basic-section')" class="panel-body">
            <div class="form-grid form-grid--three">
              <label><span>姓名</span><input :value="student?.full_name || ''" disabled /></label>
              <label><span>性别</span><select v-model="form.gender"><option value="">请选择</option><option value="男">男</option><option value="女">女</option></select></label>
              <label><span>出生日期</span><input v-model="form.birth_date" type="date" /></label>
              <label><span>籍贯</span><input v-model="form.native_place" placeholder="请输入籍贯" /></label>
              <label><span>民族</span><input v-model="form.ethnic_group" placeholder="请输入民族" /></label>
              <label><span>政治面貌</span><input v-model="form.political_status" placeholder="请输入政治面貌" /></label>
              <label><span>婚否</span><select v-model="form.marital_status"><option value="">请选择</option><option value="未婚">未婚</option><option value="已婚">已婚</option></select></label>
              <label><span>宗教信仰</span><input v-model="form.religious_belief" placeholder="请输入宗教信仰" /></label>
              <label><span>证件类型</span><input v-model="form.id_type" placeholder="证件类型" /></label>
              <label><span>证件号码</span><input :value="student?.id_number || ''" disabled /></label>
              <label><span>邮箱</span><input :value="student?.email || ''" disabled /></label>
              <label><span>联系电话</span><input :value="student?.phone_number || ''" disabled /></label>
            </div>
            <label class="form-field form-field--full"><span>通讯地址</span><input v-model="form.mailing_address" placeholder="请输入通讯地址" /></label>
            </div>
          </article>

          <article id="application-section" class="application-panel" :class="{ 'application-panel--collapsed': !isSectionExpanded('application-section') }">
            <button type="button" class="panel-toggle" @click="toggleSection('application-section')">
              <span class="panel-toggle__copy">
                <small>STEP 03</small>
                <strong>报名信息</strong>
                <span>填写志愿方向，并选择导师团队与意向导师</span>
              </span>
              <span class="panel-toggle__action">{{ isSectionExpanded('application-section') ? '收起' : '展开' }}</span>
              <span class="panel-toggle__icon" :class="{ 'panel-toggle__icon--expanded': isSectionExpanded('application-section') }" aria-hidden="true"></span>
            </button>
            <div v-show="isSectionExpanded('application-section')" class="panel-body">
            <div class="form-grid form-grid--three">
              <label><span>毕业院校</span><input v-model="form.graduation_school" placeholder="请输入毕业院校" /></label>
              <label><span>最高学位</span><select v-model="form.highest_degree"><option value="本科">本科</option><option value="硕士">硕士</option><option value="博士">博士</option></select></label>
              <label><span>英语语言能力</span><input v-model="form.english_level" placeholder="如 CET-6 / IELTS" /></label>
              <label class="form-field--full"><span>意向研究方向</span><input v-model="form.intended_field" placeholder="请输入意向研究方向" /></label>
            </div>
            <div class="team-grid">
              <button
                v-for="team in teams"
                :key="team.id"
                type="button"
                class="team-card"
                :class="{ 'team-card--active': team.team_name === selectedTeamName }"
                @click="chooseTeam(team.team_name)"
              >
                <strong>{{ team.team_name }}</strong>
                <span>{{ team.department_name }} · {{ team.discipline_name }}</span>
                <small>{{ team.research_directions.join(' / ') }}</small>
              </button>
            </div>
            <div class="form-grid form-grid--two compact-top">
              <label><span>导师团队</span><input v-model="form.selected_team_name" readonly /></label>
              <label>
                <span>意向导师</span>
                <select v-model="form.selected_advisor_name">
                  <option value="">请选择导师</option>
                  <option v-for="advisor in advisorOptions" :key="advisor" :value="advisor">{{ advisor }}</option>
                </select>
              </label>
            </div>
            </div>
          </article>

          <article id="education-section" class="application-panel" :class="{ 'application-panel--collapsed': !isSectionExpanded('education-section') }">
            <button type="button" class="panel-toggle" @click="toggleSection('education-section')">
              <span class="panel-toggle__copy">
                <small>STEP 04</small>
                <strong>教育经历</strong>
                <span>请按时间顺序填写本科与硕士阶段的培养背景</span>
              </span>
              <span class="panel-toggle__action">{{ isSectionExpanded('education-section') ? '收起' : '展开' }}</span>
              <span class="panel-toggle__icon" :class="{ 'panel-toggle__icon--expanded': isSectionExpanded('education-section') }" aria-hidden="true"></span>
            </button>
            <div v-show="isSectionExpanded('education-section')" class="panel-body">
            <label class="form-field form-field--full"><span>教育经历</span><textarea v-model="form.education_experience" rows="5" placeholder="请输入本科、硕士阶段教育经历" /></label>
            </div>
          </article>

          <article id="practice-section" class="application-panel" :class="{ 'application-panel--collapsed': !isSectionExpanded('practice-section') }">
            <button type="button" class="panel-toggle" @click="toggleSection('practice-section')">
              <span class="panel-toggle__copy">
                <small>STEP 05</small>
                <strong>实践经历</strong>
                <span>展示科研、竞赛、项目或工程实践能力</span>
              </span>
              <span class="panel-toggle__action">{{ isSectionExpanded('practice-section') ? '收起' : '展开' }}</span>
              <span class="panel-toggle__icon" :class="{ 'panel-toggle__icon--expanded': isSectionExpanded('practice-section') }" aria-hidden="true"></span>
            </button>
            <div v-show="isSectionExpanded('practice-section')" class="panel-body">
            <label class="form-field form-field--full"><span>实践经历</span><textarea v-model="form.practice_experience" rows="5" placeholder="请输入科研项目、竞赛、实习或工程实践经历" /></label>
            </div>
          </article>

          <article id="family-section" class="application-panel" :class="{ 'application-panel--collapsed': !isSectionExpanded('family-section') }">
            <button type="button" class="panel-toggle" @click="toggleSection('family-section')">
              <span class="panel-toggle__copy">
                <small>STEP 06</small>
                <strong>家庭情况</strong>
                <span>补充成长环境、家庭支持情况等信息</span>
              </span>
              <span class="panel-toggle__action">{{ isSectionExpanded('family-section') ? '收起' : '展开' }}</span>
              <span class="panel-toggle__icon" :class="{ 'panel-toggle__icon--expanded': isSectionExpanded('family-section') }" aria-hidden="true"></span>
            </button>
            <div v-show="isSectionExpanded('family-section')" class="panel-body">
            <label class="form-field form-field--full"><span>家庭情况</span><textarea v-model="form.family_info" rows="4" placeholder="请输入家庭情况说明" /></label>
            </div>
          </article>

          <article id="statement-section" class="application-panel" :class="{ 'application-panel--collapsed': !isSectionExpanded('statement-section') }">
            <button type="button" class="panel-toggle" @click="toggleSection('statement-section')">
              <span class="panel-toggle__copy">
                <small>STEP 07</small>
                <strong>个人简介与陈述</strong>
                <span>阐明申请动机、研究基础与真实性承诺</span>
              </span>
              <span class="panel-toggle__action">{{ isSectionExpanded('statement-section') ? '收起' : '展开' }}</span>
              <span class="panel-toggle__icon" :class="{ 'panel-toggle__icon--expanded': isSectionExpanded('statement-section') }" aria-hidden="true"></span>
            </button>
            <div v-show="isSectionExpanded('statement-section')" class="panel-body">
            <label class="form-field form-field--full"><span>个人简介</span><textarea v-model="form.personal_profile" rows="4" placeholder="请输入个人简介" /></label>
            <label class="form-field form-field--full"><span>推荐信息</span><textarea v-model="form.recommendation_notes" rows="4" placeholder="请输入推荐人或推荐情况说明" /></label>
            <label class="form-field form-field--full"><span>个人陈述</span><textarea v-model="form.personal_statement_text" rows="6" placeholder="请输入申请动机、研究基础与职业规划" /></label>
            <label class="form-field form-field--full"><span>补充说明</span><textarea v-model="form.self_evaluation" rows="4" placeholder="其他希望补充给招生组的说明" /></label>
            <label class="agreement-row">
              <input v-model="form.signed_agreement" type="checkbox" />
              <span>我已确认以上信息真实有效，并愿意签署本次报名表。</span>
            </label>
            <div class="submit-row">
              <button type="button" class="primary-button" :disabled="submitting" @click="submitForm">提交申请表</button>
              <span v-if="student?.submitted_at">最近提交时间：{{ student.submitted_at }}</span>
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
.application-nav button,
.plan-pick-card,
.team-card {
  cursor: pointer;
}

.application-header__user button,
.primary-button {
  border: none;
  border-radius: 12px;
}

.application-header__user button {
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.12);
  color: #fff;
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

.progress-bar {
  display: grid;
  grid-template-columns: repeat(6, minmax(0, 1fr));
  gap: 14px;
  margin-bottom: 18px;
}

.progress-step {
  position: relative;
  display: flex;
  align-items: center;
  gap: 14px;
  min-height: 82px;
  padding: 14px 18px 14px 34px;
  color: #f7fbff;
  background: linear-gradient(135deg, #b69254, #d2af6c);
  clip-path: polygon(0 0, calc(100% - 24px) 0, 100% 50%, calc(100% - 24px) 100%, 0 100%, 18px 50%);
  box-shadow: 0 16px 32px rgba(122, 87, 26, 0.18);
}

.progress-step--active {
  background: linear-gradient(135deg, #123e7c, #1b5eb2 58%, #2ba7e2);
  box-shadow: 0 18px 38px rgba(17, 62, 123, 0.28);
}

.progress-step__index {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 0.04em;
}

.progress-step__label {
  font-size: 18px;
  line-height: 1.2;
  font-weight: 700;
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

.application-nav__item--active .application-nav__copy strong {
  text-shadow: 0 1px 10px rgba(200, 240, 255, 0.28);
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
}

.panel-title {
  display: grid;
  gap: 4px;
  margin-bottom: 16px;
}

.panel-title strong {
  font-size: 22px;
  color: #173459;
}

.panel-title span {
  color: #6a7a91;
  font-size: 12px;
}

.plan-pick-grid,
.team-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

.plan-pick-card,
.team-card {
  padding: 16px;
  border: 1px solid #dbe4f2;
  border-radius: 18px;
  background: linear-gradient(180deg, #fbfdff, #f2f7ff);
  text-align: left;
  box-shadow: 0 12px 28px rgba(92, 117, 156, 0.06);
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

.plan-pick-card:hover,
.team-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 18px 36px rgba(79, 111, 163, 0.12);
}

.plan-pick-card--active,
.team-card--active {
  border-color: #173f7b;
  background: linear-gradient(180deg, rgba(23, 63, 123, 0.08), rgba(32, 113, 190, 0.08));
  box-shadow: 0 0 0 3px rgba(20, 61, 118, 0.1), 0 18px 34px rgba(33, 72, 132, 0.14);
}

.plan-pick-card span,
.plan-pick-card small,
.team-card span,
.team-card small {
  display: block;
  margin-top: 8px;
  color: #6d7c91;
}

.brochure-preview {
  display: grid;
  grid-template-columns: minmax(220px, 320px) minmax(0, 1fr);
  gap: 18px;
  margin-top: 18px;
  align-items: start;
}

.brochure-preview__media,
.brochure-preview__content {
  min-width: 0;
}

.brochure-preview img,
.brochure-preview__placeholder {
  width: 100%;
  min-height: 220px;
  border-radius: 20px;
  background: #f0f4fb;
}

.brochure-preview img {
  object-fit: cover;
}

.brochure-preview__placeholder {
  display: grid;
  place-items: center;
  color: #6f7d93;
}

.brochure-chip {
  display: inline-flex;
  width: fit-content;
  padding: 6px 10px;
  border-radius: 999px;
  background: rgba(27, 92, 170, 0.1);
  color: #1b5aa8;
  font-size: 12px;
  font-weight: 700;
}

.brochure-preview__content {
  display: grid;
  gap: 12px;
}

.brochure-preview__content strong {
  font-size: 24px;
  color: #173459;
}

.brochure-preview__content p {
  margin: 0;
  color: #52657f;
  line-height: 1.8;
}

.brochure-meta {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
  margin: 0;
}

.brochure-meta div {
  display: grid;
  gap: 4px;
  padding: 12px 14px;
  border-radius: 16px;
  background: rgba(240, 246, 255, 0.94);
}

.brochure-meta dt {
  color: #7183a0;
  font-size: 12px;
}

.brochure-meta dd {
  margin: 0;
  color: #173459;
  font-weight: 700;
}

.form-grid {
  display: grid;
  gap: 14px;
}

.form-grid--three {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.form-grid--two {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.compact-top {
  margin-top: 16px;
}

.form-field,
.agreement-row {
  display: grid;
  gap: 8px;
}

.form-field--full {
  grid-column: 1 / -1;
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
  .plan-pick-grid,
  .team-grid,
  .form-grid--three,
  .form-grid--two,
  .progress-bar,
  .brochure-preview {
    grid-template-columns: 1fr;
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
  .application-header,
  .submit-row {
    flex-direction: column;
    align-items: flex-start;
  }

  .application-page {
    padding: 14px;
  }

  .application-nav {
    grid-template-columns: 1fr;
  }
}
</style>