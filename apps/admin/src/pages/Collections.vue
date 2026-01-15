<template>
  <div class="collections-page">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-info">
        <h1 class="page-title">Collections</h1>
        <p class="page-subtitle">Manage photo collection codes and settings</p>
      </div>
      <div class="header-actions">
        <el-button type="primary" :icon="Plus" @click="showCreateDialog = true">
          Create Collection
        </el-button>
      </div>
    </div>

    <!-- Stats Cards -->
    <el-row :gutter="16" class="stats-row">
      <el-col :xs="24" :sm="8">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon active">
              <el-icon><CircleCheck /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.total || 0 }}</div>
              <div class="stat-label">Total Collections</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="8">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon success">
              <el-icon><Open /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.active || 0 }}</div>
              <div class="stat-label">Active</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="8">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon warning">
              <el-icon><Collection /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ totalPhotos }}</div>
              <div class="stat-label">Total Photos</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Filter Tabs -->
    <el-card class="filter-card">
      <el-radio-group v-model="activeTab" @change="handleTabChange">
        <el-radio-button value="all">
          All ({{ collectionsStore.collections.length }})
        </el-radio-button>
        <el-radio-button value="active">
          Active ({{ collectionsStore.activeCollections.length }})
        </el-radio-button>
        <el-radio-button value="archived">
          Archived ({{ collectionsStore.archivedCollections.length }})
        </el-radio-button>
        <el-radio-button value="closed">
          Closed ({{ collectionsStore.closedCollections.length }})
        </el-radio-button>
      </el-radio-group>

      <div class="filter-actions">
        <el-button
          :icon="Refresh"
          :loading="collectionsStore.loading"
          @click="loadCollections"
        >
          Refresh
        </el-button>
      </div>
    </el-card>

    <!-- Loading State -->
    <div v-if="collectionsStore.loading && collectionsStore.collections.length === 0" class="loading-container">
      <el-skeleton :rows="3" animated />
    </div>

    <!-- Empty State -->
    <el-card v-else-if="filteredCollections.length === 0" class="empty-state">
      <el-empty
        :image-size="120"
        :description="emptyStateMessage"
      >
        <template #extra>
          <el-button type="primary" @click="showCreateDialog = true">
            Create Your First Collection
          </el-button>
        </template>
      </el-empty>
    </el-card>

    <!-- Collections Grid -->
    <el-row v-else :gutter="16" class="collections-grid">
      <el-col
        v-for="collection in filteredCollections"
        :key="collection.id"
        :xs="24"
        :sm="12"
        :md="8"
        :lg="6"
      >
        <CollectionCard
          :collection="collection"
          @edit="handleEdit"
          @delete="handleDelete"
        />
      </el-col>
    </el-row>

    <!-- Create/Edit Dialog -->
    <CollectionForm
      v-model="showCreateDialog"
      :collection="editingCollection"
      @success="handleFormSuccess"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Plus,
  Refresh,
  CircleCheck,
  Open,
  Collection
} from '@element-plus/icons-vue'
import { useCollectionsStore, type Collection, type CollectionStats } from '../stores/collections'
import CollectionCard from '../components/CollectionCard.vue'
import CollectionForm from '../components/CollectionForm.vue'

const collectionsStore = useCollectionsStore()

// State
const showCreateDialog = ref(false)
const editingCollection = ref<Collection | undefined>(undefined)
const activeTab = ref<'all' | 'active' | 'archived' | 'closed'>('all')
const stats = ref<CollectionStats>({ total: 0 })

// Computed
const filteredCollections = computed(() => {
  if (activeTab.value === 'all') {
    return collectionsStore.collections
  }
  return collectionsStore.collections.filter(c => c.status === activeTab.value)
})

const emptyStateMessage = computed(() => {
  if (activeTab.value === 'all') {
    return 'No collections yet'
  }
  const messages = {
    active: 'No active collections',
    archived: 'No archived collections',
    closed: 'No closed collections'
  }
  return messages[activeTab.value]
})

const totalPhotos = computed(() => {
  return collectionsStore.collections.reduce(
    (sum, c) => sum + c.statistics.total_photos,
    0
  )
})

// Load collections on mount
onMounted(async () => {
  await loadCollections()
  await loadStats()
})

/**
 * Load collections from API
 */
async function loadCollections(): Promise<void> {
  try {
    await collectionsStore.fetchCollections()
  } catch (error) {
    ElMessage.error('Failed to load collections')
  }
}

/**
 * Load collection statistics
 */
async function loadStats(): Promise<void> {
  try {
    stats.value = await collectionsStore.fetchStats()
  } catch (error) {
    console.error('Failed to load stats:', error)
  }
}

/**
 * Handle tab change
 */
function handleTabChange(value: string): void {
  activeTab.value = value as 'all' | 'active' | 'archived' | 'closed'
}

/**
 * Handle edit button click
 */
function handleEdit(collection: Collection): void {
  editingCollection.value = collection
  showCreateDialog.value = true
}

/**
 * Handle delete button click
 */
async function handleDelete(code: string): Promise<void> {
  try {
    await collectionsStore.deleteCollection(code)
    ElMessage.success('Collection deleted successfully')
    await loadCollections()
    await loadStats()
  } catch (error) {
    if (typeof error === 'string') {
      ElMessage.error(error)
    } else {
      ElMessage.error('Failed to delete collection')
    }
  }
}

/**
 * Handle form success (create/update)
 */
async function handleFormSuccess(collection: Collection): Promise<void> {
  await loadCollections()
  await loadStats()
  editingCollection.value = undefined
}
</script>

<style scoped>
.collections-page {
  max-width: 1400px;
  margin: 0 auto;
  padding: 24px;
}

/* Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 16px;
}

.header-info {
  flex: 1;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  color: #303133;
  margin: 0 0 8px 0;
}

.page-subtitle {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 12px;
}

/* Stats */
.stats-row {
  margin-bottom: 24px;
}

.stat-card {
  border-radius: 8px;
  transition: all 0.3s;
}

.stat-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.stat-icon.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.stat-icon.success {
  background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
  color: white;
}

.stat-icon.warning {
  background: linear-gradient(135deg, #fccb90 0%, #d57eeb 100%);
  color: white;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: #303133;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 13px;
  color: #909399;
}

/* Filter Card */
.filter-card {
  margin-bottom: 24px;
  border-radius: 8px;
}

.filter-card :deep(.el-card__body) {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}

.filter-actions {
  display: flex;
  gap: 12px;
}

/* Collections Grid */
.collections-grid {
  margin-bottom: 24px;
}

.collections-grid > .el-col {
  margin-bottom: 16px;
}

/* Loading */
.loading-container {
  padding: 40px;
}

/* Empty State */
.empty-state {
  border-radius: 8px;
}

.empty-state :deep(.el-card__body) {
  padding: 60px 20px;
}

/* Responsive */
@media (max-width: 768px) {
  .collections-page {
    padding: 16px;
  }

  .page-header {
    flex-direction: column;
  }

  .header-actions {
    width: 100%;
  }

  .header-actions .el-button {
    flex: 1;
  }

  .filter-card :deep(.el-card__body) {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-actions {
    width: 100%;
  }

  .filter-actions .el-button {
    flex: 1;
  }
}
</style>
