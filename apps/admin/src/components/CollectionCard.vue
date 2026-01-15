<template>
  <el-card class="collection-card" shadow="hover">
    <!-- Status Badge -->
    <div class="card-header">
      <el-tag :type="statusTagType" size="small">
        {{ collection.status }}
      </el-tag>
      <el-dropdown trigger="click" @command="handleCommand">
        <el-button type="text" class="more-button">
          <el-icon><MoreFilled /></el-icon>
        </el-button>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="edit">Edit</el-dropdown-item>
            <el-dropdown-item command="delete" divided>Delete</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>

    <!-- Collection Code (Large) -->
    <div class="collection-code">
      {{ collection.code }}
    </div>

    <!-- Collection Name -->
    <h3 class="collection-name">
      {{ collection.name }}
    </h3>

    <!-- Description -->
    <p v-if="collection.description" class="collection-description">
      {{ collection.description }}
    </p>

    <!-- Statistics -->
    <div class="collection-stats">
      <div class="stat-item">
        <el-icon><Picture /></el-icon>
        <span>{{ collection.statistics.total_photos }} photos</span>
      </div>
      <div class="stat-item">
        <el-icon><Document /></el-icon>
        <span>{{ formatFileSize(collection.statistics.total_size_bytes) }}</span>
      </div>
    </div>

    <!-- Upload Status -->
    <div class="upload-status">
      <el-tag :type="collection.settings.allow_upload ? 'success' : 'info'" size="small">
        {{ collection.settings.allow_upload ? 'Upload enabled' : 'Upload disabled' }}
      </el-tag>
    </div>

    <!-- Created Info -->
    <div class="created-info">
      Created by {{ collection.created_by }} · {{ formatDate(collection.created_at) }}
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { MoreFilled, Picture, Document } from '@element-plus/icons-vue'
import type { Collection } from '../stores/collections'

interface Props {
  collection: Collection
}

interface Emits {
  (e: 'edit', collection: Collection): void
  (e: 'delete', code: string): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

/**
 * Get tag type based on collection status
 */
const statusTagType = computed(() => {
  const statusMap = {
    active: 'success',
    archived: 'warning',
    closed: 'danger'
  }
  return statusMap[props.collection.status] || 'info'
})

/**
 * Format file size in human-readable format
 */
function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

/**
 * Format date to readable string
 */
function formatDate(dateString: string): string {
  const date = new Date(dateString)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))

  if (diffDays === 0) return 'Today'
  if (diffDays === 1) return 'Yesterday'
  if (diffDays < 7) return `${diffDays} days ago`
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`
  if (diffDays < 365) return `${Math.floor(diffDays / 30)} months ago`
  return date.toLocaleDateString()
}

/**
 * Handle dropdown command
 */
function handleCommand(command: string): void {
  if (command === 'edit') {
    emit('edit', props.collection)
  } else if (command === 'delete') {
    confirmDelete()
  }
}

/**
 * Confirm and handle delete
 */
async function confirmDelete(): Promise<void> {
  try {
    await ElMessageBox.confirm(
      `Are you sure you want to delete collection "${props.collection.name}"? This will mark it as deleted but preserve the data.`,
      'Confirm Delete',
      {
        confirmButtonText: 'Delete',
        cancelButtonText: 'Cancel',
        type: 'warning',
        confirmButtonClass: 'el-button--danger'
      }
    )
    emit('delete', props.collection.code)
  } catch {
    // User cancelled
  }
}
</script>

<style scoped>
.collection-card {
  height: 100%;
  transition: all 0.3s ease;
}

.collection-card:hover {
  transform: translateY(-4px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.more-button {
  padding: 4px;
  color: #909399;
}

.more-button:hover {
  color: #409eff;
}

.collection-code {
  font-size: 32px;
  font-weight: 700;
  color: #409eff;
  text-align: center;
  margin-bottom: 12px;
  letter-spacing: 2px;
  font-family: 'Courier New', monospace;
}

.collection-name {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 8px 0;
  text-align: center;
}

.collection-description {
  font-size: 14px;
  color: #606266;
  margin: 0 0 16px 0;
  text-align: center;
  min-height: 40px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.collection-stats {
  display: flex;
  justify-content: center;
  gap: 24px;
  margin-bottom: 16px;
  padding: 12px 0;
  border-top: 1px solid #ebeef5;
  border-bottom: 1px solid #ebeef5;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #606266;
}

.stat-item .el-icon {
  font-size: 16px;
  color: #909399;
}

.upload-status {
  text-align: center;
  margin-bottom: 12px;
}

.created-info {
  font-size: 12px;
  color: #909399;
  text-align: center;
}
</style>
