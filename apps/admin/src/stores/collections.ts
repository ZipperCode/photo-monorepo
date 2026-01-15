import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

/**
 * Collection data interface
 */
export interface Collection {
  id: string
  code: string
  name: string
  description?: string
  status: 'active' | 'archived' | 'closed'
  settings: {
    allow_upload: boolean
    max_file_size: number
    allowed_extensions: string[]
  }
  statistics: {
    total_photos: number
    total_size_bytes: number
    last_upload_at: string | null
  }
  created_at: string
  created_by: string
}

/**
 * Collection creation data
 */
export interface CollectionCreate {
  name: string
  description?: string
  status?: 'active' | 'archived' | 'closed'
  settings?: {
    allow_upload?: boolean
    max_file_size?: number
    allowed_extensions?: string[]
  }
}

/**
 * Collection update data (all fields optional)
 */
export interface CollectionUpdate {
  name?: string
  description?: string
  status?: 'active' | 'archived' | 'closed'
  settings?: {
    allow_upload?: boolean
    max_file_size?: number
    allowed_extensions?: string[]
  }
}

/**
 * Collection statistics
 */
export interface CollectionStats {
  total: number
  active?: number
  archived?: number
  closed?: number
}

/**
 * Pinia store for collection management
 */
export const useCollectionsStore = defineStore('collections', () => {
  // State
  const collections = ref<Collection[]>([])
  const currentCollection = ref<Collection | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const pagination = ref({
    page: 1,
    limit: 20,
    total: 0
  })

  // Computed
  const activeCollections = computed(() =>
    collections.value.filter(c => c.status === 'active')
  )

  const archivedCollections = computed(() =>
    collections.value.filter(c => c.status === 'archived')
  )

  const closedCollections = computed(() =>
    collections.value.filter(c => c.status === 'closed')
  )

  /**
   * Get authorization headers with JWT token
   */
  function getAuthHeaders(): HeadersInit {
    const token = localStorage.getItem('auth_token')
    return {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` })
    }
  }

  /**
   * Handle API errors
   */
  function handleError(err: unknown): void {
    if (err instanceof Error) {
      error.value = err.message
    } else if (typeof err === 'string') {
      error.value = err
    } else {
      error.value = 'An unknown error occurred'
    }
    console.error('Collection API error:', err)
  }

  /**
   * Fetch paginated list of collections
   */
  async function fetchCollections(page: number = 1, limit: number = 20, status?: string): Promise<void> {
    loading.value = true
    error.value = null

    try {
      const params = new URLSearchParams({
        page: page.toString(),
        limit: limit.toString()
      })

      if (status) {
        params.append('status', status)
      }

      const response = await fetch(`${API_BASE}/api/v1/admin/collections?${params}`, {
        headers: getAuthHeaders()
      })

      if (!response.ok) {
        const data = await response.json()
        throw new Error(data.detail || 'Failed to fetch collections')
      }

      const data: Collection[] = await response.json()
      collections.value = data
      pagination.value = { page, limit, total: data.length }
    } catch (err) {
      handleError(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Fetch a single collection by code
   */
  async function fetchCollection(code: string): Promise<Collection | null> {
    loading.value = true
    error.value = null

    try {
      const response = await fetch(`${API_BASE}/api/v1/admin/collections/${code}`, {
        headers: getAuthHeaders()
      })

      if (!response.ok) {
        if (response.status === 404) {
          return null
        }
        const data = await response.json()
        throw new Error(data.detail || 'Failed to fetch collection')
      }

      const data: Collection = await response.json()
      currentCollection.value = data
      return data
    } catch (err) {
      handleError(err)
      return null
    } finally {
      loading.value = false
    }
  }

  /**
   * Create a new collection
   */
  async function createCollection(data: CollectionCreate): Promise<Collection> {
    loading.value = true
    error.value = null

    try {
      const response = await fetch(`${API_BASE}/api/v1/admin/collections`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(data)
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to create collection')
      }

      const newCollection: Collection = await response.json()

      // Add to beginning of list
      collections.value.unshift(newCollection)

      return newCollection
    } catch (err) {
      handleError(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Update an existing collection
   */
  async function updateCollection(code: string, data: CollectionUpdate): Promise<Collection | null> {
    loading.value = true
    error.value = null

    try {
      const response = await fetch(`${API_BASE}/api/v1/admin/collections/${code}`, {
        method: 'PATCH',
        headers: getAuthHeaders(),
        body: JSON.stringify(data)
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to update collection')
      }

      const updated: Collection = await response.json()

      // Update in list
      const index = collections.value.findIndex(c => c.code === code)
      if (index !== -1) {
        collections.value[index] = updated
      }

      // Update current if it's the same
      if (currentCollection.value?.code === code) {
        currentCollection.value = updated
      }

      return updated
    } catch (err) {
      handleError(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Delete a collection (soft delete)
   */
  async function deleteCollection(code: string): Promise<boolean> {
    loading.value = true
    error.value = null

    try {
      const response = await fetch(`${API_BASE}/api/v1/admin/collections/${code}`, {
        method: 'DELETE',
        headers: getAuthHeaders()
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to delete collection')
      }

      // Remove from list
      collections.value = collections.value.filter(c => c.code !== code)

      // Clear current if it's the same
      if (currentCollection.value?.code === code) {
        currentCollection.value = null
      }

      return true
    } catch (err) {
      handleError(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Fetch collection statistics
   */
  async function fetchStats(status?: string): Promise<CollectionStats> {
    loading.value = true
    error.value = null

    try {
      const params = status ? `?status=${status}` : ''
      const response = await fetch(`${API_BASE}/api/v1/admin/collections/stats/count${params}`, {
        headers: getAuthHeaders()
      })

      if (!response.ok) {
        const data = await response.json()
        throw new Error(data.detail || 'Failed to fetch statistics')
      }

      return await response.json()
    } catch (err) {
      handleError(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Clear current collection
   */
  function clearCurrentCollection(): void {
    currentCollection.value = null
  }

  /**
   * Clear error state
   */
  function clearError(): void {
    error.value = null
  }

  return {
    // State
    collections,
    currentCollection,
    loading,
    error,
    pagination,

    // Computed
    activeCollections,
    archivedCollections,
    closedCollections,

    // Actions
    fetchCollections,
    fetchCollection,
    createCollection,
    updateCollection,
    deleteCollection,
    fetchStats,
    clearCurrentCollection,
    clearError
  }
})
