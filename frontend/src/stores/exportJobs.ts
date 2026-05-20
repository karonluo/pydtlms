import axios from 'axios'
import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

import {
  downloadRegisteredPortalStudentExportJob,
  listRegisteredPortalStudentExportJobs,
  markRegisteredPortalStudentExportJobsRead,
  type RegisteredPortalStudentExportJobRecord,
} from '../api/students'


const POLL_INTERVAL_MS = 10000


function resolveStatusLevel(job: RegisteredPortalStudentExportJobRecord) {
  if (job.status === 'failed') return 'danger'
  if (job.status === 'completed') return 'success'
  return 'info'
}


export const useExportJobStore = defineStore('exportJobs', () => {
  const jobs = ref<RegisteredPortalStudentExportJobRecord[]>([])
  const unreadCount = ref(0)
  const loading = ref(false)
  const downloadingJobId = ref('')
  let timer: number | null = null

  const latestJob = computed(() => jobs.value[0] || null)
  const hasActiveJobs = computed(() => jobs.value.some((job) => job.status === 'pending' || job.status === 'running'))
  const iconStatus = computed(() => {
    if (unreadCount.value > 0 && jobs.value.some((job) => !job.is_read && job.status === 'failed')) return 'danger'
    if (unreadCount.value > 0 && jobs.value.some((job) => !job.is_read && job.status === 'completed')) return 'success'
    if (hasActiveJobs.value) return 'warning'
    return 'info'
  })

  async function fetchJobs(options?: { silent?: boolean }) {
    if (!options?.silent) {
      loading.value = true
    }
    try {
      const response = await listRegisteredPortalStudentExportJobs()
      jobs.value = response.data.items
      unreadCount.value = response.data.unread_count
    } finally {
      loading.value = false
    }
  }

  async function acknowledgeJobs() {
    if (!unreadCount.value) return
    await markRegisteredPortalStudentExportJobsRead()
    jobs.value = jobs.value.map((job) => ({ ...job, is_read: true }))
    unreadCount.value = 0
  }

  async function downloadJob(job: RegisteredPortalStudentExportJobRecord) {
    if (job.status !== 'completed') {
      return
    }
    downloadingJobId.value = job.job_id
    try {
      const response = await downloadRegisteredPortalStudentExportJob(job.job_id)
      const blob = new Blob([response.data], {
        type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      })
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      const disposition = String(response.headers['content-disposition'] || '')
      const matched = disposition.match(/filename\*=UTF-8''([^;]+)/)
      link.href = url
      link.download = matched ? decodeURIComponent(matched[1]) : job.file_name
      document.body.append(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(String(error.response?.data?.detail || error.message || '下载失败'))
      }
      throw error
    } finally {
      downloadingJobId.value = ''
    }
  }

  function startPolling() {
    if (timer !== null) return
    void fetchJobs({ silent: true })
    timer = window.setInterval(() => {
      void fetchJobs({ silent: true })
    }, POLL_INTERVAL_MS)
  }

  function stopPolling() {
    if (timer !== null) {
      window.clearInterval(timer)
      timer = null
    }
  }

  function clear() {
    stopPolling()
    jobs.value = []
    unreadCount.value = 0
    loading.value = false
    downloadingJobId.value = ''
  }

  return {
    jobs,
    unreadCount,
    loading,
    latestJob,
    hasActiveJobs,
    iconStatus,
    downloadingJobId,
    fetchJobs,
    acknowledgeJobs,
    downloadJob,
    startPolling,
    stopPolling,
    clear,
    resolveStatusLevel,
  }
})