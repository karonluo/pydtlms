<script setup lang="ts">
import axios from 'axios'
import { computed, onMounted, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import TableRowActions, { type TableRowAction } from '../../components/table/TableRowActions.vue'
import { useServerPagination } from '../../composables/useServerPagination'

import {
  createWorkflowTask,
  deleteWorkflowTask,
  executeWorkflowTaskAction,
  getWorkflowOptions,
  getWorkflowStats,
  getWorkflowTaskDetail,
  listWorkflowTasks,
  updateWorkflowTask,
  type WorkflowActionOption,
  type WorkflowOptions,
  type WorkflowStats,
  type WorkflowTaskDetailResponse,
  type WorkflowTaskRecord,
  type WorkflowTaskUpsert,
} from '../../api/workflow'

const stats = ref<WorkflowStats>({ todo_total: 0, in_progress_total: 0, approved_total: 0, rejected_total: 0, overdue_total: 0 })
const tasks = ref<WorkflowTaskRecord[]>([])
const options = ref<WorkflowOptions>({
  workflow_name_options: [],
  business_module_options: [],
  applicant_options: [],
  handler_options: [],
  current_node_options: [],
  priority_options: [],
  status_options: [],
})
const loading = ref(false)
const submitting = ref(false)
const detailLoading = ref(false)
const actionSubmitting = ref(false)
const dialogVisible = ref(false)
const detailVisible = ref(false)
const dialogMode = ref<'create' | 'edit'>('create')
const editingId = ref<number | null>(null)
const taskDetail = ref<WorkflowTaskDetailResponse | null>(null)
const actionComment = ref('')
const showHistory = ref(false)

const filters = reactive({ keyword: '', status: '', module: '' })
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
const taskPager = useServerPagination()
const detailTask = computed(() => taskDetail.value?.task ?? null)
const detailHistory = computed(() => taskDetail.value?.history ?? [])

function getErrorMessage(error: unknown) {
  if (axios.isAxiosError(error)) {
    return String(error.response?.data?.detail || error.message || '请求失败')
  }
  if (error instanceof Error) {
    return error.message
  }
  return '请求失败'
}

function isManagedTask(row: WorkflowTaskRecord) {
  return Boolean(row.available_actions.length || row.process_instance_id)
}

function actionButtonType(action: WorkflowActionOption) {
  if (action.action.includes('reject') || action.action.includes('request_revision')) {
    return 'danger'
  }
  if (action.action.includes('approve') || action.action.includes('admit') || action.action.includes('pre_admit')) {
    return 'success'
  }
  return 'primary'
}

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

async function openDetailDialog(row: WorkflowTaskRecord) {
  detailVisible.value = true
  detailLoading.value = true
  actionComment.value = ''
  showHistory.value = false
  try {
    const response = await getWorkflowTaskDetail(row.id)
    taskDetail.value = response.data
  } catch (error) {
    detailVisible.value = false
    ElMessage.error(getErrorMessage(error))
  } finally {
    detailLoading.value = false
  }
}

async function loadData() {
  loading.value = true
  try {
    const [statsResponse, tasksResponse, optionsResponse] = await Promise.all([
      getWorkflowStats(),
      listWorkflowTasks({
        keyword: filters.keyword || undefined,
        status: filters.status || undefined,
        module: filters.module || undefined,
        page: taskPager.pagination.currentPage,
        page_size: taskPager.pagination.pageSize,
      }),
      getWorkflowOptions(),
    ])
    stats.value = statsResponse.data
    tasks.value = tasksResponse.data.items
    options.value = optionsResponse.data
    taskPager.sync(tasksResponse.data.total)
  } finally {
    loading.value = false
  }
}

async function handleSearch() {
  taskPager.reset()
  await loadData()
}

async function handlePageChange(page: number) {
  taskPager.handleCurrentChange(page)
  await loadData()
}

async function handlePageSizeChange(pageSize: number) {
  taskPager.handleSizeChange(pageSize)
  await loadData()
}

async function handleReset() {
  Object.assign(filters, { keyword: '', status: '', module: '' })
  taskPager.reset()
  await loadData()
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
  } catch (error) {
    ElMessage.error(getErrorMessage(error))
  } finally {
    submitting.value = false
  }
}

