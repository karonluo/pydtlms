<script setup lang="ts">
import { Document, Download } from '@element-plus/icons-vue'
import { computed } from 'vue'
import { ElMessage } from 'element-plus'

import type { RecruitPortalApplicationDetail } from '../../api/recruitment'
import type { WorkflowActionOption, WorkflowTaskRecord } from '../../api/workflow'

const props = withDefaults(defineProps<{
  modelValue: boolean
  detail: RecruitPortalApplicationDetail | null
  workflowTask?: WorkflowTaskRecord | null
  workflowTaskLoading?: boolean
  actionLoading?: boolean
}>(), {
  workflowTask: null,
  workflowTaskLoading: false,
  actionLoading: false,
})

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  executeAction: [action: WorkflowActionOption]
}>()

const visible = computed({
  get: () => props.modelValue,
  set: (value: boolean) => emit('update:modelValue', value),
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

function resolveAttachmentDisplayName(url: string | null | undefined, fileName: string | null | undefined, fallbackLabel: string) {
  const preferred = String(fileName || '').trim()
  if (preferred) {
    return preferred
  }
  const normalized = String(url || '').trim()
  if (!normalized) {
    return fallbackLabel
  }
  const lastSegment = normalized.split('/').pop() || ''
  return decodeURIComponent(lastSegment) || fallbackLabel
}

async function triggerAttachmentDownload(url: string | null | undefined, fileName: string) {
  if (!url) {
    ElMessage.warning('附件地址不存在')
    return
  }
  try {
    const response = await fetch(url)
    if (!response.ok) {
      throw new Error('download failed')
    }
    const blob = await response.blob()
    const objectUrl = window.URL.createObjectURL(blob)
    const anchor = document.createElement('a')
    anchor.href = objectUrl
    anchor.download = fileName
    document.body.appendChild(anchor)
    anchor.click()
    document.body.removeChild(anchor)
    window.URL.revokeObjectURL(objectUrl)
  } catch {
    ElMessage.error('附件下载失败')
  }
}
</script>

<template>
  <el-drawer v-model="visible" title="学生填报内容" size="880px" destroy-on-close>
    <template v-if="detail">
      <section class="review-toolbar">
        <div class="review-toolbar__meta">
          <strong>{{ detail.student_name || '未命名申请' }}</strong>
          <span>业务编号：{{ detail.business_key || '未生成' }}</span>
          <span>报名号：{{ detail.candidate_no || '未生成' }}</span>
          <span>提交时间：{{ detail.submitted_at || '未提交' }}</span>
          <span v-if="workflowTask">当前节点：{{ workflowTask.current_node }} / {{ workflowTask.status }}</span>
        </div>
        <div class="review-toolbar__actions">
          <el-skeleton v-if="workflowTaskLoading" :rows="1" animated />
          <template v-else-if="workflowTask?.available_actions?.length">
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
          <span v-else class="review-toolbar__empty">当前无可执行审批动作</span>
        </div>
      </section>

      <section class="detail-section">
        <h3 class="dialog-section__title">基本信息</h3>
        <div class="detail-media-grid">
          <div v-if="detail.profile?.profile_photo_url" class="detail-media-card">
            <span class="detail-item__label">个人照片</span>
            <div class="detail-attachment-actions detail-attachment-actions--stacked">
              <a class="detail-attachment-link" :href="detail.profile.profile_photo_url" target="_blank" rel="noopener noreferrer">
                <el-icon><Document /></el-icon>
                <span>{{ resolveAttachmentDisplayName(detail.profile.profile_photo_url, null, '个人照片') }}</span>
              </a>
              <button type="button" class="detail-attachment-download" @click="triggerAttachmentDownload(detail.profile.profile_photo_url, resolveAttachmentDisplayName(detail.profile.profile_photo_url, null, '个人照片'))">
                <el-icon><Download /></el-icon>
                <span>下载</span>
              </button>
            </div>
          </div>
          <div v-if="detail.profile?.id_card_collage_url" class="detail-media-card">
            <span class="detail-item__label">身份证拼图</span>
            <div class="detail-attachment-actions detail-attachment-actions--stacked">
              <a class="detail-attachment-link" :href="detail.profile.id_card_collage_url" target="_blank" rel="noopener noreferrer">
                <el-icon><Document /></el-icon>
                <span>{{ resolveAttachmentDisplayName(detail.profile.id_card_collage_url, null, '身份证拼图') }}</span>
              </a>
              <button type="button" class="detail-attachment-download" @click="triggerAttachmentDownload(detail.profile.id_card_collage_url, resolveAttachmentDisplayName(detail.profile.id_card_collage_url, null, '身份证拼图'))">
                <el-icon><Download /></el-icon>
                <span>下载</span>
              </button>
            </div>
          </div>
        </div>
        <div class="detail-grid">
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
        <div v-if="detail.preferences?.length" class="detail-record-stack section-spacing-top">
          <article v-for="(item, index) in detail.preferences" :key="`detail-preference-${index}`" class="detail-record-card">
            <div class="detail-record-card__header detail-record-card__header--with-meta">
              <div>
                <strong>{{ index === 0 ? '第一志愿' : '第二志愿' }}</strong>
                <span>{{ index === 0 ? '必填' : '选填' }}</span>
              </div>
            </div>
            <div class="detail-grid">
              <div class="detail-item"><span class="detail-item__label">研究领域</span><span class="detail-item__value">{{ displayDetailValue(item.research_center_name) }}</span></div>
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
                <div class="detail-attachment-actions">
                  <a class="detail-attachment-link" :href="item.transcript_attachment_url" target="_blank" rel="noopener noreferrer"><el-icon><Document /></el-icon><span>{{ resolveAttachmentDisplayName(item.transcript_attachment_url, item.transcript_attachment_name, '成绩单附件') }}</span></a>
                  <button type="button" class="detail-attachment-download" @click="triggerAttachmentDownload(item.transcript_attachment_url, resolveAttachmentDisplayName(item.transcript_attachment_url, item.transcript_attachment_name, '成绩单附件'))"><el-icon><Download /></el-icon><span>下载</span></button>
                </div>
              </div>
              <div v-if="!isHighSchoolEducation(item.education_stage) && isGraduationStage(item.education_stage) && item.degree_certificate_attachment_url" class="detail-item detail-item--full">
                <span class="detail-item__label">学位证附件</span>
                <div class="detail-attachment-actions">
                  <a class="detail-attachment-link" :href="item.degree_certificate_attachment_url" target="_blank" rel="noopener noreferrer"><el-icon><Document /></el-icon><span>{{ resolveAttachmentDisplayName(item.degree_certificate_attachment_url, item.degree_certificate_attachment_name, '学位证附件') }}</span></a>
                  <button type="button" class="detail-attachment-download" @click="triggerAttachmentDownload(item.degree_certificate_attachment_url, resolveAttachmentDisplayName(item.degree_certificate_attachment_url, item.degree_certificate_attachment_name, '学位证附件'))"><el-icon><Download /></el-icon><span>下载</span></button>
                </div>
              </div>
              <div v-if="!isHighSchoolEducation(item.education_stage) && isGraduationStage(item.education_stage) && item.graduation_certificate_attachment_url" class="detail-item detail-item--full">
                <span class="detail-item__label">毕业证附件</span>
                <div class="detail-attachment-actions">
                  <a class="detail-attachment-link" :href="item.graduation_certificate_attachment_url" target="_blank" rel="noopener noreferrer"><el-icon><Document /></el-icon><span>{{ resolveAttachmentDisplayName(item.graduation_certificate_attachment_url, item.graduation_certificate_attachment_name, '毕业证附件') }}</span></a>
                  <button type="button" class="detail-attachment-download" @click="triggerAttachmentDownload(item.graduation_certificate_attachment_url, resolveAttachmentDisplayName(item.graduation_certificate_attachment_url, item.graduation_certificate_attachment_name, '毕业证附件'))"><el-icon><Download /></el-icon><span>下载</span></button>
                </div>
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
                <div class="detail-attachment-actions">
                  <a class="detail-attachment-link" :href="item.certificate_attachment_url" target="_blank" rel="noopener noreferrer"><el-icon><Document /></el-icon><span>{{ resolveAttachmentDisplayName(item.certificate_attachment_url, item.certificate_attachment_name, '英语证明附件') }}</span></a>
                  <button type="button" class="detail-attachment-download" @click="triggerAttachmentDownload(item.certificate_attachment_url, resolveAttachmentDisplayName(item.certificate_attachment_url, item.certificate_attachment_name, '英语证明附件'))"><el-icon><Download /></el-icon><span>下载</span></button>
                </div>
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
                <div class="detail-attachment-actions">
                  <a class="detail-attachment-link" :href="item.award_certificate_attachment_url" target="_blank" rel="noopener noreferrer"><el-icon><Document /></el-icon><span>{{ resolveAttachmentDisplayName(item.award_certificate_attachment_url, item.award_certificate_attachment_name, '获奖证明') }}</span></a>
                  <button type="button" class="detail-attachment-download" @click="triggerAttachmentDownload(item.award_certificate_attachment_url, resolveAttachmentDisplayName(item.award_certificate_attachment_url, item.award_certificate_attachment_name, '获奖证明'))"><el-icon><Download /></el-icon><span>下载</span></button>
                </div>
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
          <article v-if="detail.personal_statement?.resume_attachment_url" class="detail-text-card">
            <h4>简历附件</h4>
            <div class="detail-attachment-actions detail-attachment-actions--stacked">
              <a class="detail-attachment-link" :href="detail.personal_statement.resume_attachment_url" target="_blank" rel="noopener noreferrer"><el-icon><Document /></el-icon><span>{{ resolveAttachmentDisplayName(detail.personal_statement.resume_attachment_url, detail.personal_statement.resume_attachment_name, '简历附件') }}</span></a>
              <button type="button" class="detail-attachment-download" @click="triggerAttachmentDownload(detail.personal_statement.resume_attachment_url, resolveAttachmentDisplayName(detail.personal_statement.resume_attachment_url, detail.personal_statement.resume_attachment_name, '简历附件'))"><el-icon><Download /></el-icon><span>下载</span></button>
            </div>
          </article>
          <article v-if="detail.personal_statement?.supporting_material_attachment_url" class="detail-text-card">
            <h4>补充材料附件</h4>
            <div class="detail-attachment-actions detail-attachment-actions--stacked">
              <a class="detail-attachment-link" :href="detail.personal_statement.supporting_material_attachment_url" target="_blank" rel="noopener noreferrer"><el-icon><Document /></el-icon><span>{{ resolveAttachmentDisplayName(detail.personal_statement.supporting_material_attachment_url, detail.personal_statement.supporting_material_attachment_name, '补充材料附件') }}</span></a>
              <button type="button" class="detail-attachment-download" @click="triggerAttachmentDownload(detail.personal_statement.supporting_material_attachment_url, resolveAttachmentDisplayName(detail.personal_statement.supporting_material_attachment_url, detail.personal_statement.supporting_material_attachment_name, '补充材料附件'))"><el-icon><Download /></el-icon><span>下载</span></button>
            </div>
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
  gap: 16px;
  align-items: flex-start;
  margin-bottom: 16px;
  padding: 14px 16px;
  border-radius: 16px;
  background: linear-gradient(135deg, rgba(20, 78, 145, 0.08), rgba(17, 132, 107, 0.08));
}

.review-toolbar__meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
  color: #24415f;
}

