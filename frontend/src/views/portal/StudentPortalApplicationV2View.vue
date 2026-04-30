<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { Briefcase, EditPen, House, Medal, OfficeBuilding, Reading, School, User } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

import { changePortalStudentPassword, clearPortalToken, getPortalProfile } from '../../api/portal'
import { ensurePortalApplicationV2Available } from '../../utils/portalApplicationV2Access'
import { resolveRequestError, showPortalAlert } from '../../utils/portalAlerts'
import PortalApplicationV2Form from './applicationv2/PortalApplicationV2Form.vue'

const router = useRouter()

type PortalSectionStatus = {
  id: string
  label: string
  completed: boolean
  status: 'not-started' | 'in-progress' | 'completed'
}

type PortalApplicationViewExpose = {
  saveDraft: (showSuccess?: boolean) => Promise<boolean>
  getSectionStatuses: () => PortalSectionStatus[]
  getSavingDraft: () => boolean
  getIsSubmitted: () => boolean
}

const workflowStages = [
  { index: '1', label: '在线申请', active: true },
  { index: '2', label: '资料审核' },
  { index: '3', label: '中心面试考核' },
  { index: '4', label: '结果公布' },
  { index: '5', label: '预录取' },
]

const headerLinks = [
  { label: '首页', href: '/portal/home' },
  { label: '招生信息', href: '/portal/home#portal-news' },
  { label: '在线申请', href: '/portal/applicationv2', active: true },
  { label: '申请进度', href: '/portal/home#portal-progress' },
]

const formSections = [
  { id: 'basic-section', label: '基本信息', description: '用于确认身份、联系方式与基础背景。', icon: User },
  { id: 'application-section', label: '报名信息', description: '填写获知渠道、研究中心志愿和导师选择。', icon: OfficeBuilding },
  { id: 'education-section', label: '教育经历', description: '', icon: School },
  { id: 'practice-section', label: '实践经历', description: '补充项目、实习、工程实践或工作经历。', icon: Briefcase },
  { id: 'english-section', label: '英语能力', description: '请至少填写 1 条英语考试记录并上传证明材料。', icon: Reading },
  { id: 'family-section', label: '家庭情况', description: '父母信息必填，其他成员可按需补充。', icon: House },
  { id: 'achievement-section', label: '成果经历', description: '可补充论文发表与获奖经历，最多填写 4 条。', icon: Medal },
  { id: 'statement-section', label: '个人陈述', description: '请填写个人陈述并上传简历。', icon: EditPen },
]

const activeSectionId = ref('basic-section')

const activeSectionIndex = computed(() => formSections.findIndex((item) => item.id === activeSectionId.value))
const activeSection = computed(() => formSections[activeSectionIndex.value] || formSections[0])
const activeSectionStep = computed(() => `STEP ${String(activeSectionIndex.value + 1).padStart(2, '0')}`)
const canMovePrev = computed(() => activeSectionIndex.value > 0)
const canMoveNext = computed(() => activeSectionIndex.value >= 0 && activeSectionIndex.value < formSections.length - 1)
const applicationViewRef = ref<PortalApplicationViewExpose | null>(null)
const sectionStatuses = computed(() => applicationViewRef.value?.getSectionStatuses() || [])
const savingDraft = computed(() => applicationViewRef.value?.getSavingDraft() || false)
const submittedReadonly = computed(() => applicationViewRef.value?.getIsSubmitted() || false)
const portalStudentName = ref('学生')
const passwordDialogVisible = ref(false)
const passwordSubmitting = ref(false)
const passwordForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: '',
})

function resolveSectionStatus(sectionId: string) {
  return sectionStatuses.value.find((item) => item.id === sectionId)?.status || 'not-started'
}

function resolveSectionStatusText(sectionId: string) {
  const status = resolveSectionStatus(sectionId)
  if (status === 'completed') {
    return '已完成'
  }
  if (status === 'in-progress') {
    return '进行中'
  }
  return '未完成'
}

function goToSection(sectionId: string) {
  activeSectionId.value = sectionId
}

function goPrevSection() {
  if (!canMovePrev.value) {
    return
  }
  activeSectionId.value = formSections[activeSectionIndex.value - 1].id
}

