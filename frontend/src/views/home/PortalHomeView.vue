<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { Message, Phone, Tickets, User } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

import { changePortalStudentPassword, clearPortalToken, getPortalProfile, getPortalPublicConfig, listPortalPlans, type PortalPlanRecord, type PortalStudentRecord } from '../../api/portal'
import { resolveRequestError, showPortalAlert } from '../../utils/portalAlerts'

type ProgressCard = {
  key: string
  label: string
  hint: string
  status: 'not-started' | 'in-progress' | 'completed'
  completed: boolean
}

type WorkflowStageCard = {
  key: string
  label: string
  status: 'pending' | 'current' | 'completed' | 'returned' | 'terminated'
  description: string
}

const router = useRouter()
const defaultProfilePhotoUrl = '/images/default_head.png'
const showPortalHomeNewsSections = false
const portalAdmissionsInfoUrl = ref('')

function trimText(value: unknown): string {
  return typeof value === 'string' ? value.trim() : ''
}

function resolveProgressCount(value: unknown): number {
  const parsed = Number(value)
  return Number.isFinite(parsed) && parsed > 0 ? parsed : 0
}

const portalStudent = ref<PortalStudentRecord | null>(null)
const planList = ref<PortalPlanRecord[]>([])
const passwordDialogVisible = ref(false)
const passwordSubmitting = ref(false)
const passwordForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: '',
})

const fallbackAnnouncements = [
  { title: '2027 春季招生计划', term: '2027 春' },
  { title: '2026 智能制造联合培养', term: '2026 秋' },
  { title: '2026 工程博士专项', term: '2026 秋' },
]

const scheduleList = [
  {
    month: '2026年7月',
    items: ['公布博士招生简章目录、推免生目录', '推免博士生（春季招生）材料审核、确定综合考核名单'],
  },
  {
    month: '2026年4月',
    items: ['推免博士生（春季招生）报名申请', '公布硕士招生简章、普通招考招生目录'],
  },
]

const studentDisplayName = computed(() => trimText(portalStudent.value?.full_name) || '未注册')
const registrationNo = computed(() => {
  const student = portalStudent.value
  return trimText(student?.candidate_no) || trimText(student?.business_key) || '未提交申请'
})
const activePlan = computed(() => {
  const selectedPlanId = portalStudent.value?.selected_plan_id
  if (!selectedPlanId) {
    return null
  }
  return planList.value.find((item) => item.id === selectedPlanId) || null
})
const profilePhotoUrl = computed(() => {
  const student = portalStudent.value
  const legacyPhotoUrl = student && typeof (student as Record<string, unknown>).profile_photo_url === 'string'
    ? String((student as Record<string, unknown>).profile_photo_url)
    : ''
  const candidates = [
    student?.profile?.profile_photo_url,
    legacyPhotoUrl,
  ]
  return candidates.find((item) => typeof item === 'string' && item.trim()) || defaultProfilePhotoUrl
})
const hasSubmittedApplication = computed(() => Boolean(portalStudent.value?.submitted_at))
const completedProgressCount = computed(() => progressCards.value.filter((item) => item.completed).length)
const workflowSummary = computed(() => portalStudent.value?.workflow_progress || null)
const workflowStageCards = computed<WorkflowStageCard[]>(() => {
  const stages = workflowSummary.value?.stages || []
  return stages.map((item) => ({
    key: item.key,
    label: item.label,
    status: item.status,
    description: trimText(item.description) || resolveWorkflowStageDescription(item.status),
  }))
})
const workflowCurrentStageLabel = computed(() => workflowSummary.value?.current_stage_label || '在线申请')
const showApplicationSectionProgress = computed(() => {
  const currentStageKey = workflowSummary.value?.current_stage_key
  const stageStatus = workflowStageCards.value.find((item) => item.key === 'online_application')?.status
  if (!currentStageKey) {
    return true
  }
  return currentStageKey === 'online_application' || stageStatus === 'returned'
})

function resolveWorkflowStageDescription(status: WorkflowStageCard['status']): string {
  if (status === 'completed') {
    return '已完成'
  }
  if (status === 'current') {
    return '进行中'
  }
  if (status === 'returned') {
    return '已退回'
  }
  if (status === 'terminated') {
    return '已终止'
  }
  return '待开始'
}

