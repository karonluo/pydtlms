<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import { OfficeBuilding, User, Connection, Plus } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'

import TableRowActions, { type TableRowAction } from '../../components/table/TableRowActions.vue'
import { useServerPagination } from '../../composables/useServerPagination'
import { hasGrantedPermission } from '../../router/menuAccess'
import {
  batchDeleteCenters,
  createCenter,
  deleteCenter,
  getStudentOptions,
  listCenters,
  updateCenter,
  type CenterRecord,
  type CenterUpsert,
  type SelectOption,
  type StudentOptions,
} from '../../api/students'
import { useAuthStore } from '../../stores/auth'

const authStore = useAuthStore()
const roleSet = computed(() => new Set(authStore.roles || []))
const isAdvisorRole = computed(() => roleSet.value.has('advisor') && !roleSet.value.has('*'))
const canMaintainCenter = computed(() => hasGrantedPermission(authStore.permissions, 'research_center:write'))

const loading = ref(false)
const bootstrapping = ref(false)
const submitting = ref(false)
const deleteSubmitting = ref(false)

const centers = ref<CenterRecord[]>([])
const advisorOptions = ref<SelectOption[]>([])

const pager = useServerPagination(10)

type FilterState = {
  keyword: string
  is_enabled: '' | 'true' | 'false'
  // 注：按业务需求，导师角色隐藏"中心负责人"筛选条件；未来如需重新启用，恢复下方字段即可。
}

const filters = reactive<FilterState>({
  keyword: '',
  is_enabled: '',
})

const enabledOptions = [
  { label: '启用', value: 'true' },
  { label: '停用', value: 'false' },
]

const dialogVisible = ref(false)
const dialogMode = ref<'create' | 'edit'>('create')
const currentId = ref<number | null>(null)
const centerForm = reactive<CenterUpsert>({
  center_name: '',
  director_ids: [] as Array<string | number>,
  advisor_names: [],
  advisor_ids: [] as Array<string | number>,
  is_enabled: true,
  created_date: new Date().toISOString().slice(0, 10),
})
const formRef = ref<FormInstance>()

const deleteDialogVisible = ref(false)
const deletingCenter = ref<CenterRecord | null>(null)

const selectedCenterIds = ref<number[]>([])

const formRules: FormRules<CenterUpsert> = {
  center_name: [{ required: true, message: '请输入中心名称', trigger: 'blur' }],
  director_ids: [{ required: true, message: '请选择至少一个负责人', trigger: 'change', type: 'array', min: 1 }],
  advisor_ids: [{ required: true, message: '请选择导师团队', trigger: 'change', type: 'array' }],
}

const kpiCenterTotal = computed(() => centers.value.length)
const kpiStudentTotal = computed(() => centers.value.reduce((sum, item) => sum + Number(item.student_count || 0), 0))

const KPI_DEFINITIONS = [
  { key: 'center_total', title: '研究中心总数', value: () => String(kpiCenterTotal.value), tone: 'healthy' as const, icon: OfficeBuilding },
  { key: 'student_total', title: '关联学生总数', value: () => String(kpiStudentTotal.value), tone: 'attention' as const, icon: User },
]

const kpiCards = computed(() =>
  KPI_DEFINITIONS.map((card) => ({
    ...card,
    value: card.value(),
  })),
)

function normalizeBooleanFilter(value: '' | 'true' | 'false'): boolean | undefined {
  if (value === 'true') return true
  if (value === 'false') return false
  return undefined
}

function buildQueryParams() {
  return {
    keyword: filters.keyword || undefined,
    is_enabled: normalizeBooleanFilter(filters.is_enabled),
    // 注：按业务需求，导师角色隐藏"中心负责人"筛选条件；如需启用传 director_ids 即可
    // director_ids: [],
    page: pager.pagination.currentPage,
    page_size: pager.pagination.pageSize,
  }
}

async function fetchCenters() {
  loading.value = true
  try {
    const response = await listCenters(buildQueryParams())
    centers.value = response.data.items
    pager.sync(response.data.total)
  } catch (error) {
    ElMessage.error(extractErrorMessage(error, '加载研究中心失败'))
  } finally {
    loading.value = false
  }
}

async function fetchOptions() {
  try {
    const response = await getStudentOptions()
    const options = response.data as StudentOptions
    advisorOptions.value = (options.center_advisor_options || []).map((item) => ({
      label: item.label,
      value: String(item.value),
    }))
  } catch (error) {
    ElMessage.error(extractErrorMessage(error, '加载导师列表失败'))
  }
}

