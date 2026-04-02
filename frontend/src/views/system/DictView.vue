<script setup lang="ts">
import axios from 'axios'
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRoute } from 'vue-router'
import TableRowActions from '../../components/table/TableRowActions.vue'
import {
  createDictData,
  createDictType,
  deleteDictData,
  deleteDictType,
  getSystemOptions,
  listDictData,
  listDictTypes,
  updateDictData,
  updateDictType,
  type DictDataRecord,
  type DictDataUpsert,
  type DictTypeRecord,
  type DictTypeUpsert,
  type SelectOption,
  type SystemOptions,
} from '../../api/system'

const route = useRoute()
const loading = ref(false)
const bootstrapping = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const dialogMode = ref<'create' | 'edit'>('create')
const currentId = ref<number | null>(null)

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
const dictTypes = ref<DictTypeRecord[]>([])
const dictData = ref<DictDataRecord[]>([])

const dictTypeFilters = reactive({
  keyword: '',
  status: '',
})
const dictDataFilters = reactive({
  keyword: '',
  dict_type: '',
  status: '',
})

const dictTypeForm = reactive<DictTypeUpsert>({
  dict_name: '',
  dict_type: '',
  status: '启用',
  remark: '',
})
const dictDataForm = reactive<DictDataUpsert>({
  dict_type: '',
  label: '',
  value: '',
  sort_order: 0,
  status: '启用',
  color_type: '',
  css_class: '',
  remark: '',
})

const activeSection = computed(() => String(route.meta.section || 'dict-types'))
const isTypeSection = computed(() => activeSection.value === 'dict-types')
const sectionTitle = computed(() => (isTypeSection.value ? '字典类型管理' : '字典数据管理'))
const sectionTag = computed(() => (isTypeSection.value ? '字典模型' : '字典明细'))
const statusOptions = computed<SelectOption[]>(() => systemOptions.value.audit_status_options)
const dictTypeSelectOptions = computed<SelectOption[]>(() => dictTypes.value.map((item) => ({ label: `${item.dict_name}｜${item.dict_type}`, value: item.dict_type })))

function getErrorMessage(error: unknown) {
  if (axios.isAxiosError(error)) {
    return String(error.response?.data?.detail || error.message || '请求失败')
  }
  return '请求失败'
}

function resetForms() {
  currentId.value = null
  Object.assign(dictTypeForm, {
    dict_name: '',
    dict_type: '',
    status: '启用',
    remark: '',
  })
  Object.assign(dictDataForm, {
    dict_type: '',
    label: '',
    value: '',
    sort_order: 0,
    status: '启用',
    color_type: '',
    css_class: '',
    remark: '',
  })
}

async function loadBootstrapData() {
  bootstrapping.value = true
  try {
    const [optionResponse, typeResponse] = await Promise.all([
      getSystemOptions(),
      listDictTypes(),
    ])
    systemOptions.value = optionResponse.data
    dictTypes.value = typeResponse.data.items
  } finally {
    bootstrapping.value = false
  }
}

async function loadSectionData() {
  loading.value = true
  try {
    if (isTypeSection.value) {
      const response = await listDictTypes({
        keyword: dictTypeFilters.keyword || undefined,
        status: dictTypeFilters.status || undefined,
      })
      dictTypes.value = response.data.items
      return
    }
    const response = await listDictData({
      keyword: dictDataFilters.keyword || undefined,
      dict_type: dictDataFilters.dict_type || undefined,
      status: dictDataFilters.status || undefined,
    })
    dictData.value = response.data.items
  } finally {
    loading.value = false
  }
}

function openCreateDialog() {
  resetForms()
  dialogMode.value = 'create'
  dialogVisible.value = true
}

function openEditDialog(row: DictTypeRecord | DictDataRecord) {
  resetForms()
  dialogMode.value = 'edit'
  currentId.value = row.id
  if (isTypeSection.value) {
    const current = row as DictTypeRecord
    Object.assign(dictTypeForm, {
      dict_name: current.dict_name,
      dict_type: current.dict_type,
      status: current.status,
      remark: current.remark || '',
    })
  } else {
    const current = row as DictDataRecord
    Object.assign(dictDataForm, {
      dict_type: current.dict_type,
      label: current.label,
      value: current.value,
      sort_order: current.sort_order,
      status: current.status,
      color_type: current.color_type || '',
      css_class: current.css_class || '',
      remark: current.remark || '',
    })
  }
  dialogVisible.value = true
}