const progressCards = computed<ProgressCard[]>(() => {
  const student = portalStudent.value
  const draft = student?.application_draft
  const profile = student?.profile
  const declaration = draft?.declaration
  const snapshot = declaration?.progress_snapshot && typeof declaration.progress_snapshot === 'object'
    ? declaration.progress_snapshot as Record<string, unknown>
    : null

  const basicStarted = Boolean(
    trimText(profile?.full_name_pinyin)
    || trimText(profile?.gender || student?.gender)
    || trimText(profile?.ethnic_group || student?.ethnic_group)
    || trimText(profile?.political_status || student?.political_status)
    || trimText(profile?.mailing_address || student?.mailing_address)
    || trimText(profile?.emergency_contact_name)
    || trimText(profile?.emergency_contact_phone)
    || trimText(profile?.profile_photo_url),
  )
  const basicCompleted = Boolean(
    trimText(profile?.full_name_pinyin)
    && trimText(profile?.gender || student?.gender)
    && trimText(profile?.ethnic_group || student?.ethnic_group)
    && trimText(profile?.political_status || student?.political_status)
    && trimText(profile?.mailing_address || student?.mailing_address)
    && trimText(profile?.emergency_contact_name)
    && trimText(profile?.emergency_contact_phone)
    && trimText(profile?.profile_photo_url),
  )

  const preferences = draft?.preferences || []
  const firstPreference = preferences[0]
  const applicationStarted = Boolean(
    trimText(draft?.source_channel)
    || trimText(draft?.source_channel_other)
    || trimText(firstPreference?.research_center_name)
    || trimText(firstPreference?.advisor_name)
    || student?.selected_plan_id,
  )
  const applicationCompleted = Boolean(trimText(firstPreference?.research_center_name) || student?.selected_team_name)

  const practiceCount = resolveProgressCount(snapshot?.practice_count)
  const practiceStarted = practiceCount > 0 || Boolean((draft?.practice_experiences || []).some((item) => trimText(item.organization_name)))
  const practiceCompleted = practiceStarted

  const englishCount = resolveProgressCount(snapshot?.english_count)
  const englishStarted = englishCount > 0 || Boolean((draft?.english_proficiencies || []).some((item) => trimText(item.exam_name)))
  const englishCompleted = englishStarted

  const familyItems = draft?.family_members || []
  const familyCount = resolveProgressCount(snapshot?.family_count)
  const familyStarted = familyCount > 0 || familyItems.some((item) => trimText(item.member_name) || trimText(item.relation_type))
  const father = familyItems.find((item) => trimText(item.relation_type) === '父亲' && trimText(item.member_name))
  const mother = familyItems.find((item) => trimText(item.relation_type) === '母亲' && trimText(item.member_name))
  const familyCompleted = Boolean(father && mother)

  const achievementCount = resolveProgressCount(snapshot?.achievement_count)
  const achievementStarted = achievementCount > 0 || Boolean((draft?.achievement_records || []).some((item) => trimText(item.achievement_type)))
  const achievementCompleted = achievementStarted

  const statementText = trimText(draft?.personal_statement?.personal_statement_text || student?.personal_statement_text)
  const statementStarted = Boolean(
    statementText
    || trimText(draft?.personal_statement?.ai_problem_statement)
    || trimText(draft?.personal_statement?.ai_industry_opinion)
    || trimText(draft?.personal_statement?.resume_attachment_url)
    || declaration?.has_read_declaration,
  )
  const statementCompleted = Boolean(statementText)

  const createCard = (key: string, label: string, started: boolean, completed: boolean, pendingHint = '待完善'): ProgressCard => ({
    key,
    label,
    hint: completed ? '已完成' : started ? '完善中' : pendingHint,
    status: completed ? 'completed' : started ? 'in-progress' : 'not-started',
    completed,
  })

  if (hasSubmittedApplication.value) {
    return [
      createCard('basic', '基本信息', true, true),
      createCard('application', '报名信息', true, true),
      createCard('practice', '实践经历', true, true),
      createCard('english', '英语语言能力', true, true),
      createCard('family', '家庭情况', true, true),
      createCard('achievement', '成果经历', true, true),
      createCard('statement', '个人陈述', true, true),
      createCard('submit', '提交申请', true, true),
    ]
  }

  return [
    createCard('basic', '基本信息', basicStarted, basicCompleted),
    createCard('application', '报名信息', applicationStarted, applicationCompleted),
    createCard('practice', '实践经历', practiceStarted, practiceCompleted),
    createCard('english', '英语语言能力', englishStarted, englishCompleted),
    createCard('family', '家庭情况', familyStarted, familyCompleted),
    createCard('achievement', '成果经历', achievementStarted, achievementCompleted),
    createCard('statement', '个人陈述', statementStarted, statementCompleted),
    createCard('submit', '提交申请', Boolean(student?.submitted_at), Boolean(student?.submitted_at), '待提交'),
  ]
})

const announcements = computed(() => {
  if (!planList.value.length) {
    return fallbackAnnouncements
  }
  return planList.value.slice(0, 3).map((item) => ({
    title: item.plan_name,
    term: item.academic_term,
  }))
})

async function loadPortalHome() {
  try {
    const [profileResponse, planResponse, publicConfigResponse] = await Promise.all([getPortalProfile(), listPortalPlans(), getPortalPublicConfig()])
    portalStudent.value = profileResponse.data
    planList.value = planResponse.data.items || []
    portalAdmissionsInfoUrl.value = publicConfigResponse.data.portal_admissions_info_url || ''
  } catch {
    clearPortalToken()
    await router.replace('/portal')
  }
}