async function removeTask(row: WorkflowTaskRecord) {
  try {
    await ElMessageBox.confirm(`确定删除审批任务 ${row.title} 吗？`, '删除确认', { type: 'warning' })
    await deleteWorkflowTask(row.id)
    ElMessage.success('审批任务已删除')
    await loadData()
  } catch (error) {
    if (error === 'cancel' || error === 'close') {
      return
    }
    ElMessage.error(getErrorMessage(error))
  }
}

async function executeAction(row: WorkflowTaskRecord, action: WorkflowActionOption, comment?: string) {
  actionSubmitting.value = true
  try {
    await executeWorkflowTaskAction(row.id, { action: action.action, comment: comment || undefined })
    detailVisible.value = false
    taskDetail.value = null
    actionComment.value = ''
    showHistory.value = false
    ElMessage.success(`${action.label}已完成`)
    try {
      await loadData()
    } catch (refreshError) {
      ElMessage.warning(`操作已完成，但列表刷新失败：${getErrorMessage(refreshError)}`)
    }
  } catch (error) {
    ElMessage.error(getErrorMessage(error))
  } finally {
    actionSubmitting.value = false
  }
}

async function promptAndExecuteAction(row: WorkflowTaskRecord, action: WorkflowActionOption) {
  try {
    const promptResult = await ElMessageBox.prompt(`请输入${action.label}意见`, action.label, {
      confirmButtonText: '提交',
      cancelButtonText: '取消',
      inputType: 'textarea',
      inputValue: row.latest_comment || '',
    })
    await executeAction(row, action, promptResult.value)
  } catch (error) {
    if (error === 'cancel' || error === 'close') {
      return
    }
    ElMessage.error(getErrorMessage(error))
  }
}

async function submitDetailAction(action: WorkflowActionOption) {
  if (!detailTask.value) {
    return
  }
  await executeAction(detailTask.value, action, actionComment.value)
}

function mainActionsForRow(_row: WorkflowTaskRecord): TableRowAction<WorkflowTaskRecord>[] {
  return [
    {
      key: 'detail',
      label: '查看详情',
      type: 'primary' as const,
      onClick: (targetRow: WorkflowTaskRecord) => openDetailDialog(targetRow),
    },
  ]
}

