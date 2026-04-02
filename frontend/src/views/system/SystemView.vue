<script setup lang="ts">
import axios from 'axios'
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRoute } from 'vue-router'
import TableRowActions from '../../components/table/TableRowActions.vue'
import { buildDictColorMap, resolveDictTagType, type DictColorMap } from '../../utils/dictTag'

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
  getPermissionCatalog,
  getSystemOptions,
  getSystemStats,
  listAuditPolicies,
  listIntegrations,
  listOperationLogs,
  listRoles,
  listSyncLogs,
  listSystemUsers,
  updateAuditPolicy,
  updateIntegration,
  updateRole,
  updateSystemUser,
  type AuditPolicyRecord,
  type AuditPolicyUpsert,
  type IntegrationRecord,
  type IntegrationUpsert,
  type OperationLogRecord,
  type PermissionOption,
  type RoleRecord,
  type RoleUpsert,
  type SyncLogRecord,
  type SystemOptions,
  type SystemStats,
  type SystemUserRecord,
  type SystemUserUpsert,
} from '../../api/system'

const route = useRoute()
const loading = ref(false)
const bootstrapping = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const dialogMode = ref<'create' | 'edit'>('create')
const currentId = ref<number | null>(null)
const selectedIds = ref<number[]>([])
const systemTagColors = ref<DictColorMap>({})

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
  'sync-logs': { title: '同步日志查询', tag: '数据追踪', createLabel: '', batchDeleteLabel: '' },
}