function goNextSection() {
  if (!canMoveNext.value) {
    return
  }
  activeSectionId.value = formSections[activeSectionIndex.value + 1].id
}

async function saveCurrentSection() {
  await applicationViewRef.value?.saveDraft(true)
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

function logoutPortal() {
  clearPortalToken()
  void router.replace('/portal')
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

onMounted(async () => {
  const allowed = await ensurePortalApplicationV2Available()
  if (!allowed) {
    await router.replace('/portal/home')
    return
  }

  try {
    const response = await getPortalProfile()
    portalStudentName.value = response.data.full_name || '学生'
  } catch {
    portalStudentName.value = '学生'
  }
})
</script>

<template>
  <div class="portal-application-v2">
    <div class="portal-v2-backdrop portal-v2-backdrop--top" aria-hidden="true"></div>

    <header class="portal-v2-header">
      <div class="portal-v2-header__inner">
        <div class="portal-v2-brand">
          <img class="portal-v2-brand__logo" src="/images/logo.png" alt="上海人工智能实验室博士生招生" />
        </div>
        <nav class="portal-v2-nav" aria-label="门户导航">
          <a
            v-for="link in headerLinks"
            :key="link.label"
            :href="link.href"
            class="portal-v2-nav__link"
            :class="{ 'portal-v2-nav__link--active': link.active }"
          >
            {{ link.label }}
          </a>
        </nav>
        <div class="portal-v2-user">
          <a class="portal-v2-user__site" href="https://www.sail.sea.com" target="_blank" rel="noreferrer">实验室官网</a>
          <button type="button" class="portal-v2-user__badge" @click="openPasswordDialog">{{ portalStudentName }}</button>
          <button type="button" class="portal-v2-user__logout" @click="logoutPortal">退出</button>
        </div>
      </div>
    </header>

    <section class="portal-v2-hero">
      <div class="portal-v2-hero__glow portal-v2-hero__glow--left"></div>
      <div class="portal-v2-hero__glow portal-v2-hero__glow--right"></div>
      <div class="portal-v2-stage-wrap">
        <div class="portal-v2-stage-card portal-v2-stage-card--hidden">
          <div class="portal-v2-stage-card__header">
            <strong>在线申请</strong>
          </div>
          <div class="portal-v2-stage-bar">
            <div
              v-for="stage in workflowStages"
              :key="stage.index"
              class="portal-v2-stage"
              :class="{ 'portal-v2-stage--active': stage.active }"
            >
              <span class="portal-v2-stage__index">{{ stage.index }}</span>
              <span class="portal-v2-stage__label">{{ stage.label }}</span>
            </div>
          </div>
        </div>

        <section class="portal-v2-workbench">
          <aside class="portal-v2-side-nav">
            <button
              v-for="(section, index) in formSections"
              :key="section.id"
              type="button"
              class="portal-v2-side-nav__item"
              :class="{
                'portal-v2-side-nav__item--active': section.id === activeSectionId,
                'portal-v2-side-nav__item--completed': resolveSectionStatus(section.id) === 'completed',
                'portal-v2-side-nav__item--progress': resolveSectionStatus(section.id) === 'in-progress',
              }"
              @click="goToSection(section.id)"
            >
              <span class="portal-v2-side-nav__index">{{ index + 1 }}</span>
              <component :is="section.icon" class="portal-v2-side-nav__icon" />
              <span class="portal-v2-side-nav__copy">
                <strong>{{ section.label }}</strong>
              </span>
              <span class="portal-v2-side-nav__status">{{ resolveSectionStatusText(section.id) }}</span>
            </button>
          </aside>

          <div class="portal-v2-main-panel">
            <div class="portal-v2-main-panel__header">
              <div class="portal-v2-main-panel__step">
                <strong>{{ activeSectionStep }}</strong>
              </div>
              <div class="portal-v2-main-panel__copy">
                <h2>{{ activeSection.label }}</h2>
              </div>
            </div>

            <div class="portal-v2-embedded-wrap">
              <PortalApplicationV2Form ref="applicationViewRef" class="portal-v2-embedded" :active-section-id="activeSectionId" />
            </div>

            <div class="portal-v2-actions">
              <button type="button" class="portal-v2-actions__button portal-v2-actions__button--save" :disabled="savingDraft || submittedReadonly" @click="saveCurrentSection">{{ submittedReadonly ? '已提交只读' : savingDraft ? '保存中...' : '保存' }}</button>
              <button type="button" class="portal-v2-actions__button portal-v2-actions__button--ghost" :disabled="!canMovePrev" @click="goPrevSection">上一步</button>
              <button type="button" class="portal-v2-actions__button portal-v2-actions__button--primary" :disabled="!canMoveNext" @click="goNextSection">下一步</button>
            </div>
          </div>
        </section>
      </div>
    </section>

    <footer class="portal-v2-footer">
      <div class="portal-v2-footer__backdrop" aria-hidden="true"></div>
    </footer>

    <div v-if="passwordDialogVisible" class="portal-v2-password-dialog">
      <button type="button" class="portal-v2-password-dialog__mask" aria-label="关闭修改密码弹窗" @click="closePasswordDialog"></button>
      <div class="portal-v2-password-dialog__panel" role="dialog" aria-modal="true" aria-labelledby="portal-password-title">
        <div class="portal-v2-password-dialog__header">
          <div>
            <strong id="portal-password-title">修改登录密码</strong>
            <span>当前登录人：{{ portalStudentName }}</span>
          </div>
          <button type="button" class="portal-v2-password-dialog__close" @click="closePasswordDialog">关闭</button>
        </div>

        <div class="portal-v2-password-dialog__body">
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

        <div class="portal-v2-password-dialog__actions">
          <button type="button" class="portal-v2-password-dialog__button portal-v2-password-dialog__button--ghost" :disabled="passwordSubmitting" @click="closePasswordDialog">取消</button>
          <button type="button" class="portal-v2-password-dialog__button portal-v2-password-dialog__button--primary" :disabled="passwordSubmitting" @click="submitPasswordChange">{{ passwordSubmitting ? '提交中...' : '确认修改' }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.portal-application-v2 {
  --portal-shell-width: min(1440px, calc(100% - 48px));
  min-height: 100vh;
  position: relative;
  width: 100%;
  max-width: 100%;
  overflow-x: clip;
  background: #eef4fc;
}

.portal-v2-backdrop {
  position: absolute;
  left: 0;
  width: 100%;
  max-width: 100%;
  pointer-events: none;
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
  z-index: 0;
}

.portal-v2-backdrop--top {
  top: 0;
  height: 500px;
  background-image:
    linear-gradient(180deg, rgba(7, 45, 111, 0.94), rgba(15, 88, 184, 0.84) 50%, rgba(17, 91, 188, 0.62)),
    url('/images/top_background.png');
}

.portal-v2-header {
  position: sticky;
  top: 0;
  z-index: 30;
  background: linear-gradient(90deg, rgba(7, 49, 120, 0.96), rgba(20, 92, 189, 0.94) 54%, rgba(10, 72, 164, 0.96));
  box-shadow: 0 14px 40px rgba(8, 42, 102, 0.22);
}

.portal-v2-header__inner {
  width: min(1600px, calc(100% - 56px));
  margin: 0 auto;
  min-height: 74px;
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 28px;
  align-items: center;
}

.portal-v2-brand {
  display: inline-flex;
  align-items: center;
  min-width: 0;
}

.portal-v2-brand__logo {
  display: block;
  width: auto;
  max-width: min(100%, 372px);
  height: 48px;
  object-fit: contain;
  object-position: left center;
}

.portal-v2-nav {
  display: inline-flex;
  justify-content: center;
  gap: 20px;
}

.portal-v2-nav__link {
  position: relative;
  padding: 10px 14px;
  color: rgba(255, 255, 255, 0.92);
  text-decoration: none;
  font-size: 14px;
  font-weight: 600;
}

.portal-v2-nav__link::after {
  content: '';
  position: absolute;
  left: 14px;
  right: 14px;
  bottom: 4px;
  height: 2px;
  border-radius: 999px;
  background: transparent;
}

.portal-v2-nav__link--active::after {
  background: linear-gradient(90deg, #d0e7ff, #ffffff);
}

.portal-v2-user {
  display: inline-flex;
  align-items: center;
  gap: 12px;
}

.portal-v2-user__site {
  color: rgba(255, 255, 255, 0.88);
  font-size: 13px;
  text-decoration: none;
}

.portal-v2-user__badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 52px;
  max-width: 160px;
  min-height: 34px;
  padding: 0 12px;
  border: none;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.14);
  color: #fff;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.portal-v2-user__logout {
  min-height: 34px;
  padding: 0 12px;
  border: 1px solid rgba(255, 255, 255, 0.28);
  border-radius: 999px;
  background: transparent;
  color: rgba(255, 255, 255, 0.92);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}

.portal-v2-hero {
  position: relative;
  z-index: 1;
  overflow: visible;
  padding: 20px 24px 0;
}

.portal-v2-hero__glow {
  position: absolute;
  width: 520px;
  height: 520px;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.28;
  pointer-events: none;
}

.portal-v2-hero__glow--left {
  left: -180px;
  top: -120px;
  background: rgba(74, 162, 255, 0.5);
}

.portal-v2-hero__glow--right {
  right: -180px;
  top: -160px;
  background: rgba(58, 206, 255, 0.44);
}

.portal-v2-stage-wrap {
  position: relative;
  z-index: 1;
  width: var(--portal-shell-width);
  margin: 0 auto;
}

.portal-v2-workbench {
  display: grid;
  grid-template-columns: 236px minmax(0, 1fr);
  gap: 0;
  min-height: clamp(620px, calc(100vh - 210px), 760px);
  border-radius: 18px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.995);
  box-shadow: 0 30px 72px rgba(10, 37, 86, 0.18);
  border: 1px solid rgba(219, 227, 239, 0.78);
}