function moreActionsForRow(row: WorkflowTaskRecord): TableRowAction<WorkflowTaskRecord>[] {
  const actions: TableRowAction<WorkflowTaskRecord>[] = row.available_actions.map((action) => ({
    key: action.action,
    label: action.label,
    type: actionButtonType(action) as 'primary' | 'success' | 'warning' | 'danger' | 'info',
    onClick: () => promptAndExecuteAction(row, action),
  }))
  if (!isManagedTask(row)) {
    actions.push(
      {
        key: 'edit',
        label: '编辑任务',
        type: 'primary' as const,
        onClick: (targetRow: WorkflowTaskRecord) => openEditDialog(targetRow),
      },
      {
        key: 'delete',
        label: '删除任务',
        type: 'danger' as const,
        onClick: (targetRow: WorkflowTaskRecord) => removeTask(targetRow),
      },
    )
  }
  return actions
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
          <span class="section-desc">统一汇总各业务审批待办，按角色展示可执行流程动作，并保留完整处理历史。</span>
        </div>
        <el-tag round>当前共 {{ taskPager.pagination.total }} 项待处理</el-tag>
      </div>

      <div class="filter-panel">
        <div class="filter-panel__header">
          <strong>筛选与检索</strong>
          <span>按业务类型、业务编号或申请人快速定位。</span>
        </div>
        <el-form :inline="true" class="filter-form">
          <el-form-item>
            <el-input v-model="filters.keyword" placeholder="业务编号 / 标题 / 申请人 / 审批人" clearable style="width: 260px" @keyup.enter="handleSearch" />
          </el-form-item>
          <el-form-item>
            <el-select v-model="filters.module" placeholder="全部业务模块" clearable filterable style="width: 220px">
              <el-option v-for="item in options.business_module_options" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-select v-model="filters.status" placeholder="全部状态" clearable style="width: 180px">
              <el-option v-for="item in options.status_options" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">查询</el-button>
          </el-form-item>
          <el-form-item>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
          <el-form-item>
            <el-button @click="openCreateDialog">新增待办</el-button>
          </el-form-item>
        </el-form>
      </div>

      <el-table :data="tasks" stripe border v-loading="loading">
        <el-table-column prop="workflow_name" label="待办类型" width="150" />
        <el-table-column prop="business_key" label="业务编号" width="190" />
        <el-table-column prop="title" label="任务标题" min-width="220" />
        <el-table-column prop="status" label="当前状态" width="100" />
          <el-table-column prop="current_node" label="当前节点" width="120" />
        <el-table-column prop="current_handler" label="审批人" width="110" />
        <el-table-column prop="applicant_name" label="提交人" width="110" />
        <el-table-column prop="created_at" label="提交时间" width="160" />
        <el-table-column label="操作" width="220" align="left">
          <template #default="scope">
            <TableRowActions :row="scope.row" :main-actions="mainActionsForRow(scope.row)" :more-actions="moreActionsForRow(scope.row)" />
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-bar">
        <el-pagination
          :current-page="taskPager.pagination.currentPage"
          :page-size="taskPager.pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="taskPager.pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @current-change="handlePageChange"
          @size-change="handlePageSizeChange"
        />
      </div>
    </article>

    <el-dialog v-model="dialogVisible" :title="dialogMode === 'create' ? '新增审批任务' : '编辑审批任务'" width="760px">
      <el-form label-width="100px" class="dialog-grid">
        <el-form-item label="流程名称">
          <el-select v-model="form.workflow_name" filterable allow-create default-first-option placeholder="请选择流程名称">
            <el-option v-for="item in options.workflow_name_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="业务模块">
          <el-select v-model="form.business_module" filterable placeholder="请选择业务模块">
            <el-option v-for="item in options.business_module_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="任务标题"><el-input v-model="form.title" /></el-form-item>
        <el-form-item label="申请人">
          <el-select v-model="form.applicant_name" filterable placeholder="请选择申请人">
            <el-option v-for="item in options.applicant_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="当前处理人">
          <el-select v-model="form.current_handler" filterable placeholder="请选择处理人">
            <el-option v-for="item in options.handler_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="当前节点">
          <el-select v-model="form.current_node" filterable allow-create default-first-option placeholder="请选择流程节点">
            <el-option v-for="item in options.current_node_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="优先级">
          <el-select v-model="form.priority" placeholder="请选择优先级">
            <el-option v-for="item in options.priority_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="form.status" placeholder="请选择状态">
            <el-option v-for="item in options.status_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="创建时间"><el-date-picker v-model="form.created_at" type="datetime" value-format="YYYY-MM-DD HH:mm:ss" style="width: 100%" /></el-form-item>
        <el-form-item label="截止时间"><el-date-picker v-model="form.due_at" type="datetime" value-format="YYYY-MM-DD HH:mm:ss" style="width: 100%" /></el-form-item>
        <el-form-item label="表单摘要" class="dialog-grid__full"><el-input v-model="form.form_summary" type="textarea" :rows="3" /></el-form-item>
        <el-form-item label="最新意见" class="dialog-grid__full"><el-input v-model="form.latest_comment" type="textarea" :rows="3" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submit">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="detailVisible" title="审批详情" width="1120px" class="workflow-detail-dialog" @closed="showHistory = false">
      <div v-loading="detailLoading">
        <template v-if="detailTask">
          <div class="detail-toolbar">
            <div>
              <strong>{{ detailTask.title }}</strong>
              <p class="detail-subtitle">{{ detailTask.workflow_name }} / {{ detailTask.business_key }}</p>
            </div>
            <div class="detail-toolbar__actions">
              <el-button text type="primary" @click="showHistory = !showHistory">
                {{ showHistory ? '关闭处理历史' : '查看处理历史' }}
              </el-button>
              <el-tag :type="detailTask.status === '已通过' ? 'success' : detailTask.status === '已驳回' ? 'danger' : 'warning'" round>
                {{ detailTask.status }}
              </el-tag>
            </div>
          </div>

          <div class="detail-layout">
            <div class="detail-main">
              <el-descriptions :column="2" border class="detail-descriptions">
                <el-descriptions-item label="业务模块">{{ detailTask.business_module }}</el-descriptions-item>
                <el-descriptions-item label="申请人">{{ detailTask.applicant_name }}</el-descriptions-item>
                <el-descriptions-item label="当前节点">{{ detailTask.current_node }}</el-descriptions-item>
                <el-descriptions-item label="当前处理人">{{ detailTask.current_handler }}</el-descriptions-item>
                <el-descriptions-item label="优先级">{{ detailTask.priority }}</el-descriptions-item>
                <el-descriptions-item label="截止时间">{{ detailTask.due_at }}</el-descriptions-item>
                <el-descriptions-item label="表单摘要" :span="2">{{ detailTask.form_summary || '-' }}</el-descriptions-item>
                <el-descriptions-item label="最新意见" :span="2">{{ detailTask.latest_comment || '-' }}</el-descriptions-item>
              </el-descriptions>

              <div class="detail-action-panel">
                <div class="detail-action-panel__header">
                  <strong>当前可执行动作</strong>
                  <span v-if="detailTask.available_actions.length">仅展示当前登录角色可执行的流程动作</span>
                  <span v-else>当前任务没有可执行动作，可能已结束或当前角色无权处理</span>
                </div>
                <el-input v-model="actionComment" type="textarea" :rows="3" placeholder="请输入处理意见，可留空" />
                <div class="detail-action-buttons">
                  <el-button
                    v-for="action in detailTask.available_actions"
                    :key="action.action"
                    :type="actionButtonType(action)"
                    :loading="actionSubmitting"
                    @click="submitDetailAction(action)"
                  >
                    {{ action.label }}
                  </el-button>
                </div>
              </div>
            </div>
          </div>
        </template>
      </div>
      <template #footer>
        <el-button @click="detailVisible = false">关闭</el-button>
      </template>
    </el-dialog>

    <teleport to="body">
      <aside v-if="showHistory && detailVisible && detailTask" class="history-floating-panel">
        <div class="detail-history-panel__header">
          <div class="detail-history-panel__summary">
            <div class="detail-section-title">处理历史</div>
            <p class="detail-history-panel__subtitle">{{ detailTask.workflow_name }}</p>
            <p class="detail-history-panel__business-key">{{ detailTask.business_key }}</p>
          </div>
          <div class="detail-history-panel__header-actions">
            <span class="detail-history-panel__meta">共 {{ detailHistory.length }} 条</span>
            <el-button text type="primary" @click="showHistory = false">关闭</el-button>
          </div>
        </div>
        <div class="detail-history-panel__body">
          <el-empty v-if="!detailHistory.length" description="暂无处理历史" />
          <el-timeline v-else>
            <el-timeline-item v-for="entry in detailHistory" :key="`${entry.operated_at}-${entry.action}-${entry.operator_username}`" :timestamp="entry.operated_at" placement="top">
              <div class="history-card">
                <strong>{{ entry.action_label }}</strong>
                <p>{{ entry.operator_full_name }}（{{ entry.operator_username }}）</p>
                <p>{{ entry.from_node }} <span class="history-arrow">→</span> {{ entry.to_node || '流程结束' }}</p>
                <p>结果：{{ entry.result_status }}</p>
                <p>意见：{{ entry.comment || '-' }}</p>
              </div>
            </el-timeline-item>
          </el-timeline>
        </div>
      </aside>
    </teleport>
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

.detail-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 16px;
}

