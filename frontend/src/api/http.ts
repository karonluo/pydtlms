import axios from 'axios'

const REDIRECT_STORAGE_KEY = 'dtlms-post-login-redirect'


function redirectToLogin() {
  const currentPath = `${window.location.pathname}${window.location.search}${window.location.hash}`
  if (window.location.pathname !== '/login') {
    sessionStorage.setItem(REDIRECT_STORAGE_KEY, currentPath)
    window.location.replace(`/login?redirect=${encodeURIComponent(currentPath)}`)
  }
}

const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1',
  timeout: 10000,
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
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('dtlms-access-token')
      localStorage.removeItem('dtlms-refresh-token')
      redirectToLogin()
    }
    return Promise.reject(error)
  },
)

export default http
