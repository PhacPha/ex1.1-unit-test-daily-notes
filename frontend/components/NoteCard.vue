<template>
  <div class="bg-white p-4 shadow rounded mb-3">
    <!-- View Mode -->
    <div v-if="!isEditing">
      <h2 class="font-bold">{{ note.title }}</h2>
      <p class="text-sm text-gray-600">{{ note.content }}</p>
      <p class="text-xs text-right text-gray-400">{{ note.created_at }}</p>
      <div class="flex gap-2 mt-2">
        <button 
          @click="startEdit" 
          class="text-blue-500 text-sm hover:text-blue-700 transition-colors"
        >
          Edit
        </button>
        <button 
          @click="$emit('delete', note.id)" 
          class="text-red-500 text-sm hover:text-red-700 transition-colors"
        >
          Delete
        </button>
      </div>
    </div>

    <!-- Edit Mode -->
    <div v-else>
      <input 
        v-model="editTitle"
        placeholder="Title"
        class="w-full p-2 border rounded mb-2 font-bold"
        @keyup.enter="saveEdit"
        @keyup.escape="cancelEdit"
      />
      <textarea 
        v-model="editContent"
        placeholder="Content"
        rows="3"
        class="w-full p-2 border rounded mb-2 text-sm resize-none"
        @keyup.ctrl.enter="saveEdit"
        @keyup.escape="cancelEdit"
      ></textarea>
      <div class="flex gap-2 justify-end">
        <button 
          @click="cancelEdit"
          class="px-3 py-1 text-sm text-gray-600 hover:text-gray-800 transition-colors"
        >
          Cancel
        </button>
        <button 
          @click="saveEdit"
          :disabled="!editTitle.trim() || !editContent.trim() || isSaving"
          class="px-3 py-1 text-sm bg-blue-500 text-white rounded hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          {{ isSaving ? 'Saving...' : 'Save' }}
        </button>
      </div>
      <p class="text-xs text-gray-500 mt-1">
        Press Ctrl+Enter to save, Esc to cancel
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({ note: Object })
const emit = defineEmits(['delete', 'update'])

const isEditing = ref(false)
const isSaving = ref(false)
const editTitle = ref('')
const editContent = ref('')

const startEdit = () => {
  editTitle.value = props.note.title
  editContent.value = props.note.content
  isEditing.value = true
}

const cancelEdit = () => {
  isEditing.value = false
  editTitle.value = ''
  editContent.value = ''
}

const saveEdit = async () => {
  if (!editTitle.value.trim() || !editContent.value.trim() || isSaving.value) {
    return
  }
  
  isSaving.value = true
  
  try {
    await emit('update', {
      id: props.note.id,
      title: editTitle.value.trim(),
      content: editContent.value.trim()
    })
    isEditing.value = false
  } catch (error) {
    console.error('Failed to save edit:', error)
  } finally {
    isSaving.value = false
  }
}
</script>