.detail-toolbar__actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.detail-subtitle {
  margin: 6px 0 0;
  color: #7d91ad;
  font-size: 12px;
}

.detail-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 16px;
}

.detail-main {
  min-width: 0;
}

.detail-descriptions {
  margin-bottom: 16px;
}

.detail-action-panel {
  margin-bottom: 18px;
  padding: 12px;
  border: 1px solid rgba(212, 228, 244, 0.95);
  border-radius: 14px;
  background: linear-gradient(180deg, rgba(248, 251, 255, 0.95), rgba(241, 247, 255, 0.95));
}

.detail-action-panel__header {
  margin-bottom: 10px;
}

.detail-action-panel__header strong,
.detail-section-title,
.history-card strong {
  color: #24446d;
}

.detail-action-panel__header span {
  display: block;
  margin-top: 4px;
  color: #8093ad;
  font-size: 12px;
}

.detail-action-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 12px;
}

.detail-section-title {
  margin-bottom: 12px;
  font-size: 14px;
  font-weight: 600;
}

.detail-history-panel {
  min-width: 0;
  border: 1px solid rgba(212, 228, 244, 0.95);
  border-radius: 14px;
  background: linear-gradient(180deg, rgba(248, 251, 255, 0.92), rgba(243, 248, 255, 0.98));
  display: flex;
  flex-direction: column;
  min-height: 0;
  max-height: 68vh;
  overflow: hidden;
}

