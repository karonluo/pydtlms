<script setup lang="ts">
import axios from 'axios'
import { utils, writeFileXLSX } from 'xlsx'
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRoute } from 'vue-router'
import TableRowActions from '../../components/table/TableRowActions.vue'
import { buildDictColorMap, resolveDictTagType, type DictColorMap } from '../../utils/dictTag'
import { getEmailValidationMessage, getPhoneValidationMessage, normalizeEmail, normalizePhoneNumber } from '../../utils/contactValidation'
import { useServerPagination } from '../../composables/useServerPagination'

import {
  batchDeleteAuditPolicies,
  batchDeleteIntegrations,
  batchDeleteRoles,
  batchDeleteSystemUsers,
  createAuditPolicy,
  createIntegration,
  createRole,
  createSystemUser,
  deleteAuditPolicy,
  deleteIntegration,
  deleteRole,
  deleteSystemUser,
  downloadSystemUserTemplate,
  exportSystemUsers,
  getPermissionCatalog,
  getRoleDeletionPreview,
  getSystemOptions,
  getSystemStats,
  importSystemUserRows,
  listAuditPolicies,
  listIntegrations,
  listNotificationDeliveryLogs,
  listOperationLogs,
  listRoles,
  listSyncLogs,
  listSystemUsers,
  parseSystemUserImportFile,
  updateAuditPolicy,
  updateIntegration,
  updateRole,
  updateSystemUser,
  type AuditPolicyRecord,
  type AuditPolicyUpsert,
  type IntegrationRecord,
  type IntegrationUpsert,
  type NotificationDeliveryLogRecord,
  type OperationLogRecord,
  type PermissionOption,
  type RoleDeletionPreviewResponse,
  type RoleRecord,
  type RoleUpsert,
  type SyncLogRecord,
  type SystemOptions,
  type SystemStats,
  type SystemUserImportIssue,
  type SystemUserImportRow,
  type SystemUserImportParseResult,
  type SystemUserImportResult,
  type SystemUserRecord,
  type SystemUserUpsert,
} from '../../api/system'

const route = useRoute()
const loading = ref(false)
const bootstrapping = ref(false)
const submitting = ref(false)
const exportAllSubmitting = ref(false)
const exportSelectedSubmitting = ref(false)
const importSubmitting = ref(false)
const templateSubmitting = ref(false)
const dialogVisible = ref(false)
const userSaveResultDialogVisible = ref(false)
const userImportDialogVisible = ref(false)
const roleDeleteDialogVisible = ref(false)
const roleBatchDeleteDialogVisible = ref(false)
const dialogMode = ref<'create' | 'edit'>('create')
const currentId = ref<number | null>(null)
const selectedIds = ref<number[]>([])
const userImportInputRef = ref<HTMLInputElement | null>(null)
const systemTagColors = ref<DictColorMap>({})
const userSaveResult = ref<{ title: string; actionLabel: string; username: string; message: string } | null>(null)
const deletingRole = ref<RoleRecord | null>(null)
const roleDeletionPreview = ref<RoleDeletionPreviewResponse | null>(null)
const roleDeleteSubmitting = ref(false)
const roleBatchDeleteSubmitting = ref(false)
const USER_IMPORT_BATCH_SIZE = 20

const userImportState = reactive<{
  file: File | null
  fileName: string
  totalCount: number
  processedCount: number
  createdCount: number
  updatedCount: number
  failedCount: number
  issues: SystemUserImportIssue[]
  phase: 'idle' | 'ready' | 'importing' | 'completed'
}>({
  file: null,
  fileName: '',
  totalCount: 0,
  processedCount: 0,
  createdCount: 0,
  updatedCount: 0,
  failedCount: 0,
  issues: [],
  phase: 'idle',
})

const stats = ref<SystemStats>({
  integration_total: 0,
  active_integration_total: 0,
  operation_log_total: 0,
  sync_failure_total: 0,
  user_total: 0,
  role_total: 0,
})

const systemOptions = ref<SystemOptions>({
  account_status_options: [],
  role_scope_options: [],
  integration_direction_options: [],
  integration_cadence_options: [],
  integration_status_options: [],
  audit_status_options: [],
  operation_result_options: [],
  sync_status_options: [],
})
const permissionCatalog = ref<PermissionOption[]>([])
const roleReferenceList = ref<RoleRecord[]>([])

const users = ref<SystemUserRecord[]>([])
const roles = ref<RoleRecord[]>([])
const policies = ref<AuditPolicyRecord[]>([])
const integrations = ref<IntegrationRecord[]>([])
const operationLogs = ref<OperationLogRecord[]>([])
const notificationDeliveryLogs = ref<NotificationDeliveryLogRecord[]>([])
const syncLogs = ref<SyncLogRecord[]>([])

const userFilters = reactive({
  keyword: '',
  role_code: '',
  account_status: '',
  department_name: '',
})
const roleFilters = reactive({
  keyword: '',
  scope_name: '',
  permission: '',
})
const auditFilters = reactive({
  keyword: '',
  status: '',
})
const integrationFilters = reactive({
  keyword: '',
  status: '',
  direction: '',
})
const operationLogFilters = reactive({
  keyword: '',
  module_name: '',
  result: '',
})
const notificationLogFilters = reactive({
  keyword: '',
  channel: '',
  send_status: '',
})
const syncLogFilters = reactive({
  keyword: '',
  sync_status: '',
  source_system: '',
})

const userForm = reactive<SystemUserUpsert>({
  username: '',
  full_name: '',
  role_code: '',
  department_name: '',
  introduction: '',
  email: '',
  phone_number: '',
  account_status: '启用',
  password: '',
})
const roleForm = reactive<RoleUpsert>({
  role_code: '',
  role_name: '',
  scope_name: '',
  permissions: [],
})
const policyForm = reactive<AuditPolicyUpsert>({
  item: '',
  policy: '',
  status: '启用',
})
const integrationForm = reactive<IntegrationUpsert>({
  name: '',
  direction: '',
  cadence: '',
  status: '正常',
  owner: '',
})

const sectionMeta: Record<string, { title: string; tag: string; createLabel: string; batchDeleteLabel: string }> = {
  users: { title: '系统用户管理', tag: '身份治理', createLabel: '新建系统账号', batchDeleteLabel: '批量删除账号' },
  roles: { title: '角色权限管理', tag: '授权治理', createLabel: '新建角色', batchDeleteLabel: '批量删除角色' },
  audit: { title: '审计策略管理', tag: '审计治理', createLabel: '新建审计策略', batchDeleteLabel: '批量删除策略' },
  integrations: { title: '集成链路管理', tag: '接口治理', createLabel: '新建集成链路', batchDeleteLabel: '批量删除链路' },
  'operation-logs': { title: '操作日志查询', tag: '审计追踪', createLabel: '', batchDeleteLabel: '' },
  'notification-logs': { title: '通知发送日志', tag: '通知追踪', createLabel: '', batchDeleteLabel: '' },
  'sync-logs': { title: '同步日志查询', tag: '数据追踪', createLabel: '', batchDeleteLabel: '' },
}