.review-toolbar__meta strong {
  font-size: 16px;
  color: #173557;
}

.review-toolbar__actions {
  display: flex;
  gap: 10px;
  align-items: center;
  justify-content: flex-end;
  flex-wrap: wrap;
}

.review-toolbar__empty {
  color: #6b7f93;
  font-size: 13px;
}

.detail-section {
  margin-bottom: 20px;
  padding: 18px;
  border: 1px solid rgba(18, 50, 95, 0.08);
  border-radius: 20px;
  background: linear-gradient(180deg, rgba(246, 249, 253, 0.92), rgba(255, 255, 255, 0.98));
  box-shadow: 0 8px 24px rgba(15, 45, 88, 0.05);
}

.dialog-section__title {
  margin: 0 0 14px;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(28, 63, 102, 0.1);
  color: #1c3f66;
  font-size: 16px;
}

.detail-media-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  margin-bottom: 12px;
}

.detail-media-card {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 14px;
  border: 1px dashed rgba(23, 89, 141, 0.24);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.95);
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
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
  flex-direction: column;
  gap: 6px;
  padding: 12px 14px;
}

.detail-item--full {
  grid-column: 1 / -1;
}

.detail-item__label {
  color: #6d8094;
  font-size: 12px;
}

.detail-item__value {
  color: #18324f;
  line-height: 1.6;
  word-break: break-word;
}

.detail-record-stack,
.detail-text-list {
  display: grid;
  gap: 12px;
}

.detail-record-card,
.detail-text-card {
  padding: 14px;
}

.detail-record-card__header {
  margin-bottom: 10px;
  color: #1b3e64;
}

.detail-record-card__header--with-meta > div {
  display: grid;
  gap: 4px;
}

.detail-record-card__header--with-meta span {
  color: #6b7f93;
  font-size: 12px;
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
  margin: 0 0 8px;
  color: #173557;
}

.detail-text-card p {
  margin: 0;
  color: #24415f;
  line-height: 1.7;
  white-space: pre-wrap;
}

.detail-attachment-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
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
  color: #17598d;
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
  margin-top: 12px;
}

@media (max-width: 768px) {
  .review-toolbar {
    flex-direction: column;
  }

  .detail-media-grid,
  .detail-grid {
    grid-template-columns: 1fr;
  }
}
</style>