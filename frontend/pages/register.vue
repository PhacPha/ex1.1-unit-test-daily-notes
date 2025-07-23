<template>
  <div class="register-container">
    <div class="bg-white p-6 rounded shadow w-80">
      <h1 class="text-xl font-bold mb-4 text-center">Create Account</h1>
      
      <input
        v-model="username"
        placeholder="Username"
        class="mb-3 p-2 border w-full rounded"
        :class="{ 'border-red-500': errors.username }"
      />
      <p v-if="errors.username" class="text-red-500 text-xs mb-2">{{ errors.username }}</p>

      <input
        v-model="password"
        type="password"
        placeholder="Password"
        class="mb-3 p-2 border w-full rounded"
        :class="{ 'border-red-500': errors.password }"
      />
      <p v-if="errors.password" class="text-red-500 text-xs mb-2">{{ errors.password }}</p>

      <input
        v-model="confirmPassword"
        type="password"
        placeholder="Confirm Password"
        class="mb-4 p-2 border w-full rounded"
        :class="{ 'border-red-500': errors.confirmPassword }"
      />
      <p v-if="errors.confirmPassword" class="text-red-500 text-xs mb-4">{{ errors.confirmPassword }}</p>

      <button
        @click="handleRegister"
        :disabled="isLoading"
        class="bg-green-500 text-white p-2 w-full rounded hover:bg-green-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
      >
        {{ isLoading ? 'Creating Account...' : 'Register' }}
      </button>

      <p v-if="errorMsg" class="text-red-500 text-sm mt-3 text-center">
        {{ errorMsg }}
      </p>

      <p v-if="successMsg" class="text-green-500 text-sm mt-3 text-center">
        {{ successMsg }}
      </p>

      <div class="text-center mt-4">
        <p class="text-sm text-gray-600">
          Already have an account? 
          <NuxtLink to="/login" class="text-blue-500 hover:text-blue-700 underline">
            Login here
          </NuxtLink>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const errorMsg = ref('')
const successMsg = ref('')
const isLoading = ref(false)
const errors = ref({})
const router = useRouter()

// Lock scroll when component mounts
onMounted(() => {
  document.body.style.overflow = 'hidden'
  document.documentElement.style.overflow = 'hidden'
})

// Restore scroll when component unmounts
onUnmounted(() => {
  document.body.style.overflow = ''
  document.documentElement.style.overflow = ''
})

// Form validation
const validateForm = () => {
  errors.value = {}
  let isValid = true

  // Username validation
  if (!username.value.trim()) {
    errors.value.username = 'Username is required'
    isValid = false
  } else if (username.value.length < 3) {
    errors.value.username = 'Username must be at least 3 characters'
    isValid = false
  } else if (!/^[a-zA-Z0-9_]+$/.test(username.value)) {
    errors.value.username = 'Username can only contain letters, numbers, and underscores'
    isValid = false
  }

  // Password validation
  if (!password.value) {
    errors.value.password = 'Password is required'
    isValid = false
  } else if (password.value.length < 6) {
    errors.value.password = 'Password must be at least 6 characters'
    isValid = false
  }

  // Confirm password validation
  if (!confirmPassword.value) {
    errors.value.confirmPassword = 'Please confirm your password'
    isValid = false
  } else if (password.value !== confirmPassword.value) {
    errors.value.confirmPassword = 'Passwords do not match'
    isValid = false
  }

  return isValid
}

const handleRegister = async () => {
  errorMsg.value = ''
  successMsg.value = ''
  
  if (!validateForm()) {
    return
  }

  isLoading.value = true
  
  try {
    const res = await axios.post('http://localhost:5001/api/register', {
      username: username.value,
      password: password.value
    })

    successMsg.value = 'Account created successfully! Redirecting to login...'
    
    // Redirect to login after 2 seconds
    setTimeout(() => {
      router.push('/login')
    }, 2000)

  } catch (err) {
    errorMsg.value = err.response?.data?.msg || 'Registration failed. Please try again.'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.register-container {
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