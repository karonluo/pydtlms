<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

import {
  createWorkflowTask,
  deleteWorkflowTask,
  getWorkflowStats,
  listWorkflowTasks,
  updateWorkflowTask,
  type WorkflowStats,
  type WorkflowTaskRecord,
  type WorkflowTaskUpsert,
} from '../../api/workflow'

const stats = ref<WorkflowStats>({ todo_total: 0, in_progress_total: 0, approved_total: 0, rejected_total: 0, overdue_total: 0 })
const tasks = ref<WorkflowTaskRecord[]>([])
const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const dialogMode = ref<'create' | 'edit'>('create')
const editingId = ref<number | null>(null)

const filters = reactive({ status: '', module: '' })
const form = reactive<WorkflowTaskUpsert>({
  workflow_name: '外出研修审批',
  business_module: '培养管理',
  business_key: '',
  title: '',
  applicant_name: '',
  current_handler: '',
  current_node: '',
  priority: '中',
  status: '待处理',
  created_at: '',
  due_at: '',
  form_summary: '',
  latest_comment: '',
})

const statCards = computed(() => [
  { label: '全部待办', value: stats.value.todo_total },
  { label: '处理中', value: stats.value.in_progress_total },
  { label: '已通过', value: stats.value.approved_total },
  { label: '已驳回', value: stats.value.rejected_total },
])

function resetForm() {
  editingId.value = null
  Object.assign(form, {
    workflow_name: '外出研修审批',
    business_module: '培养管理',
    business_key: '',
    title: '',
    applicant_name: '',
    current_handler: '',
    current_node: '',
    priority: '中',
    status: '待处理',
    created_at: new Date().toISOString().slice(0, 16).replace('T', ' '),
    due_at: '',
    form_summary: '',
    latest_comment: '',
  })
}

function openCreateDialog() {
  dialogMode.value = 'create'
  resetForm()
  dialogVisible.value = true
}

function openEditDialog(row: WorkflowTaskRecord) {
  dialogMode.value = 'edit'
  editingId.value = row.id
  Object.assign(form, row)
  dialogVisible.value = true
}

async function loadData() {
  loading.value = true
  try {
    const [statsResponse, tasksResponse] = await Promise.all([
      getWorkflowStats(),
      listWorkflowTasks({ status: filters.status || undefined, module: filters.module || undefined }),
    ])
    stats.value = statsResponse.data
    tasks.value = tasksResponse.data.items
  } finally {
    loading.value = false
  }
}

async function submit() {
  submitting.value = true
  try {
    if (dialogMode.value === 'create') {
      await createWorkflowTask(form)
      ElMessage.success('审批任务已新增')
    } else if (editingId.value !== null) {
      await updateWorkflowTask(editingId.value, form)
      ElMessage.success('审批任务已更新')
    }
    dialogVisible.value = false
    await loadData()
  } finally {
    submitting.value = false
  }
}

async function removeTask(row: WorkflowTaskRecord) {
  await ElMessageBox.confirm(`确定删除审批任务 ${row.title} 吗？`, '删除确认', { type: 'warning' })
  await deleteWorkflowTask(row.id)
  ElMessage.success('审批任务已删除')
  await loadData()
}

onMounted(() => {
  void loadData()
})
</script>

