import { Outlet } from 'react-router-dom'
import { Sidebar } from './Sidebar'

export function AppShell() {
  return (
    <div className="flex h-screen overflow-hidden" style={{ background: 'var(--color-background)' }}>
      <Sidebar />
      <main className="flex-1 flex flex-col min-w-0 overflow-hidden">
        <Outlet />
      </main>
    </div>
  )
}

// Code style format review — 2026-06-04T16:40:46

// Code style format review — 2026-06-08T15:43:53