function extractErrorMessage(error: any, fallback: string): string {
  if (axios.isAxiosError(error)) {
    const data = error.response?.data as { detail?: unknown } | undefined
    const detail = data?.detail
    if (typeof detail === 'string' && detail.trim()) {
      return detail
    }
    if (Array.isArray(detail) && detail.length) {
      const first = detail[0] as { msg?: string; loc?: unknown[] }
      const loc = Array.isArray(first?.loc) ? first.loc.join('.') : ''
      const msg = first?.msg || ''
      if (msg && loc) return `${loc}: ${msg}`
      if (msg) return msg
      return JSON.stringify(detail)
    }
  }
  return fallback
}

function resetForm() {
  currentId.value = null
  Object.assign(centerForm, {
    center_name: '',
    director_ids: [] as Array<string | number>,
    advisor_names: [],
    advisor_ids: [],
    is_enabled: true,
    created_date: new Date().toISOString().slice(0, 10),
  })
  formRef.value?.clearValidate()
}

function openCreateDialog() {
  if (!canMaintainCenter.value) {
    return
  }
  dialogMode.value = 'create'
  resetForm()
  dialogVisible.value = true
}

function openEditDialog(row: CenterRecord) {
  if (!canMaintainCenter.value) {
    return
  }
  dialogMode.value = 'edit'
  currentId.value = row.id
  Object.assign(centerForm, {
    center_name: row.center_name || '',
    director_ids: Array.isArray(row.director_ids)
      ? row.director_ids.map((item) => String(item))
      : (row.director_id ? [String(row.director_id)] : []),
    advisor_names: Array.isArray(row.advisor_names) ? [...row.advisor_names] : [],
    advisor_ids: Array.isArray(row.advisor_ids) ? row.advisor_ids.map((item) => String(item)) : [],
    is_enabled: Boolean(row.is_enabled),
    created_date: row.created_date || new Date().toISOString().slice(0, 10),
  })
  dialogVisible.value = true
}

function normalizePayload(payload: CenterUpsert): CenterUpsert {
  return {
    ...payload,
    center_name: payload.center_name.trim(),
    director_ids: Array.from(new Set((payload.director_ids || []).filter(Boolean).map((item) => String(item)))),
    advisor_ids: Array.from(new Set(payload.advisor_ids.filter(Boolean).map((item) => String(item)))),
    created_date: payload.created_date || new Date().toISOString().slice(0, 10),
  }
}

async function submitDialog() {
  if (!formRef.value) {
    return
  }
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) {
    return
  }
  submitting.value = true
  try {
    const payload = normalizePayload(centerForm)
    if (dialogMode.value === 'create') {
      await createCenter(payload)
      ElMessage.success('研究中心已新增')
    } else if (currentId.value !== null) {
      await updateCenter(currentId.value, payload)
      ElMessage.success('研究中心信息已更新')
    }
    dialogVisible.value = false
    await fetchCenters()
  } catch (error) {
    ElMessage.error(extractErrorMessage(error, '研究中心保存失败'))
  } finally {
    submitting.value = false
  }
}

function openDeleteDialog(row: CenterRecord) {
  if (!canMaintainCenter.value) {
    return
  }
  deletingCenter.value = row
  deleteDialogVisible.value = true
}

function closeDeleteDialog() {
  if (deleteSubmitting.value) {
    return
  }
  deleteDialogVisible.value = false
  deletingCenter.value = null
}