.portal-v2-side-nav {
  display: grid;
  align-content: start;
  background: linear-gradient(180deg, #ffffff, #f8fbff);
  border-right: 1px solid rgba(202, 214, 234, 0.72);
}

.portal-v2-side-nav__item {
  display: grid;
  grid-template-columns: 32px 20px minmax(0, 1fr) max-content;
  column-gap: 12px;
  align-items: center;
  min-height: 72px;
  padding: 16px 16px;
  border: none;
  border-bottom: 1px solid rgba(235, 240, 248, 0.96);
  background: transparent;
  text-align: left;
  cursor: pointer;
}

.portal-v2-side-nav__item--active {
  background: linear-gradient(90deg, rgba(28, 97, 193, 0.08), rgba(28, 97, 193, 0.02));
}

.portal-v2-side-nav__item--completed .portal-v2-side-nav__status {
  color: #15803d;
}

.portal-v2-side-nav__item--progress .portal-v2-side-nav__status {
  color: #b7791f;
}

.portal-v2-side-nav__index {
  display: grid;
  place-items: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(17, 56, 112, 0.08);
  color: #32547f;
  font-size: 12px;
  font-weight: 800;
}

.portal-v2-side-nav__icon {
  width: 18px;
  height: 18px;
  color: #7a90b2;
}

.portal-v2-side-nav__item--active .portal-v2-side-nav__index {
  background: #1f73d8;
  color: #fff;
}

.portal-v2-side-nav__item--active .portal-v2-side-nav__icon {
  color: #1f73d8;
}

.portal-v2-side-nav__copy {
  display: flex;
  align-items: center;
  min-width: 0;
}

.portal-v2-side-nav__copy strong {
  color: #173459;
  font-size: 13px;
  line-height: 1.2;
  white-space: nowrap;
}

.portal-v2-side-nav__status {
  color: #8a97ab;
  font-size: 10px;
  font-weight: 700;
  line-height: 1;
  white-space: nowrap;
  margin-left: 3px;
  align-self: center;
  justify-self: end;
}

.portal-v2-main-panel {
  display: grid;
  grid-template-rows: auto minmax(0, 1fr) auto;
  min-height: 100%;
  background: linear-gradient(180deg, #ffffff, #fbfdff);
}

.portal-v2-main-panel__header {
  display: grid;
  grid-template-columns: 136px minmax(0, 1fr);
  gap: 14px;
  align-items: center;
  padding: 12px 18px;
  border-bottom: 1px solid rgba(232, 237, 245, 0.96);
  background: linear-gradient(180deg, rgba(249, 252, 255, 0.98), rgba(244, 248, 253, 0.92));
}

.portal-v2-main-panel__step,
.portal-v2-main-panel__copy {
  display: grid;
  gap: 4px;
}

.portal-v2-main-panel__step {
  align-content: center;
  min-height: 58px;
  padding: 10px 14px;
  border-radius: 14px;
  background: linear-gradient(135deg, rgba(29, 108, 214, 0.06), rgba(88, 185, 255, 0.12));
  border: 1px solid rgba(197, 219, 245, 0.92);
}

.portal-v2-main-panel__step strong {
  color: #1a4477;
  font-size: 18px;
  line-height: 1.1;
}

.portal-v2-main-panel__copy h2 {
  margin: 0;
  color: #173459;
  font-size: 22px;
  line-height: 1.18;
}

.portal-v2-main-panel__copy p {
  margin: 0;
  color: #6c7f99;
  font-size: 12px;
  line-height: 1.55;
}

.portal-v2-embedded-wrap {
  min-height: 0;
  min-width: 0;
  padding: 14px 18px 16px;
}

.portal-v2-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 12px 18px 14px;
  border-top: 1px solid rgba(232, 237, 245, 0.96);
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.92), rgba(248, 251, 255, 0.96));
}

