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

const DEFAULT_THEME_COLOR = '#27A3EA'
const REDIRECT_STORAGE_KEY = 'dtlms-post-login-redirect'

function normalizeHexColor(value: string) {
  const input = String(value || '').trim()
  const normalized = input.startsWith('#') ? input.slice(1) : input
  if (/^[0-9a-fA-F]{3}$/.test(normalized)) {
    return `#${normalized
      .split('')
      .map((item) => `${item}${item}`)
      .join('')
      .toUpperCase()}`
  }
  if (/^[0-9a-fA-F]{6}$/.test(normalized)) {
    return `#${normalized.toUpperCase()}`
  }
  return DEFAULT_THEME_COLOR
}

function hexToRgb(value: string) {
  const normalized = normalizeHexColor(value).slice(1)
  return {
    r: Number.parseInt(normalized.slice(0, 2), 16),
    g: Number.parseInt(normalized.slice(2, 4), 16),
    b: Number.parseInt(normalized.slice(4, 6), 16),
  }
}

function rgbToHex(red: number, green: number, blue: number) {
  return `#${[red, green, blue]
    .map((item) => Math.max(0, Math.min(255, Math.round(item))).toString(16).padStart(2, '0'))
    .join('')
    .toUpperCase()}`
}

function mixColor(base: string, target: string, ratio: number) {
  const baseColor = hexToRgb(base)
  const targetColor = hexToRgb(target)
  const weight = Math.max(0, Math.min(1, ratio))
  return rgbToHex(
    baseColor.r * (1 - weight) + targetColor.r * weight,
    baseColor.g * (1 - weight) + targetColor.g * weight,
    baseColor.b * (1 - weight) + targetColor.b * weight,
  )
}

function rgbaString(base: string, alpha: number) {
  const color = hexToRgb(base)
  return `rgba(${color.r}, ${color.g}, ${color.b}, ${alpha})`
}


export const useAuthStore = defineStore('auth', () => {
  const username = ref('')
  const fullName = ref('')
  const roleName = ref('')
  const permissions = ref<string[]>([])
  const profile = ref<UserProfile | null>(null)
  const sessionState = ref<SessionState>('idle')
  const sessionError = ref('')
  let hydratePromise: Promise<void> | null = null

  const initials = computed(() => fullName.value.slice(0, 1) || 'D')
  const isAuthenticated = computed(() => Boolean(localStorage.getItem('dtlms-access-token')) && sessionState.value === 'ready')
  const themeColor = computed(() => profile.value?.theme_color || '#409eff')

  const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || '/api/v1'

  function applyPrincipal(principal: Principal) {
    username.value = principal.username
    fullName.value = principal.full_name || principal.username
    roleName.value = principal.roles.includes('platform_admin') ? '平台管理员' : principal.roles.join(' / ') || '未分配角色'
    permissions.value = principal.permissions
  }

  function applyThemeColor(color: string) {
    const accent = normalizeHexColor(color)
    const rootStyle = document.documentElement.style
    rootStyle.setProperty('--brand-accent', accent)
    rootStyle.setProperty('--brand', accent)
    rootStyle.setProperty('--brand-strong', mixColor(accent, '#1E4B7D', 0.2))
    rootStyle.setProperty('--brand-deep', mixColor(accent, '#16324D', 0.42))
    rootStyle.setProperty('--brand-soft', mixColor(accent, '#FFFFFF', 0.82))
    rootStyle.setProperty('--accent', mixColor(accent, '#FFFFFF', 0.56))
    rootStyle.setProperty('--surface-dark', mixColor(accent, '#FFFFFF', 0.92))
    rootStyle.setProperty('--surface-dark-2', mixColor(accent, '#FFFFFF', 0.86))
    rootStyle.setProperty('--surface-tint', mixColor(accent, '#FFFFFF', 0.8))
    rootStyle.setProperty('--hover-bg', rgbaString(accent, 0.12))
    rootStyle.setProperty('--hover-bg-strong', rgbaString(accent, 0.18))
    rootStyle.setProperty('--border', rgbaString(accent, 0.16))
    rootStyle.setProperty('--border-strong', rgbaString(accent, 0.28))
    rootStyle.setProperty('--table-header-bg', mixColor(accent, '#FFFFFF', 0.92))
    rootStyle.setProperty('--table-row-hover-bg', mixColor(accent, '#FFFFFF', 0.95))
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
    applyThemeColor(DEFAULT_THEME_COLOR)
  }

  function rememberRedirectTarget(target: string) {
    if (!target || target === '/login') {
      return
    }
    sessionStorage.setItem(REDIRECT_STORAGE_KEY, target)
  }

  function consumeRedirectTarget() {
    const target = sessionStorage.getItem(REDIRECT_STORAGE_KEY) || ''
    sessionStorage.removeItem(REDIRECT_STORAGE_KEY)
    return target
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
    applyThemeColor(response.data.theme_color)
  }

  async function hydrateSession() {
    if (!localStorage.getItem('dtlms-access-token')) {
      sessionState.value = 'idle'
      return
    }

    if (hydratePromise) {
      return hydratePromise
    }

    hydratePromise = (async () => {
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
      } finally {
        hydratePromise = null
      }
    })()

    return hydratePromise
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
    applyThemeColor(response.data.theme_color)
  }

  async function changePassword(currentPassword: string, newPassword: string) {
    await http.post('/auth/change-password', {
      current_password: currentPassword,
      new_password: newPassword,
    })
  }

  async function logout() {
    if (localStorage.getItem('dtlms-access-token')) {
      try {
        await http.post('/auth/logout')
      } catch {
        // Ignore logout failures and still clear local session.
      }
    }
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
    applyThemeColor,
    hydrateSession,
    login,
    logout,
    saveProfile,
    changePassword,
    rememberRedirectTarget,
    consumeRedirectTarget,
  }
})
