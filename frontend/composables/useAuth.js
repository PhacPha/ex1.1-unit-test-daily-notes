import { ref, computed, readonly } from 'vue'
import axios from 'axios'

// Global state for authentication
const token = ref('')
const user = ref(null)
const isAuthenticated = computed(() => !!token.value)

export const useAuth = () => {
  // Initialize auth state from localStorage
  const initAuth = () => {
    // Only run on client-side
    if (process.client && typeof window !== 'undefined') {
      const savedToken = localStorage.getItem('token')
      const savedUser = localStorage.getItem('user')
      
      if (savedToken) {
        token.value = savedToken
      }
      
      if (savedUser) {
        try {
          user.value = JSON.parse(savedUser)
        } catch (e) {
          console.error('Failed to parse saved user:', e)
          localStorage.removeItem('user')
        }
      }
    }
  }

  // Login function
  const login = async (username, password) => {
    try {
      const res = await axios.post('http://localhost:5001/api/login', {
        username,
        password
      })

      const { access_token, username: returnedUsername } = res.data
      
      // Store token and user info
      token.value = access_token
      user.value = { username: returnedUsername }
      
      // Only access localStorage on client-side
      if (process.client && typeof window !== 'undefined') {
        localStorage.setItem('token', access_token)
        localStorage.setItem('user', JSON.stringify({ username: returnedUsername }))
      }
      
      return { success: true }
    } catch (err) {
      return {
        success: false,
        error: err.response?.data?.msg || 'Login failed. Please try again.'
      }
    }
  }

  // Logout function
  const logout = async () => {
    try {
      // Call backend logout endpoint if token exists
      if (token.value) {
        await axios.post('http://localhost:5001/api/logout', {}, {
          headers: {
            Authorization: `Bearer ${token.value}`
          }
        })
      }
    } catch (err) {
      console.error('Logout API call failed:', err)
      // Continue with client-side logout even if API call fails
    }

    // Clear client-side state
    token.value = ''
    user.value = null
    
    // Only access localStorage on client-side
    if (process.client && typeof window !== 'undefined') {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    }
  }

  // Get current user info from backend
  const fetchCurrentUser = async () => {
    if (!token.value) return null

    try {
      const res = await axios.get('http://localhost:5001/api/me', {
        headers: {
          Authorization: `Bearer ${token.value}`
        }
      })
      
      user.value = res.data
      
      // Only access localStorage on client-side
      if (process.client && typeof window !== 'undefined') {
        localStorage.setItem('user', JSON.stringify(res.data))
      }
      
      return res.data
    } catch (err) {
      console.error('Failed to fetch current user:', err)
      // If token is invalid, logout
      if (err.response?.status === 401) {
        await logout()
      }
      return null
    }
  }

  // Check if user is authenticated
  const checkAuth = () => {
    return isAuthenticated.value
  }

  return {
    // State
    token: readonly(token),
    user: readonly(user),
    isAuthenticated,

    // Methods
    initAuth,
    login,
    logout,
    fetchCurrentUser,
    checkAuth
  }
} 