<template>
  <div v-if="uploads.length > 0" class="space-y-3">
    <div class="flex items-center justify-between mb-2">
      <h3 class="text-sm font-medium text-gray-900">
        Upload Progress ({{ successCount }}/{{ uploads.length }})
      </h3>
      <span class="text-xs text-gray-500">
        {{ formatBytes(totalBytes) }}
      </span>
    </div>

    <div
      v-for="upload in uploads"
      :key="upload.filename"
      class="bg-white border rounded-lg p-3"
    >
      <div class="flex items-center justify-between mb-2">
        <div class="flex items-center space-x-2 flex-1 min-w-0">
          <div
            class="flex-shrink-0 w-5 h-5 rounded-full flex items-center justify-center"
            :class="getStatusColor(upload.status)"
          >
            <svg v-if="upload.status === 'success'" class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
            </svg>
            <svg v-else-if="upload.status === 'error'" class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
            <div v-else-if="upload.status === 'uploading'" class="w-3 h-3 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium text-gray-900 truncate">{{ upload.filename }}</p>
            <p v-if="upload.error" class="text-xs text-red-600">{{ upload.error }}</p>
            <p v-else class="text-xs text-gray-500">{{ formatBytes(upload.size) }}</p>
          </div>
        </div>
      </div>

      <div v-if="upload.status === 'uploading'" class="w-full bg-gray-200 rounded-full h-1.5">
        <div
          class="bg-blue-600 h-1.5 rounded-full transition-all duration-300"
          :style="{ width: upload.progress + '%' }"
        ></div>
      </div>
    </div>

    <div v-if="allComplete" class="mt-4 p-3 rounded-lg" :class="hasErrors ? 'bg-yellow-50' : 'bg-green-50'">
      <p class="text-sm font-medium" :class="hasErrors ? 'text-yellow-800' : 'text-green-800'">
        {{ successCount }} of {{ uploads.length }} photos uploaded successfully
      </p>
      <p v-if="hasErrors" class="text-xs text-yellow-700 mt-1">
        {{ errorCount }} failed - check errors above
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

export interface UploadItem {
  filename: string
  size: number
  status: 'pending' | 'uploading' | 'success' | 'error'
  progress: number
  error?: string
}

const props = defineProps<{
  uploads: UploadItem[]
}>()

const successCount = computed(() =>
  props.uploads.filter(u => u.status === 'success').length
)

const errorCount = computed(() =>
  props.uploads.filter(u => u.status === 'error').length
)

const allComplete = computed(() =>
  props.uploads.every(u => u.status === 'success' || u.status === 'error')
)

const hasErrors = computed(() => errorCount.value > 0)

const totalBytes = computed(() =>
  props.uploads.reduce((sum, u) => sum + u.size, 0)
)

const getStatusColor = (status: string) => {
  switch (status) {
    case 'success': return 'bg-green-500'
    case 'error': return 'bg-red-500'
    case 'uploading': return 'bg-blue-500'
    default: return 'bg-gray-300'
  }
}

const formatBytes = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}
</script>