const activeSection = computed(() => String(route.meta.section || 'users'))
const sectionConfig = computed(() => sectionMeta[activeSection.value] || sectionMeta.users)
const editableSection = computed(() => ['users', 'roles', 'audit', 'integrations'].includes(activeSection.value))
const currentTotal = computed(() => {
  if (activeSection.value === 'users') return userPager.pagination.total
  if (activeSection.value === 'roles') return rolePager.pagination.total
  if (activeSection.value === 'audit') return auditPager.pagination.total
  if (activeSection.value === 'integrations') return integrationPager.pagination.total
  if (activeSection.value === 'operation-logs') return operationLogPager.pagination.total
  if (activeSection.value === 'notification-logs') return notificationLogPager.pagination.total
  return syncLogPager.pagination.total
})
const statCards = computed(() => [
  { label: '系统账号', value: stats.value.user_total, tone: 'healthy' },
  { label: '角色总数', value: stats.value.role_total, tone: 'neutral' },
  { label: '正常链路', value: stats.value.active_integration_total, tone: 'attention' },
  { label: '同步失败', value: stats.value.sync_failure_total, tone: 'warning' },
])
const permissionGroups = computed(() => {
  const groups = new Map<string, PermissionOption[]>()
  permissionCatalog.value.forEach((item) => {
    const current = groups.get(item.module_name) || []
    current.push(item)
    groups.set(item.module_name, current)
  })
  return Array.from(groups.entries()).map(([moduleName, items]) => ({ moduleName, items }))
})
const roleOptions = computed(() => roleReferenceList.value.map((item) => ({ label: item.role_name, value: item.role_code })))
const departmentOptions = computed(() => {
  const values = Array.from(new Set(users.value.map((item) => item.department_name).filter(Boolean)))
  return values.map((item) => ({ label: item, value: item }))
})
const operationModuleOptions = computed(() => {
  const values = Array.from(new Set(operationLogs.value.map((item) => item.module_name).filter(Boolean)))
  return values.map((item) => ({ label: item, value: item }))
})
const syncSourceOptions = computed(() => {
  const values = Array.from(new Set(syncLogs.value.map((item) => item.source_system).filter(Boolean)))
  return values.map((item) => ({ label: item, value: item }))
})
const notificationChannelOptions = computed(() => {
  const values = Array.from(new Set(notificationDeliveryLogs.value.map((item) => item.channel).filter(Boolean)))
  if (!values.includes('email')) values.unshift('email')
  return values.map((item) => ({ label: item === 'email' ? '邮件' : item, value: item }))
})
const operationResultOptions = computed(() => {
  const options = [...systemOptions.value.operation_result_options]
  if (!options.some((item) => item.value === 'timeout')) {
    options.push({ label: '超时', value: 'timeout' })
  }
  return options
})
const notificationStatusOptions = [
  { label: '成功', value: 'success' },
  { label: '失败', value: 'failed' },
  { label: '已跳过', value: 'skipped' },
]
const userImportProgressPercentage = computed(() => {
  if (userImportState.totalCount <= 0) {
    return 0
  }
  return Math.min(100, Math.round((userImportState.processedCount / userImportState.totalCount) * 100))
})
const userImportStatusText = computed(() => {
  if (userImportState.phase === 'importing') {
    return '正在导入系统用户'
  }
  if (userImportState.phase === 'completed') {
    return userImportState.failedCount > 0 ? '导入完成，存在失败记录' : '导入完成'
  }
  if (userImportState.fileName) {
    return '已选择文件，点击开始导入'
  }
  return '请先在弹窗中选择要导入的 Excel 文件'
})
const userImportIssuePreview = computed(() => userImportState.issues.slice(0, 5))
const userPager = useServerPagination()
const rolePager = useServerPagination()
const auditPager = useServerPagination()
const integrationPager = useServerPagination()
const operationLogPager = useServerPagination()
const notificationLogPager = useServerPagination()
const syncLogPager = useServerPagination()

function getErrorMessage(error: unknown) {
  if (axios.isAxiosError(error)) {
    if (error.code === 'ECONNABORTED' || String(error.message || '').toLowerCase().includes('timeout')) {
      return '请求超时。系统用户导入文件较大或服务器处理较慢，请稍后重试。'
    }
    return String(error.response?.data?.detail || error.message || '请求失败')
  }
  return '请求失败'
}

function openUserSaveResultDialog(title: string, actionLabel: string, username: string, message: string) {
  userSaveResult.value = {
    title,
    actionLabel,
    username,
    message,
  }
  userSaveResultDialogVisible.value = true
}

function resetSelection() {
  selectedIds.value = []
}

function resetUserImportState() {
  userImportState.file = null
  userImportState.fileName = ''
  userImportState.totalCount = 0
  userImportState.processedCount = 0
  userImportState.createdCount = 0
  userImportState.updatedCount = 0
  userImportState.failedCount = 0
  userImportState.issues = []
  userImportState.phase = 'idle'
  if (userImportInputRef.value) {
    userImportInputRef.value.value = ''
  }
}

function openUserImportDialog() {
  if (activeSection.value !== 'users') {
    return
  }
  resetUserImportState()
  userImportDialogVisible.value = true
}

function triggerUserImportFileSelect() {
  userImportInputRef.value?.click()
}

function chunkSystemUserImportRows(rows: SystemUserImportRow[], batchSize: number) {
  const batches: SystemUserImportRow[][] = []
  for (let index = 0; index < rows.length; index += batchSize) {
    batches.push(rows.slice(index, index + batchSize))
  }
  return batches
}

function getUserImportProgressStatus() {
  if (userImportState.phase !== 'completed') {
    return undefined
  }
  return userImportState.failedCount > 0 ? 'warning' : 'success'
}

function exportUserImportIssues() {
  if (userImportState.issues.length === 0) {
    ElMessage.warning('当前没有可导出的失败明细')
    return
  }

  const worksheet = utils.json_to_sheet(
    userImportState.issues.map((item) => ({
      行号: item.row_number,
      姓名: item.full_name || '',
      账号: item.username || '',
      失败原因: item.reason,
    })),
  )
  const workbook = utils.book_new()
  utils.book_append_sheet(workbook, worksheet, '失败明细')
  writeFileXLSX(workbook, `系统用户导入失败明细_${new Date().toISOString().slice(0, 19).replace(/[-:T]/g, '')}.xlsx`)
  ElMessage.success('导入失败明细已导出')
}

function resetForms() {
  currentId.value = null
  Object.assign(userForm, {
    username: '',
    full_name: '',
    role_code: '',
    department_name: '',
    introduction: '',
    email: '',
    phone_number: '',
    account_status: '启用',
    password: '',
  })
  Object.assign(roleForm, {
    role_code: '',
    role_name: '',
    scope_name: '',
    permissions: [],
  })
  Object.assign(policyForm, {
    item: '',
    policy: '',
    status: '启用',
  })
  Object.assign(integrationForm, {
    name: '',
    direction: '',
    cadence: '',
    status: '正常',
    owner: '',
  })
}

function resetFilters() {
  Object.assign(userFilters, { keyword: '', role_code: '', account_status: '', department_name: '' })
  Object.assign(roleFilters, { keyword: '', scope_name: '', permission: '' })
  Object.assign(auditFilters, { keyword: '', status: '' })
  Object.assign(integrationFilters, { keyword: '', status: '', direction: '' })
  Object.assign(operationLogFilters, { keyword: '', module_name: '', result: '' })
  Object.assign(syncLogFilters, { keyword: '', sync_status: '', source_system: '' })
}

async function loadStats() {
  const response = await getSystemStats()
  stats.value = response.data
}

async function loadRoleReferences() {
  const response = await listRoles({ page: 1, page_size: 1000 })
  roleReferenceList.value = response.data.items
}

async function loadBootstrapData() {
  bootstrapping.value = true
  try {
    const [statsResponse, optionResponse, permissionResponse, roleResponse] = await Promise.all([
      getSystemStats(),
      getSystemOptions(),
      getPermissionCatalog(),
      listRoles({ page: 1, page_size: 1000 }),
    ])
    stats.value = statsResponse.data
    systemOptions.value = optionResponse.data
    permissionCatalog.value = permissionResponse.data.items
    roleReferenceList.value = roleResponse.data.items
    systemTagColors.value = {
      ...buildDictColorMap(optionResponse.data.account_status_options),
      ...buildDictColorMap(optionResponse.data.integration_status_options),
      ...buildDictColorMap(optionResponse.data.audit_status_options),
      ...buildDictColorMap(optionResponse.data.operation_result_options),
      ...buildDictColorMap(optionResponse.data.sync_status_options),
    }
  } finally {
    bootstrapping.value = false
  }
}

async function loadSectionData() {
  loading.value = true
  try {
    if (activeSection.value === 'users') {
      const response = await listSystemUsers({
        keyword: userFilters.keyword || undefined,
        role_code: userFilters.role_code || undefined,
        account_status: userFilters.account_status || undefined,
        department_name: userFilters.department_name || undefined,
        page: userPager.pagination.currentPage,
        page_size: userPager.pagination.pageSize,
      })
      users.value = response.data.items
      userPager.sync(response.data.total)
      return
    }
    if (activeSection.value === 'roles') {
      const response = await listRoles({
        keyword: roleFilters.keyword || undefined,
        scope_name: roleFilters.scope_name || undefined,
        permission: roleFilters.permission || undefined,
        page: rolePager.pagination.currentPage,
        page_size: rolePager.pagination.pageSize,
      })
      roles.value = response.data.items
      rolePager.sync(response.data.total)
      return
    }
    if (activeSection.value === 'audit') {
      const response = await listAuditPolicies({
        keyword: auditFilters.keyword || undefined,
        status: auditFilters.status || undefined,
        page: auditPager.pagination.currentPage,
        page_size: auditPager.pagination.pageSize,
      })
      policies.value = response.data.items
      auditPager.sync(response.data.total)
      return
    }
    if (activeSection.value === 'integrations') {
      const response = await listIntegrations({
        keyword: integrationFilters.keyword || undefined,
        status: integrationFilters.status || undefined,
        direction: integrationFilters.direction || undefined,
        page: integrationPager.pagination.currentPage,
        page_size: integrationPager.pagination.pageSize,
      })
      integrations.value = response.data.items
      integrationPager.sync(response.data.total)
      return
    }
    if (activeSection.value === 'operation-logs') {
      const response = await listOperationLogs({
        keyword: operationLogFilters.keyword || undefined,
        module_name: operationLogFilters.module_name || undefined,
        result: operationLogFilters.result || undefined,
        page: operationLogPager.pagination.currentPage,
        page_size: operationLogPager.pagination.pageSize,
      })
      operationLogs.value = response.data.items
      operationLogPager.sync(response.data.total)
      return
    }
    if (activeSection.value === 'notification-logs') {
      const response = await listNotificationDeliveryLogs({
        keyword: notificationLogFilters.keyword || undefined,
        channel: notificationLogFilters.channel || undefined,
        send_status: notificationLogFilters.send_status || undefined,
        page: notificationLogPager.pagination.currentPage,
        page_size: notificationLogPager.pagination.pageSize,
      })
      notificationDeliveryLogs.value = response.data.items
      notificationLogPager.sync(response.data.total)
      return
    }
    const response = await listSyncLogs({
      keyword: syncLogFilters.keyword || undefined,
      sync_status: syncLogFilters.sync_status || undefined,
      source_system: syncLogFilters.source_system || undefined,
      page: syncLogPager.pagination.currentPage,
      page_size: syncLogPager.pagination.pageSize,
    })
    syncLogs.value = response.data.items
    syncLogPager.sync(response.data.total)
  } finally {
    loading.value = false
  }
}

