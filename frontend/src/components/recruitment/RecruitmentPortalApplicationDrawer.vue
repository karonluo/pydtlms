<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, reactive, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'

import AttachmentPreviewActions from '../common/AttachmentPreviewActions.vue'
import type {
  AdvisorScreeningBatchSubmitRequest,
  InitialScreeningConfirmationRequest,
  RecruitPortalApplicationDetail,
} from '../../api/recruitment'
import type { WorkflowActionOption, WorkflowTaskRecord } from '../../api/workflow'

const props = withDefaults(defineProps<{
  modelValue: boolean
  detail: RecruitPortalApplicationDetail | null
  workflowTask?: WorkflowTaskRecord | null
  enableScreeningTools?: boolean
  hidePreferenceDetails?: boolean
  workflowTaskLoading?: boolean
  actionLoading?: boolean
}>(), {
  workflowTask: null,
  enableScreeningTools: false,
  hidePreferenceDetails: false,
  workflowTaskLoading: false,
  actionLoading: false,
})

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  executeAction: [action: WorkflowActionOption]
  submitAdvisorScreening: [payload: AdvisorScreeningBatchSubmitRequest]
  confirmInitialScreening: [payload: InitialScreeningConfirmationRequest]
}>()

const visible = computed({
  get: () => props.modelValue,
  set: (value: boolean) => emit('update:modelValue', value),
})

const backgroundAssessmentDialogVisible = ref(false)
const qualificationReviewHistoryDialogVisible = ref(false)
const advisorSignatureDialogVisible = ref(false)
const signatureCanvasRef = ref<HTMLCanvasElement | null>(null)
const signaturePadReady = ref(false)
const signatureDirty = ref(false)
const isSignatureDrawing = ref(false)
const ADVISOR_SCREENING_PASS_SCORE = 80

const advisorScreeningForm = reactive({
  advisor_score: undefined as number | undefined,
})

const initialScreeningForm = reactive({
  result: 'passed' as 'passed' | 'rejected',
  comment: '',
})

const declarationReminderText = '本表及证明材料仅作为申请上海人工智能实验室联培博士项目的参考依据，并承诺提交材料的所有内容均真实、准确、完整。所提供的材料中如有任何不实信息，将被取消录取资格。'

function displayDetailValue(value: unknown) {
  if (value === null || value === undefined || String(value).trim() === '') {
    return '未填写'
  }
  return String(value)
}

function hasDisplayValue(value: unknown) {
  return !(value === null || value === undefined || String(value).trim() === '')
}

const backgroundAssessmentRecords = computed(() => props.detail?.background_assessments ?? [])
const qualificationReviewHistoryRecords = computed(() => props.detail?.qualification_review_history ?? [])

const showQualificationReviewHistoryLink = computed(() => {
  if (qualificationReviewHistoryRecords.value.length > 0) {
    return true
  }
  return taskDefinitionKey.value === 'qualification_review' || String(props.workflowTask?.current_node || '').includes('资格审核')
})

const backgroundAssessmentSummary = computed(() => {
  let passed = 0
  let rejected = 0

  backgroundAssessmentRecords.value.forEach((item) => {
    const normalized = String(item.assessment_result || '').trim()
    if (['passed', 'pass', 'approved', '通过'].includes(normalized)) {
      passed += 1
      return
    }
    if (['rejected', 'reject', 'failed', '不通过'].includes(normalized)) {
      rejected += 1
    }
  })

  return {
    passed,
    rejected,
    total: backgroundAssessmentRecords.value.length,
  }
})

const showBackgroundAssessmentTools = computed(() => {
  const currentNode = String(props.workflowTask?.current_node || '').trim()
  const taskDefinitionKey = String(props.workflowTask?.task_definition_key || '').trim()
  return taskDefinitionKey === 'background_assessment' || currentNode.includes('背景评估') || backgroundAssessmentSummary.value.total > 0
})

const taskDefinitionKey = computed(() => String(props.workflowTask?.task_definition_key || '').trim())

const showAdvisorScreeningTools = computed(() => {
  return props.enableScreeningTools && (taskDefinitionKey.value === 'advisor_screening' || String(props.workflowTask?.current_node || '').includes('导师初筛'))
})

const showInitialScreeningConfirmationTools = computed(() => {
  return props.enableScreeningTools && (taskDefinitionKey.value === 'initial_screening_confirmation' || String(props.workflowTask?.current_node || '').includes('初筛确认'))
})

const hasCustomWorkflowTools = computed(() => showAdvisorScreeningTools.value || showInitialScreeningConfirmationTools.value)

const currentScreeningScore = computed(() => {
  if (!props.detail) {
    return null
  }
  if (String(props.detail.advisor_screening_round || '').trim() === 'second_choice') {
    return props.detail.second_choice_screening_score ?? null
  }
  return props.detail.first_choice_screening_score ?? null
})

const currentScreeningRoundLabel = computed(() => {
  return String(props.detail?.advisor_screening_round || '').trim() === 'second_choice' ? '第二志愿' : '第一志愿'
})

const currentScreeningSubmittedAt = computed(() => {
  return props.detail?.advisor_screening_submitted_at ?? null
})

const currentAdvisorSignaturePreview = computed(() => {
  const rawSignature = String(props.detail?.advisor_signature_base64 || '').trim()
  if (!rawSignature) {
    return ''
  }
  if (rawSignature.startsWith('data:')) {
    return rawSignature
  }
  return `data:image/png;base64,${rawSignature}`
})

const currentAdvisorScreeningAutoResult = computed(() => {
  if (advisorScreeningForm.advisor_score === undefined || advisorScreeningForm.advisor_score === null || Number.isNaN(Number(advisorScreeningForm.advisor_score))) {
    return '待判定'
  }
  return Number(advisorScreeningForm.advisor_score) >= ADVISOR_SCREENING_PASS_SCORE ? '自动通过' : '自动不通过'
})

