import axios from 'axios'

const REDIRECT_STORAGE_KEY = 'dtlms-post-login-redirect'
export const DEFAULT_HTTP_TIMEOUT_MS = 30 * 60 * 1000
const REFRESH_ENDPOINT = '/auth/refresh'

let refreshPromise: Promise<boolean> | null = null


function redirectToLogin() {
  const currentPath = `${window.location.pathname}${window.location.search}${window.location.hash}`
  if (window.location.pathname !== '/login') {
    sessionStorage.setItem(REDIRECT_STORAGE_KEY, currentPath)
    window.location.replace(`/login?redirect=${encodeURIComponent(currentPath)}`)
  }
}

async function refreshSession() {
  if (refreshPromise) {
    return refreshPromise
  }

  refreshPromise = (async () => {
    const refreshToken = localStorage.getItem('dtlms-refresh-token')
    if (!refreshToken) {
      return false
    }

    try {
      const response = await axios.post(
        `${import.meta.env.VITE_API_BASE_URL || '/api/v1'}${REFRESH_ENDPOINT}`,
        { refresh_token: refreshToken },
        { timeout: DEFAULT_HTTP_TIMEOUT_MS },
      )
      localStorage.setItem('dtlms-access-token', response.data.access_token)
      localStorage.setItem('dtlms-refresh-token', response.data.refresh_token)
      return true
    } catch {
      localStorage.removeItem('dtlms-access-token')
      localStorage.removeItem('dtlms-refresh-token')
      return false
    } finally {
      refreshPromise = null
    }
  })()

  return refreshPromise
}

const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1',
  timeout: DEFAULT_HTTP_TIMEOUT_MS,
})

http.interceptors.request.use((config) => {
  const token = localStorage.getItem('dtlms-access-token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

http.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      const originalRequest = error.config
      if (originalRequest && !originalRequest.__isRetryRequest) {
        originalRequest.__isRetryRequest = true
        const refreshed = await refreshSession()
        if (refreshed) {
          const token = localStorage.getItem('dtlms-access-token')
          if (token) {
            originalRequest.headers = originalRequest.headers || {}
            originalRequest.headers.Authorization = `Bearer ${token}`
            return http.request(originalRequest)
          }
        }
      }

      localStorage.removeItem('dtlms-access-token')
      localStorage.removeItem('dtlms-refresh-token')
      redirectToLogin()
    }
    return Promise.reject(error)
  },
)

export default http
