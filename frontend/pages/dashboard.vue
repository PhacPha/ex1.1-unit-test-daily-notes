<template>
  <div class="p-6 max-w-3xl mx-auto">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">My Notes</h1>
      <div v-if="user" class="text-gray-600">
        <span class="text-sm">Logged in as </span>
        <span class="font-medium">{{ user.username }}</span>
      </div>
    </div>

    <div class="flex gap-2 mb-4">
      <input 
        v-model="title" 
        placeholder="Title" 
        class="border p-2 w-1/3"
        @keyup.enter="createNote"
      />
      <input 
        v-model="content" 
        placeholder="Content" 
        class="border p-2 flex-1"
        @keyup.enter="createNote"
      />
      <button 
        @click="createNote" 
        :disabled="isCreating || !title.trim() || !content.trim()"
        class="bg-green-500 text-white p-2 hover:bg-green-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
      >
        {{ isCreating ? 'Adding...' : 'Add' }}
      </button>
    </div>

    <div v-if="isLoading" class="text-center py-4">
      <p class="text-gray-600">Loading notes...</p>
    </div>

    <div v-else-if="notes.length === 0" class="text-center py-8">
      <p class="text-gray-600">No notes yet. Create your first note!</p>
    </div>

    <div v-else>
      <NoteCard
        v-for="note in notes"
        :key="note.id"
        :note="note"
        @delete="deleteNote"
        @update="updateNote"
      />
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useAuth } from '~/composables/useAuth'
import { useRouter } from 'vue-router'

// Protect this page with auth middleware
definePageMeta({
  middleware: 'auth'
})

const title = ref('')
const content = ref('')
const notes = ref([])
const isLoading = ref(false)
const isCreating = ref(false)

const { token, user, isAuthenticated, initAuth, logout } = useAuth()
const router = useRouter()

// Redirect if not authenticated
onMounted(async () => {
  initAuth()
  
  if (!isAuthenticated.value) {
    await router.push('/login')
    return
  }
  
  await fetchNotes()
})

const getAuthHeaders = () => {
  return {
    Authorization: `Bearer ${token.value}`
  }
}

const handleAuthError = async (error) => {
  if (error.response?.status === 401) {
    // Token is invalid, logout and redirect
    await logout()
    await router.push('/login')
    return true
  }
  return false
}

const fetchNotes = async () => {
  if (!token.value) return
  
  isLoading.value = true
  
  try {
    const res = await axios.get('http://localhost:5001/api/notes', {
      headers: getAuthHeaders()
    })
    notes.value = res.data
  } catch (error) {
    console.error('Failed to fetch notes:', error)
    const handled = await handleAuthError(error)
    if (!handled) {
      // Handle other errors (show notification, etc.)
      console.error('Error fetching notes:', error)
    }
  } finally {
    isLoading.value = false
  }
}

const createNote = async () => {
  if (!token.value || isCreating.value) return
  
  if (!title.value.trim() || !content.value.trim()) {
    return
  }
  
  isCreating.value = true
  
  try {
    await axios.post('http://localhost:5001/api/notes', {
      title: title.value,
      content: content.value
    }, {
      headers: getAuthHeaders()
    })
    
    title.value = ''
    content.value = ''
    await fetchNotes()
  } catch (error) {
    console.error('Create note failed:', error)
    const handled = await handleAuthError(error)
    if (!handled) {
      // Handle other errors
      console.error('Error creating note:', error)
    }
  } finally {
    isCreating.value = false
  }
}

const deleteNote = async (id) => {
  if (!token.value) return
  
  try {
    await axios.delete(`http://localhost:5001/api/notes/${id}`, {
      headers: getAuthHeaders()
    })
    await fetchNotes()
  } catch (error) {
    console.error('Delete note failed:', error)
    const handled = await handleAuthError(error)
    if (!handled) {
      // Handle other errors
      console.error('Error deleting note:', error)
    }
  }
}

const updateNote = async (noteData) => {
  if (!token.value) return
  
  try {
    await axios.put(`http://localhost:5001/api/notes/${noteData.id}`, {
      title: noteData.title,
      content: noteData.content
    }, {
      headers: getAuthHeaders()
    })
    await fetchNotes()
  } catch (error) {
    console.error('Update note failed:', error)
    const handled = await handleAuthError(error)
    if (!handled) {
      // Handle other errors
      console.error('Error updating note:', error)
    }
    throw error // Re-throw to let NoteCard handle the error state
  }
}
</script>

<style scoped>
/* Add any additional styling here if needed */
</style>