const rejectionStatusValues = new Set(['驳回重填', '报名终止', '不录取'])
const defaultRejectionActionLabels = new Set(['审核不通过', '评估不通过', '初筛确认不通过', '取消申请', '终止流程', '不录取', '导师初筛自动不通过'])

const rejectionReviewComment = computed(() => {
  const status = String(props.detail?.application_status || '').trim()
  const taskStatus = String(props.workflowTask?.status || '').trim()
  if (!rejectionStatusValues.has(status) && taskStatus !== '已驳回') {
    return ''
  }
  const comment = String(props.workflowTask?.latest_comment || '').trim()
  if (!comment || defaultRejectionActionLabels.has(comment)) {
    return ''
  }
  return comment
})

function openBackgroundAssessmentDialog() {
  backgroundAssessmentDialogVisible.value = true
}

function openQualificationReviewHistoryDialog() {
  qualificationReviewHistoryDialogVisible.value = true
}

function resetCustomWorkflowForms() {
  advisorScreeningForm.advisor_score = undefined
  initialScreeningForm.result = 'passed'
  initialScreeningForm.comment = ''
  advisorSignatureDialogVisible.value = false
  signatureDirty.value = false
  signaturePadReady.value = false
}

function initializeSignatureCanvas() {
  const canvas = signatureCanvasRef.value
  if (!canvas) {
    return
  }
  const bounds = canvas.getBoundingClientRect()
  const scale = Math.max(window.devicePixelRatio || 1, 1)
  canvas.width = Math.floor(bounds.width * scale)
  canvas.height = Math.floor(bounds.height * scale)
  const context = canvas.getContext('2d')
  if (!context) {
    return
  }
  context.scale(scale, scale)
  context.fillStyle = '#ffffff'
  context.fillRect(0, 0, bounds.width, bounds.height)
  context.lineWidth = 2
  context.lineCap = 'round'
  context.lineJoin = 'round'
  context.strokeStyle = '#173557'
  signaturePadReady.value = true
  signatureDirty.value = false
}

function resolveCanvasPoint(event: PointerEvent) {
  const canvas = signatureCanvasRef.value
  if (!canvas) {
    return { x: 0, y: 0 }
  }
  const bounds = canvas.getBoundingClientRect()
  return {
    x: event.clientX - bounds.left,
    y: event.clientY - bounds.top,
  }
}

function startSignatureDrawing(event: PointerEvent) {
  const canvas = signatureCanvasRef.value
  const context = canvas?.getContext('2d')
  if (!canvas || !context) {
    return
  }
  const point = resolveCanvasPoint(event)
  isSignatureDrawing.value = true
  canvas.setPointerCapture(event.pointerId)
  context.beginPath()
  context.moveTo(point.x, point.y)
}

function moveSignatureDrawing(event: PointerEvent) {
  if (!isSignatureDrawing.value) {
    return
  }
  const canvas = signatureCanvasRef.value
  const context = canvas?.getContext('2d')
  if (!canvas || !context) {
    return
  }
  const point = resolveCanvasPoint(event)
  context.lineTo(point.x, point.y)
  context.stroke()
  signatureDirty.value = true
}

function stopSignatureDrawing(event?: PointerEvent) {
  if (!isSignatureDrawing.value) {
    return
  }
  const canvas = signatureCanvasRef.value
  if (canvas && event) {
    canvas.releasePointerCapture(event.pointerId)
  }
  isSignatureDrawing.value = false
}

function clearSignatureCanvas() {
  initializeSignatureCanvas()
}

function openAdvisorSignatureDialog() {
  if (!props.detail?.application_id) {
    ElMessage.warning('未找到申请记录，无法提交导师初筛')
    return
  }
  if (advisorScreeningForm.advisor_score === undefined || advisorScreeningForm.advisor_score === null || Number.isNaN(Number(advisorScreeningForm.advisor_score))) {
    ElMessage.warning('请先填写导师初筛分数')
    return
  }
  const score = Number(advisorScreeningForm.advisor_score)
  if (score < 0 || score > 100) {
    ElMessage.warning('导师初筛分数必须在 0 到 100 之间')
    return
  }
  advisorSignatureDialogVisible.value = true
}

function submitAdvisorScreening() {
  if (!props.detail?.application_id) {
    ElMessage.warning('未找到申请记录，无法提交导师初筛')
    return
  }
  if (!signatureDirty.value) {
    ElMessage.warning('请先完成手写签名')
    return
  }
  const canvas = signatureCanvasRef.value
  if (!canvas) {
    ElMessage.warning('签名画板尚未准备完成，请重试')
    return
  }
  emit('submitAdvisorScreening', {
    signature_base64: canvas.toDataURL('image/png'),
    items: [
      {
        application_id: props.detail.application_id,
        advisor_score: Number(advisorScreeningForm.advisor_score),
      },
    ],
  })
}

function submitInitialScreeningConfirmation() {
  emit('confirmInitialScreening', {
    result: initialScreeningForm.result,
    comment: initialScreeningForm.comment.trim() || undefined,
  })
}

function isHighSchoolEducation(stage: string | null | undefined) {
  return String(stage || '').trim() === '高中毕业'
}

function isGraduationStage(stage: string | null | undefined) {
  return String(stage || '').trim().endsWith('毕业')
}

function isPaperAchievement(type: string | null | undefined) {
  return String(type || '').trim() === '论文发表'
}

function isAwardAchievement(type: string | null | undefined) {
  return String(type || '').trim() === '获奖经历'
}

watch(advisorSignatureDialogVisible, async (visible) => {
  if (!visible) {
    stopSignatureDrawing()
    return
  }
  await nextTick()
  initializeSignatureCanvas()
})

watch(() => props.detail?.application_id, () => {
  resetCustomWorkflowForms()
})

watch(() => props.workflowTask?.task_definition_key, () => {
  resetCustomWorkflowForms()
})

onBeforeUnmount(() => {
  stopSignatureDrawing()
})
</script>