async function openPortalAdmissionsInfo() {
  const targetUrl = portalAdmissionsInfoUrl.value.trim()
  if (!targetUrl) {
    await showPortalAlert('招生信息地址暂未配置', '提示', 'warning')
    return
  }
  window.open(targetUrl, '_blank', 'noopener,noreferrer')
}

function goToApplication() {
  void router.push('/portal/application')
}

function resetPasswordForm() {
  passwordForm.currentPassword = ''
  passwordForm.newPassword = ''
  passwordForm.confirmPassword = ''
}

function openPasswordDialog() {
  passwordDialogVisible.value = true
}

function closePasswordDialog() {
  passwordDialogVisible.value = false
  resetPasswordForm()
}

async function submitPasswordChange() {
  if (!passwordForm.currentPassword || !passwordForm.newPassword || !passwordForm.confirmPassword) {
    await showPortalAlert('请填写完整的密码信息', '修改密码', 'warning')
    return
  }
  if (passwordForm.newPassword.length < 8) {
    await showPortalAlert('新密码长度不能少于 8 位', '修改密码', 'warning')
    return
  }
  if (passwordForm.newPassword !== passwordForm.confirmPassword) {
    await showPortalAlert('两次输入的新密码不一致', '修改密码', 'warning')
    return
  }

  passwordSubmitting.value = true
  try {
    const response = await changePortalStudentPassword({
      current_password: passwordForm.currentPassword,
      new_password: passwordForm.newPassword,
    })
    closePasswordDialog()
    ElMessage.success(response.data.message || '密码修改成功')
  } catch (error) {
    await showPortalAlert(resolveRequestError(error, '密码修改失败'), '修改密码失败', 'error')
  } finally {
    passwordSubmitting.value = false
  }
}

function logoutPortal() {
  clearPortalToken()
  void router.replace('/portal')
}

onMounted(() => {
  void loadPortalHome()
})
</script>