function validateForm() {
  if (isTypeSection.value) {
    if (!dictTypeForm.dict_name || !dictTypeForm.dict_type || !dictTypeForm.status) {
      ElMessage.warning('请完整填写字典类型信息')
      return false
    }
    return true
  }
  if (!dictDataForm.dict_type || !dictDataForm.label || !dictDataForm.value || !dictDataForm.status) {
    ElMessage.warning('请完整填写字典数据')
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
    if (isTypeSection.value) {
      if (dialogMode.value === 'create') {
        await createDictType(dictTypeForm)
      } else if (currentId.value !== null) {
        await updateDictType(currentId.value, dictTypeForm)
      }
      await loadBootstrapData()
      await loadSectionData()
    } else {
      if (dialogMode.value === 'create') {
        await createDictData(dictDataForm)
      } else if (currentId.value !== null) {
        await updateDictData(currentId.value, dictDataForm)
      }
      await loadBootstrapData()
      await loadSectionData()
    }
    dialogVisible.value = false
    ElMessage.success(dialogMode.value === 'create' ? '保存成功' : '更新成功')
  } catch (error) {
    ElMessage.error(getErrorMessage(error))
  } finally {
    submitting.value = false
  }
}

async function handleDelete(row: DictTypeRecord | DictDataRecord) {
  const targetName = isTypeSection.value ? (row as DictTypeRecord).dict_name : (row as DictDataRecord).label
  try {
    await ElMessageBox.confirm(`确定删除“${targetName}”吗？`, '确认删除', { type: 'warning' })
    if (isTypeSection.value) {
      await deleteDictType(row.id)
      await loadBootstrapData()
    } else {
      await deleteDictData(row.id)
    }
    await loadSectionData()
    ElMessage.success('删除成功')
  } catch (error) {
    if (error === 'cancel') {
      return
    }
    ElMessage.error(getErrorMessage(error))
  }
}

watch(
  () => route.fullPath,
  async () => {
    resetForms()
    await loadBootstrapData()
    await loadSectionData()
  },
)

onMounted(async () => {
  await loadBootstrapData()
  await loadSectionData()
})
</script>