async function refreshAfterMutation(reloadRoles = false) {
  await loadStats()
  if (reloadRoles) {
    await loadRoleReferences()
  }
  await loadSectionData()
}

function openCreateDialog() {
  dialogMode.value = 'create'
  resetForms()
  dialogVisible.value = true
}

function openEditDialog(row: SystemUserRecord | RoleRecord | AuditPolicyRecord | IntegrationRecord) {
  dialogMode.value = 'edit'
  currentId.value = row.id
  if (activeSection.value === 'users') {
    const user = row as SystemUserRecord
    Object.assign(userForm, {
      username: user.username,
      full_name: user.full_name,
      role_code: user.role_code,
      department_name: user.department_name,
      introduction: user.introduction || '',
      email: user.email || '',
      phone_number: user.phone_number || '',
      account_status: user.account_status,
      password: '',
    })
  } else if (activeSection.value === 'roles') {
    const role = row as RoleRecord
    Object.assign(roleForm, {
      role_code: role.role_code,
      role_name: role.role_name,
      scope_name: role.scope_name,
      permissions: [...role.permissions],
    })
  } else if (activeSection.value === 'audit') {
    const policy = row as AuditPolicyRecord
    Object.assign(policyForm, {
      item: policy.item,
      policy: policy.policy,
      status: policy.status,
    })
  } else {
    const integration = row as IntegrationRecord
    Object.assign(integrationForm, {
      name: integration.name,
      direction: integration.direction,
      cadence: integration.cadence,
      status: integration.status,
      owner: integration.owner,
    })
  }
  dialogVisible.value = true
}

function validateForm() {
  if (activeSection.value === 'users') {
    if (!userForm.username || !userForm.full_name || !userForm.role_code || !userForm.account_status) {
      ElMessage.warning('请完整填写系统账号信息')
      return false
    }
    if (userForm.role_code === 'advisor' && !String(userForm.introduction || '').trim()) {
      ElMessage.warning('角色为导师时必须填写介绍')
      return false
    }
    const emailValidationMessage = getEmailValidationMessage(userForm.email || '', dialogMode.value === 'edit')
    if (emailValidationMessage) {
      ElMessage.warning(emailValidationMessage)
      return false
    }
    const phoneValidationMessage = getPhoneValidationMessage(userForm.phone_number || '', dialogMode.value === 'edit')
    if (phoneValidationMessage) {
      ElMessage.warning(phoneValidationMessage)
      return false
    }
    return true
  }
  if (activeSection.value === 'roles') {
    if (!roleForm.role_code || !roleForm.role_name || !roleForm.scope_name || roleForm.permissions.length === 0) {
      ElMessage.warning('请完整配置角色名称、范围和权限')
      return false
    }
    return true
  }
  if (activeSection.value === 'audit') {
    if (!policyForm.item || !policyForm.policy || !policyForm.status) {
      ElMessage.warning('请完整填写审计策略信息')
      return false
    }
    return true
  }
  if (!integrationForm.name || !integrationForm.direction || !integrationForm.cadence || !integrationForm.status || !integrationForm.owner) {
    ElMessage.warning('请完整填写集成链路信息')
    return false
  }
  return true
}

function isSystemUserFieldRequired(field: 'username' | 'full_name' | 'role_code' | 'account_status' | 'email' | 'phone_number' | 'introduction') {
  if (field === 'introduction') {
    return userForm.role_code === 'advisor'
  }
  if (field === 'email' || field === 'phone_number') {
    return dialogMode.value === 'edit'
  }
  return true
}

async function submit() {
  if (!validateForm()) {
    return
  }

  submitting.value = true
  try {
    if (activeSection.value === 'users') {
      const payload: SystemUserUpsert = {
        ...userForm,
        introduction: userForm.introduction?.trim() || undefined,
        email: normalizeEmail(userForm.email || ''),
        phone_number: normalizePhoneNumber(userForm.phone_number || ''),
        password: userForm.password?.trim() || undefined,
      }
      if (dialogMode.value === 'create') {
        await createSystemUser(payload)
        dialogVisible.value = false
        await refreshAfterMutation(true)
        openUserSaveResultDialog('保存成功', '新建账号', payload.username, '系统账号已创建。')
      } else if (currentId.value !== null) {
        await updateSystemUser(currentId.value, payload)
        dialogVisible.value = false
        await refreshAfterMutation(true)
        openUserSaveResultDialog('保存成功', '维护账号', payload.username, '系统账号已更新。')
      }
      return
    }

    if (activeSection.value === 'roles') {
      const payload: RoleUpsert = {
        ...roleForm,
        permissions: [...roleForm.permissions],
      }
      if (dialogMode.value === 'create') {
        await createRole(payload)
        ElMessage.success('角色已创建')
      } else if (currentId.value !== null) {
        await updateRole(currentId.value, payload)
        ElMessage.success('角色权限已更新')
      }
      dialogVisible.value = false
      await refreshAfterMutation(true)
      return
    }

    if (activeSection.value === 'audit') {
      if (dialogMode.value === 'create') {
        await createAuditPolicy(policyForm)
        ElMessage.success('审计策略已创建')
      } else if (currentId.value !== null) {
        await updateAuditPolicy(currentId.value, policyForm)
        ElMessage.success('审计策略已更新')
      }
      dialogVisible.value = false
      await refreshAfterMutation()
      return
    }

    if (dialogMode.value === 'create') {
      await createIntegration(integrationForm)
      ElMessage.success('集成链路已创建')
    } else if (currentId.value !== null) {
      await updateIntegration(currentId.value, integrationForm)
      ElMessage.success('集成链路已更新')
    }
    dialogVisible.value = false
    await refreshAfterMutation()
  } catch (error) {
    const message = getErrorMessage(error)
    if (activeSection.value === 'users') {
      openUserSaveResultDialog(
        '保存失败',
        dialogMode.value === 'create' ? '新建账号' : '维护账号',
        userForm.username || '未填写账号',
        `系统账号保存失败：${message}`,
      )
      return
    }
    ElMessage.error(message)
  } finally {
    submitting.value = false
  }
}

watch(() => userSaveResultDialogVisible.value, (visible) => {
  if (!visible) {
    userSaveResult.value = null
  }
})

async function handleDelete(row: SystemUserRecord | RoleRecord | AuditPolicyRecord | IntegrationRecord) {
  const targetName = activeSection.value === 'users'
    ? (row as SystemUserRecord).full_name
    : activeSection.value === 'roles'
      ? (row as RoleRecord).role_name
      : activeSection.value === 'audit'
        ? (row as AuditPolicyRecord).item
        : (row as IntegrationRecord).name

  if (activeSection.value === 'roles') {
    try {
      const role = row as RoleRecord
      const preview = (await getRoleDeletionPreview(role.id)).data
      deletingRole.value = role
      roleDeletionPreview.value = preview
      roleDeleteDialogVisible.value = true
    } catch (error) {
      ElMessage.error(getErrorMessage(error))
    }
    return
  }

  await ElMessageBox.confirm(`确定删除 ${targetName} 吗？`, '删除确认', { type: 'warning' })

  try {
    if (activeSection.value === 'users') {
      await deleteSystemUser(row.id)
      ElMessage.success('系统账号已删除')
      await refreshAfterMutation(true)
      return
    }
    if (activeSection.value === 'roles') {
      await deleteRole(row.id)
      ElMessage.success('角色已删除')
      await refreshAfterMutation(true)
      return
    }
    if (activeSection.value === 'audit') {
      await deleteAuditPolicy(row.id)
      ElMessage.success('审计策略已删除')
      await refreshAfterMutation()
      return
    }
    await deleteIntegration(row.id)
    ElMessage.success('集成链路已删除')
    await refreshAfterMutation()
  } catch (error) {
    ElMessage.error(getErrorMessage(error))
  }
}

