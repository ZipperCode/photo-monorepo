<template>
  <el-dialog
    v-model="visible"
    :title="isEditMode ? 'Edit Collection' : 'Create Collection'"
    width="600px"
    @close="handleClose"
  >
    <el-form
      ref="formRef"
      :model="form"
      :rules="formRules"
      label-width="140px"
      @submit.prevent="handleSubmit"
    >
      <!-- Collection Name -->
      <el-form-item label="Collection Name" prop="name">
        <el-input
          v-model="form.name"
          placeholder="e.g., Wedding Photos, Event Name"
          maxlength="100"
          show-word-limit
        />
      </el-form-item>

      <!-- Description -->
      <el-form-item label="Description" prop="description">
        <el-input
          v-model="form.description"
          type="textarea"
          placeholder="Optional description"
          :rows="3"
          maxlength="500"
          show-word-limit
        />
      </el-form-item>

      <!-- Status -->
      <el-form-item label="Status" prop="status">
        <el-select v-model="form.status" placeholder="Select status">
          <el-option label="Active" value="active">
            <div class="status-option">
              <el-tag type="success" size="small">Active</el-tag>
              <span class="status-desc">Accepting uploads</span>
            </div>
          </el-option>
          <el-option label="Archived" value="archived">
            <div class="status-option">
              <el-tag type="warning" size="small">Archived</el-tag>
              <span class="status-desc">Read-only, preserved</span>
            </div>
          </el-option>
          <el-option label="Closed" value="closed">
            <div class="status-option">
              <el-tag type="danger" size="small">Closed</el-tag>
              <span class="status-desc">Not accepting uploads</span>
            </div>
          </el-option>
        </el-select>
      </el-form-item>

      <!-- Upload Settings -->
      <el-divider content-position="left">Upload Settings</el-divider>

      <el-form-item label="Allow Uploads">
        <el-switch
          v-model="form.settings!.allow_upload"
          active-text="Enabled"
          inactive-text="Disabled"
        />
        <span class="form-tip">
          When enabled, users can upload photos to this collection
        </span>
      </el-form-item>

      <el-form-item label="Max File Size">
        <el-input-number
          v-model="form.settings!.max_file_size"
          :min="1"
          :max="100"
          :step="1"
          controls-position="right"
        />
        <span class="unit-label">MB</span>
        <span class="form-tip">
          Maximum size per photo (1-100 MB)
        </span>
      </el-form-item>

      <el-form-item label="Allowed Extensions">
        <el-checkbox-group v-model="selectedExtensions">
          <el-checkbox label=".jpg">JPG</el-checkbox>
          <el-checkbox label=".jpeg">JPEG</el-checkbox>
          <el-checkbox label=".png">PNG</el-checkbox>
          <el-checkbox label=".gif">GIF</el-checkbox>
          <el-checkbox label=".webp">WebP</el-checkbox>
        </el-checkbox-group>
      </el-form-item>

      <!-- Generated Code (Display Only) -->
      <el-alert
        v-if="generatedCode"
        title="Collection Code Generated!"
        type="success"
        :closable="false"
        show-icon
        class="code-alert"
      >
        <template #default>
          <div class="generated-code">
            {{ generatedCode }}
          </div>
          <div class="code-tip">
            Share this code with users to allow them to upload photos
          </div>
        </template>
      </el-alert>
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">Cancel</el-button>
        <el-button
          type="primary"
          :loading="collectionsStore.loading"
          @click="handleSubmit"
        >
          {{ isEditMode ? 'Save Changes' : 'Create Collection' }}
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch } from 'vue'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { useCollectionsStore, type Collection, type CollectionCreate } from '../stores/collections'

interface Props {
  modelValue: boolean
  collection?: Collection
}