<template>
  <el-drawer v-model="visible" title="学生填报内容" size="840px" destroy-on-close>
    <template v-if="detail">
      <section class="review-toolbar">
        <div class="review-toolbar__meta">
          <strong>{{ detail.student_name || '未命名申请' }}</strong>
          <span>业务编号：{{ detail.business_key || '未生成' }}</span>
          <span>报名号：{{ detail.candidate_no || '未生成' }}</span>
          <span>提交时间：{{ detail.submitted_at || '未提交' }}</span>
          <span v-if="workflowTask" class="review-toolbar__node-line">
            <span>当前节点：{{ workflowTask.current_node }} / {{ workflowTask.status }}</span>
            <button v-if="showQualificationReviewHistoryLink" type="button" class="review-toolbar__detail-link" @click="openQualificationReviewHistoryDialog">
              审核历史
            </button>
          </span>
        </div>
        <div class="review-toolbar__actions">
          <el-skeleton v-if="workflowTaskLoading" :rows="1" animated />
          <template v-else>
            <span v-if="showBackgroundAssessmentTools" class="review-toolbar__assessment-counts">
              已完成评估 {{ backgroundAssessmentSummary.total }} 人
            </span>
            <button v-if="showBackgroundAssessmentTools" type="button" class="review-toolbar__detail-link" @click="openBackgroundAssessmentDialog">
              详情
            </button>
            <template v-if="workflowTask?.available_actions?.length">
              <el-button
                v-for="action in workflowTask.available_actions"
                :key="action.action"
                :type="action.action.includes('reject') ? 'danger' : 'primary'"
                :loading="actionLoading"
                @click="emit('executeAction', action)"
              >
                {{ action.label }}
              </el-button>
            </template>
            <span v-else-if="!hasCustomWorkflowTools" class="review-toolbar__empty">当前无可执行审批动作</span>
          </template>
        </div>
      </section>

      <section v-if="rejectionReviewComment" class="review-rejection-comment">
        <strong>未通过原因</strong>
        <p>{{ rejectionReviewComment }}</p>
      </section>

      <section v-if="showAdvisorScreeningTools || showInitialScreeningConfirmationTools" class="detail-section">
        <h3 class="dialog-section__title">初筛操作</h3>

        <div v-if="showAdvisorScreeningTools" class="screening-panel">
          <div class="screening-panel__summary">
            <div class="detail-item">
              <span class="detail-item__label">当前初筛轮次</span>
              <span class="detail-item__value">{{ currentScreeningRoundLabel }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-item__label">当前流程状态</span>
              <span class="detail-item__value">{{ displayDetailValue(detail.application_status) }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-item__label">历史初筛分数</span>
              <span class="detail-item__value">{{ currentScreeningScore ?? '未提交' }}</span>
            </div>
          </div>
          <div class="screening-panel__form">
            <el-form label-position="top">
              <el-form-item label="导师初筛分数">
                <el-input-number v-model="advisorScreeningForm.advisor_score" :min="0" :max="100" :precision="2" :step="1" style="width: 100%" />
              </el-form-item>
              <el-form-item label="自动结论">
                <el-tag :type="currentAdvisorScreeningAutoResult === '自动通过' ? 'success' : currentAdvisorScreeningAutoResult === '自动不通过' ? 'danger' : 'info'">
                  {{ currentAdvisorScreeningAutoResult }}
                </el-tag>
                <div>80 分以下自动判定为不通过，80 分及以上自动判定为通过。</div>
              </el-form-item>
            </el-form>
            <div class="screening-panel__actions">
              <el-button type="primary" :loading="actionLoading" @click="openAdvisorSignatureDialog">签名并提交导师初筛</el-button>
            </div>
          </div>
        </div>

        <div v-if="showInitialScreeningConfirmationTools" class="screening-panel">
          <div class="screening-panel__summary">
            <div class="detail-item">
              <span class="detail-item__label">导师初筛状态</span>
              <span class="detail-item__value">{{ displayDetailValue(detail.advisor_screening_status) }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-item__label">初筛环节</span>
              <span class="detail-item__value">{{ currentScreeningRoundLabel }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-item__label">导师初筛分数</span>
              <span class="detail-item__value">{{ currentScreeningScore ?? '未填写' }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-item__label">导师提交时间</span>
              <span class="detail-item__value">{{ displayDetailValue(currentScreeningSubmittedAt) }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-item__label">建议下一阶段</span>
              <span class="detail-item__value">{{ displayDetailValue(detail.next_stage_name || '入营面试') }}</span>
            </div>
          </div>
          <div class="screening-panel__form">
            <div class="screening-signature-panel">
              <span class="detail-item__label">导师手写签名</span>
              <div v-if="currentAdvisorSignaturePreview" class="screening-signature-panel__preview">
                <img :src="currentAdvisorSignaturePreview" alt="导师手写签名" class="screening-signature-panel__image" />
              </div>
              <div v-else class="screening-signature-panel__empty">当前未查询到导师手写签名</div>
            </div>
            <el-form label-position="top">
              <el-form-item label="初筛确认结果">
                <el-radio-group v-model="initialScreeningForm.result">
                  <el-radio value="passed">通过</el-radio>
                  <el-radio value="rejected">不通过</el-radio>
                </el-radio-group>
              </el-form-item>
              <el-form-item label="确认意见">
                <el-input v-model="initialScreeningForm.comment" type="textarea" :rows="4" maxlength="500" show-word-limit placeholder="请输入初筛确认意见，可选" />
              </el-form-item>
            </el-form>
            <div class="screening-panel__actions">
              <el-button type="primary" :loading="actionLoading" @click="submitInitialScreeningConfirmation">提交初筛确认</el-button>
            </div>
          </div>
        </div>
      </section>

      <el-dialog v-model="backgroundAssessmentDialogVisible" title="背景评估完成情况" width="720px" append-to-body>
        <div class="assessment-summary">
          <div class="assessment-summary__card">
            <span class="assessment-summary__label">已完成评估</span>
            <strong class="assessment-summary__value">{{ backgroundAssessmentSummary.total }} 人</strong>
          </div>
        </div>
        <el-table v-if="backgroundAssessmentRecords.length" :data="backgroundAssessmentRecords" border>
          <el-table-column prop="evaluator_name" label="评估人" min-width="120">
            <template #default="scope">
              {{ displayDetailValue(scope.row.evaluator_name || scope.row.evaluator_username) }}
            </template>
          </el-table-column>
          <el-table-column prop="evaluator_username" label="评估人账号" min-width="160">
            <template #default="scope">
              {{ displayDetailValue(scope.row.evaluator_username) }}
            </template>
          </el-table-column>
          <el-table-column prop="assessment_comment" label="评估意见" min-width="220">
            <template #default="scope">
              {{ displayDetailValue(scope.row.assessment_comment) }}
            </template>
          </el-table-column>
          <el-table-column prop="assessed_at" label="评估时间" min-width="180">
            <template #default="scope">
              {{ displayDetailValue(scope.row.assessed_at) }}
            </template>
          </el-table-column>
        </el-table>
        <el-empty v-else description="当前暂无书院管理员评估记录" />
      </el-dialog>

      <el-dialog v-model="qualificationReviewHistoryDialogVisible" title="资格审核历史" width="760px" append-to-body>
        <el-table v-if="qualificationReviewHistoryRecords.length" :data="qualificationReviewHistoryRecords" border>
          <el-table-column prop="reviewer_name" label="审核人" min-width="140">
            <template #default="scope">
              {{ displayDetailValue(scope.row.reviewer_name || scope.row.reviewer_username) }}
            </template>
          </el-table-column>
          <el-table-column prop="reviewed_at" label="审核日期时间" min-width="180">
            <template #default="scope">
              {{ displayDetailValue(scope.row.reviewed_at) }}
            </template>
          </el-table-column>
          <el-table-column prop="action_label" label="操作动作" min-width="120">
            <template #default="scope">
              {{ displayDetailValue(scope.row.action_label) }}
            </template>
          </el-table-column>
          <el-table-column prop="review_comment" label="历史意见" min-width="240">
            <template #default="scope">
              {{ displayDetailValue(scope.row.review_comment) }}
            </template>
          </el-table-column>
        </el-table>
        <el-empty v-else description="当前暂无资格审核历史记录" />
      </el-dialog>

      <el-dialog v-model="advisorSignatureDialogVisible" title="导师签名确认" width="680px" append-to-body>
        <div class="signature-dialog">
          <p class="signature-dialog__hint">请在下方画板完成手写签名。签名完成后，当前导师初筛分数将立即提交，系统按 80 分阈值自动判定结果且不可重复修改。</p>
          <div class="signature-dialog__meta">
            <span>分数：{{ advisorScreeningForm.advisor_score ?? '未填写' }}</span>
            <span>结果：{{ currentAdvisorScreeningAutoResult }}</span>
            <span>轮次：{{ currentScreeningRoundLabel }}</span>
          </div>
          <canvas
            ref="signatureCanvasRef"
            class="signature-dialog__canvas"
            @pointerdown="startSignatureDrawing"
            @pointermove="moveSignatureDrawing"
            @pointerup="stopSignatureDrawing"
            @pointerleave="stopSignatureDrawing"
          />
          <div class="signature-dialog__actions">
            <el-button @click="clearSignatureCanvas">清空签名</el-button>
          </div>
        </div>
        <template #footer>
          <el-button @click="advisorSignatureDialogVisible = false">取消</el-button>
          <el-button type="primary" :loading="actionLoading" @click="submitAdvisorScreening">确认提交</el-button>
        </template>
      </el-dialog>

      <section class="detail-section">
        <h3 class="dialog-section__title">基本信息</h3>
        <div v-if="detail.personal_statement?.resume_attachment_url" class="detail-text-list section-spacing-top">
          <article class="detail-text-card">
            <h4>简历附件</h4>
            <AttachmentPreviewActions
              :url="detail.personal_statement.resume_attachment_url"
              :file-name="detail.personal_statement.resume_attachment_name"
              fallback-label="简历附件"
              preview-title="简历附件预览"
              stacked
            />
          </article>
        </div>
        <div class="detail-media-grid section-spacing-top">
          <div v-if="detail.profile?.profile_photo_url" class="detail-media-card">
            <span class="detail-item__label">个人照片</span>
            <AttachmentPreviewActions
              :url="detail.profile.profile_photo_url"
              fallback-label="个人照片"
              preview-title="个人照片预览"
              image-alt="个人照片"
              :inline-image="true"
              stacked
            />
          </div>
          <div v-if="detail.profile?.id_card_collage_url" class="detail-media-card">
            <span class="detail-item__label">身份证拼图</span>
            <AttachmentPreviewActions
              :url="detail.profile.id_card_collage_url"
              fallback-label="身份证拼图"
              preview-title="身份证拼图预览"
              image-alt="身份证拼图"
              :inline-image="true"
              stacked
            />
          </div>
        </div>
        <div class="detail-grid section-spacing-top">
          <div class="detail-item"><span class="detail-item__label">姓名</span><span class="detail-item__value">{{ displayDetailValue(detail.student_name) }}</span></div>
          <div class="detail-item"><span class="detail-item__label">姓名拼音</span><span class="detail-item__value">{{ displayDetailValue(detail.profile?.full_name_pinyin) }}</span></div>
          <div class="detail-item"><span class="detail-item__label">性别</span><span class="detail-item__value">{{ displayDetailValue(detail.profile?.gender) }}</span></div>
          <div class="detail-item"><span class="detail-item__label">民族</span><span class="detail-item__value">{{ displayDetailValue(detail.profile?.ethnic_group) }}</span></div>
          <div class="detail-item"><span class="detail-item__label">政治面貌</span><span class="detail-item__value">{{ displayDetailValue(detail.profile?.political_status) }}</span></div>
          <div class="detail-item"><span class="detail-item__label">籍贯</span><span class="detail-item__value">{{ displayDetailValue(detail.profile?.native_place) }}</span></div>
          <div class="detail-item"><span class="detail-item__label">证件类型</span><span class="detail-item__value">{{ displayDetailValue(detail.profile?.id_type) }}</span></div>
          <div class="detail-item"><span class="detail-item__label">证件号码</span><span class="detail-item__value">{{ displayDetailValue(detail.id_number) }}</span></div>
          <div class="detail-item"><span class="detail-item__label">邮箱</span><span class="detail-item__value">{{ displayDetailValue(detail.email) }}</span></div>
          <div class="detail-item"><span class="detail-item__label">手机号码</span><span class="detail-item__value">{{ displayDetailValue(detail.phone_number) }}</span></div>
          <div class="detail-item detail-item--full"><span class="detail-item__label">通讯地址</span><span class="detail-item__value">{{ displayDetailValue(detail.profile?.mailing_address) }}</span></div>
          <div class="detail-item"><span class="detail-item__label">紧急联系人姓名</span><span class="detail-item__value">{{ displayDetailValue(detail.profile?.emergency_contact_name) }}</span></div>
          <div class="detail-item"><span class="detail-item__label">紧急联系人手机</span><span class="detail-item__value">{{ displayDetailValue(detail.profile?.emergency_contact_phone) }}</span></div>
        </div>
      </section>

      <section class="detail-section">
        <h3 class="dialog-section__title">报名信息</h3>
        <div v-if="hidePreferenceDetails" class="empty-inline section-spacing-top">当前场景仅供查看学生填报内容，志愿与导师指向信息已隐藏。</div>
        <div v-else-if="detail.preferences?.length" class="detail-record-stack section-spacing-top">
          <article v-for="(item, index) in detail.preferences" :key="`detail-preference-${index}`" class="detail-record-card">
            <div class="detail-record-card__header detail-record-card__header--with-meta">
              <div>
                <strong>{{ index === 0 ? '第一志愿' : '第二志愿' }}</strong>
                <span>{{ index === 0 ? '必填' : '选填' }}</span>
              </div>
            </div>
            <div class="detail-grid">
              <div class="detail-item"><span class="detail-item__label">意向导师</span><span class="detail-item__value">{{ displayDetailValue(item.advisor_name) }}</span></div>
            </div>
          </article>
        </div>
        <div v-else class="empty-inline">当前未填写报名志愿。</div>

        <div class="detail-subsection section-spacing-top">
          <div class="detail-subsection__title">了解项目方式</div>
          <div class="detail-grid detail-grid--single">
            <div class="detail-item"><span class="detail-item__label">获知渠道</span><span class="detail-item__value">{{ displayDetailValue(detail.source_channel) }}</span></div>
            <div v-if="hasDisplayValue(detail.source_channel_other)" class="detail-item"><span class="detail-item__label">其他说明</span><span class="detail-item__value">{{ displayDetailValue(detail.source_channel_other) }}</span></div>
          </div>
        </div>
      </section>

      <section class="detail-section">
        <h3 class="dialog-section__title">教育经历</h3>
        <div v-if="detail.education_experiences?.length" class="detail-record-stack">
          <article v-for="(item, index) in detail.education_experiences" :key="`detail-education-${index}`" class="detail-record-card">
            <div class="detail-record-card__header"><strong>教育经历 {{ index + 1 }}</strong></div>
            <div class="detail-grid">
              <div class="detail-item"><span class="detail-item__label">教育阶段</span><span class="detail-item__value">{{ displayDetailValue(item.education_stage) }}</span></div>
              <div class="detail-item"><span class="detail-item__label">开始年月</span><span class="detail-item__value">{{ displayDetailValue(item.start_month) }}</span></div>
              <div class="detail-item"><span class="detail-item__label">结束年月</span><span class="detail-item__value">{{ displayDetailValue(item.end_month) }}</span></div>
              <div class="detail-item"><span class="detail-item__label">就读学校</span><span class="detail-item__value">{{ displayDetailValue(item.school_name) }}</span></div>
              <div v-if="!isHighSchoolEducation(item.education_stage)" class="detail-item"><span class="detail-item__label">就读专业</span><span class="detail-item__value">{{ displayDetailValue(item.major_name) }}</span></div>
              <div v-if="!isHighSchoolEducation(item.education_stage)" class="detail-item"><span class="detail-item__label">期间平均成绩</span><span class="detail-item__value">{{ displayDetailValue(item.average_score) }}</span></div>
              <div v-if="!isHighSchoolEducation(item.education_stage)" class="detail-item"><span class="detail-item__label">期间绩点</span><span class="detail-item__value">{{ displayDetailValue(item.gpa) }}</span></div>
              <div v-if="!isHighSchoolEducation(item.education_stage)" class="detail-item"><span class="detail-item__label">成绩排名</span><span class="detail-item__value">{{ displayDetailValue(item.ranking) }}</span></div>
              <div class="detail-item"><span class="detail-item__label">证明人姓名</span><span class="detail-item__value">{{ displayDetailValue(item.verifier_name) }}</span></div>
              <div class="detail-item"><span class="detail-item__label">证明人手机</span><span class="detail-item__value">{{ displayDetailValue(item.verifier_phone) }}</span></div>
              <div v-if="!isHighSchoolEducation(item.education_stage) && item.transcript_attachment_url" class="detail-item detail-item--full">
                <span class="detail-item__label">成绩单附件</span>
                <AttachmentPreviewActions :url="item.transcript_attachment_url" :file-name="item.transcript_attachment_name" fallback-label="成绩单附件" preview-title="成绩单附件预览" />
              </div>
              <div v-if="!isHighSchoolEducation(item.education_stage) && isGraduationStage(item.education_stage) && item.degree_certificate_attachment_url" class="detail-item detail-item--full">
                <span class="detail-item__label">学位证附件</span>
                <AttachmentPreviewActions :url="item.degree_certificate_attachment_url" :file-name="item.degree_certificate_attachment_name" fallback-label="学位证附件" preview-title="学位证附件预览" />
              </div>
              <div v-if="!isHighSchoolEducation(item.education_stage) && isGraduationStage(item.education_stage) && item.graduation_certificate_attachment_url" class="detail-item detail-item--full">
                <span class="detail-item__label">毕业证附件</span>
                <AttachmentPreviewActions :url="item.graduation_certificate_attachment_url" :file-name="item.graduation_certificate_attachment_name" fallback-label="毕业证附件" preview-title="毕业证附件预览" />
              </div>
            </div>
          </article>
        </div>
        <div v-else class="empty-inline">当前未填写教育经历。</div>
      </section>

      <section class="detail-section">
        <h3 class="dialog-section__title">实践经历</h3>
        <div v-if="detail.practice_experiences?.length" class="detail-record-stack">
          <article v-for="(item, index) in detail.practice_experiences" :key="`detail-practice-${index}`" class="detail-record-card">
            <div class="detail-record-card__header"><strong>实践经历 {{ index + 1 }}</strong></div>
            <div class="detail-grid">
              <div class="detail-item"><span class="detail-item__label">开始年月</span><span class="detail-item__value">{{ displayDetailValue(item.start_month) }}</span></div>
              <div class="detail-item"><span class="detail-item__label">结束年月</span><span class="detail-item__value">{{ displayDetailValue(item.end_month) }}</span></div>
              <div class="detail-item"><span class="detail-item__label">实习实践/工作单位</span><span class="detail-item__value">{{ displayDetailValue(item.organization_name) }}</span></div>
              <div class="detail-item"><span class="detail-item__label">岗位</span><span class="detail-item__value">{{ displayDetailValue(item.position_name) }}</span></div>
              <div class="detail-item"><span class="detail-item__label">证明人姓名</span><span class="detail-item__value">{{ displayDetailValue(item.verifier_name) }}</span></div>
              <div class="detail-item"><span class="detail-item__label">证明人手机</span><span class="detail-item__value">{{ displayDetailValue(item.verifier_phone) }}</span></div>
              <div class="detail-item detail-item--full"><span class="detail-item__label">职责</span><span class="detail-item__value">{{ displayDetailValue(item.responsibility_text) }}</span></div>
            </div>
          </article>
        </div>
        <div v-else class="empty-inline">当前未填写实践经历。</div>
      </section>

      <section class="detail-section">
        <h3 class="dialog-section__title">英语能力</h3>
        <div v-if="detail.english_proficiencies?.length" class="detail-record-stack">
          <article v-for="(item, index) in detail.english_proficiencies" :key="`detail-english-${index}`" class="detail-record-card">
            <div class="detail-record-card__header"><strong>英语能力 {{ index + 1 }}</strong></div>
            <div class="detail-grid">
              <div class="detail-item"><span class="detail-item__label">英语考试名称</span><span class="detail-item__value">{{ displayDetailValue(item.exam_name) }}</span></div>
              <div class="detail-item"><span class="detail-item__label">成绩</span><span class="detail-item__value">{{ displayDetailValue(item.score_text) }}</span></div>
              <div v-if="item.certificate_attachment_url" class="detail-item detail-item--full">
                <span class="detail-item__label">英语证明附件</span>
                <AttachmentPreviewActions :url="item.certificate_attachment_url" :file-name="item.certificate_attachment_name" fallback-label="英语证明附件" preview-title="英语证明附件预览" />
              </div>
            </div>
          </article>
        </div>
        <div v-else class="empty-inline">当前未填写英语能力。</div>
      </section>

      <section class="detail-section">
        <h3 class="dialog-section__title">家庭情况</h3>
        <div v-if="detail.family_members?.length" class="detail-record-stack">
          <article v-for="(item, index) in detail.family_members" :key="`detail-family-${index}`" class="detail-record-card">
            <div class="detail-record-card__header"><strong>家庭成员 {{ index + 1 }}</strong></div>
            <div class="detail-grid">
              <div class="detail-item"><span class="detail-item__label">与本人关系</span><span class="detail-item__value">{{ displayDetailValue(item.relation_type) }}</span></div>
              <div class="detail-item"><span class="detail-item__label">姓名</span><span class="detail-item__value">{{ displayDetailValue(item.member_name) }}</span></div>
              <div class="detail-item"><span class="detail-item__label">联系电话</span><span class="detail-item__value">{{ displayDetailValue(item.contact_phone) }}</span></div>
              <div class="detail-item"><span class="detail-item__label">工作单位</span><span class="detail-item__value">{{ displayDetailValue(item.employer_name) }}</span></div>
              <div class="detail-item"><span class="detail-item__label">职务</span><span class="detail-item__value">{{ displayDetailValue(item.job_title) }}</span></div>
            </div>
          </article>
        </div>
        <div v-else class="empty-inline">当前未填写家庭成员信息。</div>
      </section>

      <section class="detail-section">
        <h3 class="dialog-section__title">成果经历</h3>
        <div v-if="detail.achievement_records?.length" class="detail-record-stack">
          <article v-for="(item, index) in detail.achievement_records" :key="`detail-achievement-${index}`" class="detail-record-card">
            <div class="detail-record-card__header"><strong>成果经历 {{ index + 1 }}</strong></div>
            <div class="detail-grid">
              <div class="detail-item"><span class="detail-item__label">类型</span><span class="detail-item__value">{{ displayDetailValue(item.achievement_type) }}</span></div>
              <div v-if="hasDisplayValue(item.achievement_month)" class="detail-item"><span class="detail-item__label">日期</span><span class="detail-item__value">{{ displayDetailValue(item.achievement_month) }}</span></div>
              <div v-if="isPaperAchievement(item.achievement_type) && hasDisplayValue(item.paper_title)" class="detail-item"><span class="detail-item__label">论文名称</span><span class="detail-item__value">{{ displayDetailValue(item.paper_title) }}</span></div>
              <div v-if="isPaperAchievement(item.achievement_type) && hasDisplayValue(item.author_order)" class="detail-item"><span class="detail-item__label">作者序位</span><span class="detail-item__value">{{ displayDetailValue(item.author_order) }}</span></div>
              <div v-if="isPaperAchievement(item.achievement_type) && hasDisplayValue(item.journal_or_conference)" class="detail-item detail-item--full"><span class="detail-item__label">期刊名称</span><span class="detail-item__value">{{ displayDetailValue(item.journal_or_conference) }}</span></div>
              <div v-if="isPaperAchievement(item.achievement_type) && hasDisplayValue(item.description_text)" class="detail-item detail-item--full"><span class="detail-item__label">描述</span><span class="detail-item__value">{{ displayDetailValue(item.description_text) }}</span></div>
              <div v-if="isAwardAchievement(item.achievement_type) && hasDisplayValue(item.award_name)" class="detail-item"><span class="detail-item__label">奖项名称</span><span class="detail-item__value">{{ displayDetailValue(item.award_name) }}</span></div>
              <div v-if="isAwardAchievement(item.achievement_type) && hasDisplayValue(item.award_rank)" class="detail-item"><span class="detail-item__label">获奖名次</span><span class="detail-item__value">{{ displayDetailValue(item.award_rank) }}</span></div>
              <div v-if="isAwardAchievement(item.achievement_type) && item.award_certificate_attachment_url" class="detail-item detail-item--full">
                <span class="detail-item__label">获奖证明上传</span>
                <AttachmentPreviewActions :url="item.award_certificate_attachment_url" :file-name="item.award_certificate_attachment_name" fallback-label="获奖证明" preview-title="获奖证明预览" />
              </div>
              <div v-if="isAwardAchievement(item.achievement_type) && hasDisplayValue(item.description_text)" class="detail-item detail-item--full"><span class="detail-item__label">描述</span><span class="detail-item__value">{{ displayDetailValue(item.description_text) }}</span></div>
            </div>
          </article>
        </div>
        <div v-else class="empty-inline">当前未填写成果经历。</div>
      </section>

      <section class="detail-section">
        <h3 class="dialog-section__title">个人陈述</h3>
        <div class="detail-text-list">
          <article class="detail-text-card"><h4>个人陈述</h4><p>{{ displayDetailValue(detail.personal_statement?.personal_statement_text) }}</p></article>
          <article class="detail-text-card"><h4>你认为目前 AI 技术发展过程中还未被解决的，且你未来希望去作为科研目标解决的最重要问题是什么？</h4><p>{{ displayDetailValue(detail.personal_statement?.ai_problem_statement) }}</p></article>
          <article class="detail-text-card"><h4>AI 行业不同观点</h4><p>{{ displayDetailValue(detail.personal_statement?.ai_industry_opinion) }}</p></article>
          <article v-if="detail.personal_statement?.supporting_material_attachment_url" class="detail-text-card">
            <h4>补充材料附件</h4>
            <AttachmentPreviewActions
              :url="detail.personal_statement.supporting_material_attachment_url"
              :file-name="detail.personal_statement.supporting_material_attachment_name"
              fallback-label="补充材料附件"
              preview-title="补充材料附件预览"
              stacked
            />
          </article>
        </div>
      </section>

      <section class="detail-section">
        <h3 class="dialog-section__title">提交声明</h3>
        <div class="detail-text-list">
          <article class="detail-text-card"><h4>声明确认</h4><p>{{ detail.declaration?.has_read_declaration ? '已阅读并确认声明' : '未确认声明' }}</p></article>
          <article class="detail-text-card"><h4>声明内容</h4><p>{{ declarationReminderText }}</p></article>
        </div>
      </section>
    </template>
  </el-drawer>
</template>

<style scoped>
.review-toolbar {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: flex-start;
  min-width: 0;
  margin-bottom: 12px;
  padding: 12px 14px;
  border-radius: 14px;
  background: linear-gradient(135deg, rgba(20, 78, 145, 0.08), rgba(17, 132, 107, 0.08));
}

.review-toolbar__meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
  color: #24415f;
}

.review-toolbar__meta strong {
  font-size: 16px;
  color: #173557;
  overflow-wrap: anywhere;
}

.review-toolbar__node-line {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.review-toolbar__actions {
  display: flex;
  gap: 10px;
  align-items: center;
  justify-content: flex-end;
  flex-wrap: wrap;
  min-width: 0;
}

.review-toolbar__empty {
  color: #6b7f93;
  font-size: 13px;
}

.review-toolbar__assessment-counts {
  color: #24415f;
  font-size: 13px;
  font-weight: 600;
  line-height: 1.5;
  white-space: normal;
  overflow-wrap: anywhere;
}

.review-toolbar__detail-link {
  border: none;
  background: transparent;
  color: #1d5fbf;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
  padding: 0 2px;
  text-decoration: underline;
  text-underline-offset: 3px;
}

.review-toolbar__detail-link:hover {
  color: #173f80;
}

.review-rejection-comment {
  margin-bottom: 12px;
  padding: 12px 14px;
  border: 1px solid #f0b4b4;
  border-radius: 14px;
  background: #fff5f5;
  color: #9a2f2f;
}

.review-rejection-comment strong {
  display: block;
  margin-bottom: 6px;
  font-size: 14px;
}

.review-rejection-comment p {
  margin: 0;
  line-height: 1.7;
  white-space: pre-wrap;
}

.assessment-summary {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 12px;
  margin-bottom: 16px;
}

.assessment-summary__card {
  padding: 14px 16px;
  border: 1px solid rgba(28, 63, 102, 0.12);
  border-radius: 14px;
  background: linear-gradient(180deg, rgba(246, 249, 253, 0.92), rgba(255, 255, 255, 0.98));
}

.assessment-summary__label {
  display: block;
  color: #6b7f93;
  font-size: 13px;
  margin-bottom: 6px;
}

.assessment-summary__value {
  color: #173557;
  font-size: 20px;
}

.screening-panel {
  display: grid;
  gap: 14px;
}

.screening-panel + .screening-panel {
  margin-top: 18px;
  padding-top: 18px;
  border-top: 1px dashed rgba(28, 63, 102, 0.18);
}

.screening-panel__summary {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

.screening-panel__form {
  border: 1px dashed rgba(23, 89, 141, 0.2);
  border-radius: 16px;
  padding: 14px;
  background: rgba(255, 255, 255, 0.96);
}

.screening-panel__actions {
  display: flex;
  justify-content: flex-end;
}

.screening-signature-panel {
  display: grid;
  gap: 10px;
}

.screening-signature-panel__preview {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 180px;
  padding: 12px;
  border: 1px dashed rgba(23, 89, 141, 0.28);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.96);
}

.screening-signature-panel__image {
  display: block;
  max-width: 100%;
  max-height: 220px;
  object-fit: contain;
}

.screening-signature-panel__empty {
  padding: 14px;
  border: 1px dashed rgba(23, 89, 141, 0.2);
  border-radius: 16px;
  color: #6d8094;
  background: rgba(255, 255, 255, 0.82);
}

.signature-dialog {
  display: grid;
  gap: 12px;
}

.signature-dialog__hint {
  margin: 0;
  color: #48617c;
  line-height: 1.7;
}

.signature-dialog__meta {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  color: #173557;
  font-size: 13px;
  font-weight: 600;
}

.signature-dialog__canvas {
  width: 100%;
  height: 240px;
  border: 1px dashed rgba(23, 89, 141, 0.36);
  border-radius: 16px;
  background: #ffffff;
  touch-action: none;
}

.signature-dialog__actions {
  display: flex;
  justify-content: flex-end;
}

.detail-section {
  margin-bottom: 14px;
  padding: 14px;
  border: 1px solid rgba(18, 50, 95, 0.08);
  border-radius: 16px;
  background: linear-gradient(180deg, rgba(246, 249, 253, 0.92), rgba(255, 255, 255, 0.98));
  box-shadow: 0 8px 24px rgba(15, 45, 88, 0.05);
}

.dialog-section__title {
  margin: 0 0 10px;
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(28, 63, 102, 0.1);
  color: #1c3f66;
  font-size: 16px;
}

.detail-media-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
  margin-bottom: 10px;
}

.detail-media-card {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
  padding: 6px;
  border: 1px dashed rgba(23, 89, 141, 0.24);
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.95);
}

.detail-media-card > .detail-item__label {
  flex: 0 0 auto;
  line-height: 1.2;
}

.detail-item :deep(.attachment-preview-block) {
  flex: 1 1 auto;
  min-width: 0;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px;
}

.detail-grid--single {
  grid-template-columns: 1fr;
}

.detail-item,
.detail-record-card,
.detail-text-card {
  border: 1px solid rgba(18, 50, 95, 0.08);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.94);
}

.detail-item {
  display: flex;
  align-items: baseline;
  gap: 8px;
  min-width: 0;
  padding: 5px 8px;
}

.detail-item--full {
  grid-column: 1 / -1;
}

.detail-item__label {
  flex: 0 0 88px;
  color: #6d8094;
  font-size: 11px;
  line-height: 1.25;
  white-space: nowrap;
}

.detail-item__value {
  flex: 1 1 auto;
  min-width: 0;
  color: #18324f;
  font-size: 12px;
  line-height: 1.25;
  word-break: break-word;
}

.detail-record-stack,
.detail-text-list {
  display: grid;
  gap: 8px;
}

.detail-record-card,
.detail-text-card {
  padding: 8px;
}

.detail-record-card__header {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
  min-width: 0;
  margin-bottom: 6px;
  color: #1b3e64;
  font-size: 12px;
}

.detail-record-card__header strong {
  overflow-wrap: anywhere;
}

.detail-record-card__header--with-meta > div {
  display: grid;
  gap: 4px;
  min-width: 0;
}

.detail-record-card__header--with-meta span {
  color: #6b7f93;
  font-size: 11px;
  overflow-wrap: anywhere;
}

.detail-subsection {
  display: grid;
  gap: 10px;
}

.detail-subsection__title {
  color: #1b3e64;
  font-size: 14px;
  font-weight: 700;
}

.detail-text-card h4 {
  margin: 0 0 6px;
  color: #173557;
}

.detail-text-card p {
  margin: 0;
  color: #24415f;
  font-size: 12px;
  line-height: 1.32;
  white-space: pre-wrap;
}

.detail-attachment-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  min-width: 0;
}

.detail-attachment-actions--stacked {
  align-items: flex-start;
  flex-direction: column;
}

.detail-attachment-link,
.detail-attachment-download {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  max-width: 100%;
  color: #17598d;
}

.detail-attachment-link span,
.detail-attachment-download span {
  overflow-wrap: anywhere;
  word-break: break-word;
}

.detail-attachment-link {
  text-decoration: none;
}

.detail-attachment-download {
  border: none;
  background: transparent;
  cursor: pointer;
  padding: 0;
}

.empty-inline {
  color: #70839a;
  font-size: 13px;
}

.section-spacing-top {
  margin-top: 10px;
}

@media (max-width: 768px) {
  .review-toolbar {
    flex-direction: column;
  }

  .assessment-summary {
    grid-template-columns: 1fr;
  }

  .screening-panel__summary,
  .detail-media-grid,
  .detail-grid {
    grid-template-columns: 1fr;
  }

  .detail-attachment-link,
  .detail-attachment-download {
    width: 100%;
    justify-content: flex-start;
  }

  .detail-item {
    align-items: flex-start;
  }

  .detail-item__label {
    flex-basis: 76px;
  }
}
</style>