import axios from 'axios'
import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

import http from '../api/http'


type SessionState = 'idle' | 'loading' | 'ready' | 'error'


type Principal = {
  username: string
  full_name: string
  roles: string[]
  permissions: string[]
}


type UserProfile = {
  username: string
  full_name: string
  role_name: string
  department_name: string
  phone_number?: string | null
  email?: string | null
  theme_color: string
}


type TokenResponse = {
  access_token: string
  refresh_token: string
}


export const useAuthStore = defineStore('auth', () => {
  const username = ref('')
  const fullName = ref('')
  const roleName = ref('')
  const permissions = ref<string[]>([])
  const profile = ref<UserProfile | null>(null)
  const sessionState = ref<SessionState>('idle')
  const sessionError = ref('')

  const initials = computed(() => fullName.value.slice(0, 1) || 'D')
  const isAuthenticated = computed(() => Boolean(localStorage.getItem('dtlms-access-token')) && sessionState.value === 'ready')
  const themeColor = computed(() => profile.value?.theme_color || '#0f4cbd')

  const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/v1'

  function applyPrincipal(principal: Principal) {
    username.value = principal.username
    fullName.value = principal.full_name || principal.username
    roleName.value = principal.roles.includes('platform_admin') ? '平台管理员' : principal.roles.join(' / ') || '未分配角色'
    permissions.value = principal.permissions
  }

  function clearSession() {
    localStorage.removeItem('dtlms-access-token')
    localStorage.removeItem('dtlms-refresh-token')
    username.value = ''
    fullName.value = ''
    roleName.value = ''
    permissions.value = []
    profile.value = null
    sessionState.value = 'idle'
    sessionError.value = ''
    document.documentElement.style.setProperty('--brand-accent', '#0f4cbd')
  }

  async function requestToken(usernameValue: string, password: string) {
    const payload = new URLSearchParams()
    payload.set('username', usernameValue)
    payload.set('password', password)
    payload.set('grant_type', 'password')

    const response = await axios.post<TokenResponse>(`${apiBaseUrl}/auth/token`, payload, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })

    localStorage.setItem('dtlms-access-token', response.data.access_token)
    localStorage.setItem('dtlms-refresh-token', response.data.refresh_token)
  }

  async function loadPrincipal() {
    const response = await http.get<Principal>('/auth/me')
    applyPrincipal(response.data)
  }

  async function loadProfile() {
    const response = await http.get<UserProfile>('/auth/profile')
    profile.value = response.data
    fullName.value = response.data.full_name
    roleName.value = response.data.role_name
    document.documentElement.style.setProperty('--brand-accent', response.data.theme_color)
  }

  async function hydrateSession() {
    if (!localStorage.getItem('dtlms-access-token')) {
      sessionState.value = 'idle'
      return
    }

    if (sessionState.value === 'loading') {
      return
    }

    sessionState.value = 'loading'
    sessionError.value = ''

    try {
      await loadPrincipal()
      await loadProfile()
      sessionState.value = 'ready'
    } catch (error) {
      clearSession()
      sessionState.value = 'error'
      sessionError.value = '会话已失效，请重新登录。'
      throw error
    }
  }

  async function login(usernameValue: string, password: string) {
    sessionState.value = 'loading'
    sessionError.value = ''
    try {
      await requestToken(usernameValue, password)
      await loadPrincipal()
      await loadProfile()
      sessionState.value = 'ready'
    } catch (error) {
      clearSession()
      sessionState.value = 'error'
      sessionError.value = '登录失败，请检查账号和密码。'
      throw error
    }
  }

  async function saveProfile(payload: Pick<UserProfile, 'full_name' | 'phone_number' | 'email' | 'theme_color'>) {
    const response = await http.put<UserProfile>('/auth/profile', payload)
    profile.value = response.data
    fullName.value = response.data.full_name
    roleName.value = response.data.role_name
    document.documentElement.style.setProperty('--brand-accent', response.data.theme_color)
  }

  async function changePassword(currentPassword: string, newPassword: string) {
    await http.post('/auth/change-password', {
      current_password: currentPassword,
      new_password: newPassword,
    })
  }

  function logout() {
    clearSession()
  }

  return {
    username,
    fullName,
    roleName,
    permissions,
    profile,
    initials,
    isAuthenticated,
    themeColor,
    sessionState,
    sessionError,
    hydrateSession,
    login,
    logout,
    saveProfile,
    changePassword,
  }
})