<template>
  <section class="workflow-stack">
    <section class="stat-grid">
      <article v-for="card in statCards" :key="card.label" class="stat-card">
        <p>{{ card.label }}</p>
        <strong>{{ card.value }}</strong>
        <span>待审批业务</span>
      </article>
    </section>

    <article class="section-card">
      <div class="section-card__header">
        <div>
          <p class="section-tag">工作台 / 流程待办</p>
          <h2>审批工作台</h2>
          <span class="section-desc">统一汇总合同、发货通知、开票申请等待审批业务，便于审批人集中处理。</span>
        </div>
        <el-tag round>当前共 {{ tasks.length }} 项待处理</el-tag>
      </div>

      <div class="filter-panel">
        <div class="filter-panel__header">
          <strong>筛选与检索</strong>
          <span>按业务类型、业务编号或申请人快速定位。</span>
        </div>
        <el-form :inline="true" class="filter-form">
          <el-form-item>
            <el-input v-model="filters.module" placeholder="按业务类型、申请人、标题检索" clearable />
          </el-form-item>
          <el-form-item>
            <el-input v-model="filters.status" placeholder="状态：待处理 / 已通过" clearable />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="loadData">查询</el-button>
          </el-form-item>
          <el-form-item>
            <el-button @click="openCreateDialog">新增待办</el-button>
          </el-form-item>
        </el-form>
      </div>

      <el-table :data="tasks" stripe v-loading="loading">
        <el-table-column prop="workflow_name" label="待办类型" width="150" />
        <el-table-column prop="business_key" label="业务编号" width="150" />
        <el-table-column prop="title" label="任务标题" min-width="220" />
        <el-table-column prop="status" label="当前状态" width="100" />
        <el-table-column prop="current_handler" label="审批人" width="110" />
        <el-table-column prop="applicant_name" label="提交人" width="110" />
        <el-table-column prop="created_at" label="提交时间" width="160" />
        <el-table-column label="操作" width="160" fixed="right">
          <template #default="scope">
            <el-button link type="primary" @click="openEditDialog(scope.row)">查看原单</el-button>
            <el-button link type="success" @click="openEditDialog(scope.row)">通过</el-button>
            <el-button link type="danger" @click="removeTask(scope.row)">驳回</el-button>
          </template>
        </el-table-column>
      </el-table>
    </article>

    <el-dialog v-model="dialogVisible" :title="dialogMode === 'create' ? '新增审批任务' : '编辑审批任务'" width="760px">
      <el-form label-width="100px" class="dialog-grid">
        <el-form-item label="流程名称"><el-input v-model="form.workflow_name" /></el-form-item>
        <el-form-item label="业务模块"><el-input v-model="form.business_module" /></el-form-item>
        <el-form-item label="业务主键"><el-input v-model="form.business_key" /></el-form-item>
        <el-form-item label="任务标题"><el-input v-model="form.title" /></el-form-item>
        <el-form-item label="申请人"><el-input v-model="form.applicant_name" /></el-form-item>
        <el-form-item label="当前处理人"><el-input v-model="form.current_handler" /></el-form-item>
        <el-form-item label="当前节点"><el-input v-model="form.current_node" /></el-form-item>
        <el-form-item label="优先级"><el-input v-model="form.priority" /></el-form-item>
        <el-form-item label="状态"><el-input v-model="form.status" /></el-form-item>
        <el-form-item label="创建时间"><el-input v-model="form.created_at" /></el-form-item>
        <el-form-item label="截止时间"><el-input v-model="form.due_at" /></el-form-item>
        <el-form-item label="表单摘要" class="dialog-grid__full"><el-input v-model="form.form_summary" type="textarea" :rows="3" /></el-form-item>
        <el-form-item label="最新意见" class="dialog-grid__full"><el-input v-model="form.latest_comment" type="textarea" :rows="3" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submit">保存</el-button>
      </template>
    </el-dialog>
  </section>
</template>

<style scoped>
.workflow-stack,
.stat-grid {
  display: grid;
  gap: 14px;
}

.stat-grid {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.stat-card,
.section-card {
  border: 1px solid rgba(203, 223, 244, 0.94);
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.94);
  box-shadow: 0 18px 40px rgba(67, 108, 159, 0.08);
}

.stat-card {
  padding: 14px 16px;
}

.stat-card p,
.stat-card strong,
.stat-card span,
.section-tag,
.section-card h2,
.section-desc,
.filter-panel__header span {
  margin: 0;
}

.stat-card strong {
  display: block;
  margin-top: 6px;
  color: #234264;
  font-size: 22px;
}

.stat-card span {
  display: block;
  margin-top: 4px;
  color: #859ab2;
  font-size: 12px;
}

.section-card {
  padding: 16px;
}

.section-card__header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  gap: 12px;
  margin-bottom: 12px;
}

.section-tag {
  color: #8298b1;
  font-size: 11px;
}

.section-card h2 {
  margin-top: 6px;
  color: #1f3e64;
  font-size: 18px;
}

.section-desc {
  display: block;
  margin-top: 6px;
  color: #7d91ad;
  font-size: 12px;
}

.filter-panel {
  margin-bottom: 12px;
  padding: 12px;
  border: 1px solid rgba(212, 228, 244, 0.95);
  border-radius: 14px;
  background: linear-gradient(180deg, rgba(248, 251, 255, 0.95), rgba(241, 247, 255, 0.95));
}

.filter-panel__header strong {
  color: #24446d;
}

.filter-panel__header span {
  display: block;
  margin-top: 4px;
  color: #8093ad;
  font-size: 12px;
}

.filter-form {
  margin-top: 10px;
}

.dialog-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 4px 18px;
}

.dialog-grid__full {
  grid-column: 1 / -1;
}

@media (max-width: 1080px) {
  .stat-grid,
  .dialog-grid {
    grid-template-columns: 1fr;
  }
}
</style>
