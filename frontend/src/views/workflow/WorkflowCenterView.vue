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
  { label: '待处理', value: stats.value.todo_total },
  { label: '处理中', value: stats.value.in_progress_total },
  { label: '已通过', value: stats.value.approved_total },
  { label: '已驳回', value: stats.value.rejected_total },
  { label: '已超期', value: stats.value.overdue_total },
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
  <section class="content-stack">
    <section class="stat-grid">
      <article v-for="card in statCards" :key="card.label" class="stat-card">
        <p>{{ card.label }}</p>
        <strong>{{ card.value }}</strong>
      </article>
    </section>

    <article class="section-card">
      <div class="section-card__header">
        <div>
          <p class="section-tag">审批中心</p>
          <h2>流程任务清单</h2>
        </div>
        <el-button type="primary" round @click="openCreateDialog">新增审批任务</el-button>
      </div>
      <el-form :inline="true" class="filter-form">
        <el-form-item label="状态">
          <el-input v-model="filters.status" placeholder="待处理 / 处理中 / 已通过" clearable />
        </el-form-item>
        <el-form-item label="业务模块">
          <el-input v-model="filters.module" placeholder="培养管理 / 学位管理" clearable />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadData">查询</el-button>
        </el-form-item>
      </el-form>
      <el-table :data="tasks" stripe v-loading="loading">
        <el-table-column prop="workflow_name" label="流程名称" width="140" />
        <el-table-column prop="business_module" label="业务模块" width="110" />
        <el-table-column prop="title" label="任务标题" min-width="220" />
        <el-table-column prop="current_node" label="当前节点" width="120" />
        <el-table-column prop="current_handler" label="当前处理人" width="120" />
        <el-table-column prop="status" label="状态" width="100" />
        <el-table-column prop="due_at" label="截止时间" width="160" />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="scope">
            <el-button link type="primary" @click="openEditDialog(scope.row)">编辑</el-button>
            <el-button link type="danger" @click="removeTask(scope.row)">删除</el-button>
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
.content-stack,
.stat-grid {
  display: grid;
  gap: 22px;
}

.stat-grid {
  grid-template-columns: repeat(5, minmax(0, 1fr));
}

.stat-card,
.section-card {
  border: 1px solid rgba(18, 50, 95, 0.08);
  border-radius: 26px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 18px 44px rgba(14, 40, 88, 0.07);
}

.stat-card {
  padding: 18px 20px;
}

.stat-card p,
.stat-card strong,
.section-tag,
.section-card h2 {
  margin: 0;
}

.stat-card strong {
  display: block;
  margin-top: 10px;
  font-size: 28px;
  color: #12315e;
}

.section-card {
  padding: 22px;
}

.section-card__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-bottom: 18px;
}

.section-tag {
  color: #7183a0;
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.section-card h2 {
  margin-top: 6px;
  color: #12284d;
}

.filter-form {
  margin-bottom: 18px;
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