async function handleBatchDelete() {
  if (selectedIds.value.length === 0) {
    ElMessage.warning('请先选择要删除的数据')
    return
  }

  if (activeSection.value === 'roles') {
    roleBatchDeleteDialogVisible.value = true
    return
  }

  await ElMessageBox.confirm(`已选择 ${selectedIds.value.length} 条记录，确认批量删除吗？`, '批量删除确认', { type: 'warning' })

  try {
    if (activeSection.value === 'users') {
      await batchDeleteSystemUsers(selectedIds.value)
      ElMessage.success('所选系统账号已删除')
      resetSelection()
      await refreshAfterMutation(true)
      return
    }
    if (activeSection.value === 'roles') {
      await batchDeleteRoles(selectedIds.value)
      ElMessage.success('所选角色已删除')
      resetSelection()
      await refreshAfterMutation(true)
      return
    }
    if (activeSection.value === 'audit') {
      await batchDeleteAuditPolicies(selectedIds.value)
      ElMessage.success('所选审计策略已删除')
      resetSelection()
      await refreshAfterMutation()
      return
    }
    await batchDeleteIntegrations(selectedIds.value)
    ElMessage.success('所选集成链路已删除')
    resetSelection()
    await refreshAfterMutation()
  } catch (error) {
    ElMessage.error(getErrorMessage(error))
  }
}

async function submitRoleDeleteDialog() {
  if (!deletingRole.value) {
    roleDeleteDialogVisible.value = false
    return
  }
  if (roleDeletionPreview.value && !roleDeletionPreview.value.can_force_delete) {
    ElMessage.warning('该角色仍有用户未配置其他角色，请先重新配置后再删除')
    return
  }
  roleDeleteSubmitting.value = true
  try {
    await deleteRole(deletingRole.value.id, true)
    ElMessage.success('角色已删除')
    roleDeleteDialogVisible.value = false
    deletingRole.value = null
    roleDeletionPreview.value = null
    resetSelection()
    await refreshAfterMutation(true)
  } catch (error) {
    ElMessage.error(getErrorMessage(error))
  } finally {
    roleDeleteSubmitting.value = false
  }
}

async function submitRoleBatchDeleteDialog() {
  roleBatchDeleteSubmitting.value = true
  try {
    await batchDeleteRoles(selectedIds.value)
    ElMessage.success('所选角色已删除')
    roleBatchDeleteDialogVisible.value = false
    resetSelection()
    await refreshAfterMutation(true)
  } catch (error) {
    ElMessage.error(getErrorMessage(error))
  } finally {
    roleBatchDeleteSubmitting.value = false
  }
}