<template>
  <div class="portal-home-page">
    <header class="portal-home-header">
      <div class="portal-home-header__inner">
        <div class="portal-home-header__brand">
          <img class="portal-home-header__logo" src="/images/logo.png" alt="上海人工智能实验室博士生招生" />
        </div>
        <nav class="portal-home-header__nav" aria-label="门户导航">
          <a class="portal-home-header__nav-link portal-home-header__nav-link--active" href="/portal/home">首页</a>
          <button type="button" class="portal-home-header__nav-link" @click="openPortalAdmissionsInfo">招生信息</button>
          <a class="portal-home-header__nav-link" href="/portal/application" @click.prevent="goToApplication">在线申请</a>
          <a class="portal-home-header__nav-link" href="#portal-progress">申请进度</a>
        </nav>
        <div class="portal-home-header__actions">
          <a class="portal-home-header__site" href="https://www.shlab.org.cn" target="_blank" rel="noreferrer">实验室官网</a>
          <button type="button" class="portal-home-header__user">{{ studentDisplayName }}</button>
          <button type="button" class="portal-home-header__logout" @click="logoutPortal">退出</button>
        </div>
      </div>
    </header>

    <section class="portal-home-hero">
      <div class="portal-home-hero__overlay"></div>
      <div class="portal-home-hero__shell">
        <div class="portal-home-hero__copy">
          <h1>欢迎加入上海人工智能实验室！</h1>
          <p style="font-weight:bolder">上海人工智能实验室自2022年启动博士生联合培养项目以来，已与国内十余所顶尖高校建立深度合作关系，致力于在通用人工智能（AGI）及相关前沿领域培养高水平科研人才。</p>
          <!--<span>建成国际一流人工智能实验室，中国人工智能原创理论和关键技术的策源地。</span>-->
        </div>
      </div>
    </section>

    <main class="portal-home-main">
      <section class="portal-home-profile-card">
        <div class="portal-home-profile-card__avatar-panel">
          <img class="portal-home-profile-card__avatar-image" :src="profilePhotoUrl" :alt="studentDisplayName" />
        </div>
        <div class="portal-home-profile-card__content">
          <div class="portal-home-profile-card__top">
            <div>
              <h2>{{ studentDisplayName }}</h2>
            </div>
            <button type="button" class="portal-home-profile-card__manage" @click="openPasswordDialog">账号管理 →</button>
          </div>
          <div class="portal-home-profile-card__meta-grid">
            <div class="portal-home-profile-card__meta">
              <hr class="portal-home-profile-card__rule" />
              <div class="portal-home-profile-card__meta-label">
                <el-icon><User /></el-icon>
                <span>报名号</span>
              </div>
              <strong>{{ registrationNo }}</strong>
            </div>
            <div class="portal-home-profile-card__meta">
              <hr class="portal-home-profile-card__rule" />
              <div class="portal-home-profile-card__meta-label">
                <el-icon><Tickets /></el-icon>
                <span>招生计划</span>
              </div>
              <strong>{{ activePlan?.plan_name || '未填写' }}</strong>
            </div>
            <div class="portal-home-profile-card__meta">
              <hr class="portal-home-profile-card__rule" />
              <div class="portal-home-profile-card__meta-label">
                <el-icon><Phone /></el-icon>
                <span>手机</span>
              </div>
              <strong>{{ portalStudent?.phone_number || '未填写' }}</strong>
            </div>
            <div class="portal-home-profile-card__meta">
              <hr class="portal-home-profile-card__rule" />
              <div class="portal-home-profile-card__meta-label">
                <el-icon><Message /></el-icon>
                <span>邮箱</span>
              </div>
              <strong>{{ portalStudent?.email || '未填写' }}</strong>
            </div>
          </div>
        </div>
      </section>

      <section id="portal-progress" class="portal-home-progress">
        <div class="portal-home-progress__header">
          <h3>我的申请进度</h3>
          <p v-if="showApplicationSectionProgress">已完成 {{ completedProgressCount }}/{{ progressCards.length }} 项，继续填写即可提交申请。</p>
        </div>

        <div class="portal-home-progress__workflow">
          <div class="portal-home-workflow__header">
            <div>
              <h4>申请环节状态</h4>
              <p>当前所在环节：{{ workflowCurrentStageLabel }}</p>
            </div>
          </div>

          <div class="portal-home-workflow__timeline" aria-label="申请流程阶段条">
            <template v-for="(stage, index) in workflowStageCards" :key="stage.key">
              <article
                class="portal-home-workflow__stage"
                :class="[
                  `portal-home-workflow__stage--${stage.status}`,
                  { 'portal-home-workflow__stage--arrow-hidden': index === workflowStageCards.length - 1 },
                ]"
              >
                <span class="portal-home-workflow__stage-index">{{ String(index + 1).padStart(2, '0') }}</span>
                <strong>{{ stage.label }}</strong>
                <p>{{ stage.description }}</p>
              </article>
              <span v-if="index < workflowStageCards.length - 1" class="portal-home-workflow__arrow" aria-hidden="true">→</span>
            </template>
          </div>
        </div>

        <div v-if="showApplicationSectionProgress" class="portal-home-progress__grid">
          <article
            v-for="card in progressCards"
            :key="card.key"
            class="portal-home-progress__item"
            :class="{ 'portal-home-progress__item--completed': card.completed }"
          >
            <div class="portal-home-progress__item-top">
              <strong>{{ card.label }}</strong>
              <i :class="{ 'portal-home-progress__item-icon--done': card.completed }">{{ card.completed ? '○' : '◔' }}</i>
            </div>
            <span>{{ card.completed ? '已完成' : card.hint }}</span>
          </article>
        </div>

        <button v-if="showApplicationSectionProgress" type="button" class="portal-home-progress__cta" @click="goToApplication">
          继续填写报名信息
          <span>→</span>
        </button>
      </section>

      <section
        class="portal-home-banner"
        role="button"
        tabindex="0"
        @click="openPortalAdmissionsInfo"
        @keydown.enter.prevent="openPortalAdmissionsInfo"
        @keydown.space.prevent="openPortalAdmissionsInfo"
      >
        <div class="portal-home-banner__inner">
          <p>查看更多上海人工智能实验室招生信息</p>
          <span class="portal-home-banner__action">了解更多 <span>→</span></span>
        </div>
      </section>

      <section v-if="showPortalHomeNewsSections" id="portal-news" class="portal-home-info-grid">
        <article class="portal-home-info-card">
          <div class="portal-home-info-card__title-row">
            <h3>招生信息</h3>
            <span>→</span>
          </div>
          <div class="portal-home-info-card__list">
            <div v-for="item in announcements" :key="`${item.title}-${item.term}`" class="portal-home-info-card__news-item">
              <span>{{ item.title }}</span>
              <time>{{ item.term }}</time>
            </div>
          </div>
        </article>

        <article class="portal-home-info-card">
          <div class="portal-home-info-card__title-row">
            <h3>报考日程</h3>
            <span>→</span>
          </div>
          <div class="portal-home-schedule">
            <div v-for="section in scheduleList" :key="section.month" class="portal-home-schedule__item">
              <div class="portal-home-schedule__month">{{ section.month }}</div>
              <ul>
                <li v-for="entry in section.items" :key="entry">{{ entry }}</li>
              </ul>
            </div>
          </div>
        </article>
      </section>
    </main>

    <footer class="portal-home-footer"></footer>

    <div v-if="passwordDialogVisible" class="portal-home-password-dialog">
      <button type="button" class="portal-home-password-dialog__mask" aria-label="关闭修改密码弹窗" @click="closePasswordDialog"></button>
      <div class="portal-home-password-dialog__panel" role="dialog" aria-modal="true" aria-labelledby="portal-home-password-title">
        <div class="portal-home-password-dialog__header">
          <div>
            <strong id="portal-home-password-title">修改登录密码</strong>
            <span>当前登录人：{{ studentDisplayName }}</span>
          </div>
          <button type="button" class="portal-home-password-dialog__close" @click="closePasswordDialog">关闭</button>
        </div>

        <div class="portal-home-password-dialog__body">
          <label>
            <span>当前密码</span>
            <input v-model="passwordForm.currentPassword" type="password" placeholder="请输入当前密码" />
          </label>
          <label>
            <span>新密码</span>
            <input v-model="passwordForm.newPassword" type="password" placeholder="至少 8 位" />
          </label>
          <label>
            <span>确认新密码</span>
            <input v-model="passwordForm.confirmPassword" type="password" placeholder="请再次输入新密码" />
          </label>
        </div>

        <div class="portal-home-password-dialog__actions">
          <button type="button" class="portal-home-password-dialog__button portal-home-password-dialog__button--ghost" :disabled="passwordSubmitting" @click="closePasswordDialog">取消</button>
          <button type="button" class="portal-home-password-dialog__button portal-home-password-dialog__button--primary" :disabled="passwordSubmitting" @click="submitPasswordChange">{{ passwordSubmitting ? '提交中...' : '确认修改' }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.portal-home-page {
  min-height: 100vh;
  color: #143a6f;
  background:
    linear-gradient(180deg, #dcecff 0%, #f7fbff 240px, #ffffff 241px, #ffffff 100%);
}

.portal-home-header {
  position: sticky;
  top: 0;
  z-index: 30;
  background: linear-gradient(90deg, rgba(6, 60, 128, 0.96), rgba(31, 114, 215, 0.94) 56%, rgba(10, 88, 175, 0.96));
  box-shadow: 0 6px 18px rgba(7, 42, 99, 0.14);
}

.portal-home-header__inner,
.portal-home-hero__shell,
.portal-home-main {
  width: min(1280px, calc(100% - 56px));
  margin: 0 auto;
}

.portal-home-header__inner {
  min-height: 62px;
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 24px;
}

.portal-home-header__logo {
  display: block;
  height: 36px;
  object-fit: contain;
}

.portal-home-header__nav,
.portal-home-header__actions {
  display: flex;
  align-items: center;
}

.portal-home-header__nav {
  justify-content: center;
  gap: 28px;
}

.portal-home-header__nav-link,
.portal-home-header__site {
  color: rgba(255, 255, 255, 0.92);
  text-decoration: none;
  font-size: 13px;
}

.portal-home-header__nav-link {
  position: relative;
  padding: 8px 6px;
  border: none;
  background: transparent;
  font-weight: 600;
  letter-spacing: 0.04em;
  cursor: pointer;
}

.portal-home-header__nav-link::after {
  content: '';
  position: absolute;
  left: 6px;
  right: 6px;
  bottom: -2px;
  height: 2px;
  border-radius: 999px;
  background: transparent;
}

.portal-home-header__nav-link--active::after {
  background: linear-gradient(90deg, #d6ebff, #ffffff);
}

.portal-home-header__actions {
  gap: 10px;
}

.portal-home-header__user,
.portal-home-header__logout {
  min-height: 30px;
  padding: 0 10px;
  border-radius: 999px;
  color: #fff;
  font-size: 12px;
  cursor: pointer;
}

.portal-home-header__user {
  border: none;
  background: rgba(255, 255, 255, 0.16);
}

.portal-home-header__logout {
  border: 1px solid rgba(255, 255, 255, 0.32);
  background: transparent;
}

.portal-home-hero {
  position: relative;
  min-height: 420px;
  background:
    linear-gradient(90deg, rgba(232, 241, 251, 0.9) 0%, rgba(232, 241, 251, 0.68) 28%, rgba(232, 241, 251, 0.14) 62%, rgba(232, 241, 251, 0.06) 100%),
    url('/images/top_builder_background.png') center 32%/cover no-repeat;
}

.portal-home-hero__overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.28) 46%, rgba(255, 255, 255, 0.36));
}

