import { reactive } from 'vue'

export function useServerPagination(initialPageSize = 10) {
  const pagination = reactive({
    currentPage: 1,
    pageSize: initialPageSize,
    total: 0,
  })

  function reset() {
    pagination.currentPage = 1
  }

  function sync(total: number) {
    pagination.total = total
    const maxPage = Math.max(1, Math.ceil(total / pagination.pageSize))
    if (pagination.currentPage > maxPage) {
      pagination.currentPage = maxPage
    }
  }

  function handleCurrentChange(page: number) {
    pagination.currentPage = page
  }

  function handleSizeChange(pageSize: number) {
    pagination.pageSize = pageSize
    pagination.currentPage = 1
  }

  return {
    pagination,
    reset,
    sync,
    handleCurrentChange,
    handleSizeChange,
  }
}