import axios from 'axios'

const API_BASE = '/api/v1'

export const apiClient = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
})

// Attach JWT to every request
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// Handle 401 globally - redirect to login
apiClient.interceptors.response.use(
  (res) => res,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Auth
export const authApi = {
  login: (username: string, password: string) =>
    apiClient.post('/auth/login', new URLSearchParams({ username, password }), {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    }),
  register: (data: { username: string; email: string; password: string }) =>
    apiClient.post('/auth/register', data),
  me: () => apiClient.get('/auth/me'),
}

// Analytics
export const analyticsApi = {
  getOverview: () => apiClient.get('/analytics'),
  getUsage: () => apiClient.get('/analytics/usage'),
  getCosts: () => apiClient.get('/analytics/costs'),
}

// Providers
export const providersApi = {
  list: () => apiClient.get('/providers'),
}

// Experiments
export const experimentsApi = {
  list: () => apiClient.get('/experiments'),
  create: (data: object) => apiClient.post('/experiments', data),
  getStats: (id: string) => apiClient.get(`/experiments/${id}/stats`),
}

// Webhooks
export const webhooksApi = {
  create: (data: { url: string; trigger_event: string }) =>
    apiClient.post('/webhooks', data),
}

// Health
export const healthApi = {
  check: () => apiClient.get('/health'),
}

// Chat stream — returns a ReadableStream for SSE
export function streamChat(
  body: object,
  onToken: (token: string) => void,
  onComplete: (metadata: object) => void,
  onError: (err: string) => void,
  signal?: AbortSignal
): void {
  const token = localStorage.getItem('access_token')
  fetch('/api/v1/chat/stream', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: JSON.stringify(body),
    signal,
  }).then(async (res) => {
    if (!res.ok) {
      onError(`HTTP ${res.status}`)
      return
    }
    const reader = res.body!.getReader()
    const decoder = new TextDecoder()
    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      const chunk = decoder.decode(value, { stream: true })
      chunk.split('\n\n').forEach((line) => {
        if (!line.startsWith('data:')) return
        try {
          const data = JSON.parse(line.replace('data:', '').trim())
          if (data.token) onToken(data.token)
          else if (data.status === 'completed') onComplete(data.metadata ?? {})
          else if (data.error) onError(data.error)
        } catch {}
      })
    }
  }).catch((err) => {
    if (err.name !== 'AbortError') onError(err.message)
  })
}

// Code style format review — 2026-05-29T17:39:16

// Code style format review — 2026-06-11T21:45:17