.portal-home-hero__shell {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  min-height: 420px;
  padding-top: 42px;
}

.portal-home-hero__copy {
  max-width: 610px;
  margin-top: 22px;
}

.portal-home-hero__copy h1 {
  margin: 0 0 18px;
  color: #0054bf;
  max-width: 560px;
  font-size: 34px;
  line-height: 1.32;
  font-weight: 800;
}

.portal-home-hero__copy p {
  margin: 0 0 12px;
  color: #213e62;
  max-width: 520px;
  font-size: 13px;
  line-height: 1.8;
}

.portal-home-hero__copy span {
  display: block;
  color: #3f5d84;
  max-width: 540px;
  font-size: 13px;
  line-height: 1.8;
}

.portal-home-main {
  margin-top: -74px;
  padding-bottom: 64px;
}

.portal-home-profile-card,
.portal-home-progress,
.portal-home-info-card {
  background: #fff;
  box-shadow: 0 14px 34px rgba(17, 53, 108, 0.08);
}

.portal-home-profile-card {
  position: relative;
  z-index: 2;
  display: grid;
  grid-template-columns: auto minmax(0, 1fr);
  height: 278px;
  gap: 0;
  padding: 0;
  border-radius: 0;
  overflow: hidden;
}

.portal-home-profile-card__avatar-panel {
  display: block;
  align-self: stretch;
  height: 278px;
  min-height: 278px;
  background: transparent;
}