async function submitDeleteDialog() {
  // eslint-disable-next-line no-console
  console.log('[submitDeleteDialog] called, submitting=', deleteSubmitting.value, 'targetId=', deletingCenter.value?.id)
  if (deleteSubmitting.value) {
    // Already running; ignore the second click that may fire during the close animation.
    return
  }
  if (!deletingCenter.value) {
    return
  }
  // Capture id up front; deletingCenter may be cleared by closeDeleteDialog before fetchCenters.
  const targetId = deletingCenter.value.id
  let deleteSucceeded = false
  try {
    deleteSubmitting.value = true
    await deleteCenter(targetId)
    deleteSucceeded = true
    ElMessage.success('研究中心已删除')
  } catch (error) {
    const message = extractErrorMessage(error, '研究中心删除失败')
    ElMessage.error(message)
  } finally {
    deleteSubmitting.value = false
  }
  // Always close the dialog (success OR failure) so the UI does not get stuck.
  closeDeleteDialog()
  // Always refresh the list so a 404 (already-deleted) row is removed from the table.
  try {
    await fetchCenters()
  } catch (fetchError) {
    // ignore: list refresh failure should not block the delete feedback
  }
  // Surface an extra warning if delete returned 404 (row was already gone).
  if (!deleteSucceeded) {
    // The error message was already shown above; nothing more to do here.
  }
}
async function handleBatchDelete() {
  if (!canMaintainCenter.value) {
    return
  }
  if (!selectedCenterIds.value.length) {
    ElMessage.warning('请先勾选要删除的研究中心')
    return
  }
  try {
    await ElMessageBox.confirm(
      `确定批量删除已选 ${selectedCenterIds.value.length} 个研究中心吗？`,
      '批量删除确认',
      { type: 'warning', confirmButtonText: '确定删除', cancelButtonText: '取消' },
    )
  } catch {
    return
  }
  try {
    const response = await batchDeleteCenters(selectedCenterIds.value)
    ElMessage.success(`已删除 ${response.data.success_count} 个研究中心`)
    selectedCenterIds.value = []
    await fetchCenters()
  } catch (error) {
    ElMessage.error(extractErrorMessage(error, '批量删除失败'))
  }
}

function handleSearch() {
  pager.reset()
  void fetchCenters()
}

function handleResetFilters() {
  filters.keyword = ''
  filters.is_enabled = ''
  selectedCenterIds.value = []
  pager.reset()
  void fetchCenters()
}

function handleSelectionChange(rows: CenterRecord[]) {
  selectedCenterIds.value = rows.map((item) => item.id)
}

function handleDirectorsChange(values: Array<string | number>) {
  // Keep every director in the advisor team (mirrors StudentsView behavior).
  const normalized = (values || []).map((item) => String(item)).filter(Boolean)
  centerForm.director_ids = Array.from(new Set(normalized))
  if (normalized.length) {
    const merged = new Set([
      ...centerForm.advisor_ids.map((item) => String(item)),
      ...normalized,
    ])
    centerForm.advisor_ids = Array.from(merged)
  } else if (centerForm.advisor_ids.length) {
    centerForm.director_ids = [String(centerForm.advisor_ids[0])]
  }
}

const tableActions = computed<TableRowAction<CenterRecord>[]>(() =>
  canMaintainCenter.value
    ? [{ key: 'edit', label: '编辑', type: 'primary', onClick: openEditDialog }]
    : [],
)

const tableMoreActions = computed<TableRowAction<CenterRecord>[]>(() =>
  canMaintainCenter.value
    ? [{ key: 'delete', label: '删除', type: 'danger', onClick: openDeleteDialog }]
    : [],
)

const filterCollapsed = ref(false)
function toggleFilterCollapsed() {
  filterCollapsed.value = !filterCollapsed.value
}

onMounted(async () => {
  bootstrapping.value = true
  try {
    await Promise.all([fetchOptions(), fetchCenters()])
  } finally {
    bootstrapping.value = false
  }
})
</script>

