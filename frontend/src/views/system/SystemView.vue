<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useRoute } from 'vue-router'

import {
  createAuditPolicy,
  createIntegration,
  createRole,
  createSystemUser,
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
  type IntegrationRecord,
  type OperationLogRecord,
  type RoleRecord,
  type SyncLogRecord,
  type SystemStats,
  type SystemUserRecord,
} from '../../api/system'

const route = useRoute()
const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const dialogMode = ref<'create' | 'edit'>('create')
const currentId = ref<number | null>(null)

const stats = ref<SystemStats>({
  integration_total: 0,
  active_integration_total: 0,
  operation_log_total: 0,
  sync_failure_total: 0,
  user_total: 0,
  role_total: 0,
})

const users = ref<SystemUserRecord[]>([])
const roles = ref<RoleRecord[]>([])
const policies = ref<AuditPolicyRecord[]>([])
const integrations = ref<IntegrationRecord[]>([])
const operationLogs = ref<OperationLogRecord[]>([])
const syncLogs = ref<SyncLogRecord[]>([])

const userForm = reactive<Omit<SystemUserRecord, 'id'>>({
  username: '',
  full_name: '',
  role_code: '',
  department_name: '',
  phone_number: '',
  account_status: '启用',
})
const roleForm = reactive<Omit<RoleRecord, 'id'>>({
  role_code: '',
  role_name: '',
  scope_name: '',
  permissions: [],
})
const policyForm = reactive<Omit<AuditPolicyRecord, 'id'>>({
  item: '',
  policy: '',
})
const integrationForm = reactive<Omit<IntegrationRecord, 'id'>>({
  name: '',
  direction: '',
  cadence: '',
  status: '正常',
  owner: '',
})
const rolePermissionsText = ref('')

const activeSection = computed(() => String(route.meta.section || 'users'))
const sectionTitle = computed(
  () =>
    ({
      users: '系统用户管理',
      roles: '角色权限管理',
      audit: '审计策略管理',
      integrations: '集成链路管理',
      'operation-logs': '操作日志查询',
      'sync-logs': '同步日志查询',
    }[activeSection.value] || '系统治理'),
)
const statCards = computed(() => [
  { label: '系统用户', value: stats.value.user_total },
  { label: '角色总数', value: stats.value.role_total },
  { label: '活跃集成', value: stats.value.active_integration_total },
  { label: '同步失败', value: stats.value.sync_failure_total },
])
const editableSection = computed(() => ['users', 'roles', 'audit', 'integrations'].includes(activeSection.value))

function resetForms() {
  currentId.value = null
  Object.assign(userForm, {
    username: '',
    full_name: '',
    role_code: '',
    department_name: '',
    phone_number: '',
    account_status: '启用',
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
  })
  Object.assign(integrationForm, {
    name: '',
    direction: '',
    cadence: '',
    status: '正常',
    owner: '',
  })
  rolePermissionsText.value = ''
}

async function loadData() {
  loading.value = true
  try {
    const [statsResponse, userResponse, roleResponse, policyResponse, integrationResponse, operationResponse, syncResponse] = await Promise.all([
      getSystemStats(),
      listSystemUsers(),
      listRoles(),
      listAuditPolicies(),
      listIntegrations(),
      listOperationLogs(),
      listSyncLogs(),
    ])
    stats.value = statsResponse.data
    users.value = userResponse.data.items
    roles.value = roleResponse.data.items
    policies.value = policyResponse.data.items
    integrations.value = integrationResponse.data.items
    operationLogs.value = operationResponse.data.items
    syncLogs.value = syncResponse.data.items
  } finally {
    loading.value = false
  }
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
    Object.assign(userForm, row)
  } else if (activeSection.value === 'roles') {
    const roleRow = row as RoleRecord
    Object.assign(roleForm, roleRow)
    rolePermissionsText.value = roleRow.permissions.join(', ')
  } else if (activeSection.value === 'audit') {
    Object.assign(policyForm, row)
  } else {
    Object.assign(integrationForm, row)
  }
  dialogVisible.value = true
}

