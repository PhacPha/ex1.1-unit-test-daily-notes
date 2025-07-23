<template>
  <div class="login-container">
    <div class="bg-white p-6 rounded shadow w-80">
      <h1 class="text-xl font-bold mb-4 text-center">Login</h1>
      
      <input
        v-model="username"
        placeholder="Username"
        class="mb-3 p-2 border w-full rounded"
        @keyup.enter="handleLogin"
      />

      <input
        v-model="password"
        type="password"
        placeholder="Password"
        class="mb-4 p-2 border w-full rounded"
        @keyup.enter="handleLogin"
      />

      <button
        @click="handleLogin"
        :disabled="isLoading"
        class="bg-blue-500 text-white p-2 w-full rounded hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
      >
        {{ isLoading ? 'Logging in...' : 'Login' }}
      </button>

      <p v-if="errorMsg" class="text-red-500 text-sm mt-3 text-center">
        {{ errorMsg }}
      </p>

      <div class="text-center mt-4">
        <p class="text-sm text-gray-600">
          Don't have an account? 
          <NuxtLink to="/register" class="text-blue-500 hover:text-blue-700 underline">
            Register here
          </NuxtLink>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '~/composables/useAuth'

const username = ref('')
const password = ref('')
const errorMsg = ref('')
const isLoading = ref(false)
const router = useRouter()

const { login, isAuthenticated } = useAuth()

// Lock scroll when component mounts
onMounted(() => {
  document.body.style.overflow = 'hidden'
  document.documentElement.style.overflow = 'hidden'
  
  // Redirect if already authenticated
  if (isAuthenticated.value) {
    router.push('/dashboard')
  }
})

// Restore scroll when component unmounts
onUnmounted(() => {
  document.body.style.overflow = ''
  document.documentElement.style.overflow = ''
})

const handleLogin = async () => {
  if (isLoading.value) return
  
  errorMsg.value = ''
  
  if (!username.value.trim() || !password.value.trim()) {
    errorMsg.value = 'Please enter both username and password'
    return
  }
  
  isLoading.value = true
  
  try {
    const result = await login(username.value, password.value)
    
    if (result.success) {
      // Login successful, redirect to dashboard
      await router.push('/dashboard')
    } else {
      errorMsg.value = result.error
    }
  } catch (error) {
    errorMsg.value = 'An unexpected error occurred. Please try again.'
    console.error('Login error:', error)
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 120px); /* Account for navbar and footer height */
  background-color: #f3f4f6;
  padding: 20px 0;
}

/* Ensure the layout works properly */
:global(html, body) {
  height: 100%;
  margin: 0;
  padding: 0;
}

/* Make sure the main content area uses available space correctly */
:global(.flex-1) {
  display: flex !important;
  flex-direction: column;
}
</style>