<template>
  <section class="system-dict-page">
    <header class="hero-card">
      <div>
        <p class="eyebrow">{{ sectionTag }}</p>
        <h2>{{ sectionTitle }}</h2>
        <p>对照 ruoyi-vue-pro 的字典模型，将系统下拉选项和状态项收口到数据库字典表统一治理。</p>
      </div>
      <el-button type="primary" @click="openCreateDialog">{{ isTypeSection ? '新建字典类型' : '新建字典数据' }}</el-button>
    </header>

    <el-card shadow="never" class="panel-card">
      <el-form v-if="isTypeSection" class="filter-form" :inline="true">
        <el-form-item>
          <el-input v-model="dictTypeFilters.keyword" placeholder="字典名称 / 字典类型" clearable />
        </el-form-item>
        <el-form-item>
          <el-select v-model="dictTypeFilters.status" placeholder="全部状态" clearable style="width: 160px">
            <el-option v-for="item in statusOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadSectionData">查询</el-button>
        </el-form-item>
      </el-form>

      <el-form v-else class="filter-form" :inline="true">
        <el-form-item>
          <el-input v-model="dictDataFilters.keyword" placeholder="标签 / 键值 / 字典类型" clearable />
        </el-form-item>
        <el-form-item>
          <el-select v-model="dictDataFilters.dict_type" placeholder="全部字典类型" clearable filterable style="width: 240px">
            <el-option v-for="item in dictTypeSelectOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-select v-model="dictDataFilters.status" placeholder="全部状态" clearable style="width: 160px">
            <el-option v-for="item in statusOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadSectionData">查询</el-button>
        </el-form-item>
      </el-form>

      <el-table v-if="isTypeSection" :data="dictTypes" stripe v-loading="loading || bootstrapping">
        <el-table-column prop="dict_name" label="字典名称" min-width="180" />
        <el-table-column prop="dict_type" label="字典类型" min-width="220" />
        <el-table-column prop="status" label="状态" width="100" />
        <el-table-column prop="data_count" label="数据条数" width="100" />
        <el-table-column prop="remark" label="备注" min-width="220" show-overflow-tooltip />
        <el-table-column label="操作" width="170" fixed="right">
          <template #default="scope">
            <TableRowActions :row="scope.row" :main-actions="[{ key: 'edit', label: '编辑', onClick: () => openEditDialog(scope.row) }]" :more-actions="[{ key: 'delete', label: '删除', onClick: () => handleDelete(scope.row) }]" />
          </template>
        </el-table-column>
      </el-table>

      <el-table v-else :data="dictData" stripe v-loading="loading || bootstrapping">
        <el-table-column prop="dict_name" label="字典名称" min-width="160" />
        <el-table-column prop="dict_type" label="字典类型" min-width="200" />
        <el-table-column prop="label" label="标签" min-width="140" />
        <el-table-column prop="value" label="键值" min-width="140" />
        <el-table-column prop="sort_order" label="排序" width="90" />
        <el-table-column prop="status" label="状态" width="100" />
        <el-table-column prop="color_type" label="颜色" width="100" />
        <el-table-column prop="remark" label="备注" min-width="180" show-overflow-tooltip />
        <el-table-column label="操作" width="170" fixed="right">
          <template #default="scope">
            <TableRowActions :row="scope.row" :main-actions="[{ key: 'edit', label: '编辑', onClick: () => openEditDialog(scope.row) }]" :more-actions="[{ key: 'delete', label: '删除', onClick: () => handleDelete(scope.row) }]" />
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="dialogMode === 'create' ? (isTypeSection ? '新建字典类型' : '新建字典数据') : (isTypeSection ? '编辑字典类型' : '编辑字典数据')" width="720px">
      <el-form v-if="isTypeSection" label-width="110px" class="dialog-grid">
        <el-form-item label="字典名称">
          <el-input v-model="dictTypeForm.dict_name" />
        </el-form-item>
        <el-form-item label="字典类型">
          <el-input v-model="dictTypeForm.dict_type" :disabled="dialogMode === 'edit'" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="dictTypeForm.status" style="width: 100%">
            <el-option v-for="item in statusOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注" class="span-2">
          <el-input v-model="dictTypeForm.remark" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>

      <el-form v-else label-width="110px" class="dialog-grid">
        <el-form-item label="字典类型">
          <el-select v-model="dictDataForm.dict_type" filterable style="width: 100%">
            <el-option v-for="item in dictTypeSelectOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="字典标签">
          <el-input v-model="dictDataForm.label" />
        </el-form-item>
        <el-form-item label="字典键值">
          <el-input v-model="dictDataForm.value" />
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="dictDataForm.sort_order" :min="0" :max="9999" style="width: 100%" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="dictDataForm.status" style="width: 100%">
            <el-option v-for="item in statusOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="颜色类型">
          <el-input v-model="dictDataForm.color_type" placeholder="default / success / warning" />
        </el-form-item>
        <el-form-item label="CSS 类">
          <el-input v-model="dictDataForm.css_class" />
        </el-form-item>
        <el-form-item label="备注" class="span-2">
          <el-input v-model="dictDataForm.remark" type="textarea" :rows="3" />
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
.system-dict-page {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.hero-card {
  display: flex;
  justify-content: space-between;
  gap: 24px;
  align-items: flex-start;
  padding: 24px 28px;
  border-radius: 20px;
  background: linear-gradient(135deg, #f6f8ee 0%, #eef3ff 100%);
  border: 1px solid rgba(15, 76, 189, 0.12);
}

.hero-card h2 {
  margin: 6px 0 8px;
  font-size: 28px;
  line-height: 1.2;
}

.hero-card p {
  margin: 0;
  max-width: 720px;
  color: #52607a;
}

.eyebrow {
  font-size: 12px;
  letter-spacing: 0.18em;
  color: #0f4cbd;
  text-transform: uppercase;
}

.panel-card {
  border-radius: 18px;
}

.filter-form {
  margin-bottom: 12px;
}

.dialog-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  column-gap: 18px;
}

.span-2 {
  grid-column: 1 / -1;
}

@media (max-width: 900px) {
  .hero-card {
    flex-direction: column;
  }

  .dialog-grid {
    grid-template-columns: 1fr;
  }

  .span-2 {
    grid-column: auto;
  }
}
</style>