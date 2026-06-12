<script setup lang="ts">
import axios from 'axios'
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'

import { listAdvisorScreeningSubmittedApplications, type AdvisorScreeningSubmittedApplicationRecord } from '../../api/recruitment'
import { useAuthStore } from '../../stores/auth'
import { useServerPagination } from '../../composables/useServerPagination'

const authStore = useAuthStore()
const loading = ref(false)
const rows = ref<AdvisorScreeningSubmittedApplicationRecord[]>([])
const pagination = useServerPagination()

const filters = reactive({
  keyword: '',
})

const roleSet = computed(() => new Set(authStore.roles))
const canAccessSubmittedTab = computed(() => ['advisor', 'platform_admin'].some((role) => roleSet.value.has(role)))

function formatSubmittedTime(value?: string | null) {
  return value || '-'
}

function resolveSubmittedChoiceLabel(row: AdvisorScreeningSubmittedApplicationRecord) {
  return row.choice_name || (row.first_choice_screening_submitted_at ? '第一志愿' : row.second_choice_screening_submitted_at ? '第二志愿' : '-')
}

function resolveSubmittedScoreLabel(row: AdvisorScreeningSubmittedApplicationRecord) {
  return row.choice_score === null || row.choice_score === undefined ? '-' : String(row.choice_score)
}

async function loadRows() {
  if (!canAccessSubmittedTab.value) {
    rows.value = []
    pagination.sync(0)
    return
  }
  loading.value = true
  try {
    const response = await listAdvisorScreeningSubmittedApplications({
      keyword: filters.keyword || undefined,
      page: pagination.pagination.currentPage,
      page_size: pagination.pagination.pageSize,
    })
    rows.value = response.data.items
    pagination.sync(response.data.total)
  } catch (error) {
    const message = axios.isAxiosError(error) ? String(error.response?.data?.detail || error.message) : '加载已提交记录失败'
    ElMessage.error(message)
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  pagination.pagination.currentPage = 1
  void loadRows()
}

function handleReset() {
  filters.keyword = ''
  pagination.pagination.currentPage = 1
  void loadRows()
}

watch(() => pagination.pagination.currentPage, () => {
  void loadRows()
})

watch(() => pagination.pagination.pageSize, () => {
  pagination.pagination.currentPage = 1
  void loadRows()
})

onMounted(() => {
  void loadRows()
})
</script>

<template>
  <div class="advisor-screening-submitted-view">
    <div class="page-header">
      <div>
        <div class="page-kicker">导师初筛</div>
        <h1>已提交</h1>
        <p>查询导师已提交的初筛记录，支持按报名号和学生姓名检索。</p>
      </div>
      <div class="header-meta">
        <el-tag type="info">报名号：candidate_no</el-tag>
        <el-tag type="success">独立页面</el-tag>
      </div>
    </div>

    <el-card class="filter-card" shadow="never">
      <el-form inline :model="filters" class="filter-form">
        <el-form-item label="关键字">
          <el-input v-model="filters.keyword" clearable placeholder="请输入报名号或学生姓名" @keyup.enter="handleSearch" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card" shadow="never">
      <el-table :data="rows" v-loading="loading" border stripe :empty-text="canAccessSubmittedTab ? '暂无已提交记录' : '当前账号无权限查看该页面'">
        <el-table-column prop="candidate_no" label="报名号" min-width="150" />
        <el-table-column prop="full_name" label="学生姓名" min-width="120" />
        <el-table-column prop="plan_id" label="计划ID" width="100" align="center" />
        <el-table-column label="志愿" min-width="120">
          <template #default="{ row }">
            {{ resolveSubmittedChoiceLabel(row) }}
          </template>
        </el-table-column>
        <el-table-column label="分数" width="100" align="center">
          <template #default="{ row }">
            {{ resolveSubmittedScoreLabel(row) }}
          </template>
        </el-table-column>
        <el-table-column label="提交时间" min-width="180">
          <template #default="{ row }">
            {{ formatSubmittedTime(row.first_choice_screening_submitted_at || row.second_choice_screening_submitted_at) }}
          </template>
        </el-table-column>
        <el-table-column prop="choice_name" label="志愿名称" min-width="120" />
      </el-table>

      <div class="pagination-bar">
        <el-pagination
          v-model:current-page="pagination.pagination.currentPage"
          v-model:page-size="pagination.pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
        />
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.advisor-screening-submitted-view {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
}

.page-kicker {
  font-size: 12px;
  color: var(--el-color-info);
  letter-spacing: 0.08em;
}

h1 {
  margin: 6px 0 8px;
  font-size: 24px;
  line-height: 1.2;
}

p {
  margin: 0;
  color: var(--el-text-color-secondary);
}

.header-meta {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.filter-card,
.table-card {
  border-radius: 14px;
}

.filter-form {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.pagination-bar {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
  }

  .header-meta {
    justify-content: flex-start;
  }

  .pagination-bar {
    justify-content: center;
  }
}
</style>