async function submit() {
  submitting.value = true
  try {
    if (activeSection.value === 'users') {
      if (dialogMode.value === 'create') {
        await createSystemUser(userForm)
      } else if (currentId.value !== null) {
        await updateSystemUser(currentId.value, userForm)
      }
    } else if (activeSection.value === 'roles') {
      roleForm.permissions = rolePermissionsText.value
        .split(',')
        .map((item) => item.trim())
        .filter(Boolean)
      if (dialogMode.value === 'create') {
        await createRole(roleForm)
      } else if (currentId.value !== null) {
        await updateRole(currentId.value, roleForm)
      }
    } else if (activeSection.value === 'audit') {
      if (dialogMode.value === 'create') {
        await createAuditPolicy(policyForm)
      } else if (currentId.value !== null) {
        await updateAuditPolicy(currentId.value, policyForm)
      }
    } else if (activeSection.value === 'integrations') {
      if (dialogMode.value === 'create') {
        await createIntegration(integrationForm)
      } else if (currentId.value !== null) {
        await updateIntegration(currentId.value, integrationForm)
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
          <p class="section-tag">平台治理</p>
          <h2>{{ sectionTitle }}</h2>
        </div>
        <el-button v-if="editableSection" type="primary" round @click="openCreateDialog">新增记录</el-button>
      </div>

      <el-table v-if="activeSection === 'users'" :data="users" stripe v-loading="loading">
        <el-table-column prop="username" label="账号" width="130" />
        <el-table-column prop="full_name" label="姓名" width="120" />
        <el-table-column prop="role_code" label="角色编码" width="120" />
        <el-table-column prop="department_name" label="部门" width="140" />
        <el-table-column prop="account_status" label="状态" width="100" />
        <el-table-column prop="phone_number" label="电话" min-width="160" />
        <el-table-column label="操作" width="100">
          <template #default="scope"><el-button link type="primary" @click="openEditDialog(scope.row)">编辑</el-button></template>
        </el-table-column>
      </el-table>

      <el-table v-else-if="activeSection === 'roles'" :data="roles" stripe v-loading="loading">
        <el-table-column prop="role_name" label="角色名称" width="140" />
        <el-table-column prop="role_code" label="角色编码" width="140" />
        <el-table-column prop="scope_name" label="适用范围" width="140" />
        <el-table-column label="权限集合" min-width="320">
          <template #default="scope">{{ scope.row.permissions.join('、') }}</template>
        </el-table-column>
        <el-table-column label="操作" width="100">
          <template #default="scope"><el-button link type="primary" @click="openEditDialog(scope.row)">编辑</el-button></template>
        </el-table-column>
      </el-table>

      <el-table v-else-if="activeSection === 'audit'" :data="policies" stripe v-loading="loading">
        <el-table-column prop="item" label="审计项" width="220" />
        <el-table-column prop="policy" label="审计策略" min-width="420" />
        <el-table-column label="操作" width="100">
          <template #default="scope"><el-button link type="primary" @click="openEditDialog(scope.row)">编辑</el-button></template>
        </el-table-column>
      </el-table>

      <el-table v-else-if="activeSection === 'integrations'" :data="integrations" stripe v-loading="loading">
        <el-table-column prop="name" label="系统名称" width="180" />
        <el-table-column prop="direction" label="同步方向" width="140" />
        <el-table-column prop="cadence" label="同步频率" width="120" />
        <el-table-column prop="status" label="状态" width="100" />
        <el-table-column prop="owner" label="责任人" width="120" />
        <el-table-column label="操作" width="100">
          <template #default="scope"><el-button link type="primary" @click="openEditDialog(scope.row)">编辑</el-button></template>
        </el-table-column>
      </el-table>

      <el-table v-else-if="activeSection === 'operation-logs'" :data="operationLogs" stripe v-loading="loading">
        <el-table-column prop="operated_at" label="发生时间" width="180" />
        <el-table-column prop="operator_username" label="操作账号" width="120" />
        <el-table-column prop="module_name" label="模块" width="120" />
        <el-table-column prop="action" label="动作" width="120" />
        <el-table-column prop="entity_name" label="对象" width="160" />
        <el-table-column prop="summary" label="摘要" min-width="240" />
      </el-table>

      <el-table v-else :data="syncLogs" stripe v-loading="loading">
        <el-table-column prop="source_system" label="源系统" width="160" />
        <el-table-column prop="target_system" label="目标系统" width="160" />
        <el-table-column prop="sync_status" label="同步状态" width="120" />
        <el-table-column prop="record_count" label="记录数" width="100" />
        <el-table-column prop="executed_at" label="执行时间" width="180" />
        <el-table-column prop="failure_reason" label="失败原因" min-width="220" />
      </el-table>
    </section>

    <el-dialog v-model="dialogVisible" :title="dialogMode === 'create' ? `新增${sectionTitle}` : `编辑${sectionTitle}`" width="760px">
      <el-form v-if="activeSection === 'users'" label-width="110px" class="dialog-grid">
        <el-form-item label="账号"><el-input v-model="userForm.username" /></el-form-item>
        <el-form-item label="姓名"><el-input v-model="userForm.full_name" /></el-form-item>
        <el-form-item label="角色编码"><el-input v-model="userForm.role_code" /></el-form-item>
        <el-form-item label="部门"><el-input v-model="userForm.department_name" /></el-form-item>
        <el-form-item label="状态"><el-input v-model="userForm.account_status" /></el-form-item>
        <el-form-item label="电话"><el-input v-model="userForm.phone_number" /></el-form-item>
      </el-form>

      <el-form v-else-if="activeSection === 'roles'" label-width="110px" class="dialog-grid">
        <el-form-item label="角色名称"><el-input v-model="roleForm.role_name" /></el-form-item>
        <el-form-item label="角色编码"><el-input v-model="roleForm.role_code" /></el-form-item>
        <el-form-item label="适用范围"><el-input v-model="roleForm.scope_name" /></el-form-item>
        <el-form-item label="权限集合" class="dialog-grid__full"><el-input v-model="rolePermissionsText" type="textarea" :rows="4" placeholder="逗号分隔权限编码" /></el-form-item>
      </el-form>

      <el-form v-else-if="activeSection === 'audit'" label-width="110px" class="dialog-grid">
        <el-form-item label="审计项"><el-input v-model="policyForm.item" /></el-form-item>
        <el-form-item label="审计策略" class="dialog-grid__full"><el-input v-model="policyForm.policy" type="textarea" :rows="4" /></el-form-item>
      </el-form>

      <el-form v-else-if="activeSection === 'integrations'" label-width="110px" class="dialog-grid">
        <el-form-item label="系统名称"><el-input v-model="integrationForm.name" /></el-form-item>
        <el-form-item label="同步方向"><el-input v-model="integrationForm.direction" /></el-form-item>
        <el-form-item label="同步频率"><el-input v-model="integrationForm.cadence" /></el-form-item>
        <el-form-item label="状态"><el-input v-model="integrationForm.status" /></el-form-item>
        <el-form-item label="责任人"><el-input v-model="integrationForm.owner" /></el-form-item>
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

.section-tag,
.section-card h2,
.pill-card p {
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

.pill-card {
  padding: 18px;
  border-radius: 22px;
  background: linear-gradient(135deg, rgba(245, 248, 255, 0.98), rgba(235, 245, 255, 0.92));
}

.pill-card strong {
  display: block;
  margin-top: 10px;
  color: #12315e;
  font-size: 28px;
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
