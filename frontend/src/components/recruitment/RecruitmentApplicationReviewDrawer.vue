<script setup lang="ts">
import { computed } from 'vue'

import AttachmentPreviewActions from '../common/AttachmentPreviewActions.vue'
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
      { label: '报名号', key: 'candidate_no' },
      { label: '姓名', key: 'student_name' },
      { label: '提交时间', key: 'applied_at' },
      { label: '资料审核', key: 'material_status' },
      { label: '申请状态', key: 'application_status' },
      { label: '审核人', key: 'reviewer_name' },
      { label: '最终评分', key: 'final_score' },
    ],
  },
  {
    title: '报名概览',
    fields: [
      { label: '毕业院校', key: 'graduation_school' },
      { label: '最高学历', key: 'highest_degree' },
      { label: '研究方向', key: 'intended_field' },
      { label: '意向导师', key: 'intended_advisor_name' },
      { label: '是否接受调剂', key: 'accept_adjustment' },
      { label: '来源渠道', key: 'source_channel' },
      { label: '来源渠道补充', key: 'source_channel_other' },
    ],
  },
]

const ROLE_DISPLAY_NAME_MAP: Record<string, string> = {
  platform_admin: '平台管理员',
  advisor: '导师',
  AILABMGT: '书院管理员',
  academy_admin: '书院管理员',
  secretary: '学位秘书',
}

function hasDisplayValue(value: unknown) {
  return !(value === null || value === undefined || String(value).trim() === '')
}

function displayDetailValue(value: unknown) {
  if (value === null || value === undefined || String(value).trim() === '') {
    return '未填写'
  }
  return String(value)
}

function displayRoleName(roleCode: unknown) {
  const normalized = String(roleCode || '').trim()
  if (!normalized) {
    return '未填写'
  }
  return ROLE_DISPLAY_NAME_MAP[normalized] || normalized
}

function backgroundAssessmentTagType(result: string | null | undefined) {
  return String(result || '').trim() === '通过' ? 'success' : 'danger'
}

</script>

