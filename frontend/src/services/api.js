/**
 * API Service
 * Handles all API calls to the backend
 */

import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Auth API
export const authAPI = {
  login: (email, password) => api.post('/users/login', null, { params: { email, password } }),
  register: (userData) => api.post('/users/register', userData),
  getCurrentUser: () => api.get('/users/me'),
}

// Interview API
export const interviewAPI = {
  create: (interviewData) => api.post('/interviews/', interviewData),
  getAll: (params) => api.get('/interviews/', { params }),
  getById: (id) => api.get(`/interviews/${id}`),
  start: (id) => api.post(`/interviews/${id}/start`),
  submitResponse: (id, response) => api.post(`/interviews/${id}/responses`, response),
  complete: (id) => api.post(`/interviews/${id}/complete`),
}

// Question API
export const questionAPI = {
  getAll: (params) => api.get('/questions/', { params }),
  generate: (params) => api.post('/questions/generate', null, { params }),
}

// Video API
export const videoAPI = {
  createRoom: (roomName, maxParticipants = 2) => 
    api.post('/video/rooms', null, { params: { room_name: roomName, max_participants: maxParticipants } }),
  getToken: (roomName, identity) => 
    api.post('/video/tokens', null, { params: { room_name: roomName, identity } }),
  getRoom: (roomSid) => api.get(`/video/rooms/${roomSid}`),
}

// Dashboard API
export const dashboardAPI = {
  getCandidates: (params) => api.get('/dashboard/candidates', { params }),
  getStatistics: () => api.get('/dashboard/statistics'),
  getCandidateDetail: (id) => api.get(`/dashboard/candidates/${id}`),
}

// Application API
export const applicationAPI = {
  create: (applicationData) => api.post('/applications/', applicationData),
  getAll: (params) => api.get('/applications/', { params }),
  getById: (id) => api.get(`/applications/${id}`),
  uploadCV: (id, file) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post(`/applications/${id}/upload-cv`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  accept: (id) => api.post(`/applications/${id}/accept`),
  reject: (id) => api.post(`/applications/${id}/reject`),
  update: (id, data) => api.patch(`/applications/${id}`, data),
}

export default api