async function handleUserExport(mode: 'filtered' | 'selected') {
  if (activeSection.value !== 'users') {
    return
  }
  if (mode === 'selected' && selectedIds.value.length === 0) {
    ElMessage.warning('请先选择要导出的系统用户')
    return
  }

  const loadingRef = mode === 'selected' ? exportSelectedSubmitting : exportAllSubmitting
  loadingRef.value = true
  try {
    const response = await exportSystemUsers(
      mode === 'selected'
        ? { ids: selectedIds.value }
        : {
            keyword: userFilters.keyword || undefined,
            role_code: userFilters.role_code || undefined,
            account_status: userFilters.account_status || undefined,
            department_name: userFilters.department_name || undefined,
          },
    )
    const blob = new Blob([response.data], {
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    const disposition = String(response.headers['content-disposition'] || '')
    const matched = disposition.match(/filename\*=UTF-8''([^;]+)/)
    link.href = url
    link.download = matched ? decodeURIComponent(matched[1]) : '系统用户导出.xlsx'
    document.body.append(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
    ElMessage.success(mode === 'selected' ? '选中系统用户已导出' : '系统用户筛选结果已导出')
  } catch (error) {
    ElMessage.error(getErrorMessage(error))
  } finally {
    loadingRef.value = false
  }
}

function handleUserImport(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) {
    return
  }

  userImportState.file = file
  userImportState.fileName = file.name
  userImportState.totalCount = 0
  userImportState.processedCount = 0
  userImportState.createdCount = 0
  userImportState.updatedCount = 0
  userImportState.failedCount = 0
  userImportState.issues = []
  userImportState.phase = 'ready'
}

async function submitUserImport() {
  if (!userImportState.file) {
    ElMessage.warning('请先选择要导入的 Excel 文件')
    return
  }

  importSubmitting.value = true
  try {
    userImportState.totalCount = 0
    userImportState.processedCount = 0
    userImportState.createdCount = 0
    userImportState.updatedCount = 0
    userImportState.failedCount = 0
    userImportState.issues = []
    userImportState.phase = 'importing'

    const parsedResponse = await parseSystemUserImportFile(userImportState.file)
    const parsedResult: SystemUserImportParseResult = parsedResponse.data
    const rows = parsedResult.rows
    userImportState.totalCount = parsedResult.total_count
    if (rows.length === 0) {
      userImportState.phase = 'ready'
      ElMessage.warning('导入文件中没有可处理的系统用户数据')
      return
    }

    const batches = chunkSystemUserImportRows(rows, USER_IMPORT_BATCH_SIZE)
    for (const batch of batches) {
      const response = await importSystemUserRows(batch)
      const result: SystemUserImportResult = response.data
      userImportState.processedCount += result.total_count
      userImportState.createdCount += result.created_count
      userImportState.updatedCount += result.updated_count
      userImportState.failedCount += result.failed_count
      userImportState.issues.push(...result.issues)
    }

    userImportState.phase = 'completed'
    resetSelection()
    await refreshAfterMutation(true)

    if (userImportState.failedCount > 0) {
      const topIssues = userImportState.issues.slice(0, 3).map((item) => `${item.full_name || '未命名'}${item.username ? `(${item.username})` : ''}：${item.reason}`)
      ElMessage.warning(`系统用户导入完成，新增 ${userImportState.createdCount} 条，更新 ${userImportState.updatedCount} 条，失败 ${userImportState.failedCount} 条。${topIssues.join('；')}`)
    } else {
      ElMessage.success(`系统用户导入完成，新增 ${userImportState.createdCount} 条，更新 ${userImportState.updatedCount} 条。全部成功`)
    }
  } catch (error) {
    userImportState.phase = userImportState.processedCount > 0 ? 'completed' : 'ready'
    ElMessage.error(getErrorMessage(error))
  } finally {
    importSubmitting.value = false
  }
}

async function handleUserTemplateDownload() {
  templateSubmitting.value = true
  try {
    const response = await downloadSystemUserTemplate()
    const blob = new Blob([response.data], {
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    const disposition = String(response.headers['content-disposition'] || '')
    const matched = disposition.match(/filename\*=UTF-8''([^;]+)/)
    link.href = url
    link.download = matched ? decodeURIComponent(matched[1]) : '系统用户导入模板.xlsx'
    document.body.append(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
    ElMessage.success('系统用户导入模板已下载')
  } catch (error) {
    ElMessage.error(getErrorMessage(error))
  } finally {
    templateSubmitting.value = false
  }
}

async function handleSearch() {
  try {
    if (activeSection.value === 'users') userPager.reset()
    else if (activeSection.value === 'roles') rolePager.reset()
    else if (activeSection.value === 'audit') auditPager.reset()
    else if (activeSection.value === 'integrations') integrationPager.reset()
    else if (activeSection.value === 'operation-logs') operationLogPager.reset()
    else if (activeSection.value === 'notification-logs') notificationLogPager.reset()
    else syncLogPager.reset()
    await loadSectionData()
  } catch (error) {
    ElMessage.error(getErrorMessage(error))
  }
}

async function handleReset() {
  resetFilters()
  userPager.reset()
  rolePager.reset()
  auditPager.reset()
  integrationPager.reset()
  operationLogPager.reset()
  notificationLogPager.reset()
  syncLogPager.reset()
  await handleSearch()
}

async function handleUserPageChange(page: number) {
  userPager.handleCurrentChange(page)
  await loadSectionData()
}

async function handleUserPageSizeChange(size: number) {
  userPager.handleSizeChange(size)
  await loadSectionData()
}

async function handleRolePageChange(page: number) {
  rolePager.handleCurrentChange(page)
  await loadSectionData()
}

async function handleRolePageSizeChange(size: number) {
  rolePager.handleSizeChange(size)
  await loadSectionData()
}

async function handleAuditPageChange(page: number) {
  auditPager.handleCurrentChange(page)
  await loadSectionData()
}

async function handleAuditPageSizeChange(size: number) {
  auditPager.handleSizeChange(size)
  await loadSectionData()
}

async function handleIntegrationPageChange(page: number) {
  integrationPager.handleCurrentChange(page)
  await loadSectionData()
}

async function handleIntegrationPageSizeChange(size: number) {
  integrationPager.handleSizeChange(size)
  await loadSectionData()
}

async function handleOperationLogPageChange(page: number) {
  operationLogPager.handleCurrentChange(page)
  await loadSectionData()
}

async function handleOperationLogPageSizeChange(size: number) {
  operationLogPager.handleSizeChange(size)
  await loadSectionData()
}

async function handleNotificationLogPageChange(page: number) {
  notificationLogPager.handleCurrentChange(page)
  await loadSectionData()
}

async function handleNotificationLogPageSizeChange(size: number) {
  notificationLogPager.handleSizeChange(size)
  await loadSectionData()
}

async function handleSyncLogPageChange(page: number) {
  syncLogPager.handleCurrentChange(page)
  await loadSectionData()
}

async function handleSyncLogPageSizeChange(size: number) {
  syncLogPager.handleSizeChange(size)
  await loadSectionData()
}

function handleSelectionChange(rows: Array<{ id: number }>) {
  selectedIds.value = rows.map((item) => item.id)
}

function getTagType(status: string) {
  return resolveDictTagType(status, systemTagColors.value)
}

function resultLabel(value: string) {
  return value === 'success' ? '成功' : value === 'failed' ? '失败' : value === 'timeout' ? '超时' : value === 'skipped' ? '已跳过' : value
}

watch(
  () => activeSection.value,
  async () => {
    resetFilters()
    resetSelection()
    dialogVisible.value = false
    userImportDialogVisible.value = false
    resetUserImportState()
    await loadSectionData()
  },
)

watch(
  () => userImportDialogVisible.value,
  (visible) => {
    if (!visible && !importSubmitting.value) {
      resetUserImportState()
    }
  },
)

onMounted(async () => {
  try {
    await loadBootstrapData()
    await loadSectionData()
  } catch (error) {
    ElMessage.error(getErrorMessage(error))
  }
})
</script>

<template>
  <section class="content-stack">
    <section class="state-grid">
      <article v-for="card in statCards" :key="card.label" class="state-card" :data-tone="card.tone">
        <p>{{ card.label }}</p>
        <strong>{{ card.value }}</strong>
      </article>
    </section>

    <article class="section-card" v-loading="bootstrapping">
      <div class="section-card__header">
        <div>
          <p class="section-tag">{{ sectionConfig.tag }}</p>
          <h2>{{ sectionConfig.title }}</h2>
        </div>
        <div class="header-actions">
          <span class="summary-text">当前共 {{ currentTotal }} 条记录</span>
          <el-button
            v-if="activeSection === 'users'"
            plain
            :loading="templateSubmitting"
            @click="handleUserTemplateDownload"
          >
            下载导入模板
          </el-button>
          <el-button
            v-if="activeSection === 'users'"
            plain
            :loading="importSubmitting"
            @click="openUserImportDialog"
          >
            导入用户
          </el-button>
          <el-button
            v-if="activeSection === 'users'"
            plain
            :loading="exportAllSubmitting"
            @click="handleUserExport('filtered')"
          >
            导出筛选结果
          </el-button>
          <el-button
            v-if="activeSection === 'users'"
            plain
            :disabled="selectedIds.length === 0"
            :loading="exportSelectedSubmitting"
            @click="handleUserExport('selected')"
          >
            导出选中
          </el-button>
          <el-button v-if="editableSection" type="danger" plain :disabled="selectedIds.length === 0" @click="handleBatchDelete">
            {{ sectionConfig.batchDeleteLabel }}
          </el-button>
          <el-button v-if="editableSection" type="primary" round @click="openCreateDialog">
            {{ sectionConfig.createLabel }}
          </el-button>
        </div>
      </div>

      <el-form v-if="activeSection === 'users'" class="filter-form" :inline="true">
        <el-form-item label="关键字">
          <el-input v-model="userFilters.keyword" placeholder="账号 / 姓名 / 部门" clearable />
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="userFilters.role_code" placeholder="全部角色" clearable filterable style="width: 180px">
            <el-option v-for="item in roleOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="账号状态">
          <el-select v-model="userFilters.account_status" placeholder="全部状态" clearable style="width: 160px">
            <el-option v-for="item in systemOptions.account_status_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="所属部门">
          <el-select v-model="userFilters.department_name" placeholder="全部部门" clearable filterable style="width: 200px">
            <el-option v-for="item in departmentOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <el-form v-else-if="activeSection === 'roles'" class="filter-form" :inline="true">
        <el-form-item label="关键字">
          <el-input v-model="roleFilters.keyword" placeholder="角色编码 / 角色名称" clearable />
        </el-form-item>
        <el-form-item label="适用范围">
          <el-select v-model="roleFilters.scope_name" placeholder="全部范围" clearable style="width: 180px">
            <el-option v-for="item in systemOptions.role_scope_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="包含权限">
          <el-select v-model="roleFilters.permission" placeholder="全部权限" clearable filterable style="width: 220px">
            <el-option v-for="item in permissionCatalog" :key="item.code" :label="item.name" :value="item.code" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <el-form v-else-if="activeSection === 'audit'" class="filter-form" :inline="true">
        <el-form-item label="关键字">
          <el-input v-model="auditFilters.keyword" placeholder="审计项 / 策略描述" clearable />
        </el-form-item>
        <el-form-item label="策略状态">
          <el-select v-model="auditFilters.status" placeholder="全部状态" clearable style="width: 160px">
            <el-option v-for="item in systemOptions.audit_status_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <el-form v-else-if="activeSection === 'integrations'" class="filter-form" :inline="true">
        <el-form-item label="关键字">
          <el-input v-model="integrationFilters.keyword" placeholder="系统名称 / 责任人 / 同步方向" clearable />
        </el-form-item>
        <el-form-item label="同步方向">
          <el-select v-model="integrationFilters.direction" placeholder="全部方向" clearable style="width: 220px">
            <el-option v-for="item in systemOptions.integration_direction_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="链路状态">
          <el-select v-model="integrationFilters.status" placeholder="全部状态" clearable style="width: 160px">
            <el-option v-for="item in systemOptions.integration_status_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <el-form v-else-if="activeSection === 'operation-logs'" class="filter-form" :inline="true">
        <el-form-item label="关键字">
          <el-input v-model="operationLogFilters.keyword" placeholder="操作账号 / 对象 / 摘要" clearable />
        </el-form-item>
        <el-form-item label="业务模块">
          <el-select v-model="operationLogFilters.module_name" placeholder="全部模块" clearable filterable style="width: 180px">
            <el-option v-for="item in operationModuleOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="处理结果">
          <el-select v-model="operationLogFilters.result" placeholder="全部结果" clearable style="width: 160px">
            <el-option v-for="item in systemOptions.operation_result_options" :key="item.value" :label="item.label" :value="item.value" />
                      <el-option v-for="item in operationResultOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <el-form v-else-if="activeSection === 'notification-logs'" class="filter-form" :inline="true">
        <el-form-item label="关键字">
          <el-input v-model="notificationLogFilters.keyword" placeholder="收件人 / 主题 / 模板编码 / 失败原因 / 业务编号" clearable />
        </el-form-item>
        <el-form-item label="发送渠道">
          <el-select v-model="notificationLogFilters.channel" placeholder="全部渠道" clearable style="width: 160px">
            <el-option v-for="item in notificationChannelOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="发送结果">
          <el-select v-model="notificationLogFilters.send_status" placeholder="全部结果" clearable style="width: 160px">
            <el-option v-for="item in notificationStatusOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <el-form v-else class="filter-form" :inline="true">
        <el-form-item label="关键字">
          <el-input v-model="syncLogFilters.keyword" placeholder="源系统 / 目标系统 / 失败原因" clearable />
        </el-form-item>
        <el-form-item label="同步结果">
          <el-select v-model="syncLogFilters.sync_status" placeholder="全部结果" clearable style="width: 160px">
            <el-option v-for="item in systemOptions.sync_status_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="源系统">
          <el-select v-model="syncLogFilters.source_system" placeholder="全部源系统" clearable filterable style="width: 180px">
            <el-option v-for="item in syncSourceOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <el-table v-if="activeSection === 'users'" :data="users" stripe border v-loading="loading" @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="52" />
        <el-table-column prop="username" label="账号" width="130" />
        <el-table-column prop="full_name" label="姓名" width="120" />
        <el-table-column prop="role_name" label="岗位角色" width="140" />
        <el-table-column prop="department_name" label="部门" width="140" />
        <el-table-column prop="email" label="邮箱" min-width="220" show-overflow-tooltip />
        <el-table-column label="账号状态" width="110">
          <template #default="scope">
            <el-tag :type="getTagType(scope.row.account_status)">{{ scope.row.account_status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="phone_number" label="电话" min-width="160" />
        <el-table-column prop="last_login_at" label="最近登录" width="180" />
        <el-table-column label="操作" width="128" align="left">
          <template #default="scope">
            <TableRowActions :row="scope.row" :main-actions="[{ key: 'edit', label: '维护账号', type: 'primary', onClick: openEditDialog }]" :more-actions="[{ key: 'delete', label: '删除', type: 'danger', onClick: handleDelete }]" />
          </template>
        </el-table-column>
      </el-table>

      <el-table v-else-if="activeSection === 'roles'" :data="roles" stripe border v-loading="loading" @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="52" />
        <el-table-column prop="role_name" label="角色名称" width="140" />
        <el-table-column prop="role_code" label="角色编码" width="140" />
        <el-table-column prop="scope_name" label="适用范围" width="140" />
        <el-table-column prop="user_count" label="已分配人数" width="110" />
        <el-table-column label="权限集合" min-width="320">
          <template #default="scope">
            <div class="tag-list">
              <el-tag v-for="permission in scope.row.permissions" :key="permission" effect="plain">{{ permission }}</el-tag>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="128" align="left">
          <template #default="scope">
            <TableRowActions :row="scope.row" :main-actions="[{ key: 'edit', label: '分配权限', type: 'primary', onClick: openEditDialog }]" :more-actions="[{ key: 'delete', label: '删除', type: 'danger', onClick: handleDelete }]" />
          </template>
        </el-table-column>
      </el-table>

      <el-table v-else-if="activeSection === 'audit'" :data="policies" stripe border v-loading="loading" @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="52" />
        <el-table-column prop="item" label="审计项" width="220" />
        <el-table-column label="策略状态" width="110">
          <template #default="scope">
            <el-tag :type="getTagType(scope.row.status)">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="policy" label="审计策略" min-width="420" />
        <el-table-column label="操作" width="128" align="left">
          <template #default="scope">
            <TableRowActions :row="scope.row" :main-actions="[{ key: 'edit', label: '维护策略', type: 'primary', onClick: openEditDialog }]" :more-actions="[{ key: 'delete', label: '删除', type: 'danger', onClick: handleDelete }]" />
          </template>
        </el-table-column>
      </el-table>

      <el-table v-else-if="activeSection === 'integrations'" :data="integrations" stripe border v-loading="loading" @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="52" />
        <el-table-column prop="name" label="系统名称" width="180" />
        <el-table-column prop="direction" label="同步方向" width="140" />
        <el-table-column prop="cadence" label="同步频率" width="120" />
        <el-table-column label="链路状态" width="110">
          <template #default="scope">
            <el-tag :type="getTagType(scope.row.status)">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="owner" label="责任人" width="120" />
        <el-table-column label="操作" width="128" align="left">
          <template #default="scope">
            <TableRowActions :row="scope.row" :main-actions="[{ key: 'edit', label: '维护链路', type: 'primary', onClick: openEditDialog }]" :more-actions="[{ key: 'delete', label: '删除', type: 'danger', onClick: handleDelete }]" />
          </template>
        </el-table-column>
      </el-table>

      <el-table v-else-if="activeSection === 'operation-logs'" :data="operationLogs" stripe border v-loading="loading">
        <el-table-column prop="operated_at" label="发生时间" width="180" />
        <el-table-column prop="operator_username" label="操作账号" width="120" />
        <el-table-column prop="module_name" label="模块" width="120" />
        <el-table-column prop="action" label="动作" width="120" />
        <el-table-column prop="entity_name" label="对象" width="160" />
        <el-table-column label="结果" width="100">
          <template #default="scope">
            <el-tag :type="getTagType(scope.row.result)">{{ resultLabel(scope.row.result) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="summary" label="摘要" min-width="240" />
      </el-table>

      <el-table v-else-if="activeSection === 'notification-logs'" :data="notificationDeliveryLogs" stripe border v-loading="loading">
        <el-table-column prop="sent_at" label="发送时间" width="168" />
        <el-table-column label="渠道" width="88">
          <template #default="scope">
            <el-tag effect="plain">{{ scope.row.channel === 'email' ? '邮件' : scope.row.channel }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="recipient" label="收件人" width="220" show-overflow-tooltip />
        <el-table-column label="通知内容" min-width="300">
          <template #default="scope">
            <div class="notification-log__cell">
              <div class="notification-log__primary" :title="scope.row.subject || '-'">{{ scope.row.subject || '-' }}</div>
              <div class="notification-log__secondary" :title="`${scope.row.template_code || '-'}${scope.row.business_key ? ` / ${scope.row.business_key}` : ''}`">
                {{ scope.row.template_code || '-' }}
                <span v-if="scope.row.business_key"> / {{ scope.row.business_key }}</span>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="结果" width="96">
          <template #default="scope">
            <el-tag :type="getTagType(scope.row.send_status)">{{ resultLabel(scope.row.send_status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="失败原因" min-width="220">
          <template #default="scope">
            <div class="notification-log__failure" :title="scope.row.failure_reason || '-'">{{ scope.row.failure_reason || '-' }}</div>
          </template>
        </el-table-column>
      </el-table>

      <el-table v-else :data="syncLogs" stripe border v-loading="loading">
        <el-table-column prop="source_system" label="源系统" width="160" />
        <el-table-column prop="target_system" label="目标系统" width="160" />
        <el-table-column label="同步状态" width="120">
          <template #default="scope">
            <el-tag :type="getTagType(scope.row.sync_status)">{{ resultLabel(scope.row.sync_status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="record_count" label="记录数" width="100" />
        <el-table-column prop="executed_at" label="执行时间" width="180" />
        <el-table-column prop="failure_reason" label="失败原因" min-width="220" />
      </el-table>

      <div v-if="editableSection && selectedIds.length > 0" class="selection-summary">
        已选择 {{ selectedIds.length }} 条记录，可执行批量删除。
      </div>

      <input ref="userImportInputRef" type="file" accept=".xlsx" class="hidden-input" @change="handleUserImport" />

      <div class="pagination-bar">
        <el-pagination
          v-if="activeSection === 'users'"
          :current-page="userPager.pagination.currentPage"
          :page-size="userPager.pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="userPager.pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @current-change="handleUserPageChange"
          @size-change="handleUserPageSizeChange"
        />
        <el-pagination
          v-else-if="activeSection === 'roles'"
          :current-page="rolePager.pagination.currentPage"
          :page-size="rolePager.pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="rolePager.pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @current-change="handleRolePageChange"
          @size-change="handleRolePageSizeChange"
        />
        <el-pagination
          v-else-if="activeSection === 'audit'"
          :current-page="auditPager.pagination.currentPage"
          :page-size="auditPager.pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="auditPager.pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @current-change="handleAuditPageChange"
          @size-change="handleAuditPageSizeChange"
        />
        <el-pagination
          v-else-if="activeSection === 'integrations'"
          :current-page="integrationPager.pagination.currentPage"
          :page-size="integrationPager.pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="integrationPager.pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @current-change="handleIntegrationPageChange"
          @size-change="handleIntegrationPageSizeChange"
        />
        <el-pagination
          v-else-if="activeSection === 'operation-logs'"
          :current-page="operationLogPager.pagination.currentPage"
          :page-size="operationLogPager.pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="operationLogPager.pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @current-change="handleOperationLogPageChange"
          @size-change="handleOperationLogPageSizeChange"
        />
        <el-pagination
          v-else-if="activeSection === 'notification-logs'"
          :current-page="notificationLogPager.pagination.currentPage"
          :page-size="notificationLogPager.pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="notificationLogPager.pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @current-change="handleNotificationLogPageChange"
          @size-change="handleNotificationLogPageSizeChange"
        />
        <el-pagination
          v-else
          :current-page="syncLogPager.pagination.currentPage"
          :page-size="syncLogPager.pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="syncLogPager.pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @current-change="handleSyncLogPageChange"
          @size-change="handleSyncLogPageSizeChange"
        />
      </div>
    </article>

    <el-dialog
      v-model="userImportDialogVisible"
      title="导入系统用户"
      width="680px"
      destroy-on-close
      :close-on-click-modal="!importSubmitting"
      :close-on-press-escape="!importSubmitting"
      :show-close="!importSubmitting"
    >
      <div class="dialog-form user-import-dialog">
        <el-alert
          type="info"
          :closable="false"
          show-icon
          title="导入说明"
          description="请在弹窗中选择系统用户导入模板 Excel。导入过程中会分批处理并实时显示已导入条数、总条数和进度。"
        />

        <section class="user-import-panel">
          <div>
            <div class="user-import-panel__label">导入文件</div>
            <div class="user-import-panel__filename">{{ userImportState.fileName || '未选择 Excel 文件' }}</div>
          </div>
          <el-button plain :disabled="importSubmitting" @click="triggerUserImportFileSelect">
            {{ userImportState.fileName ? '重新选择 Excel' : '选择 Excel' }}
          </el-button>
        </section>

        <section class="user-import-progress-card">
          <div class="user-import-progress-card__header">
            <div>
              <span class="user-import-progress-card__label">导入进度</span>
              <strong>{{ userImportState.processedCount }} / {{ userImportState.totalCount }}</strong>
            </div>
            <span class="user-import-progress-card__status">{{ userImportStatusText }}</span>
          </div>
          <el-progress :percentage="userImportProgressPercentage" :status="getUserImportProgressStatus()" :stroke-width="14" />
        </section>

        <section class="user-import-stats">
          <article>
            <span>新增</span>
            <strong>{{ userImportState.createdCount }}</strong>
          </article>
          <article>
            <span>更新</span>
            <strong>{{ userImportState.updatedCount }}</strong>
          </article>
          <article>
            <span>失败</span>
            <strong>{{ userImportState.failedCount }}</strong>
          </article>
        </section>

        <section v-if="userImportIssuePreview.length > 0" class="user-import-issues">
          <div class="user-import-issues__header">
            <div class="user-import-issues__title">失败预览</div>
            <span class="user-import-issues__meta">共 {{ userImportState.issues.length }} 条，当前展示前 {{ userImportIssuePreview.length }} 条</span>
          </div>
          <ul>
            <li v-for="item in userImportIssuePreview" :key="`${item.row_number}-${item.username || item.full_name || 'row'}`">
              第 {{ item.row_number }} 行，{{ item.full_name || '未命名' }}{{ item.username ? `（${item.username}）` : '' }}：{{ item.reason }}
            </li>
          </ul>
        </section>
      </div>
      <template #footer>
        <el-button :disabled="importSubmitting" @click="userImportDialogVisible = false">关闭</el-button>
        <el-button
          v-if="userImportState.phase === 'completed' && userImportState.failedCount > 0"
          plain
          :disabled="importSubmitting"
          @click="exportUserImportIssues"
        >
          导出失败明细
        </el-button>
        <el-button type="primary" :loading="importSubmitting" @click="submitUserImport">开始导入</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="dialogVisible" :title="dialogMode === 'create' ? sectionConfig.createLabel : `维护${sectionConfig.title}`" width="820px">
      <el-form v-if="activeSection === 'users'" label-width="110px" class="dialog-grid">
        <el-form-item>
          <template #label>
            <span class="required-label"><span v-if="isSystemUserFieldRequired('username')" class="required-mark">*</span>登录账号</span>
          </template>
          <el-input v-model="userForm.username" placeholder="请输入登录账号" />
        </el-form-item>
        <el-form-item>
          <template #label>
            <span class="required-label"><span v-if="isSystemUserFieldRequired('full_name')" class="required-mark">*</span>姓名</span>
          </template>
          <el-input v-model="userForm.full_name" placeholder="请输入真实姓名" />
        </el-form-item>
        <el-form-item>
          <template #label>
            <span class="required-label"><span v-if="isSystemUserFieldRequired('role_code')" class="required-mark">*</span>角色分配</span>
          </template>
          <el-select v-model="userForm.role_code" placeholder="请选择角色" style="width: 100%">
            <el-option v-for="item in roleOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="所属部门"><el-input v-model="userForm.department_name" placeholder="请输入所属部门，可留空" /></el-form-item>
        <el-form-item class="dialog-grid__full">
          <template #label>
            <span class="required-label"><span v-if="isSystemUserFieldRequired('introduction')" class="required-mark">*</span>介绍</span>
          </template>
          <el-input
            v-model="userForm.introduction"
            type="textarea"
            :rows="4"
            placeholder="请输入人员介绍；当角色为导师时必填"
          />
        </el-form-item>
        <el-form-item>
          <template #label>
            <span class="required-label"><span v-if="isSystemUserFieldRequired('email')" class="required-mark">*</span>邮箱</span>
          </template>
          <el-input v-model="userForm.email" placeholder="新建可留空，修改时必填" />
        </el-form-item>
        <el-form-item>
          <template #label>
            <span class="required-label"><span v-if="isSystemUserFieldRequired('account_status')" class="required-mark">*</span>账号状态</span>
          </template>
          <el-select v-model="userForm.account_status" placeholder="请选择账号状态" style="width: 100%">
            <el-option v-for="item in systemOptions.account_status_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <template #label>
            <span class="required-label"><span v-if="isSystemUserFieldRequired('phone_number')" class="required-mark">*</span>联系电话</span>
          </template>
          <el-input v-model="userForm.phone_number" placeholder="新建可留空，修改时必填" />
        </el-form-item>
        <el-form-item label="登录密码" class="dialog-grid__full">
          <el-input v-model="userForm.password" show-password :placeholder="dialogMode === 'create' ? '留空则使用默认初始密码 ChangeMe@123' : '留空则保持原密码不变'" />
        </el-form-item>
      </el-form>

      <el-form v-else-if="activeSection === 'roles'" label-width="110px" class="dialog-grid">
        <el-form-item label="角色名称"><el-input v-model="roleForm.role_name" placeholder="请输入角色名称" /></el-form-item>
        <el-form-item label="角色编码"><el-input v-model="roleForm.role_code" placeholder="请输入角色编码" /></el-form-item>
        <el-form-item label="适用范围">
          <el-select v-model="roleForm.scope_name" placeholder="请选择适用范围" style="width: 100%">
            <el-option v-for="item in systemOptions.role_scope_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="权限分配" class="dialog-grid__full">
          <div class="permission-panel">
            <section v-for="group in permissionGroups" :key="group.moduleName" class="permission-group">
              <div class="permission-group__title">{{ group.moduleName }}</div>
              <el-checkbox-group v-model="roleForm.permissions" class="permission-checkboxes">
                <el-checkbox v-for="item in group.items" :key="item.code" :label="item.code">
                  <div class="permission-item">
                    <strong>{{ item.name }}</strong>
                    <span>{{ item.description }}</span>
                  </div>
                </el-checkbox>
              </el-checkbox-group>
            </section>
          </div>
        </el-form-item>
      </el-form>

      <el-form v-else-if="activeSection === 'audit'" label-width="110px" class="dialog-grid">
        <el-form-item label="审计项"><el-input v-model="policyForm.item" placeholder="请输入审计项名称" /></el-form-item>
        <el-form-item label="策略状态">
          <el-select v-model="policyForm.status" placeholder="请选择策略状态" style="width: 100%">
            <el-option v-for="item in systemOptions.audit_status_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="审计策略" class="dialog-grid__full"><el-input v-model="policyForm.policy" type="textarea" :rows="4" placeholder="请输入审计规则说明" /></el-form-item>
      </el-form>

      <el-form v-else-if="activeSection === 'integrations'" label-width="110px" class="dialog-grid">
        <el-form-item label="系统名称"><el-input v-model="integrationForm.name" placeholder="请输入系统名称" /></el-form-item>
        <el-form-item label="责任人"><el-input v-model="integrationForm.owner" placeholder="请输入责任岗位或部门" /></el-form-item>
        <el-form-item label="同步方向">
          <el-select v-model="integrationForm.direction" placeholder="请选择同步方向" style="width: 100%">
            <el-option v-for="item in systemOptions.integration_direction_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="同步频率">
          <el-select v-model="integrationForm.cadence" placeholder="请选择同步频率" style="width: 100%">
            <el-option v-for="item in systemOptions.integration_cadence_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="链路状态">
          <el-select v-model="integrationForm.status" placeholder="请选择链路状态" style="width: 100%">
            <el-option v-for="item in systemOptions.integration_status_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submit">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="userSaveResultDialogVisible" :title="userSaveResult?.title || '保存结果'" width="640px" destroy-on-close>
      <div class="dialog-form reset-password-dialog">
        <template v-if="userSaveResult">
          <div class="reset-password-summary system-save-result-summary">
            <div>
              <span class="reset-password-summary__label">操作</span>
              <strong>{{ userSaveResult.actionLabel }}</strong>
            </div>
            <div>
              <span class="reset-password-summary__label">系统账号</span>
              <strong>{{ userSaveResult.username }}</strong>
            </div>
          </div>
          <div class="reset-password-result">
            <p class="reset-password-result__message">{{ userSaveResult.message }}</p>
          </div>
        </template>
      </div>
      <template #footer>
        <el-button type="primary" @click="userSaveResultDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>

    <el-dialog
      v-model="roleDeleteDialogVisible"
      title="删除确认"
      width="640px"
      destroy-on-close
      :close-on-click-modal="!roleDeleteSubmitting"
      :close-on-press-escape="!roleDeleteSubmitting"
      :show-close="!roleDeleteSubmitting"
      @closed="deletingRole = null; roleDeletionPreview = null"
    >
      <div v-if="deletingRole" class="dialog-form delete-center-dialog role-delete-dialog">
        <p class="delete-center-dialog__lead">删除前会先检查该角色的使用情况。若用户还有其他角色，系统会先解绑再删除；若某个用户只剩这一个角色，则需要先重新配置。</p>
        <div class="delete-center-dialog__summary">
          <div>
            <span class="delete-center-dialog__label">角色名称</span>
            <strong>{{ deletingRole.role_name }}</strong>
          </div>
          <div>
            <span class="delete-center-dialog__label">角色编码</span>
            <strong>{{ deletingRole.role_code }}</strong>
          </div>
          <div>
            <span class="delete-center-dialog__label">适用范围</span>
            <strong>{{ deletingRole.scope_name || '系统管理' }}</strong>
          </div>
          <div>
            <span class="delete-center-dialog__label">权限数量</span>
            <strong>{{ deletingRole.permissions.length }}</strong>
          </div>
        </div>

        <el-alert
          v-if="roleDeletionPreview"
          :type="roleDeletionPreview.blocking_user_count > 0 ? 'warning' : 'info'"
          :closable="false"
          :title="roleDeletionPreview.blocking_user_count > 0 ? '存在必须先重新配置的用户' : '可以自动解绑后删除'"
          :description="roleDeletionPreview.message"
          show-icon
        />

        <div v-if="roleDeletionPreview && roleDeletionPreview.assigned_users.length > 0" class="role-delete-users">
          <div class="role-delete-users__header">
            <strong>关联用户</strong>
            <span>共 {{ roleDeletionPreview.assigned_user_count }} 人</span>
          </div>
          <el-table :data="roleDeletionPreview.assigned_users" size="small" border stripe>
            <el-table-column prop="username" label="账号" min-width="120" />
            <el-table-column prop="full_name" label="姓名" min-width="120" />
            <el-table-column prop="role_count" label="当前角色数" width="120" align="center" />
            <el-table-column label="处理结果" min-width="180">
              <template #default="scope">
                <el-tag v-if="scope.row.can_be_unbound" type="success" effect="light">可自动解绑</el-tag>
                <el-tag v-else type="warning" effect="light">需先重新配置</el-tag>
                <span v-if="scope.row.fallback_role_name" class="role-delete-users__fallback">下一个角色：{{ scope.row.fallback_role_name }}</span>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
      <template #footer>
        <el-button :disabled="roleDeleteSubmitting" @click="roleDeleteDialogVisible = false">取消</el-button>
        <el-button
          type="danger"
          :disabled="roleDeleteSubmitting || !!(roleDeletionPreview && !roleDeletionPreview.can_force_delete)"
          :loading="roleDeleteSubmitting"
          @click="submitRoleDeleteDialog"
        >
          确认解绑并删除
        </el-button>
      </template>
    </el-dialog>

    <el-dialog
      v-model="roleBatchDeleteDialogVisible"
      title="批量删除确认"
      width="640px"
      destroy-on-close
      :close-on-click-modal="!roleBatchDeleteSubmitting"
      :close-on-press-escape="!roleBatchDeleteSubmitting"
      :show-close="!roleBatchDeleteSubmitting"
    >
      <div class="dialog-form delete-center-dialog role-delete-dialog">
        <p class="delete-center-dialog__lead">已选择 {{ selectedIds.length }} 个角色，确认批量删除吗？删除后不可恢复。</p>
        <div class="delete-center-dialog__summary">
          <div>
            <span class="delete-center-dialog__label">选中数量</span>
            <strong>{{ selectedIds.length }}</strong>
          </div>
          <div>
            <span class="delete-center-dialog__label">操作范围</span>
            <strong>仅删除选中的角色记录</strong>
          </div>
          <div>
            <span class="delete-center-dialog__label">提醒</span>
            <strong>相关权限分配将同时清除</strong>
          </div>
          <div>
            <span class="delete-center-dialog__label">说明</span>
            <strong>请确认这些角色不再使用</strong>
          </div>
        </div>
      </div>
      <template #footer>
        <el-button :disabled="roleBatchDeleteSubmitting" @click="roleBatchDeleteDialogVisible = false">取消</el-button>
        <el-button type="danger" :loading="roleBatchDeleteSubmitting" @click="submitRoleBatchDeleteDialog">确认删除</el-button>
      </template>
    </el-dialog>
  </section>
</template>

<style scoped>
.content-stack,
.state-grid {
  display: grid;
  gap: 22px;
}

.state-grid {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.section-card {
  border: 1px solid rgba(18, 50, 95, 0.08);
  border-radius: 26px;
  padding: 22px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 18px 44px rgba(14, 40, 88, 0.07);
}

.section-card__header {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: center;
  margin-bottom: 18px;
}

.hidden-input {
  display: none;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.summary-text {
  color: #7183a0;
  font-size: 13px;
}

.section-tag,
.section-card h2,
.state-card p {
  margin: 0;
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

.state-card {
  padding: 18px;
  border-radius: 22px;
  background: linear-gradient(135deg, rgba(245, 248, 255, 0.98), rgba(235, 245, 255, 0.92));
}

.state-card strong {
  display: block;
  margin-top: 10px;
  color: #12315e;
  font-size: 28px;
}

.filter-form {
  margin-bottom: 14px;
}

.tag-list {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.dialog-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 4px 18px;
}

.dialog-grid__full {
  grid-column: 1 / -1;
}

.required-label {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.required-mark {
  color: #d93025;
  font-weight: 700;
  line-height: 1;
}

.permission-panel {
  width: 100%;
  display: grid;
  gap: 12px;
}

.permission-group {
  border: 1px solid rgba(18, 50, 95, 0.08);
  border-radius: 16px;
  padding: 14px 16px;
  background: rgba(244, 248, 252, 0.76);
}

.permission-group__title {
  margin-bottom: 10px;
  font-weight: 600;
  color: #12315e;
}

.permission-checkboxes {
  display: grid;
  gap: 10px;
}

.permission-item {
  display: grid;
  gap: 4px;
}

.permission-item strong {
  color: #12284d;
}

.permission-item span {
  color: #6d7f99;
  font-size: 12px;
}

.selection-summary {
  margin-top: 14px;
  color: #7183a0;
  font-size: 13px;
}

.notification-log__cell {
  display: grid;
  gap: 4px;
  min-width: 0;
}

.notification-log__primary,
.notification-log__secondary,
.notification-log__failure {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.notification-log__primary {
  color: #12284d;
  font-weight: 600;
}

.notification-log__secondary {
  color: #7183a0;
  font-size: 12px;
}

.notification-log__failure {
  color: #5f6f87;
}

.dialog-form {
  padding-top: 8px;
}

.user-import-dialog {
  display: grid;
  gap: 16px;
}

.user-import-panel,
.user-import-progress-card,
.user-import-stats article,
.user-import-issues {
  border: 1px solid rgba(18, 50, 95, 0.08);
  border-radius: 16px;
  background: rgba(244, 248, 252, 0.78);
}

.user-import-panel {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 16px 18px;
}

.user-import-panel__label,
.user-import-progress-card__label,
.user-import-issues__title {
  color: #7183a0;
  font-size: 12px;
}

.user-import-panel__filename {
  margin-top: 6px;
  color: #12284d;
  font-weight: 600;
  word-break: break-all;
}

.user-import-progress-card {
  display: grid;
  gap: 12px;
  padding: 16px 18px;
}

.user-import-progress-card__header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 16px;
}

.user-import-progress-card__header strong {
  display: block;
  margin-top: 6px;
  color: #12315e;
  font-size: 24px;
}

.user-import-progress-card__status {
  color: #5f6f87;
  font-size: 13px;
}

.user-import-stats {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

.user-import-stats article {
  display: grid;
  gap: 6px;
  padding: 14px 16px;
}

.user-import-stats span {
  color: #7183a0;
  font-size: 12px;
}

.user-import-stats strong {
  color: #12284d;
  font-size: 22px;
}

.user-import-issues {
  padding: 16px 18px;
}

.user-import-issues__header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 12px;
}

.user-import-issues__meta {
  color: #7183a0;
  font-size: 12px;
}

.user-import-issues ul {
  margin: 10px 0 0;
  padding-left: 18px;
  color: #4b5d78;
}

.user-import-issues li + li {
  margin-top: 8px;
}

.reset-password-dialog {
  display: grid;
  gap: 16px;
}

.role-delete-dialog {
  display: grid;
  gap: 16px;
}

.role-delete-users {
  display: grid;
  gap: 12px;
}

.role-delete-users__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  color: #475569;
}

.role-delete-users__fallback {
  display: inline-block;
  margin-left: 8px;
  color: #909399;
  font-size: 12px;
}

.reset-password-summary {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  padding: 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #f8fafc;
}

.reset-password-summary__label {
  display: block;
  margin-bottom: 6px;
  color: #909399;
  font-size: 12px;
}

.reset-password-summary strong {
  color: #303133;
  font-size: 14px;
  word-break: break-word;
}

.reset-password-result {
  display: grid;
  gap: 14px;
}

.reset-password-result__message {
  margin: 0;
  color: #606266;
  line-height: 1.7;
  white-space: pre-line;
}

@media (max-width: 980px) {
  .state-grid,
  .dialog-grid {
    grid-template-columns: 1fr;
  }

  .reset-password-summary {
    grid-template-columns: 1fr;
  }

  .user-import-panel,
  .user-import-progress-card__header,
  .user-import-issues__header {
    align-items: flex-start;
    flex-direction: column;
  }

  .user-import-stats {
    grid-template-columns: 1fr;
  }

  .section-card__header {
    align-items: flex-start;
    flex-direction: column;
  }
}
</style>