<template>
  <el-drawer v-model="visible" title="报名申请详情" size="720px" destroy-on-close>
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
        <h3 class="dialog-section__title">背景评估</h3>
        <div v-if="application.background_assessments?.length" class="detail-record-stack">
          <article v-for="(item, index) in application.background_assessments" :key="`detail-background-assessment-${index}`" class="detail-record-card">
            <div class="detail-record-card__header">
              <strong>{{ item.evaluator_name || item.evaluator_username || `评估记录 ${index + 1}` }}</strong>
            </div>
            <div class="detail-grid">
              <div class="detail-item">
                <span class="detail-item__label">评估人账号</span>
                <span class="detail-item__value">{{ displayDetailValue(item.evaluator_username) }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-item__label">角色</span>
                <span class="detail-item__value">{{ displayRoleName(item.evaluator_role_code) }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-item__label">评估结果</span>
                <span class="detail-item__value"><el-tag :type="backgroundAssessmentTagType(item.assessment_result)" round>{{ displayDetailValue(item.assessment_result) }}</el-tag></span>
              </div>
              <div class="detail-item">
                <span class="detail-item__label">评估时间</span>
                <span class="detail-item__value">{{ displayDetailValue(item.assessed_at) }}</span>
              </div>
              <div class="detail-item detail-item--full">
                <span class="detail-item__label">评估意见</span>
                <span class="detail-item__value">{{ displayDetailValue(item.assessment_comment) }}</span>
              </div>
            </div>
          </article>
        </div>
        <div v-else class="empty-inline">当前还没有背景评估记录。</div>
      </section>

      <section class="detail-section">
        <h3 class="dialog-section__title">身份与联系信息</h3>
        <div v-if="application.personal_statement?.resume_attachment_url || application.personal_statement_attachment" class="detail-text-list section-spacing-top">
          <article class="detail-text-card">
            <h4>个人简历附件</h4>
            <AttachmentPreviewActions
              :url="application.personal_statement?.resume_attachment_url || application.personal_statement_attachment"
              :file-name="application.personal_statement?.resume_attachment_name"
              fallback-label="个人简历附件"
              preview-title="个人简历附件预览"
              stacked
            />
          </article>
        </div>
        <div class="detail-text-list section-spacing-top">
          <article v-if="application.profile?.profile_photo_url" class="detail-text-card">
            <h4>证件照</h4>
            <AttachmentPreviewActions
              :url="application.profile.profile_photo_url"
              fallback-label="证件照"
              preview-title="证件照预览"
              image-alt="证件照"
              :inline-image="true"
              stacked
            />
          </article>
          <article v-if="application.profile?.id_card_collage_url" class="detail-text-card">
            <h4>身份证拼图</h4>
            <AttachmentPreviewActions
              :url="application.profile.id_card_collage_url"
              fallback-label="身份证拼图"
              preview-title="身份证拼图预览"
              image-alt="身份证拼图"
              :inline-image="true"
              stacked
            />
          </article>
        </div>
        <div class="detail-grid section-spacing-top">
          <div class="detail-item"><span class="detail-item__label">姓名拼音</span><span class="detail-item__value">{{ displayDetailValue(application.profile?.full_name_pinyin) }}</span></div>
          <div class="detail-item"><span class="detail-item__label">性别</span><span class="detail-item__value">{{ displayDetailValue(application.profile?.gender || application.gender) }}</span></div>
          <div class="detail-item"><span class="detail-item__label">出生日期</span><span class="detail-item__value">{{ displayDetailValue(application.profile?.birth_date) }}</span></div>
          <div class="detail-item"><span class="detail-item__label">民族</span><span class="detail-item__value">{{ displayDetailValue(application.profile?.ethnic_group) }}</span></div>
          <div class="detail-item"><span class="detail-item__label">政治面貌</span><span class="detail-item__value">{{ displayDetailValue(application.profile?.political_status || application.political_status) }}</span></div>
          <div class="detail-item"><span class="detail-item__label">婚姻状况</span><span class="detail-item__value">{{ displayDetailValue(application.profile?.marital_status || application.marital_status) }}</span></div>
          <div class="detail-item"><span class="detail-item__label">宗教信仰</span><span class="detail-item__value">{{ displayDetailValue(application.profile?.religious_belief || application.religious_belief) }}</span></div>
          <div class="detail-item"><span class="detail-item__label">籍贯</span><span class="detail-item__value">{{ displayDetailValue(application.profile?.native_place || application.native_place) }}</span></div>
          <div class="detail-item"><span class="detail-item__label">联系电话</span><span class="detail-item__value">{{ displayDetailValue(application.phone_number) }}</span></div>
          <div class="detail-item"><span class="detail-item__label">邮箱</span><span class="detail-item__value">{{ displayDetailValue(application.email) }}</span></div>
          <div class="detail-item"><span class="detail-item__label">证件类型</span><span class="detail-item__value">{{ displayDetailValue(application.profile?.id_type || application.id_type) }}</span></div>
          <div class="detail-item"><span class="detail-item__label">证件号码</span><span class="detail-item__value">{{ displayDetailValue(application.id_number) }}</span></div>
          <div class="detail-item detail-item--full"><span class="detail-item__label">通讯地址</span><span class="detail-item__value">{{ displayDetailValue(application.profile?.mailing_address || application.mailing_address) }}</span></div>
          <div class="detail-item"><span class="detail-item__label">紧急联系人</span><span class="detail-item__value">{{ displayDetailValue(application.profile?.emergency_contact_name) }}</span></div>
          <div class="detail-item"><span class="detail-item__label">紧急联系人电话</span><span class="detail-item__value">{{ displayDetailValue(application.profile?.emergency_contact_phone) }}</span></div>
        </div>
      </section>

      <section class="detail-section">
        <h3 class="dialog-section__title">报名信息</h3>
        <div v-if="hasDisplayValue(application.first_choice) || hasDisplayValue(application.second_choice)" class="detail-record-stack">
          <article class="detail-record-card">
            <div class="detail-record-card__header">
              <strong>第一志愿</strong>
            </div>
            <div class="detail-grid">
              <div class="detail-item">
                <span class="detail-item__label">意向导师</span>
                <span class="detail-item__value">{{ displayDetailValue(application.first_choice) }}</span>
              </div>
            </div>
          </article>
          <article v-if="hasDisplayValue(application.second_choice)" class="detail-record-card">
            <div class="detail-record-card__header">
              <strong>第二志愿</strong>
            </div>
            <div class="detail-grid">
              <div class="detail-item">
                <span class="detail-item__label">意向导师</span>
                <span class="detail-item__value">{{ displayDetailValue(application.second_choice) }}</span>
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
                <AttachmentPreviewActions :url="item.transcript_attachment_url" :file-name="item.transcript_attachment_name" fallback-label="成绩单附件" preview-title="成绩单附件预览" />
              </div>
              <div v-if="item.degree_certificate_attachment_url" class="detail-item detail-item--full">
                <span class="detail-item__label">学位证附件</span>
                <AttachmentPreviewActions :url="item.degree_certificate_attachment_url" :file-name="item.degree_certificate_attachment_name" fallback-label="学位证附件" preview-title="学位证附件预览" />
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
        <h3 class="dialog-section__title">英语能力</h3>
        <div v-if="application.english_proficiencies?.length" class="detail-record-stack">
          <article v-for="(item, index) in application.english_proficiencies" :key="`detail-english-${index}`" class="detail-record-card">
            <div class="detail-record-card__header">
              <strong>英语能力 {{ index + 1 }}</strong>
            </div>
            <div class="detail-grid">
              <div class="detail-item"><span class="detail-item__label">考试名称</span><span class="detail-item__value">{{ displayDetailValue(item.exam_name) }}</span></div>
              <div class="detail-item"><span class="detail-item__label">成绩</span><span class="detail-item__value">{{ displayDetailValue(item.score_text) }}</span></div>
              <div v-if="item.certificate_attachment_url" class="detail-item detail-item--full">
                <span class="detail-item__label">英语证书附件</span>
                <AttachmentPreviewActions :url="item.certificate_attachment_url" :file-name="item.certificate_attachment_name" fallback-label="英语证书附件" preview-title="英语证书附件预览" />
              </div>
            </div>
          </article>
        </div>
        <div v-else class="empty-inline">当前未填写英语能力。</div>
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
        <h3 class="dialog-section__title">成果经历</h3>
        <div v-if="application.achievement_records?.length" class="detail-record-stack">
          <article v-for="(item, index) in application.achievement_records" :key="`detail-achievement-${index}`" class="detail-record-card">
            <div class="detail-record-card__header">
              <strong>成果经历 {{ index + 1 }}</strong>
            </div>
            <div class="detail-grid">
              <div class="detail-item"><span class="detail-item__label">成果类型</span><span class="detail-item__value">{{ displayDetailValue(item.achievement_type) }}</span></div>
              <div v-if="hasDisplayValue(item.achievement_month)" class="detail-item"><span class="detail-item__label">成果时间</span><span class="detail-item__value">{{ displayDetailValue(item.achievement_month) }}</span></div>
              <div v-if="hasDisplayValue(item.paper_title)" class="detail-item detail-item--full"><span class="detail-item__label">论文标题</span><span class="detail-item__value">{{ displayDetailValue(item.paper_title) }}</span></div>
              <div v-if="hasDisplayValue(item.author_order)" class="detail-item"><span class="detail-item__label">作者排序</span><span class="detail-item__value">{{ displayDetailValue(item.author_order) }}</span></div>
              <div v-if="hasDisplayValue(item.journal_or_conference)" class="detail-item"><span class="detail-item__label">期刊/会议</span><span class="detail-item__value">{{ displayDetailValue(item.journal_or_conference) }}</span></div>
              <div v-if="hasDisplayValue(item.publish_or_index_month)" class="detail-item"><span class="detail-item__label">发表/收录时间</span><span class="detail-item__value">{{ displayDetailValue(item.publish_or_index_month) }}</span></div>
              <div v-if="hasDisplayValue(item.award_name)" class="detail-item"><span class="detail-item__label">奖项名称</span><span class="detail-item__value">{{ displayDetailValue(item.award_name) }}</span></div>
              <div v-if="hasDisplayValue(item.award_rank)" class="detail-item"><span class="detail-item__label">奖项等级/名次</span><span class="detail-item__value">{{ displayDetailValue(item.award_rank) }}</span></div>
              <div v-if="hasDisplayValue(item.awarding_organization)" class="detail-item"><span class="detail-item__label">颁奖单位</span><span class="detail-item__value">{{ displayDetailValue(item.awarding_organization) }}</span></div>
              <div v-if="hasDisplayValue(item.award_level)" class="detail-item"><span class="detail-item__label">奖项级别</span><span class="detail-item__value">{{ displayDetailValue(item.award_level) }}</span></div>
              <div v-if="hasDisplayValue(item.award_year)" class="detail-item"><span class="detail-item__label">获奖年份</span><span class="detail-item__value">{{ displayDetailValue(item.award_year) }}</span></div>
              <div v-if="hasDisplayValue(item.description_text)" class="detail-item detail-item--full"><span class="detail-item__label">成果说明</span><span class="detail-item__value">{{ displayDetailValue(item.description_text) }}</span></div>
              <div v-if="hasDisplayValue(item.responsibility_text)" class="detail-item detail-item--full"><span class="detail-item__label">本人贡献</span><span class="detail-item__value">{{ displayDetailValue(item.responsibility_text) }}</span></div>
              <div v-if="item.award_certificate_attachment_url" class="detail-item detail-item--full">
                <span class="detail-item__label">成果证明附件</span>
                <AttachmentPreviewActions :url="item.award_certificate_attachment_url" :file-name="item.award_certificate_attachment_name" fallback-label="成果证明附件" preview-title="成果证明附件预览" />
              </div>
            </div>
          </article>
        </div>
        <div v-else class="empty-inline">当前未填写成果经历。</div>
      </section>

      <section class="detail-section">
        <h3 class="dialog-section__title">附件材料</h3>
        <div class="detail-text-list">
          <article v-if="application.personal_statement?.supporting_material_attachment_url || application.material_list_attachment" class="detail-text-card">
            <h4>补充材料附件</h4>
            <AttachmentPreviewActions
              :url="application.personal_statement?.supporting_material_attachment_url || application.material_list_attachment"
              :file-name="application.personal_statement?.supporting_material_attachment_name || application.material_list_attachment_name"
              fallback-label="补充材料附件"
              preview-title="补充材料附件预览"
              stacked
            />
          </article>
          <article v-if="application.material_list_attachment" class="detail-text-card">
            <h4>材料清单附件</h4>
            <AttachmentPreviewActions
              :url="application.material_list_attachment"
              :file-name="application.material_list_attachment_name"
              fallback-label="材料清单附件"
              preview-title="材料清单附件预览"
              stacked
            />
          </article>
        </div>
      </section>

      <section class="detail-section">
        <h3 class="dialog-section__title">个人陈述与补充说明</h3>
        <div class="detail-text-list">
          <article class="detail-text-card"><h4>个人陈述</h4><p>{{ displayDetailValue(application.personal_statement?.personal_statement_text) }}</p></article>
          <article class="detail-text-card"><h4>成长经历</h4><p>{{ displayDetailValue(application.personal_statement?.growth_experience_text) }}</p></article>
          <article class="detail-text-card"><h4>项目申报理由</h4><p>{{ displayDetailValue(application.personal_statement?.program_application_reason_text) }}</p></article>
          <article class="detail-text-card"><h4>职业规划</h4><p>{{ displayDetailValue(application.personal_statement?.career_plan_text) }}</p></article>
          <article class="detail-text-card"><h4>关键科研问题</h4><p>{{ displayDetailValue(application.personal_statement?.ai_problem_statement || application.research_problem) }}</p></article>
          <article class="detail-text-card"><h4>AI 行业不同观点</h4><p>{{ displayDetailValue(application.personal_statement?.ai_industry_opinion || application.dissenting_view) }}</p></article>
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
  gap: 12px;
  align-items: flex-start;
  margin-bottom: 12px;
  padding: 12px 14px;
  border-radius: 14px;
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
  margin-bottom: 14px;
}

.dialog-section__title {
  margin: 0 0 10px;
  color: #1c3f66;
  font-size: 16px;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px;
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

.detail-item :deep(.attachment-preview-block) {
  flex: 1 1 auto;
  min-width: 0;
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
  margin-bottom: 6px;
  color: #1b3e64;
  font-size: 12px;
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

  .detail-item {
    align-items: flex-start;
  }

  .detail-item__label {
    flex-basis: 76px;
  }
}
</style>