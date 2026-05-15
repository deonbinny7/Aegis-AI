import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Suspense, lazy } from 'react'
import { ProtectedRoute } from '@/components/layout/ProtectedRoute'
import { AppShell } from '@/components/layout/AppShell'
import { Spinner } from '@/components/ui'
import { LoginPage } from '@/pages/LoginPage'
import { RegisterPage } from '@/pages/RegisterPage'

// Lazy-loaded pages for code splitting
const DashboardPage = lazy(() => import('@/pages/DashboardPage').then(m => ({ default: m.DashboardPage })))
const PlaygroundPage = lazy(() => import('@/pages/PlaygroundPage').then(m => ({ default: m.PlaygroundPage })))
const AnalyticsPage = lazy(() => import('@/pages/AnalyticsPage').then(m => ({ default: m.AnalyticsPage })))
const CostsPage = lazy(() => import('@/pages/CostsPage').then(m => ({ default: m.CostsPage })))
const ExperimentsPage = lazy(() => import('@/pages/ExperimentsPage').then(m => ({ default: m.ExperimentsPage })))
const ProvidersPage = lazy(() => import('@/pages/ProvidersPage').then(m => ({ default: m.ProvidersPage })))
const MonitoringPage = lazy(() => import('@/pages/MonitoringPage').then(m => ({ default: m.MonitoringPage })))
const PromptsPage = lazy(() => import('@/pages/PromptsPage').then(m => ({ default: m.PromptsPage })))
const ComparePage = lazy(() => import('@/pages/ComparePage').then(m => ({ default: m.ComparePage })))
const AuditPage = lazy(() => import('@/pages/AuditPage').then(m => ({ default: m.AuditPage })))
const SettingsPage = lazy(() => import('@/pages/SettingsPage').then(m => ({ default: m.SettingsPage })))

const qc = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 30,
      retry: 1,
    },
  },
})

function PageLoader() {
  return (
    <div className="flex-1 flex items-center justify-center">
      <Spinner className="w-8 h-8" />
    </div>
  )
}

export default function App() {
  return (
    <QueryClientProvider client={qc}>
      <BrowserRouter>
        <Routes>
          {/* Public routes */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          {/* Protected routes inside AppShell */}
          <Route element={<ProtectedRoute />}>
            <Route element={<AppShell />}>
              <Route index element={<Navigate to="/dashboard" replace />} />
              <Route path="/dashboard" element={<Suspense fallback={<PageLoader />}><DashboardPage /></Suspense>} />
              <Route path="/playground" element={<Suspense fallback={<PageLoader />}><PlaygroundPage /></Suspense>} />
              <Route path="/compare" element={<Suspense fallback={<PageLoader />}><ComparePage /></Suspense>} />
              <Route path="/prompts" element={<Suspense fallback={<PageLoader />}><PromptsPage /></Suspense>} />
              <Route path="/analytics" element={<Suspense fallback={<PageLoader />}><AnalyticsPage /></Suspense>} />
              <Route path="/costs" element={<Suspense fallback={<PageLoader />}><CostsPage /></Suspense>} />
              <Route path="/experiments" element={<Suspense fallback={<PageLoader />}><ExperimentsPage /></Suspense>} />
              <Route path="/providers" element={<Suspense fallback={<PageLoader />}><ProvidersPage /></Suspense>} />
              <Route path="/monitoring" element={<Suspense fallback={<PageLoader />}><MonitoringPage /></Suspense>} />
              <Route path="/audit" element={<Suspense fallback={<PageLoader />}><AuditPage /></Suspense>} />
              <Route path="/settings" element={<Suspense fallback={<PageLoader />}><SettingsPage /></Suspense>} />
              {/* Stubs for remaining nav items */}
              <Route path="/history" element={<Suspense fallback={<PageLoader />}><DashboardPage /></Suspense>} />
              <Route path="/users" element={<Suspense fallback={<PageLoader />}><AuditPage /></Suspense>} />
              <Route path="/api-keys" element={<Suspense fallback={<PageLoader />}><SettingsPage /></Suspense>} />
            </Route>
          </Route>

          {/* 404 fallback */}
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}
