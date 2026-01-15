<template>
  <div class="dashboard">
    <!-- Header with user info and logout -->
    <div class="dashboard-header">
      <div class="header-info">
        <h2 class="dashboard-title">Admin Dashboard</h2>
        <p class="dashboard-subtitle">Photo Collection Management System</p>
      </div>
      <div class="header-actions">
        <span class="user-info">
          Welcome, <strong>{{ authStore.user?.username || 'Admin' }}</strong>
        </span>
        <el-button type="danger" plain @click="handleLogout">
          Logout
        </el-button>
      </div>
    </div>

    <!-- Content placeholder -->
    <el-card class="dashboard-card">
      <div class="card-content">
        <el-result
          icon="success"
          title="Admin Dashboard"
          sub-title="Manage your photo collections and upload codes"
        >
          <template #extra>
            <div class="dashboard-actions">
              <el-button type="primary" size="large" @click="$router.push('/collections')">
                Manage Collections
              </el-button>
            </div>
            <div class="phase-info">
              <el-tag type="success">Phase 3: Collection Management Complete</el-tag>
            </div>
          </template>
        </el-result>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

/**
 * Handle logout action
 */
async function handleLogout() {
  try {
    await ElMessageBox.confirm(
      'Are you sure you want to logout?',
      'Confirm Logout',
      {
        confirmButtonText: 'Logout',
        cancelButtonText: 'Cancel',
        type: 'warning',
      }
    )

    authStore.logout()
    ElMessage.success('Logged out successfully')
    router.push('/login')
  } catch {
    // User cancelled
  }
}
</script>

<style scoped>
.dashboard {
  max-width: 1400px;
  margin: 0 auto;
  padding: 24px;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.header-info {
  flex: 1;
}

.dashboard-title {
  font-size: 24px;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 4px 0;
}

.dashboard-subtitle {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-info {
  font-size: 14px;
  color: #374151;
  padding: 8px 12px;
  background: #f3f4f6;
  border-radius: 6px;
}

.dashboard-card {
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.card-content {
  padding: 40px 20px;
}

.dashboard-actions {
  margin-bottom: 16px;
}

.phase-info {
  display: flex;
  justify-content: center;
  gap: 8px;
}
</style>