const activeSection = computed(() => String(route.meta.section || 'users'))
const sectionConfig = computed(() => sectionMeta[activeSection.value] || sectionMeta.users)
const editableSection = computed(() => ['users', 'roles', 'audit', 'integrations'].includes(activeSection.value))
const currentTotal = computed(() => {
  if (activeSection.value === 'users') return users.value.length
  if (activeSection.value === 'roles') return roles.value.length
  if (activeSection.value === 'audit') return policies.value.length
  if (activeSection.value === 'integrations') return integrations.value.length
  if (activeSection.value === 'operation-logs') return operationLogs.value.length
  return syncLogs.value.length
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

function getErrorMessage(error: unknown) {
  if (axios.isAxiosError(error)) {
    return String(error.response?.data?.detail || error.message || '请求失败')
  }
  return '请求失败'
}

function resetSelection() {
  selectedIds.value = []
}

function resetForms() {
  currentId.value = null
  Object.assign(userForm, {
    username: '',
    full_name: '',
    role_code: '',
    department_name: '',
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
  const response = await listRoles()
  roleReferenceList.value = response.data.items
}

async function loadBootstrapData() {
  bootstrapping.value = true
  try {
    const [statsResponse, optionResponse, permissionResponse, roleResponse] = await Promise.all([
      getSystemStats(),
      getSystemOptions(),
      getPermissionCatalog(),
      listRoles(),
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
      })
      users.value = response.data.items
      return
    }
    if (activeSection.value === 'roles') {
      const response = await listRoles({
        keyword: roleFilters.keyword || undefined,
        scope_name: roleFilters.scope_name || undefined,
        permission: roleFilters.permission || undefined,
      })
      roles.value = response.data.items
      return
    }
    if (activeSection.value === 'audit') {
      const response = await listAuditPolicies({
        keyword: auditFilters.keyword || undefined,
        status: auditFilters.status || undefined,
      })
      policies.value = response.data.items
      return
    }
    if (activeSection.value === 'integrations') {
      const response = await listIntegrations({
        keyword: integrationFilters.keyword || undefined,
        status: integrationFilters.status || undefined,
        direction: integrationFilters.direction || undefined,
      })
      integrations.value = response.data.items
      return
    }
    if (activeSection.value === 'operation-logs') {
      const response = await listOperationLogs({
        keyword: operationLogFilters.keyword || undefined,
        module_name: operationLogFilters.module_name || undefined,
        result: operationLogFilters.result || undefined,
      })
      operationLogs.value = response.data.items
      return
    }
    const response = await listSyncLogs({
      keyword: syncLogFilters.keyword || undefined,
      sync_status: syncLogFilters.sync_status || undefined,
      source_system: syncLogFilters.source_system || undefined,
    })
    syncLogs.value = response.data.items
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
    if (!userForm.username || !userForm.full_name || !userForm.role_code || !userForm.department_name || !userForm.account_status) {
      ElMessage.warning('请完整填写系统账号信息')
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

async function submit() {
  if (!validateForm()) {
    return
  }

  submitting.value = true
  try {
    if (activeSection.value === 'users') {
      const payload: SystemUserUpsert = {
        ...userForm,
        phone_number: userForm.phone_number?.trim() || '',
        password: userForm.password?.trim() || undefined,
      }
      if (dialogMode.value === 'create') {
        await createSystemUser(payload)
        ElMessage.success('系统账号已创建')
      } else if (currentId.value !== null) {
        await updateSystemUser(currentId.value, payload)
        ElMessage.success('系统账号已更新')
      }
      dialogVisible.value = false
      await refreshAfterMutation(true)
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
    ElMessage.error(getErrorMessage(error))
  } finally {
    submitting.value = false
  }
}

async function handleDelete(row: SystemUserRecord | RoleRecord | AuditPolicyRecord | IntegrationRecord) {
  const targetName = activeSection.value === 'users'
    ? (row as SystemUserRecord).full_name
    : activeSection.value === 'roles'
      ? (row as RoleRecord).role_name
      : activeSection.value === 'audit'
        ? (row as AuditPolicyRecord).item
        : (row as IntegrationRecord).name

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

async function handleSearch() {
  try {
    await loadSectionData()
  } catch (error) {
    ElMessage.error(getErrorMessage(error))
  }
}

async function handleReset() {
  resetFilters()
  await handleSearch()
}

function handleSelectionChange(rows: Array<{ id: number }>) {
  selectedIds.value = rows.map((item) => item.id)
}

function getTagType(status: string) {
  return resolveDictTagType(status, systemTagColors.value)
}

function resultLabel(value: string) {
  return value === 'success' ? '成功' : value === 'failed' ? '失败' : value
}

watch(
  () => activeSection.value,
  async () => {
    resetFilters()
    resetSelection()
    dialogVisible.value = false
    await loadSectionData()
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

      <el-table v-if="activeSection === 'users'" :data="users" stripe v-loading="loading" @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="52" />
        <el-table-column prop="username" label="账号" width="130" />
        <el-table-column prop="full_name" label="姓名" width="120" />
        <el-table-column prop="role_name" label="岗位角色" width="140" />
        <el-table-column prop="department_name" label="部门" width="140" />
        <el-table-column label="账号状态" width="110">
          <template #default="scope">
            <el-tag :type="getTagType(scope.row.account_status)">{{ scope.row.account_status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="phone_number" label="电话" min-width="160" />
        <el-table-column prop="last_login_at" label="最近登录" width="180" />
        <el-table-column label="操作" width="128" align="center">
          <template #default="scope">
            <TableRowActions :row="scope.row" :main-actions="[{ key: 'edit', label: '维护账号', type: 'primary', onClick: openEditDialog }]" :more-actions="[{ key: 'delete', label: '删除', type: 'danger', onClick: handleDelete }]" />
          </template>
        </el-table-column>
      </el-table>

      <el-table v-else-if="activeSection === 'roles'" :data="roles" stripe v-loading="loading" @selection-change="handleSelectionChange">
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
        <el-table-column label="操作" width="128" align="center">
          <template #default="scope">
            <TableRowActions :row="scope.row" :main-actions="[{ key: 'edit', label: '分配权限', type: 'primary', onClick: openEditDialog }]" :more-actions="[{ key: 'delete', label: '删除', type: 'danger', onClick: handleDelete }]" />
          </template>
        </el-table-column>
      </el-table>

      <el-table v-else-if="activeSection === 'audit'" :data="policies" stripe v-loading="loading" @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="52" />
        <el-table-column prop="item" label="审计项" width="220" />
        <el-table-column label="策略状态" width="110">
          <template #default="scope">
            <el-tag :type="getTagType(scope.row.status)">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="policy" label="审计策略" min-width="420" />
        <el-table-column label="操作" width="128" align="center">
          <template #default="scope">
            <TableRowActions :row="scope.row" :main-actions="[{ key: 'edit', label: '维护策略', type: 'primary', onClick: openEditDialog }]" :more-actions="[{ key: 'delete', label: '删除', type: 'danger', onClick: handleDelete }]" />
          </template>
        </el-table-column>
      </el-table>

      <el-table v-else-if="activeSection === 'integrations'" :data="integrations" stripe v-loading="loading" @selection-change="handleSelectionChange">
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
        <el-table-column label="操作" width="128" align="center">
          <template #default="scope">
            <TableRowActions :row="scope.row" :main-actions="[{ key: 'edit', label: '维护链路', type: 'primary', onClick: openEditDialog }]" :more-actions="[{ key: 'delete', label: '删除', type: 'danger', onClick: handleDelete }]" />
          </template>
        </el-table-column>
      </el-table>

      <el-table v-else-if="activeSection === 'operation-logs'" :data="operationLogs" stripe v-loading="loading">
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

      <el-table v-else :data="syncLogs" stripe v-loading="loading">
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
    </article>

    <el-dialog v-model="dialogVisible" :title="dialogMode === 'create' ? sectionConfig.createLabel : `维护${sectionConfig.title}`" width="820px">
      <el-form v-if="activeSection === 'users'" label-width="110px" class="dialog-grid">
        <el-form-item label="登录账号"><el-input v-model="userForm.username" placeholder="请输入登录账号" /></el-form-item>
        <el-form-item label="姓名"><el-input v-model="userForm.full_name" placeholder="请输入真实姓名" /></el-form-item>
        <el-form-item label="角色分配">
          <el-select v-model="userForm.role_code" placeholder="请选择角色" style="width: 100%">
            <el-option v-for="item in roleOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="所属部门"><el-input v-model="userForm.department_name" placeholder="请输入所属部门" /></el-form-item>
        <el-form-item label="账号状态">
          <el-select v-model="userForm.account_status" placeholder="请选择账号状态" style="width: 100%">
            <el-option v-for="item in systemOptions.account_status_options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="联系电话"><el-input v-model="userForm.phone_number" placeholder="请输入联系电话" /></el-form-item>
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

@media (max-width: 980px) {
  .state-grid,
  .dialog-grid {
    grid-template-columns: 1fr;
  }

  .section-card__header {
    align-items: flex-start;
    flex-direction: column;
  }
}
</style>