.portal-v2-actions__button {
  min-width: 96px;
  min-height: 38px;
  padding: 0 18px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
}

.portal-v2-actions__button:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.portal-v2-actions__button--ghost {
  border: 1px solid #d2ddec;
  background: #fff;
  color: #355a88;
}

.portal-v2-actions__button--save {
  border: 1px solid #d2ddec;
  background: linear-gradient(180deg, #edf4ff, #dceafe);
  color: #194b8b;
}

.portal-v2-actions__button--primary {
  border: none;
  background: linear-gradient(135deg, #1f73d8, #1b58b3);
  color: #fff;
}

.portal-v2-stage-card {
  margin-bottom: 18px;
  border-radius: 26px 26px 0 0;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.95), rgba(245, 249, 255, 0.92));
  box-shadow: 0 24px 58px rgba(18, 46, 102, 0.18);
  overflow: hidden;
}

.portal-v2-stage-card__header {
  padding: 22px 24px 14px;
  color: #0f2c58;
  font-size: 19px;
  font-weight: 800;
}

.portal-v2-stage-bar {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 10px;
  padding: 0 18px 18px;
}

.portal-v2-stage-card--hidden {
  display: none;
}

.portal-v2-stage {
  display: flex;
  align-items: center;
  gap: 10px;
  min-height: 54px;
  padding: 0 18px;
  border-radius: 999px;
  background: linear-gradient(180deg, #f5f8fd, #edf3fb);
  color: #7c8ca3;
  border: 1px solid rgba(170, 186, 216, 0.34);
}

.portal-v2-stage--active {
  background: linear-gradient(135deg, #1f73d8, #1b58b3);
  color: #fff;
  border-color: transparent;
  box-shadow: 0 14px 28px rgba(29, 94, 185, 0.24);
}

.portal-v2-stage__index {
  display: grid;
  place-items: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: rgba(12, 44, 88, 0.08);
  font-size: 12px;
  font-weight: 800;
}

.portal-v2-stage--active .portal-v2-stage__index {
  background: rgba(255, 255, 255, 0.18);
}

.portal-v2-stage__label {
  font-size: 14px;
  font-weight: 700;
}

.portal-v2-embedded {
  display: block;
}

.portal-v2-embedded :deep(.section-page),
.portal-v2-embedded :deep(.record-list) {
  gap: 12px;
}

.portal-v2-embedded :deep(.section-card),
.portal-v2-embedded :deep(.toolbar-card),
.portal-v2-embedded :deep(.record-card),
.portal-v2-embedded :deep(.empty-card),
.portal-v2-embedded :deep(.photo-card) {
  padding: 14px 16px;
  border-radius: 12px;
  background: #fff;
  border: 1px solid rgba(217, 226, 239, 0.96);
  box-shadow: none;
}

.portal-v2-embedded :deep(.photo-card) {
  grid-template-columns: 124px minmax(0, 1fr);
  gap: 16px;
}

.portal-v2-embedded :deep(.photo-card__preview) {
  width: 124px;
  height: 156px;
  border-radius: 10px;
}

.portal-v2-embedded :deep(.photo-card__content) {
  gap: 8px;
}

.portal-v2-embedded :deep(.photo-card__content strong) {
  font-size: 16px;
}

.portal-v2-embedded :deep(.photo-card__content p) {
  max-width: 460px;
  font-size: 12px;
  line-height: 1.5;
}

.portal-v2-embedded :deep(.section-grid),
.portal-v2-embedded :deep(.upload-grid) {
  gap: 12px;
}

.portal-v2-embedded :deep(.section-grid) {
  padding: 14px 16px;
  border-radius: 12px;
  background: #fff;
  border: 1px solid rgba(217, 226, 239, 0.96);
  box-shadow: none;
}

.portal-v2-embedded :deep(.section-grid label),
.portal-v2-embedded :deep(.upload-card),
.portal-v2-embedded :deep(.note-card) {
  gap: 6px;
}

.portal-v2-embedded :deep(.section-grid label),
.portal-v2-embedded :deep(.toolbar-card span),
.portal-v2-embedded :deep(.record-card__header span),
.portal-v2-embedded :deep(.upload-card small),
.portal-v2-embedded :deep(.empty-card),
.portal-v2-embedded :deep(.note-card span) {
  font-size: 11px;
}

.portal-v2-embedded :deep(.toolbar-card strong),
.portal-v2-embedded :deep(.record-card__header strong),
.portal-v2-embedded :deep(.note-card strong) {
  font-size: 15px;
}

.portal-v2-embedded :deep(.toolbar-card),
.portal-v2-embedded :deep(.record-card__header) {
  gap: 10px;
}

.portal-v2-embedded :deep(.toolbar-card > div),
.portal-v2-embedded :deep(.record-card__header > div) {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
  flex-wrap: wrap;
}

.portal-v2-embedded :deep(.toolbar-card > div > span),
.portal-v2-embedded :deep(.record-card__header > div > span) {
  display: inline-flex;
  align-items: center;
  line-height: 1.4;
}

.portal-v2-embedded :deep(.section-grid input),
.portal-v2-embedded :deep(.section-grid select),
.portal-v2-embedded :deep(.section-grid textarea),
.portal-v2-embedded :deep(.upload-card input),
.portal-v2-embedded :deep(.upload-box__input) {
  min-height: 38px;
  padding: 7px 10px;
  border-radius: 8px;
  border-color: #d7e1ee;
  font-size: 13px;
}

.portal-v2-embedded :deep(.section-grid textarea) {
  min-height: 88px;
}

.portal-v2-embedded :deep(.upload-card),
.portal-v2-embedded :deep(.note-card) {
  margin-top: 12px;
  padding: 12px 14px;
  border-radius: 12px;
  background: #fafcff;
}

.portal-v2-embedded :deep(.agreement-row),
.portal-v2-embedded :deep(.submit-row) {
  margin-top: 12px;
}

.portal-v2-embedded :deep(.action-button),
.portal-v2-embedded :deep(.submit-button) {
  min-height: 36px;
  padding: 0 16px;
  border-radius: 8px;
  font-size: 13px;
}

.portal-v2-embedded :deep(.link-button) {
  font-size: 12px;
}

.portal-v2-footer {
  position: relative;
  margin-top: 18px;
  min-height: 386px;
  overflow: hidden;
  background: linear-gradient(180deg, #0a5ca9 0%, #0d67b6 100%);
}

.portal-v2-footer__backdrop {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(180deg, rgba(8, 48, 115, 0.08), rgba(8, 48, 115, 0.34)),
    url('/images/bottom_backgound.png?v=20260429');
  background-repeat: no-repeat;
  background-position: center bottom;
  background-size: cover;
  opacity: 0.97;
}

.portal-v2-password-dialog {
  position: fixed;
  inset: 0;
  z-index: 60;
}

.portal-v2-password-dialog__mask {
  position: absolute;
  inset: 0;
  border: none;
  background: rgba(4, 22, 56, 0.46);
}

.portal-v2-password-dialog__panel {
  position: relative;
  z-index: 1;
  width: min(420px, calc(100% - 32px));
  margin: 12vh auto 0;
  padding: 22px;
  border-radius: 16px;
  background: #ffffff;
  box-shadow: 0 28px 64px rgba(8, 37, 86, 0.28);
}

.portal-v2-password-dialog__header {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: flex-start;
}

.portal-v2-password-dialog__header div {
  display: grid;
  gap: 6px;
}

.portal-v2-password-dialog__header strong {
  color: #173459;
  font-size: 20px;
}

.portal-v2-password-dialog__header span {
  color: #6f82a0;
  font-size: 12px;
}

.portal-v2-password-dialog__close {
  border: none;
  background: transparent;
  color: #5c7294;
  cursor: pointer;
}

.portal-v2-password-dialog__body {
  display: grid;
  gap: 14px;
  margin-top: 18px;
}

.portal-v2-password-dialog__body label {
  display: grid;
  gap: 6px;
  color: #4a607f;
  font-size: 13px;
}

.portal-v2-password-dialog__body input {
  width: 100%;
  min-height: 40px;
  padding: 8px 12px;
  border: 1px solid #d7e1ee;
  border-radius: 8px;
  background: #fff;
  color: #23344d;
}

.portal-v2-password-dialog__actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 18px;
}

.portal-v2-password-dialog__button {
  min-width: 96px;
  min-height: 38px;
  padding: 0 16px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
}

.portal-v2-password-dialog__button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.portal-v2-password-dialog__button--ghost {
  border: 1px solid #d2ddec;
  background: #fff;
  color: #355a88;
}

.portal-v2-password-dialog__button--primary {
  border: none;
  background: linear-gradient(135deg, #1f73d8, #1b58b3);
  color: #fff;
}

@media (max-width: 1280px) {
  .portal-v2-header__inner,
  .portal-v2-stage-wrap {
    width: min(1280px, calc(100% - 24px));
  }

  .portal-v2-stage-bar {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 1024px) {
  .portal-v2-header__inner {
    grid-template-columns: 1fr;
    justify-items: start;
    padding: 12px 0;
  }

  .portal-v2-nav {
    flex-wrap: wrap;
    justify-content: flex-start;
  }

  .portal-v2-stage-bar {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .portal-v2-workbench {
    grid-template-columns: 1fr;
    min-height: clamp(640px, calc(100vh - 190px), 860px);
  }

  .portal-v2-side-nav {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    border-right: none;
    border-bottom: 1px solid rgba(202, 214, 234, 0.72);
  }

  .portal-v2-side-nav__item {
    min-height: 58px;
  }
}

@media (max-width: 720px) {
  .portal-v2-stage-bar {
    grid-template-columns: 1fr;
  }

  .portal-v2-backdrop--top {
    height: 360px;
  }

  .portal-v2-side-nav {
    grid-template-columns: 1fr;
  }

  .portal-v2-main-panel__header {
    grid-template-columns: 1fr;
  }

  .portal-v2-embedded-wrap {
    padding: 12px;
  }

  .portal-v2-embedded :deep(.photo-card),
  .portal-v2-embedded :deep(.section-grid),
  .portal-v2-embedded :deep(.upload-grid) {
    grid-template-columns: 1fr;
  }

  .portal-v2-embedded :deep(.photo-card__preview) {
    width: 112px;
    height: 142px;
  }

  .portal-v2-workbench {
    min-height: auto;
  }

  .portal-v2-footer {
    min-height: 386px;
  }

  .portal-v2-brand__logo {
    height: 40px;
    max-width: min(100%, 300px);
  }

  .portal-v2-password-dialog__panel {
    margin-top: 10vh;
    padding: 18px;
  }
}
</style>
