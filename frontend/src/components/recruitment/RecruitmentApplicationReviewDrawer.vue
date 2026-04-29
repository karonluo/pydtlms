<script setup lang="ts">
import { Document, Download } from '@element-plus/icons-vue'
import { computed } from 'vue'
import { ElMessage } from 'element-plus'

import type { RecruitApplicationRecord } from '../../api/recruitment'
import type { WorkflowActionOption, WorkflowTaskRecord } from '../../api/workflow'

const props = withDefaults(defineProps<{
  modelValue: boolean
  application: RecruitApplicationRecord | null
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

const applicationDetailSections: Array<{ title: string; fields: Array<{ label: string; key: keyof RecruitApplicationRecord }> }> = [
  {
    title: '基础信息',
    fields: [
      { label: '业务编号', key: 'business_key' },
      { label: '轮次', key: 'review_round' },
      { label: '姓名', key: 'student_name' },
      { label: '性别', key: 'gender' },
      { label: '电话', key: 'phone_number' },
      { label: '邮箱', key: 'email' },
      { label: '第一志愿', key: 'first_choice' },
      { label: '第二志愿', key: 'second_choice' },
      { label: '意向导师', key: 'intended_advisor_name' },
      { label: '资料审核', key: 'material_status' },
      { label: '申请状态', key: 'application_status' },
      { label: '审核人', key: 'reviewer_name' },
    ],
  },
  {
    title: '身份与联系信息',
    fields: [
      { label: '政治面貌', key: 'political_status' },
      { label: '婚姻状况', key: 'marital_status' },
      { label: '宗教信仰', key: 'religious_belief' },
      { label: '籍贯', key: 'native_place' },
      { label: '证件类型', key: 'id_type' },
      { label: '证件号码', key: 'id_number' },
      { label: '通讯地址', key: 'mailing_address' },
      { label: '毕业院校', key: 'graduation_school' },
      { label: '最高学历', key: 'highest_degree' },
      { label: '研究方向', key: 'intended_field' },
      { label: '来源渠道', key: 'discovery_channel' },
      { label: '最终评分', key: 'final_score' },
    ],
  },
]

function displayDetailValue(value: unknown) {
  if (value === null || value === undefined || String(value).trim() === '') {
    return '未填写'
  }
  return String(value)
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
  <el-drawer v-model="visible" title="报名申请详情" size="760px" destroy-on-close>
    <template v-if="application">
      <section class="review-toolbar">
        <div class="review-toolbar__meta">
          <strong>{{ application.student_name || '未命名申请' }}</strong>
          <span>业务编号：{{ application.business_key || '未生成' }}</span>
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

      <section v-for="section in applicationDetailSections" :key="section.title" class="detail-section">
        <h3 class="dialog-section__title">{{ section.title }}</h3>
        <div class="detail-grid">
          <div v-for="field in section.fields" :key="field.key" class="detail-item">
            <span class="detail-item__label">{{ field.label }}</span>
            <span class="detail-item__value">{{ displayDetailValue(application[field.key]) }}</span>
          </div>
        </div>
      </section>

      <section class="detail-section">
        <h3 class="dialog-section__title">报名信息</h3>
        <div v-if="application.preferences?.length" class="detail-record-stack">
          <article v-for="(item, index) in application.preferences" :key="`detail-preference-${index}`" class="detail-record-card">
            <div class="detail-record-card__header">
              <strong>{{ index === 0 ? '第一志愿' : '第二志愿' }}</strong>
            </div>
            <div class="detail-grid">
              <div class="detail-item">
                <span class="detail-item__label">研究中心/方向</span>
                <span class="detail-item__value">{{ displayDetailValue(item.research_center_name) }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-item__label">意向导师</span>
                <span class="detail-item__value">{{ displayDetailValue(item.advisor_name) }}</span>
              </div>
            </div>
          </article>
        </div>
        <div v-else class="empty-inline">当前未填写报名志愿。</div>
      </section>

      <section class="detail-section">
        <h3 class="dialog-section__title">教育经历</h3>
        <div v-if="application.education_experiences?.length" class="detail-record-stack">
          <article v-for="(item, index) in application.education_experiences" :key="`detail-education-${index}`" class="detail-record-card">
            <div class="detail-record-card__header">
              <strong>教育经历 {{ index + 1 }}</strong>
            </div>
            <div class="detail-grid">
              <div class="detail-item"><span class="detail-item__label">教育阶段</span><span class="detail-item__value">{{ displayDetailValue(item.education_stage) }}</span></div>
              <div class="detail-item"><span class="detail-item__label">院校</span><span class="detail-item__value">{{ displayDetailValue(item.school_name) }}</span></div>
              <div class="detail-item"><span class="detail-item__label">专业</span><span class="detail-item__value">{{ displayDetailValue(item.major_name) }}</span></div>
              <div class="detail-item"><span class="detail-item__label">开始时间</span><span class="detail-item__value">{{ displayDetailValue(item.start_month) }}</span></div>
              <div class="detail-item"><span class="detail-item__label">结束时间</span><span class="detail-item__value">{{ displayDetailValue(item.end_month) }}</span></div>
              <div class="detail-item"><span class="detail-item__label">平均分</span><span class="detail-item__value">{{ displayDetailValue(item.average_score) }}</span></div>
              <div class="detail-item"><span class="detail-item__label">绩点</span><span class="detail-item__value">{{ displayDetailValue(item.gpa) }}</span></div>
              <div class="detail-item"><span class="detail-item__label">排名</span><span class="detail-item__value">{{ displayDetailValue(item.ranking) }}</span></div>
              <div class="detail-item"><span class="detail-item__label">证明人</span><span class="detail-item__value">{{ displayDetailValue(item.verifier_name) }}</span></div>
              <div class="detail-item"><span class="detail-item__label">证明人电话</span><span class="detail-item__value">{{ displayDetailValue(item.verifier_phone) }}</span></div>
              <div v-if="item.transcript_attachment_url" class="detail-item detail-item--full">
                <span class="detail-item__label">成绩单附件</span>
                <div class="detail-attachment-actions">
                  <a class="detail-attachment-link" :href="item.transcript_attachment_url" target="_blank" rel="noopener noreferrer">
                    <el-icon><Document /></el-icon>
                    <span>{{ resolveAttachmentDisplayName(item.transcript_attachment_url, item.transcript_attachment_name, '成绩单附件') }}</span>
                  </a>
                  <button type="button" class="detail-attachment-download" @click="triggerAttachmentDownload(item.transcript_attachment_url, resolveAttachmentDisplayName(item.transcript_attachment_url, item.transcript_attachment_name, '成绩单附件'))">
                    <el-icon><Download /></el-icon>
                    <span>下载</span>
                  </button>
                </div>
              </div>
              <div v-if="item.degree_certificate_attachment_url" class="detail-item detail-item--full">
                <span class="detail-item__label">学位证附件</span>
                <div class="detail-attachment-actions">
                  <a class="detail-attachment-link" :href="item.degree_certificate_attachment_url" target="_blank" rel="noopener noreferrer">
                    <el-icon><Document /></el-icon>
                    <span>{{ resolveAttachmentDisplayName(item.degree_certificate_attachment_url, item.degree_certificate_attachment_name, '学位证附件') }}</span>
                  </a>
                  <button type="button" class="detail-attachment-download" @click="triggerAttachmentDownload(item.degree_certificate_attachment_url, resolveAttachmentDisplayName(item.degree_certificate_attachment_url, item.degree_certificate_attachment_name, '学位证附件'))">
                    <el-icon><Download /></el-icon>
                    <span>下载</span>
                  </button>
                </div>
              </div>
            </div>
          </article>
        </div>
        <div v-else class="empty-inline">当前未填写教育经历。</div>
      </section>

      <section class="detail-section">
        <h3 class="dialog-section__title">实践经历</h3>
        <div v-if="application.practice_experiences?.length" class="detail-record-stack">
          <article v-for="(item, index) in application.practice_experiences" :key="`detail-practice-${index}`" class="detail-record-card">
            <div class="detail-record-card__header">
              <strong>实践经历 {{ index + 1 }}</strong>
            </div>
            <div class="detail-grid">
              <div class="detail-item"><span class="detail-item__label">单位名称</span><span class="detail-item__value">{{ displayDetailValue(item.organization_name) }}</span></div>
              <div class="detail-item"><span class="detail-item__label">岗位名称</span><span class="detail-item__value">{{ displayDetailValue(item.position_name) }}</span></div>
              <div class="detail-item"><span class="detail-item__label">开始时间</span><span class="detail-item__value">{{ displayDetailValue(item.start_month) }}</span></div>
              <div class="detail-item"><span class="detail-item__label">结束时间</span><span class="detail-item__value">{{ displayDetailValue(item.end_month) }}</span></div>
              <div class="detail-item"><span class="detail-item__label">证明人</span><span class="detail-item__value">{{ displayDetailValue(item.verifier_name) }}</span></div>
              <div class="detail-item"><span class="detail-item__label">证明人电话</span><span class="detail-item__value">{{ displayDetailValue(item.verifier_phone) }}</span></div>
              <div class="detail-item detail-item--full"><span class="detail-item__label">职责说明</span><span class="detail-item__value">{{ displayDetailValue(item.responsibility_text) }}</span></div>
            </div>
          </article>
        </div>
        <div v-else class="empty-inline">当前未填写实践经历。</div>
      </section>

      <section class="detail-section">
        <h3 class="dialog-section__title">家庭情况</h3>
        <div v-if="application.family_members?.length" class="detail-record-stack">
          <article v-for="(item, index) in application.family_members" :key="`detail-family-${index}`" class="detail-record-card">
            <div class="detail-record-card__header">
              <strong>家庭成员 {{ index + 1 }}</strong>
            </div>
            <div class="detail-grid">
              <div class="detail-item"><span class="detail-item__label">姓名</span><span class="detail-item__value">{{ displayDetailValue(item.member_name) }}</span></div>
              <div class="detail-item"><span class="detail-item__label">关系</span><span class="detail-item__value">{{ displayDetailValue(item.relation_type) }}</span></div>
              <div class="detail-item"><span class="detail-item__label">工作单位</span><span class="detail-item__value">{{ displayDetailValue(item.employer_name) }}</span></div>
              <div class="detail-item"><span class="detail-item__label">职务</span><span class="detail-item__value">{{ displayDetailValue(item.job_title) }}</span></div>
              <div class="detail-item detail-item--full"><span class="detail-item__label">联系电话</span><span class="detail-item__value">{{ displayDetailValue(item.contact_phone) }}</span></div>
            </div>
          </article>
        </div>
        <div v-else class="empty-inline">当前未填写家庭成员信息。</div>
      </section>

      <section class="detail-section">
        <h3 class="dialog-section__title">附件材料</h3>
        <div class="detail-text-list">
          <article v-if="application.personal_statement?.resume_attachment_url || application.personal_statement_attachment" class="detail-text-card">
            <h4>个人陈述附件</h4>
            <div class="detail-attachment-actions detail-attachment-actions--stacked">
              <a class="detail-attachment-link" :href="application.personal_statement?.resume_attachment_url || application.personal_statement_attachment || '#'" target="_blank" rel="noopener noreferrer">
                <el-icon><Document /></el-icon>
                <span>{{ resolveAttachmentDisplayName(application.personal_statement?.resume_attachment_url || application.personal_statement_attachment, application.personal_statement?.resume_attachment_name, '个人陈述附件') }}</span>
              </a>
              <button type="button" class="detail-attachment-download" @click="triggerAttachmentDownload(application.personal_statement?.resume_attachment_url || application.personal_statement_attachment, resolveAttachmentDisplayName(application.personal_statement?.resume_attachment_url || application.personal_statement_attachment, application.personal_statement?.resume_attachment_name, '个人陈述附件'))">
                <el-icon><Download /></el-icon>
                <span>下载</span>
              </button>
            </div>
          </article>
          <article v-if="application.material_list_attachment" class="detail-text-card">
            <h4>材料清单附件</h4>
            <div class="detail-attachment-actions detail-attachment-actions--stacked">
              <a class="detail-attachment-link" :href="application.material_list_attachment" target="_blank" rel="noopener noreferrer">
                <el-icon><Document /></el-icon>
                <span>{{ resolveAttachmentDisplayName(application.material_list_attachment, application.material_list_attachment_name, '材料清单附件') }}</span>
              </a>
              <button type="button" class="detail-attachment-download" @click="triggerAttachmentDownload(application.material_list_attachment, resolveAttachmentDisplayName(application.material_list_attachment, application.material_list_attachment_name, '材料清单附件'))">
                <el-icon><Download /></el-icon>
                <span>下载</span>
              </button>
            </div>
          </article>
        </div>
      </section>

      <section class="detail-section">
        <h3 class="dialog-section__title">个人陈述与补充说明</h3>
        <div class="detail-text-list">
          <article class="detail-text-card"><h4>本人自我评价</h4><p>{{ displayDetailValue(application.self_evaluation) }}</p></article>
          <article class="detail-text-card"><h4>个人陈述</h4><p>{{ displayDetailValue(application.personal_statement?.personal_statement_text) }}</p></article>
          <article class="detail-text-card"><h4>关键科研问题</h4><p>{{ displayDetailValue(application.personal_statement?.ai_problem_statement || application.research_problem) }}</p></article>
          <article class="detail-text-card"><h4>AI 行业不同观点</h4><p>{{ displayDetailValue(application.personal_statement?.ai_industry_opinion || application.dissenting_view) }}</p></article>
          <article class="detail-text-card"><h4>研究现状与局限</h4><p>{{ displayDetailValue(application.research_status_analysis) }}</p></article>
          <article class="detail-text-card"><h4>问题解决后的影响</h4><p>{{ displayDetailValue(application.research_impact) }}</p></article>
          <article class="detail-text-card"><h4>AI 对社会影响判断</h4><p>{{ displayDetailValue(application.ai_society_impact) }}</p></article>
          <article class="detail-text-card"><h4>学生活动经历</h4><p>{{ displayDetailValue(application.student_activity_experience) }}</p></article>
          <article class="detail-text-card"><h4>补充简介</h4><p>{{ displayDetailValue(application.supplementary_profile) }}</p></article>
          <article class="detail-text-card"><h4>声明确认</h4><p>{{ application.declaration?.has_read_declaration ? '已阅读并确认声明' : '未确认声明' }}</p></article>
          <article v-if="application.declaration?.declaration_text" class="detail-text-card"><h4>声明内容</h4><p>{{ displayDetailValue(application.declaration?.declaration_text) }}</p></article>
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
  margin-bottom: 18px;
}

.dialog-section__title {
  margin: 0 0 12px;
  color: #1c3f66;
  font-size: 16px;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
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

@media (max-width: 768px) {
  .review-toolbar {
    flex-direction: column;
  }

  .detail-grid {
    grid-template-columns: 1fr;
  }
}
</style>