<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useRoute } from 'vue-router'
import TableRowActions from '../../components/table/TableRowActions.vue'

import {
  createThesis,
  createThesisReview,
  getDegreeOptions,
  getDegreeStats,
  listTheses,
  listThesisReviews,
  updateThesis,
  updateThesisReview,
  type DegreeOptions,
  type DegreeStats,
  type ThesisRecord,
  type ThesisReviewRecord,
  type ThesisReviewUpsert,
  type ThesisUpsert,
} from '../../api/degree'

const route = useRoute()
const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const dialogMode = ref<'create' | 'edit'>('create')
const currentId = ref<number | null>(null)

const stats = ref<DegreeStats>({
  thesis_total: 0,
  plagiarism_pending_total: 0,
  blind_review_pending_total: 0,
  defense_pending_total: 0,
  degree_granted_total: 0,
})

const theses = ref<ThesisRecord[]>([])
const reviews = ref<ThesisReviewRecord[]>([])
const options = ref<DegreeOptions>({
  student_options: [],
  advisor_options: [],
  thesis_options: [],
  thesis_status_options: [],
  blind_review_status_options: [],
  defense_status_options: [],
  degree_status_options: [],
  expert_options: [],
  review_status_options: [],
})

const thesisForm = reactive<ThesisUpsert>({
  student_no: '',
  student_name: '',
  advisor_name: '',
  title: '',
  plagiarism_rate: undefined,
  thesis_status: '开题中',
  blind_review_status: '待送审',
  defense_status: '待安排',
  degree_status: '未授位',
})

const reviewForm = reactive<ThesisReviewUpsert>({
  thesis_id: 0,
  thesis_title: '',
  expert_name: '',
  review_score: undefined,
  review_status: '待反馈',
  review_comment: '',
})

const activeSection = computed(() => String(route.meta.section || 'theses'))
const sectionTitle = computed(() => ({ theses: '论文主档管理', reviews: '盲审评阅管理' }[activeSection.value] || '学位管理'))
const statCards = computed(() => [
  { label: '论文总数', value: stats.value.thesis_total },
  { label: '待查重', value: stats.value.plagiarism_pending_total },
  { label: '待盲审', value: stats.value.blind_review_pending_total },
  { label: '待答辩', value: stats.value.defense_pending_total },
])

function resetForms() {
  currentId.value = null
  Object.assign(thesisForm, {
    student_no: '',
    student_name: '',
    advisor_name: '',
    title: '',
    plagiarism_rate: undefined,
    thesis_status: '开题中',
    blind_review_status: '待送审',
    defense_status: '待安排',
    degree_status: '未授位',
  })
  Object.assign(reviewForm, {
    thesis_id: 0,
    thesis_title: '',
    expert_name: '',
    review_score: undefined,
    review_status: '待反馈',
    review_comment: '',
  })
}

async function loadData() {
  loading.value = true
  try {
    const [statsResponse, thesisResponse, reviewResponse, optionsResponse] = await Promise.all([
      getDegreeStats(),
      listTheses(),
      listThesisReviews(),
      getDegreeOptions(),
    ])
    stats.value = statsResponse.data
    theses.value = thesisResponse.data.items
    reviews.value = reviewResponse.data.items
    options.value = optionsResponse.data
  } finally {
    loading.value = false
  }
}

const thesisLookup = computed(() => {
  return new Map(theses.value.map((item) => [item.id, item]))
})

watch(
  () => thesisForm.student_no,
  (studentNo) => {
    const matched = thesisLookup.value.size ? theses.value.find((item) => item.student_no === studentNo) : undefined
    if (!matched) {
      return
    }
    thesisForm.student_name = matched.student_name
    thesisForm.advisor_name = matched.advisor_name
  },
)

watch(
  () => reviewForm.thesis_id,
  (thesisId) => {
    const matched = thesisLookup.value.get(thesisId)
    if (!matched) {
      return
    }
    reviewForm.thesis_title = matched.title
  },
)

function openCreateDialog() {
  dialogMode.value = 'create'
  resetForms()
  dialogVisible.value = true
}

function openEditDialog(row: ThesisRecord | ThesisReviewRecord) {
  dialogMode.value = 'edit'
  currentId.value = row.id
  if (activeSection.value === 'theses') {
    Object.assign(thesisForm, row)
  } else {
    Object.assign(reviewForm, row)
  }
  dialogVisible.value = true
}

async function submit() {
  submitting.value = true
  try {
    if (activeSection.value === 'theses') {
      if (dialogMode.value === 'create') {
        await createThesis(thesisForm)
      } else if (currentId.value !== null) {
        await updateThesis(currentId.value, thesisForm)
      }
    } else {
      if (dialogMode.value === 'create') {
        await createThesisReview(reviewForm)
      } else if (currentId.value !== null) {
        await updateThesisReview(currentId.value, reviewForm)
      }
    }
    ElMessage.success('保存成功')
    dialogVisible.value = false
    await loadData()
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  void loadData()
})
</script>