interface Emits {
  (e: 'update:modelValue', value: boolean): void
  (e: 'success', collection: Collection): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const collectionsStore = useCollectionsStore()
const formRef = ref<FormInstance>()
const generatedCode = ref<string>('')

// Dialog visibility
const visible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

// Form mode
const isEditMode = computed(() => !!props.collection)

// Form data
const form = reactive<CollectionCreate>({
  name: '',
  description: '',
  status: 'active',
  settings: {
    allow_upload: true,
    max_file_size: 10,
    allowed_extensions: ['.jpg', '.jpeg', '.png', '.gif', '.webp']
  }
})

// Selected extensions for checkbox group
const selectedExtensions = ref<string[]>([
  '.jpg', '.jpeg', '.png', '.gif', '.webp'
])

// Watch for changes in selected extensions
watch(selectedExtensions, (newVal) => {
  if (form.settings) {
    form.settings.allowed_extensions = newVal
  }
}, { deep: true })

// Form validation rules
const formRules: FormRules = {
  name: [
    { required: true, message: 'Please enter collection name', trigger: 'blur' },
    { min: 3, max: 100, message: 'Name must be 3-100 characters', trigger: 'blur' }
  ],
  status: [
    { required: true, message: 'Please select status', trigger: 'change' }
  ]
}

// Initialize form when collection prop changes
watch(() => props.collection, (collection) => {
  if (collection) {
    // Edit mode - populate form with existing data
    form.name = collection.name
    form.description = collection.description || ''
    form.status = collection.status
    form.settings = { ...collection.settings }
    selectedExtensions.value = collection.settings.allowed_extensions || []
    generatedCode.value = ''
  } else {
    // Create mode - reset form
    resetForm()
  }
}, { immediate: true })

/**
 * Reset form to default values
 */
function resetForm(): void {
  form.name = ''
  form.description = ''
  form.status = 'active'
  form.settings = {
    allow_upload: true,
    max_file_size: 10,
    allowed_extensions: ['.jpg', '.jpeg', '.png', '.gif', '.webp']
  }
  selectedExtensions.value = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
  generatedCode.value = ''
  formRef.value?.clearValidate()
}

/**
 * Handle dialog close
 */
function handleClose(): void {
  emit('update:modelValue', false)
  setTimeout(resetForm, 300) // Reset after dialog closes
}

/**
 * Handle form submission
 */
async function handleSubmit(): Promise<void> {
  if (!formRef.value) return

  try {
    await formRef.value.validate()

    // Convert max_file_size from MB to bytes
    const submitData: CollectionCreate = {
      name: form.name,
      description: form.description || undefined,
      status: form.status,
      settings: {
        ...form.settings,
        max_file_size: (form.settings!.max_file_size || 10) * 1024 * 1024
      }
    }

    let result: Collection

    if (isEditMode.value && props.collection) {
      // Update existing collection
      result = await collectionsStore.updateCollection(
        props.collection.code,
        submitData
      )!
      ElMessage.success('Collection updated successfully')
    } else {
      // Create new collection
      result = await collectionsStore.createCollection(submitData)
      generatedCode.value = result.code
      ElMessage.success('Collection created successfully')
    }

    emit('success', result)

    // Close dialog after a short delay to show the generated code
    if (!isEditMode.value) {
      setTimeout(() => {
        handleClose()
      }, 2000)
    } else {
      handleClose()
    }
  } catch (error) {
    console.error('Form submission error:', error)
    if (typeof error === 'string') {
      ElMessage.error(error)
    }
  }
}
</script>

<style scoped>
.status-option {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-desc {
  font-size: 12px;
  color: #909399;
}

.form-tip {
  display: block;
  margin-top: 4px;
  font-size: 12px;
  color: #909399;
}

.unit-label {
  margin-left: 8px;
  color: #606266;
}

.code-alert {
  margin-top: 16px;
}

.generated-code {
  font-size: 32px;
  font-weight: 700;
  color: #67c23a;
  text-align: center;
  letter-spacing: 4px;
  font-family: 'Courier New', monospace;
  margin: 8px 0;
}

.code-tip {
  font-size: 13px;
  color: #606266;
  text-align: center;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

/* Checkbox group styling */
:deep(.el-checkbox-group) {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

:deep(.el-checkbox) {
  margin-right: 0;
}

/* Select option styling */
:deep(.el-select-dropdown__item) {
  padding: 8px 12px;
}
</style>
