import { Bell, LogOut, User } from 'lucide-react'
import { useAuthStore } from '@/store'
import { useNavigate } from 'react-router-dom'

interface TopbarProps {
  title: string
  subtitle?: string
}

export function Topbar({ title, subtitle }: TopbarProps) {
  const { user, logout } = useAuthStore()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <header className="h-16 flex items-center justify-between px-6 glass border-b border-[rgba(99,102,241,0.15)] flex-shrink-0">
      <div>
        <h1 className="font-semibold text-slate-100 text-base">{title}</h1>
        {subtitle && <p className="text-xs text-slate-500">{subtitle}</p>}
      </div>

      <div className="flex items-center gap-3">
        {/* Status pill */}
        <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full glass text-xs text-emerald-400 border border-emerald-500/20">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
          System Healthy
        </div>

        <button className="relative w-8 h-8 flex items-center justify-center rounded-full hover:bg-white/5 text-slate-400 hover:text-slate-200 transition-colors">
          <Bell className="w-4 h-4" />
        </button>

        <div className="flex items-center gap-2 pl-3 border-l border-slate-700">
          <div className="w-7 h-7 rounded-full gradient-primary flex items-center justify-center">
            <User className="w-3.5 h-3.5 text-white" />
          </div>
          <span className="text-xs text-slate-300 hidden sm:block">{user?.username ?? 'User'}</span>
          <button
            onClick={handleLogout}
            className="w-7 h-7 flex items-center justify-center rounded-full hover:bg-red-500/10 text-slate-500 hover:text-red-400 transition-colors"
            title="Logout"
          >
            <LogOut className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </header>
  )
}
