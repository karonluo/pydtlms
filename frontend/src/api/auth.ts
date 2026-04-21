import axios from 'axios'

import http from './http'


export type LoginPayload = {
  username: string
  password: string
}


export type UserProfile = {
  username: string
  full_name: string
  role_name: string
  department_name: string
  phone_number?: string | null
  email?: string | null
  theme_color: string
}


export type PasswordChangePayload = {
  current_password: string
  new_password: string
}


export function loginRequest(payload: LoginPayload) {
  const body = new URLSearchParams()
  body.set('username', payload.username)
  body.set('password', payload.password)
  body.set('grant_type', 'password')
  return axios.post(`${import.meta.env.VITE_API_BASE_URL || '/api/v1'}/auth/token`, body, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  })
}


export function getProfile() {
  return http.get<UserProfile>('/auth/profile')
}


export function updateProfile(payload: Pick<UserProfile, 'full_name' | 'phone_number' | 'email' | 'theme_color'>) {
  return http.put<UserProfile>('/auth/profile', payload)
}


export function changePassword(payload: PasswordChangePayload) {
  return http.post('/auth/change-password', payload)
}
