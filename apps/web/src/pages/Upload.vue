<template>
  <div class="min-h-screen bg-gray-50 py-8 px-4">
    <div class="max-w-3xl mx-auto">
      <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
        <h1 class="text-2xl font-bold text-gray-900 mb-2">Upload Photos</h1>
        <p class="text-gray-600 mb-4">
          Upload your photos to collection: <span class="font-mono font-semibold">{{ collectionCode }}</span>
        </p>

        <div v-if="error" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
          <p class="text-sm text-red-800">{{ error }}</p>
        </div>

        <FileDropZone v-model:files="selectedFiles" />

        <div v-if="selectedFiles.length > 0 && !isUploading" class="mt-4">
          <button
            @click="startUpload"
            class="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-4 rounded-lg transition-colors"
          >
            Upload {{ selectedFiles.length }} photo{{ selectedFiles.length > 1 ? 's' : '' }}
          </button>
        </div>
      </div>

      <div v-if="uploads.length > 0" class="bg-white rounded-lg shadow-sm p-6">
        <UploadProgress :uploads="uploads" />

        <div v-if="allComplete && !hasErrors" class="mt-4">
          <button
            @click="reset"
            class="w-full bg-gray-600 hover:bg-gray-700 text-white font-medium py-3 px-4 rounded-lg transition-colors"
          >
            Upload More Photos
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import FileDropZone from '../components/upload/FileDropZone.vue'
import UploadProgress, { type UploadItem } from '../components/upload/UploadProgress.vue'

const route = useRoute()
const collectionCode = ref(route.params.code as string || '')

const selectedFiles = ref<File[]>([])
const uploads = ref<UploadItem[]>([])
const isUploading = ref(false)
const error = ref('')

const allComplete = computed(() =>
  uploads.value.length > 0 && uploads.value.every(u => u.status === 'success' || u.status === 'error')
)

const hasErrors = computed(() =>
  uploads.value.some(u => u.status === 'error')
)

const startUpload = async () => {
  if (!collectionCode.value) {
    error.value = 'Please enter a collection code'
    return
  }

  if (selectedFiles.value.length === 0) {
    error.value = 'Please select at least one photo'
    return
  }

  error.value = ''
  isUploading.value = true

  // Initialize upload items
  uploads.value = selectedFiles.value.map(file => ({
    filename: file.name,
    size: file.size,
    status: 'pending' as const,
    progress: 0
  }))

  // Create FormData
  const formData = new FormData()
  selectedFiles.value.forEach(file => {
    formData.append('files', file)
  })

  try {
    // Update all to uploading
    uploads.value.forEach(u => {
      u.status = 'uploading'
      u.progress = 50
    })

    // Upload to API
    const response = await axios.post(
      `http://localhost:8000/api/v1/collections/${collectionCode.value}/photos`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / (progressEvent.total || 1))
          uploads.value.forEach(u => {
            if (u.status === 'uploading') {
              u.progress = percentCompleted
            }
          })
        }
      }
    )

    // Update status based on response
    const { uploaded, failed } = response.data

    // Mark successful uploads
    uploaded.forEach((result: any) => {
      const upload = uploads.value.find(u => u.filename === result.filename)
      if (upload) {
        upload.status = 'success'
        upload.progress = 100
      }
    })

    // Mark failed uploads
    failed.forEach((result: any) => {
      const upload = uploads.value.find(u => u.filename === result.filename)
      if (upload) {
        upload.status = 'error'
        upload.error = result.error
      }
    })

  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Upload failed. Please try again.'
    uploads.value.forEach(u => {
      if (u.status === 'uploading') {
        u.status = 'error'
        u.error = 'Upload failed'
      }
    })
  } finally {
    isUploading.value = false
  }
}

const reset = () => {
  selectedFiles.value = []
  uploads.value = []
  error.value = ''
}
</script>
