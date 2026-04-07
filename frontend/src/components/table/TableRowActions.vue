<script setup lang="ts">
import { MoreFilled } from '@element-plus/icons-vue'

export type TableRowAction<Row = any> = {
  key: string
  label: string
  type?: 'primary' | 'success' | 'warning' | 'danger' | 'info'
  disabled?: boolean
  onClick: (row: Row) => void | Promise<void>
}

const props = withDefaults(defineProps<{
  row: any
  mainActions?: TableRowAction[]
  moreActions?: TableRowAction[]
}>(), {
  mainActions: () => [],
  moreActions: () => [],
})

function runAction(action: TableRowAction) {
  void action.onClick(props.row)
}

function handleDropdownCommand(key: string) {
  const action = props.moreActions.find((item) => item.key === key)
  if (action && !action.disabled) {
    runAction(action)
  }
}
</script>

<template>
  <div class="table-row-actions" @click.stop>
    <el-button
      v-for="action in mainActions"
      :key="action.key"
      link
      size="small"
      :type="action.type || 'primary'"
      :disabled="action.disabled"
      @click.stop="runAction(action)"
    >
      {{ action.label }}
    </el-button>

    <el-dropdown v-if="moreActions.length" trigger="click" @command="handleDropdownCommand">
      <el-button link size="small" type="primary" @click.stop>
        更多
        <el-icon><MoreFilled /></el-icon>
      </el-button>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item
            v-for="action in moreActions"
            :key="action.key"
            :command="action.key"
            :disabled="action.disabled"
            :class="{ 'is-danger': action.type === 'danger' }"
          >
            {{ action.label }}
          </el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
  </div>
</template>

<style scoped>
.table-row-actions {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 6px;
  white-space: nowrap;
  width: 100%;
}

.table-row-actions :deep(.el-button) {
  margin: 0;
  padding: 0 2px;
}

.table-row-actions :deep(.el-dropdown) {
  line-height: 1;
}

.table-row-actions :deep(.is-danger) {
  color: var(--el-color-danger);
}
</style>