<template>
  <section class="content-stack">
    <section class="stat-grid">
      <article v-for="card in statCards" :key="card.label" class="pill-card">
        <p>{{ card.label }}</p>
        <strong>{{ card.value }}</strong>
      </article>
    </section>

    <section class="section-card">
      <div class="section-card__header">
        <div>
          <p class="section-tag">学位过程</p>
          <h2>{{ sectionTitle }}</h2>
        </div>
        <el-button type="primary" round @click="openCreateDialog">新增记录</el-button>
      </div>

      <el-table v-if="activeSection === 'theses'" :data="theses" stripe v-loading="loading">
        <el-table-column prop="student_no" label="学号" width="120" />
        <el-table-column prop="student_name" label="学生" width="100" />
        <el-table-column prop="advisor_name" label="导师" width="100" />
        <el-table-column prop="title" label="论文题目" min-width="240" />
        <el-table-column prop="thesis_status" label="论文状态" width="120" />
        <el-table-column prop="blind_review_status" label="盲审状态" width="120" />
        <el-table-column prop="defense_status" label="答辩状态" width="120" />
        <el-table-column prop="degree_status" label="授位状态" width="120" />
        <el-table-column label="操作" width="90" align="center">
          <template #default="scope"><TableRowActions :row="scope.row" :main-actions="[{ key: 'edit', label: '编辑', type: 'primary', onClick: openEditDialog }]" /></template>
        </el-table-column>
      </el-table>

      <el-table v-else :data="reviews" stripe v-loading="loading">
        <el-table-column prop="thesis_id" label="论文ID" width="100" />
        <el-table-column prop="thesis_title" label="论文题目" min-width="240" />
        <el-table-column prop="expert_name" label="评审专家" width="120" />
        <el-table-column prop="review_score" label="评分" width="100" />
        <el-table-column prop="review_status" label="评审状态" width="120" />
        <el-table-column prop="review_comment" label="评审意见" min-width="260" />
        <el-table-column label="操作" width="90" align="center">
          <template #default="scope"><TableRowActions :row="scope.row" :main-actions="[{ key: 'edit', label: '编辑', type: 'primary', onClick: openEditDialog }]" /></template>
        </el-table-column>
      </el-table>
    </section>

    <el-dialog v-model="dialogVisible" :title="dialogMode === 'create' ? `新增${sectionTitle}` : `编辑${sectionTitle}`" width="760px">
      <el-form v-if="activeSection === 'theses'" label-width="110px" class="dialog-grid">
        <el-form-item label="学生">
          <el-select v-model="thesisForm.student_no" filterable placeholder="请选择学生">
            <el-option v-for="item in options.student_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="学号"><el-input v-model="thesisForm.student_no" disabled /></el-form-item>
        <el-form-item label="学生姓名"><el-input v-model="thesisForm.student_name" disabled /></el-form-item>
        <el-form-item label="导师">
          <el-select v-model="thesisForm.advisor_name" filterable placeholder="请选择导师">
            <el-option v-for="item in options.advisor_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="论文状态">
          <el-select v-model="thesisForm.thesis_status" placeholder="请选择论文状态">
            <el-option v-for="item in options.thesis_status_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="盲审状态">
          <el-select v-model="thesisForm.blind_review_status" placeholder="请选择盲审状态">
            <el-option v-for="item in options.blind_review_status_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="答辩状态">
          <el-select v-model="thesisForm.defense_status" placeholder="请选择答辩状态">
            <el-option v-for="item in options.defense_status_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="授位状态">
          <el-select v-model="thesisForm.degree_status" placeholder="请选择授位状态">
            <el-option v-for="item in options.degree_status_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="查重率"><el-input-number v-model="thesisForm.plagiarism_rate" :min="0" :max="100" :precision="1" controls-position="right" /></el-form-item>
        <el-form-item label="论文题目" class="dialog-grid__full"><el-input v-model="thesisForm.title" type="textarea" :rows="3" /></el-form-item>
      </el-form>

      <el-form v-else label-width="110px" class="dialog-grid">
        <el-form-item label="论文主档">
          <el-select v-model="reviewForm.thesis_id" filterable placeholder="请选择论文" style="width: 100%">
            <el-option v-for="item in options.thesis_options" :key="item.value" :label="item.label" :value="Number(item.value)" />
          </el-select>
        </el-form-item>
        <el-form-item label="论文ID"><el-input-number v-model="reviewForm.thesis_id" :min="1" controls-position="right" disabled /></el-form-item>
        <el-form-item label="论文题目"><el-input v-model="reviewForm.thesis_title" disabled /></el-form-item>
        <el-form-item label="评审专家">
          <el-select v-model="reviewForm.expert_name" filterable allow-create default-first-option placeholder="请选择评审专家">
            <el-option v-for="item in options.expert_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="评审状态">
          <el-select v-model="reviewForm.review_status" placeholder="请选择评审状态">
            <el-option v-for="item in options.review_status_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="评分"><el-input-number v-model="reviewForm.review_score" :min="0" :max="100" :precision="1" controls-position="right" /></el-form-item>
        <el-form-item label="评审意见" class="dialog-grid__full"><el-input v-model="reviewForm.review_comment" type="textarea" :rows="4" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submit">保存</el-button>
      </template>
    </el-dialog>
  </section>
</template>

<style scoped>
.content-stack,
.stat-grid {
  display: grid;
  gap: 14px;
}

.stat-grid {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.section-card {
  border: 1px solid rgba(18, 50, 95, 0.08);
  border-radius: 20px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 18px 44px rgba(14, 40, 88, 0.07);
}

.section-card__header {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
  margin-bottom: 12px;
}

.section-tag,
.section-card h2,
.pill-card p {
  margin: 0;
}

.section-tag {
  color: #7183a0;
  font-size: 11px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.section-card h2 {
  margin-top: 4px;
  color: #12284d;
  font-size: 16px;
}

.pill-card {
  padding: 14px 16px;
  border-radius: 18px;
  background: linear-gradient(135deg, rgba(245, 248, 255, 0.98), rgba(235, 245, 255, 0.92));
}

.pill-card strong {
  display: block;
  margin-top: 6px;
  color: #12315e;
  font-size: 22px;
}

.dialog-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 4px 18px;
}

.dialog-grid__full {
  grid-column: 1 / -1;
}

@media (max-width: 980px) {
  .stat-grid,
  .dialog-grid {
    grid-template-columns: 1fr;
  }
}
</style>
