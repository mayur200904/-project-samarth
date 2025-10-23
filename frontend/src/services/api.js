import axios from 'axios'

// Hardcoded for reliability - change if backend runs on different port
const API_BASE_URL = 'http://localhost:8000/api/v1'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 60000, // 60 seconds for complex queries
})

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message)
    throw error
  }
)

/**
 * Ask a question and get an answer with citations
 */
export const askQuestion = async (message, conversationId = null) => {
  try {
    const response = await api.post('/chat', {
      message,
      conversation_id: conversationId,
    })
    return response.data
  } catch (error) {
    throw new Error(
      error.response?.data?.detail || 
      'Failed to process question. Please ensure the backend server is running.'
    )
  }
}

/**
 * Get list of available datasets
 */
export const getDatasets = async (category = null) => {
  try {
    const params = category ? { category } : {}
    const response = await api.get('/datasets', { params })
    return response.data
  } catch (error) {
    throw new Error(
      error.response?.data?.detail || 
      'Failed to fetch datasets'
    )
  }
}

/**
 * Get detailed information about a specific dataset
 */
export const getDataset = async (datasetId) => {
  try {
    const response = await api.get(`/datasets/${datasetId}`)
    return response.data
  } catch (error) {
    throw new Error(
      error.response?.data?.detail || 
      `Failed to fetch dataset: ${datasetId}`
    )
  }
}

/**
 * Query a dataset with filters
 */
export const queryDataset = async (datasetId, filters = null, limit = 100) => {
  try {
    const response = await api.post('/datasets/query', {
      dataset_id: datasetId,
      filters,
      limit,
    })
    return response.data
  } catch (error) {
    throw new Error(
      error.response?.data?.detail || 
      'Failed to query dataset'
    )
  }
}

/**
 * Refresh a dataset from the API
 */
export const refreshDataset = async (datasetId) => {
  try {
    const response = await api.post(`/datasets/${datasetId}/refresh`)
    return response.data
  } catch (error) {
    throw new Error(
      error.response?.data?.detail || 
      'Failed to refresh dataset'
    )
  }
}

/**
 * Check API health
 */
export const checkHealth = async () => {
  try {
    const response = await api.get('/health')
    return response.data
  } catch (error) {
    throw new Error('API health check failed')
  }
}

export default api
