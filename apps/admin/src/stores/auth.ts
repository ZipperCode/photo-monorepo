import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

interface LoginRequest {
  username: string
  password: string
}

interface TokenResponse {
  access_token: string
  token_type: string
  expires_in: number
}

interface UserInfo {
  id: string
  username: string
  created_at: string
}

export const useAuthStore = defineStore('auth', () => {
  // State
  const token = ref<string | null>(localStorage.getItem('auth_token'))
  const user = ref<UserInfo | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // API base URL
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

  // Computed
  const isAuthenticated = computed(() => !!token.value)

  // Actions

  /**
   * Login with username and password
   */
  async function login(credentials: LoginRequest): Promise<boolean> {
    loading.value = true
    error.value = null

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Login failed')
      }

      const data: TokenResponse = await response.json()

      // Store token
      token.value = data.access_token
      localStorage.setItem('auth_token', data.access_token)

      // Fetch user info
      await fetchUserInfo()

      return true
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Login failed'
      return false
    } finally {
      loading.value = false
    }
  }

  /**
   * Fetch current user information
   */
  async function fetchUserInfo(): Promise<void> {
    if (!token.value) {
      return
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/auth/me`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token.value}`,
        },
      })

      if (!response.ok) {
        throw new Error('Failed to fetch user info')
      }

      const userInfo: UserInfo = await response.json()
      user.value = userInfo
    } catch (err) {
      console.error('Failed to fetch user info:', err)
      // If token is invalid, clear it
      logout()
    }
  }

  /**
   * Logout and clear authentication state
   */
  function logout(): void {
    token.value = null
    user.value = null
    error.value = null
    localStorage.removeItem('auth_token')
  }

  /**
   * Initialize auth state from localStorage
   */
  async function initialize(): Promise<void> {
    const storedToken = localStorage.getItem('auth_token')
    if (storedToken) {
      token.value = storedToken
      await fetchUserInfo()
    }
  }

  // Return store interface
  return {
    // State
    token,
    user,
    loading,
    error,
    // Computed
    isAuthenticated,
    // Actions
    login,
    logout,
    fetchUserInfo,
    initialize,
  }
})
