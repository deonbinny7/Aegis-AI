import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface AuthState {
  token: string | null
  user: { username: string; email: string } | null
  setToken: (token: string) => void
  setUser: (user: { username: string; email: string }) => void
  logout: () => void
  isAuthenticated: () => boolean
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      token: null,
      user: null,
      setToken: (token) => {
        localStorage.setItem('access_token', token)
        set({ token })
      },
      setUser: (user) => set({ user }),
      logout: () => {
        localStorage.removeItem('access_token')
        set({ token: null, user: null })
      },
      isAuthenticated: () => !!get().token,
    }),
    { name: 'auth-storage' }
  )
)

interface PlaygroundState {
  provider: string
  model: string
  temperature: number
  maxTokens: number
  promptName: string | null
  sessionId: string | null
  setProvider: (p: string) => void
  setModel: (m: string) => void
  setTemperature: (t: number) => void
  setMaxTokens: (n: number) => void
  setPromptName: (n: string | null) => void
  setSessionId: (id: string | null) => void
}

export const usePlaygroundStore = create<PlaygroundState>()((set) => ({
  provider: 'openai',
  model: 'gpt-4o',
  temperature: 0.7,
  maxTokens: 1024,
  promptName: null,
  sessionId: null,
  setProvider: (p) => set({ provider: p }),
  setModel: (m) => set({ model: m }),
  setTemperature: (t) => set({ temperature: t }),
  setMaxTokens: (n) => set({ maxTokens: n }),
  setPromptName: (n) => set({ promptName: n }),
  setSessionId: (id) => set({ sessionId: id }),
}))

interface UIState {
  sidebarCollapsed: boolean
  theme: 'dark' | 'light'
  toggleSidebar: () => void
  setTheme: (t: 'dark' | 'light') => void
}

export const useUIStore = create<UIState>()(
  persist(
    (set) => ({
      sidebarCollapsed: false,
      theme: 'dark',
      toggleSidebar: () =>
        set((s) => ({ sidebarCollapsed: !s.sidebarCollapsed })),
      setTheme: (t) => set({ theme: t }),
    }),
    { name: 'ui-storage' }
  )
)
