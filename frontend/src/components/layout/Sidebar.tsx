import { NavLink } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import {
  LayoutDashboard, MessageSquare, Zap, FileText, BarChart3,
  DollarSign, FlaskConical, Server, Settings, ChevronLeft,
  ChevronRight, Brain, Shield, GitCompare, Activity,
  KeyRound, Users
} from 'lucide-react'
import { useUIStore } from '@/store'
import { cn } from '@/lib/utils'

const navGroups = [
  {
    label: 'Platform',
    items: [
      { to: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
      { to: '/playground', icon: MessageSquare, label: 'AI Playground' },
      { to: '/compare', icon: GitCompare, label: 'Model Compare' },
      { to: '/history', icon: Brain, label: 'Conversations' },
    ],
  },
  {
    label: 'Prompts',
    items: [
      { to: '/prompts', icon: FileText, label: 'Prompt Library' },
    ],
  },
  {
    label: 'Observability',
    items: [
      { to: '/analytics', icon: BarChart3, label: 'Analytics' },
      { to: '/costs', icon: DollarSign, label: 'Cost Dashboard' },
      { to: '/experiments', icon: FlaskConical, label: 'Experiments' },
      { to: '/providers', icon: Server, label: 'Providers' },
      { to: '/monitoring', icon: Activity, label: 'Monitoring' },
    ],
  },
  {
    label: 'Admin',
    items: [
      { to: '/users', icon: Users, label: 'User Management' },
      { to: '/api-keys', icon: KeyRound, label: 'API Keys' },
      { to: '/audit', icon: Shield, label: 'Audit Trail' },
      { to: '/settings', icon: Settings, label: 'Settings' },
    ],
  },
]

export function Sidebar() {
  const { sidebarCollapsed, toggleSidebar } = useUIStore()

  return (
    <motion.aside
      initial={false}
      animate={{ width: sidebarCollapsed ? 68 : 240 }}
      transition={{ duration: 0.2, ease: 'easeInOut' }}
      className="relative flex flex-col glass-strong border-r border-[rgba(99,102,241,0.15)] z-20 overflow-hidden"
      style={{ minHeight: '100vh' }}
    >
      {/* Logo */}
      <div className="flex items-center gap-3 h-16 px-4 border-b border-[rgba(99,102,241,0.15)] flex-shrink-0">
        <div className="w-8 h-8 rounded-lg gradient-primary flex items-center justify-center flex-shrink-0">
          <Zap className="w-4 h-4 text-white" />
        </div>
        <AnimatePresence>
          {!sidebarCollapsed && (
            <motion.div
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -10 }}
              transition={{ duration: 0.15 }}
            >
              <span className="font-semibold text-base gradient-text whitespace-nowrap">
                PrivGuard AI
              </span>
              <p className="text-[10px] text-slate-500 whitespace-nowrap">Enterprise Platform</p>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Nav */}
      <nav className="flex-1 overflow-y-auto overflow-x-hidden py-4 scrollbar-thin">
        {navGroups.map((group) => (
          <div key={group.label} className="mb-6">
            <AnimatePresence>
              {!sidebarCollapsed && (
                <motion.p
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="px-4 mb-1 text-[10px] uppercase tracking-widest text-slate-600 font-semibold"
                >
                  {group.label}
                </motion.p>
              )}
            </AnimatePresence>
            {group.items.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  cn(
                    'flex items-center gap-3 mx-2 mb-0.5 px-3 py-2 rounded-lg text-sm transition-all duration-150',
                    isActive
                      ? 'bg-indigo-500/15 text-indigo-400 border border-indigo-500/20'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'
                  )
                }
                title={sidebarCollapsed ? item.label : undefined}
              >
                <item.icon className="w-4 h-4 flex-shrink-0" />
                <AnimatePresence>
                  {!sidebarCollapsed && (
                    <motion.span
                      initial={{ opacity: 0, x: -8 }}
                      animate={{ opacity: 1, x: 0 }}
                      exit={{ opacity: 0, x: -8 }}
                      transition={{ duration: 0.15 }}
                      className="whitespace-nowrap"
                    >
                      {item.label}
                    </motion.span>
                  )}
                </AnimatePresence>
              </NavLink>
            ))}
          </div>
        ))}
      </nav>

      {/* Collapse toggle */}
      <button
        onClick={toggleSidebar}
        className="absolute top-4 -right-3 w-6 h-6 rounded-full glass border border-indigo-500/30 flex items-center justify-center hover:border-indigo-400/60 transition-colors z-30"
      >
        {sidebarCollapsed
          ? <ChevronRight className="w-3 h-3 text-indigo-400" />
          : <ChevronLeft className="w-3 h-3 text-indigo-400" />
        }
      </button>
    </motion.aside>
  )
}

// Code style format review — 2026-06-16T10:17:35
