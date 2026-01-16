<template>
  <div
    class="border-2 border-dashed rounded-lg p-8 text-center transition-colors"
    :class="[
      isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400',
      files.length > 0 ? 'mb-4' : ''
    ]"
    @dragover.prevent="isDragging = true"
    @dragleave.prevent="isDragging = false"
    @drop.prevent="handleDrop"
  >
    <input
      ref="fileInput"
      type="file"
      multiple
      accept="image/*"
      class="hidden"
      @change="handleFileSelect"
    />

    <div v-if="files.length === 0">
      <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
        <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
      </svg>
      <p class="mt-2 text-sm text-gray-600">
        Drag and drop photos here, or
        <button
          type="button"
          class="text-blue-600 hover:text-blue-500 font-medium"
          @click="$refs.fileInput.click()"
        >
          browse
        </button>
      </p>
      <p class="mt-1 text-xs text-gray-500">PNG, JPG, GIF up to 50MB</p>
    </div>

    <div v-else>
      <p class="text-sm text-gray-600">
        {{ files.length }} file{{ files.length > 1 ? 's' : '' }} selected
      </p>
      <button
        type="button"
        class="mt-2 text-blue-600 hover:text-blue-500 text-sm font-medium"
        @click="$refs.fileInput.click()"
      >
        Add more files
      </button>
    </div>
  </div>

  <div v-if="files.length > 0" class="space-y-2">
    <div
      v-for="(file, index) in files"
      :key="index"
      class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
    >
      <div class="flex items-center space-x-3 flex-1 min-w-0">
        <svg class="h-5 w-5 text-gray-400 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clip-rule="evenodd" />
        </svg>
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium text-gray-900 truncate">{{ file.name }}</p>
          <p class="text-xs text-gray-500">{{ formatFileSize(file.size) }}</p>
        </div>
      </div>
      <button
        type="button"
        class="ml-3 text-red-600 hover:text-red-500"
        @click="removeFile(index)"
      >
        <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  'update:files': [files: File[]]
}>()

const files = ref<File[]>([])
const isDragging = ref(false)
const fileInput = ref<HTMLInputElement>()

const handleDrop = (e: DragEvent) => {
  isDragging.value = false
  const droppedFiles = Array.from(e.dataTransfer?.files || [])
  addFiles(droppedFiles)
}

const handleFileSelect = (e: Event) => {
  const target = e.target as HTMLInputElement
  const selectedFiles = Array.from(target.files || [])
  addFiles(selectedFiles)
  target.value = ''
}

const addFiles = (newFiles: File[]) => {
  const imageFiles = newFiles.filter(file => file.type.startsWith('image/'))
  files.value.push(...imageFiles)
  emit('update:files', files.value)
}

const removeFile = (index: number) => {
  files.value.splice(index, 1)
  emit('update:files', files.value)
}

const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}
</script>
