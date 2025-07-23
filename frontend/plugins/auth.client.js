import { useAuth } from '~/composables/useAuth'

export default defineNuxtPlugin(() => {
  const { initAuth } = useAuth()
  
  // Initialize authentication state when the app starts
  initAuth()
}) 