.portal-home-profile-card__avatar-image {
  width: auto;
  height: 278px;
  max-width: none;
  display: block;
  border-radius: 0;
  background: transparent;
}

.portal-home-profile-card__content {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 28px 48px 28px;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.985), rgba(255, 255, 255, 0.985)),
    url('/images/login_background.png') right top / 360px auto no-repeat;
}

.portal-home-profile-card__top {
  display: flex;
  justify-content: space-between;
  gap: 24px;
  align-items: center;
  margin-bottom: 30px;
}

.portal-home-profile-card__top h2 {
  margin: 0;
  font-size: 20px;
  line-height: 1.2;
  font-weight: 700;
  color: #222c3c;
}

.portal-home-profile-card__manage {
  border: none;
  background: transparent;
  color: #3d91f2;
  font-size: 18px;
  line-height: 1.2;
  font-weight: 500;
  cursor: pointer;
}

.portal-home-profile-card__meta-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 28px;
}

.portal-home-profile-card__meta {
  min-width: 0;
}

.portal-home-profile-card__rule {
  margin: 0 0 22px;
  border: 0;
  border-top: 1px solid #e6ebf2;
}

.portal-home-profile-card__meta-label {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 18px;
  color: #5d6673;
}

.portal-home-profile-card__meta-label .el-icon {
  font-size: 18px;
  color: #737b87;
}

.portal-home-profile-card__meta-label span {
  display: block;
  color: #555f6d;
  font-size: 16px;
  line-height: 1.2;
}

.portal-home-profile-card__meta strong {
  display: block;
  color: #444;
  font-size: 20px;
  font-weight: 400;
  line-height: 1.3;
  letter-spacing: 0.01em;
  white-space: nowrap;
}

.portal-home-progress {
  margin-top: 28px;
  padding: 26px 28px 0;
  border-radius: 8px;
}