.detail-history-panel__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  padding: 14px 14px 12px;
  border-bottom: 1px solid rgba(212, 228, 244, 0.95);
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.88), rgba(247, 251, 255, 0.96));
}

.detail-history-panel__summary {
  min-width: 0;
  flex: 1;
}

.detail-history-panel__header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.detail-history-panel__subtitle {
  margin: 4px 0 0;
  color: #7f94ae;
  font-size: 12px;
  line-height: 1.4;
}

.detail-history-panel__business-key {
  margin: 2px 0 0;
  color: #6d84a0;
  font-size: 12px;
  line-height: 1.4;
  word-break: break-all;
}

.detail-history-panel__meta {
  color: #7f94ae;
  font-size: 12px;
  min-width: 40px;
  text-align: center;
  white-space: nowrap;
}

.detail-history-panel__body {
  height: calc(100vh - 120px);
  overflow-y: auto;
  padding: 14px;
}

.history-floating-panel {
  position: fixed;
  top: 72px;
  right: 20px;
  width: 340px;
  height: calc(100vh - 96px);
  z-index: 5000;
  display: flex;
  flex-direction: column;
  border: 1px solid rgba(212, 228, 244, 0.95);
  border-radius: 18px 0 0 18px;
  background: rgba(255, 255, 255, 0.98);
  overflow: hidden;
  box-shadow: 0 24px 60px rgba(42, 78, 122, 0.18);
}

.detail-history-panel__body :deep(.el-timeline) {
  margin: 0;
}

.detail-history-panel__body :deep(.el-timeline-item__timestamp) {
  color: #8093ad;
  font-size: 12px;
}

.history-card {
  padding: 10px 12px;
  border: 1px solid rgba(212, 228, 244, 0.95);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 8px 18px rgba(72, 106, 146, 0.06);
}

.history-card p {
  margin: 4px 0 0;
  color: #69809c;
  font-size: 12px;
}

.history-arrow {
  margin: 0 4px;
  color: #4b6d95;
}

@media (max-width: 1080px) {
  .stat-grid,
  .dialog-grid {
    grid-template-columns: 1fr;
  }

  .detail-toolbar {
    flex-direction: column;
    align-items: stretch;
  }

  .detail-toolbar__actions {
    justify-content: space-between;
  }

  .history-floating-panel {
    top: 0;
    right: 0;
    width: min(92vw, 340px);
    height: 100vh;
    border-radius: 0;
  }
}
</style>
