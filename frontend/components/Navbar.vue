<template>
  <nav class="bg-blue-600 text-white px-6 py-4 flex justify-between items-center">
    <NuxtLink to="/" class="font-bold text-xl">DailyNotes</NuxtLink>
    
    <div class="space-x-4 flex items-center">
      <!-- Show loading state during hydration -->
      <template v-if="!mounted">
        <NuxtLink to="/login" class="hover:text-blue-200 transition-colors">
          Login
        </NuxtLink>
        <NuxtLink to="/register" class="hover:text-blue-200 transition-colors">
          Register
        </NuxtLink>
      </template>
      
      <!-- Show when NOT authenticated (after mounting) -->
      <template v-else-if="!isAuthenticated">
        <NuxtLink to="/login" class="hover:text-blue-200 transition-colors">
          Login
        </NuxtLink>
        <NuxtLink to="/register" class="hover:text-blue-200 transition-colors">
          Register
        </NuxtLink>
      </template>
      
      <!-- Show when authenticated (after mounting) -->
      <template v-else>
        <NuxtLink to="/dashboard" class="hover:text-blue-200 transition-colors">
          Dashboard
        </NuxtLink>
        
        <!-- User greeting -->
        <span v-if="user" class="text-blue-200">
          Welcome, {{ user.username }}!
        </span>
        
        <!-- Logout button -->
        <button 
          @click="handleLogout"
          :disabled="isLoggingOut"
          class="bg-red-500 hover:bg-red-600 disabled:bg-red-300 px-3 py-1 rounded transition-colors"
        >
          {{ isLoggingOut ? 'Logging out...' : 'Logout' }}
        </button>
      </template>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuth } from '~/composables/useAuth'
import { useRouter } from 'vue-router'

const { isAuthenticated, user, logout, initAuth } = useAuth()
const router = useRouter()
const isLoggingOut = ref(false)
const mounted = ref(false)

// Handle logout
const handleLogout = async () => {
  if (isLoggingOut.value) return
  
  isLoggingOut.value = true
  
  try {
    await logout()
    // Redirect to home page after logout
    await router.push('/')
  } catch (error) {
    console.error('Logout failed:', error)
  } finally {
    isLoggingOut.value = false
  }
}

// Initialize auth state when component mounts (client-side only)
onMounted(() => {
  initAuth()
  mounted.value = true
})
</script>