.portal-home-progress__workflow {
  margin-top: 18px;
  padding: 18px 18px 16px;
  border: 1px solid #e8eff9;
  border-radius: 10px;
  background: linear-gradient(180deg, #fbfdff, #f7faff);
}

.portal-home-workflow__header {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: flex-start;
}

.portal-home-workflow__header h4 {
  margin: 0 0 6px;
  font-size: 16px;
  color: #0053bc;
}

.portal-home-workflow__header p {
  margin: 0;
  color: #8b9eb7;
  font-size: 12px;
}

.portal-home-workflow__timeline {
  display: flex;
  align-items: stretch;
  gap: 8px;
  margin-top: 14px;
  overflow-x: auto;
  padding-bottom: 4px;
}

.portal-home-workflow__stage {
  position: relative;
  flex: 1 0 132px;
  min-width: 132px;
  padding: 12px 12px 11px;
  border-radius: 10px;
  border: 1px solid #dfe9f8;
  background: linear-gradient(180deg, #f8fbff, #ffffff);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.7);
}

.portal-home-workflow__stage-index {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 34px;
  height: 22px;
  margin-bottom: 10px;
  border-radius: 999px;
  background: #e8f1ff;
  color: #1567d7;
  font-size: 11px;
  font-weight: 700;
}

.portal-home-workflow__stage strong {
  display: block;
  margin-bottom: 6px;
  color: #203c60;
  font-size: 13px;
}

.portal-home-workflow__stage p {
  margin: 0;
  color: #7f92ad;
  font-size: 11px;
  line-height: 1.45;
}

.portal-home-workflow__arrow {
  flex: 0 0 auto;
  align-self: center;
  color: #6b9ce0;
  font-size: 18px;
  font-weight: 700;
}

.portal-home-workflow__stage--completed {
  border-color: #cfe8d7;
  background: linear-gradient(180deg, #f2fbf4, #ffffff);
}

.portal-home-workflow__stage--completed .portal-home-workflow__stage-index {
  background: #ddf4e3;
  color: #207447;
}

.portal-home-workflow__stage--completed strong,
.portal-home-workflow__stage--completed p {
  color: #25573a;
}

.portal-home-workflow__stage--current {
  border-color: #6daaf1;
  background: linear-gradient(180deg, #edf5ff, #ffffff);
  box-shadow: 0 10px 24px rgba(24, 103, 214, 0.12);
}

.portal-home-workflow__stage--current .portal-home-workflow__stage-index {
  background: linear-gradient(90deg, #0e6ddd, #2a8ef4);
  color: #fff;
}

.portal-home-workflow__stage--returned {
  border-color: #f0c56c;
  background: linear-gradient(180deg, #fff8e9, #ffffff);
}

.portal-home-workflow__stage--returned .portal-home-workflow__stage-index {
  background: #ffe8b0;
  color: #9a6400;
}

.portal-home-workflow__stage--returned strong,
.portal-home-workflow__stage--returned p {
  color: #8a5f10;
}

.portal-home-workflow__stage--terminated {
  border-color: #f1c4c4;
  background: linear-gradient(180deg, #fff5f5, #ffffff);
}

.portal-home-workflow__stage--terminated .portal-home-workflow__stage-index {
  background: #ffd8d8;
  color: #b42318;
}

.portal-home-workflow__stage--terminated strong,
.portal-home-workflow__stage--terminated p {
  color: #9a2f2f;
}

.portal-home-progress__header h3 {
  margin: 0 0 8px;
  font-size: 20px;
  color: #0053bc;
}

.portal-home-progress__header p {
  margin: 0;
  color: #8b9eb7;
  font-size: 13px;
}

.portal-home-progress__grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
  padding: 18px 0 24px;
}

.portal-home-progress__item {
  padding: 14px 14px 13px;
  border: 1px solid #edf2f7;
  border-radius: 6px;
  background: #fff;
}

.portal-home-progress__item-top {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  align-items: center;
  margin-bottom: 8px;
}

.portal-home-progress__item strong {
  font-size: 14px;
  color: #203c60;
}

.portal-home-progress__item span {
  color: #91a2b9;
  font-size: 11px;
}

.portal-home-progress__item--completed strong,
.portal-home-progress__item--completed span {
  color: #1f6b3a;
  font-weight: 700;
}

.portal-home-progress__item i {
  font-style: normal;
  color: #2b7ce0;
}

.portal-home-progress__item-icon--done {
  color: #1f6b3a;
}

.portal-home-progress__cta {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 14px;
  width: calc(100% + 56px);
  min-height: 52px;
  margin: 0 -28px;
  border: none;
  color: #fff;
  font-size: 15px;
  font-weight: 700;
  background: linear-gradient(90deg, #0d67db, #1575e7);
  cursor: pointer;
}

.portal-home-banner {
  margin-top: 30px;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  background:
    linear-gradient(180deg, rgba(7, 62, 138, 0.54), rgba(7, 62, 138, 0.54)),
    url('/images/middle_background.png') center/cover no-repeat;
}

.portal-home-banner__inner {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 32px;
  width: min(1280px, calc(100% - 56px));
  min-height: 122px;
  margin: 0 auto;
  color: #fff;
}

.portal-home-banner__inner p {
  margin: 0;
  font-size: 26px;
  font-weight: 700;
  letter-spacing: 0.02em;
}

.portal-home-banner__action {
  color: #fff;
  font-size: 17px;
}

.portal-home-info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-top: 32px;
}

.portal-home-info-card {
  padding: 28px 28px 22px;
}

.portal-home-info-card__title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
}

.portal-home-info-card__title-row h3 {
  margin: 0;
  font-size: 18px;
  color: #102d54;
}

.portal-home-info-card__title-row span {
  font-size: 20px;
  color: #1c4989;
}

.portal-home-info-card__news-item {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  padding: 14px 0;
  border-top: 1px solid #eef2f7;
}

.portal-home-info-card__news-item span {
  color: #1d2f45;
  font-size: 13px;
  line-height: 1.7;
}

.portal-home-info-card__news-item time {
  white-space: nowrap;
  color: #9aa8bb;
  font-size: 12px;
}

.portal-home-schedule {
  display: grid;
  gap: 16px;
}

.portal-home-schedule__item {
  display: grid;
  grid-template-columns: 96px 1fr;
  gap: 14px;
}

.portal-home-schedule__month {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 42px;
  color: #fff;
  font-size: 12px;
  font-weight: 700;
  background: linear-gradient(180deg, #1671e6, #0f61ca);
}

.portal-home-schedule ul {
  margin: 0;
  padding-left: 18px;
  color: #3b516d;
  font-size: 13px;
}

.portal-home-schedule li + li {
  margin-top: 8px;
}

.portal-home-footer {
  margin-top: 52px;
  height: 412px;
  background: url('/images/bottom_backgound.png?v=20260429') center/cover no-repeat;
}

.portal-home-footer__info img {
  height: 38px;
  margin-bottom: 28px;
}

.portal-home-footer__info p,
.portal-home-footer__contact span,
.portal-home-footer__contact strong {
  display: block;
  margin: 8px 0;
}

.portal-home-footer__contact {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-end;
}

.portal-home-footer__icons {
  display: flex;
  gap: 12px;
  margin-top: 12px;
  font-size: 24px;
}

.portal-home-password-dialog {
  position: fixed;
  inset: 0;
  z-index: 80;
}

.portal-home-password-dialog__mask {
  position: absolute;
  inset: 0;
  border: none;
  background: rgba(9, 29, 62, 0.42);
}

.portal-home-password-dialog__panel {
  position: relative;
  z-index: 1;
  width: min(460px, calc(100vw - 32px));
  margin: 12vh auto 0;
  padding: 22px 22px 20px;
  border-radius: 24px;
  background: #ffffff;
  box-shadow: 0 28px 72px rgba(7, 42, 99, 0.24);
}

.portal-home-password-dialog__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
}

.portal-home-password-dialog__header strong,
.portal-home-password-dialog__header span {
  display: block;
}

.portal-home-password-dialog__header strong {
  color: #18355d;
  font-size: 20px;
}

.portal-home-password-dialog__header span {
  margin-top: 6px;
  color: #6f86a7;
  font-size: 13px;
}

.portal-home-password-dialog__close {
  border: none;
  background: transparent;
  color: #6f86a7;
  cursor: pointer;
}

.portal-home-password-dialog__body {
  display: grid;
  gap: 14px;
  margin-top: 22px;
}

.portal-home-password-dialog__body label {
  display: grid;
  gap: 8px;
}

.portal-home-password-dialog__body span {
  color: #18355d;
  font-size: 13px;
  font-weight: 600;
}

.portal-home-password-dialog__body input {
  min-height: 44px;
  padding: 0 14px;
  border: 1px solid #d7e3f3;
  border-radius: 12px;
  outline: none;
}

.portal-home-password-dialog__body input:focus {
  border-color: #4b84d4;
  box-shadow: 0 0 0 3px rgba(75, 132, 212, 0.12);
}

.portal-home-password-dialog__actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 22px;
}

.portal-home-password-dialog__button {
  min-width: 96px;
  min-height: 40px;
  padding: 0 18px;
  border-radius: 12px;
  cursor: pointer;
}

.portal-home-password-dialog__button--ghost {
  border: 1px solid #d7e3f3;
  background: #fff;
  color: #31537f;
}

.portal-home-password-dialog__button--primary {
  border: none;
  background: linear-gradient(135deg, #1f73d8, #1b58b3);
  color: #fff;
}

@media (max-width: 1100px) {
  .portal-home-header__inner,
  .portal-home-hero__shell,
  .portal-home-main,
  .portal-home-footer__shell,
  .portal-home-banner__inner {
    width: min(100% - 24px, 1280px);
  }

  .portal-home-profile-card,
  .portal-home-info-grid,
  .portal-home-profile-card__meta-grid,
  .portal-home-progress__grid {
    grid-template-columns: 1fr;
    flex-direction: column;
  }

  .portal-home-workflow__header {
    flex-direction: column;
  }
}

@media (max-width: 768px) {
  .portal-home-header__inner {
    grid-template-columns: 1fr;
    justify-items: start;
    padding: 12px 0;
  }

  .portal-home-header__nav,
  .portal-home-header__actions {
    flex-wrap: wrap;
    justify-content: flex-start;
  }

  .portal-home-hero {
    min-height: 320px;
  }

  .portal-home-hero__shell {
    min-height: 320px;
  }

  .portal-home-hero__copy h1 {
    font-size: 30px;
    max-width: 100%;
  }

  .portal-home-hero__shell {
    padding-top: 18px;
  }

  .portal-home-hero__copy {
    margin-top: 8px;
  }

  .portal-home-profile-card {
    grid-template-columns: 1fr;
    height: auto;
  }

  .portal-home-profile-card__avatar-panel {
    height: auto;
    min-height: 0;
  }

  .portal-home-profile-card__avatar-image {
    height: 278px;
    margin: 0 auto;
  }

  .portal-home-profile-card__content,
  .portal-home-progress,
  .portal-home-progress__workflow,
  .portal-home-progress {
    padding-left: 20px;
    padding-right: 20px;
  }

  .portal-home-main {
    margin-top: -52px;
  }

  .portal-home-progress__cta {
    width: calc(100% + 40px);
    margin: 0 -20px;
  }

  .portal-home-progress__grid,
  .portal-home-profile-card__meta-grid,
  .portal-home-info-grid {
    grid-template-columns: 1fr;
  }

  .portal-home-workflow__timeline {
    gap: 8px;
  }

  .portal-home-workflow__stage {
    min-width: 126px;
  }

  .portal-home-banner__inner {
    flex-direction: column;
    gap: 10px;
    text-align: center;
    padding: 18px 0;
  }

  .portal-home-banner__inner p {
    font-size: 18px;
  }
}
</style>