<template>
  <section class="camp-offer-page">
    <header class="camp-offer-page__header">
      <div class="camp-offer-page__title">
        <p class="camp-offer-page__tag">学生管理 / 研究中心</p>
        <h2>研究中心</h2>
      </div>
      <div class="camp-offer-kpi-strip">
        <div
          v-for="card in kpiCards"
          :key="card.key"
          class="camp-offer-kpi-tile"
          :data-status="card.tone"
          :title="card.title"
        >
          <el-icon class="camp-offer-kpi-tile__icon">
            <component :is="card.icon" />
          </el-icon>
          <span class="camp-offer-kpi-tile__value">{{ card.value }}</span>
          <span class="camp-offer-kpi-tile__label">{{ card.title }}</span>
        </div>
      </div>
      <div class="camp-offer-page__actions">
        <template v-if="canMaintainCenter">
          <el-button
            type="danger"
            plain
            :disabled="!selectedCenterIds.length || isAdvisorRole"
            @click="handleBatchDelete"
          >
            批量删除
          </el-button>
          <el-button type="primary" @click="openCreateDialog">
            <el-icon style="margin-right: 4px"><Plus /></el-icon>
            新增研究中心
          </el-button>
        </template>
      </div>
    </header>

    <el-card shadow="never" class="filter-card" :class="{ 'is-collapsed': filterCollapsed }">
      <div class="filter-card__head">
        <span class="filter-card__title">筛选条件</span>
        <el-button text class="filter-card__toggle" @click="toggleFilterCollapsed">
          <span>{{ filterCollapsed ? '展开' : '收起' }}</span>
        </el-button>
      </div>
      <el-form v-show="!filterCollapsed" label-width="80px" class="filter-form">
        <div class="filter-row filter-row--primary">
          <el-form-item label="关键字" class="filter-row__item">
            <el-input
              v-model="filters.keyword"
              placeholder="研究中心名称 / 负责人 / 导师团队"
              clearable
              @keyup.enter="handleSearch"
            />
          </el-form-item>
          <el-form-item label="是否启用" class="filter-row__item">
            <el-select v-model="filters.is_enabled" placeholder="全部状态" clearable style="width: 160px">
              <el-option v-for="item in enabledOptions" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>

          <el-form-item class="filter-row__item">
            <el-button type="primary" @click="handleSearch">查询</el-button>
            <el-button @click="handleResetFilters">重置</el-button>
          </el-form-item>
        </div>
      </el-form>
    </el-card>

    <el-table
      :data="centers"
      border
      v-loading="loading || bootstrapping"
      table-layout="fixed"
      @selection-change="handleSelectionChange"
    >
      <el-table-column v-if="canMaintainCenter" type="selection" width="44" />
      <el-table-column prop="center_name" label="研究中心名称" min-width="180" show-overflow-tooltip />
      <el-table-column label="负责人" min-width="160" show-overflow-tooltip>
        <template #default="scope">
          <span :title="(scope.row.directors || []).map((d: { user_id: number; full_name: string }) => d.full_name).join('、')">
            {{ ((scope.row.directors || []).map((d: { user_id: number; full_name: string }) => d.full_name).join('、')) || scope.row.director_name || '未配置' }}
          </span>
        </template>
      </el-table-column>
      <el-table-column label="导师团队" min-width="220" show-overflow-tooltip>
        <template #default="scope">
          <span :title="(scope.row.advisor_names || []).join('、')">
            <el-icon style="vertical-align: -2px; margin-right: 4px"><Connection /></el-icon>
            {{ (scope.row.advisor_names || []).join('、') || '未配置' }}
          </span>
        </template>
      </el-table-column>
      <el-table-column label="学生数" width="100" align="center">
        <template #default="scope">
          <strong>{{ scope.row.student_count ?? 0 }}</strong>
        </template>
      </el-table-column>
      <el-table-column label="是否启用" width="110" align="center">
        <template #default="scope">
          <el-tag :type="scope.row.is_enabled ? 'success' : 'info'">
            {{ scope.row.is_enabled ? '启用' : '停用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_date" label="创建日期" width="120" show-overflow-tooltip />
      <el-table-column v-if="canMaintainCenter" label="操作" width="160" align="left" fixed="right">
        <template #default="scope">
          <TableRowActions
            :row="scope.row"
            :main-actions="tableActions"
            :more-actions="tableMoreActions"
          />
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination-bar">
      <el-pagination
        :current-page="pager.pagination.currentPage"
        :page-size="pager.pagination.pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="pager.pagination.total"
        layout="total, sizes, prev, pager, next, jumper"
        @current-change="pager.handleCurrentChange($event); fetchCenters()"
        @size-change="pager.handleSizeChange($event); fetchCenters()"
      />
    </div>

    <el-dialog
      v-model="dialogVisible"
      :title="dialogMode === 'create' ? '新增研究中心' : '编辑研究中心'"
      width="640px"
      destroy-on-close
      :close-on-click-modal="!submitting"
      :close-on-press-escape="!submitting"
      :show-close="!submitting"
    >
      <el-form ref="formRef" :model="centerForm" :rules="formRules" label-width="96px" class="dialog-form">
        <div class="dialog-grid">
          <el-form-item label="中心名称" prop="center_name">
            <el-input v-model="centerForm.center_name" placeholder="请输入中心名称" />
          </el-form-item>
          <el-form-item label="负责人" prop="director_ids">
            <el-select
              v-model="centerForm.director_ids"
              multiple
              filterable
              collapse-tags
              collapse-tags-tooltip
              placeholder="请选择至少一名负责人"
              @change="handleDirectorsChange"
            >
              <el-option v-for="item in advisorOptions" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
          <el-form-item label="导师团队" prop="advisor_ids" class="dialog-grid--full">
            <el-select v-model="centerForm.advisor_ids" multiple filterable placeholder="请选择导师团队">
              <el-option v-for="item in advisorOptions" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
          <el-form-item label="是否启用">
            <el-switch v-model="centerForm.is_enabled" inline-prompt active-text="启用" inactive-text="停用" />
          </el-form-item>
          <el-form-item label="创建日期">
            <el-date-picker
              v-model="centerForm.created_date"
              type="date"
              value-format="YYYY-MM-DD"
              placeholder="请选择创建日期"
            />
          </el-form-item>
        </div>
      </el-form>
      <template #footer>
        <el-button :disabled="submitting" @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submitDialog">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog
      v-model="deleteDialogVisible"
      title="删除研究中心"
      width="560px"
      destroy-on-close
      :close-on-click-modal="!deleteSubmitting"
      :close-on-press-escape="!deleteSubmitting"
      :show-close="!deleteSubmitting"
      @closed="deletingCenter = null"
    >
      <div v-if="deletingCenter" class="dialog-form">
        <p>确定删除该研究中心吗？删除后不可恢复。</p>
        <ul class="delete-summary">
          <li><span>研究中心</span><strong>{{ deletingCenter.center_name }}</strong></li>
          <li><span>负责人</span><strong>{{ (deletingCenter.directors || []).map((d: { user_id: number; full_name: string }) => d.full_name).join('、') || deletingCenter.director_name || '未配置' }}</strong></li>
          <li><span>学生数</span><strong>{{ deletingCenter.student_count ?? 0 }}</strong></li>
        </ul>
      </div>
      <template #footer>
        <el-button :disabled="deleteSubmitting" @click="closeDeleteDialog">取消</el-button>
        <el-button type="danger" :loading="deleteSubmitting" @click="submitDeleteDialog">确认删除</el-button>
      </template>
    </el-dialog>
  </section>
</template>

<style scoped>
.camp-offer-page {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.camp-offer-page__header {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.camp-offer-page__title {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.camp-offer-page__tag {
  margin: 0;
  font-size: 12px;
  color: var(--el-text-color-secondary);
  letter-spacing: 0.4px;
}

.camp-offer-page__title h2 {
  margin: 0;
  font-size: 22px;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.camp-offer-kpi-strip {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 12px;
}

.camp-offer-kpi-tile {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 16px;
  border-radius: 8px;
  background: var(--el-fill-color-blank);
  border: 1px solid var(--el-border-color-lighter);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
}

.camp-offer-kpi-tile[data-status="healthy"] {
  border-color: var(--el-color-success-light-5);
  background: var(--el-color-success-light-9);
}

.camp-offer-kpi-tile[data-status="attention"] {
  border-color: var(--el-color-warning-light-5);
  background: var(--el-color-warning-light-9);
}

.camp-offer-kpi-tile__icon {
  font-size: 22px;
  color: var(--el-color-primary);
}

.camp-offer-kpi-tile[data-status="healthy"] .camp-offer-kpi-tile__icon {
  color: var(--el-color-success);
}

.camp-offer-kpi-tile[data-status="attention"] .camp-offer-kpi-tile__icon {
  color: var(--el-color-warning);
}

.camp-offer-kpi-tile__value {
  font-size: 22px;
  font-weight: 600;
}

.camp-offer-kpi-tile__label {
  font-size: 12px;
  color: var(--el-text-color-secondary);
  margin-left: auto;
}

.camp-offer-page__actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.filter-card {
  border-radius: 8px;
}

.filter-card__head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.filter-card__title {
  font-weight: 600;
  font-size: 14px;
}

.filter-card.is-collapsed .filter-form {
  display: none;
}

.filter-form {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
}

.filter-row__item {
  margin: 0;
}

.dialog-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.dialog-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px 16px;
}

.dialog-grid--full {
  grid-column: span 2;
}

.pagination-bar {
  display: flex;
  justify-content: flex-end;
  margin-top: 8px;
}

.delete-summary {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px 16px;
}

.delete-summary li {
  display: flex;
  gap: 6px;
  align-items: center;
  font-size: 13px;
  color: var(--el-text-color-regular);
}

.delete-summary li > span {
  color: var(--el-text-color-secondary);
}
</style>