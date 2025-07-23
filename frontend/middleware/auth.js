import { useAuth } from '~/composables/useAuth'

export default defineNuxtRouteMiddleware(() => {
  const { isAuthenticated, initAuth } = useAuth()
  
  // Initialize auth state if not already initialized
  initAuth()
  
  // Check if user is authenticated
  if (!isAuthenticated.value) {
    return navigateTo('/login')
  }
})