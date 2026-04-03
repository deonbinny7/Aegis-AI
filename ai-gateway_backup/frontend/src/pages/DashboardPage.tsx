import { useQuery } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import {
  Activity, DollarSign, Zap, Users, Server,
  FlaskConical, TrendingUp, Clock, RefreshCcw
} from 'lucide-react'
import { Topbar } from '@/components/layout/Topbar'
import { StatCard, Card, Badge, Spinner } from '@/components/ui'
import { analyticsApi, providersApi } from '@/api/client'
import { formatCurrency, formatNumber } from '@/lib/utils'
import {
  ResponsiveContainer, LineChart, Line, AreaChart, Area,
  XAxis, YAxis, Tooltip, CartesianGrid
} from 'recharts'

const mockTimeSeries = Array.from({ length: 12 }, (_, i) => ({
  hour: `${i * 2}:00`,
  requests: Math.floor(Math.random() * 200) + 50,
  tokens: Math.floor(Math.random() * 50000) + 10000,
  cost: parseFloat((Math.random() * 2).toFixed(4)),
}))

const CustomTooltip = ({ active, payload, label }: { active?: boolean; payload?: {value: number; dataKey: string; color: string}[]; label?: string }) => {
  if (!active || !payload?.length) return null
  return (
    <div className="glass-strong rounded-lg p-3 text-xs border border-indigo-500/20">
      <p className="text-slate-400 mb-2">{label}</p>
      {payload.map((p) => (
        <p key={p.dataKey} style={{ color: p.color }} className="font-mono">{p.dataKey}: {p.value.toLocaleString()}</p>
      ))}
    </div>
  )
}

export function DashboardPage() {
  const { data: analytics, isLoading: analyticsLoading } = useQuery({
    queryKey: ['analytics'],
    queryFn: () => analyticsApi.getOverview().then(r => r.data),
    refetchInterval: 30000,
  })

  const { data: providers } = useQuery({
    queryKey: ['providers'],
    queryFn: () => providersApi.list().then(r => r.data),
    refetchInterval: 60000,
  })

  return (
    <div className="flex flex-col flex-1 overflow-hidden">
      <Topbar title="Dashboard" subtitle="Enterprise AI Platform overview" />
      <div className="flex-1 overflow-y-auto p-6 space-y-6 scrollbar-thin">

        {/* Stat Grid */}
        <div className="grid grid-cols-2 xl:grid-cols-4 gap-4">
          <StatCard label="Total Requests" value={formatNumber(analytics?.total_requests ?? 12847)} icon={Activity} trend="12% this week" trendUp delay={0} />
          <StatCard label="Active Sessions" value={analytics?.active_sessions ?? 284} icon={Users} trend="Live" trendUp delay={0.05} />
          <StatCard label="Avg Latency" value={`${analytics?.avg_latency_ms ?? 342}ms`} icon={Clock} trend="8% faster" trendUp delay={0.1} />
          <StatCard label="Total Cost (30d)" value={formatCurrency(analytics?.total_cost_usd ?? 24.68)} icon={DollarSign} trend="vs last month" trendUp={false} delay={0.15} />
        </div>

        {/* Charts row */}
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
            <Card title="Request Throughput" subtitle="Requests per hour (last 24h)">
              {analyticsLoading ? (
                <div className="h-48 flex items-center justify-center"><Spinner /></div>
              ) : (
                <ResponsiveContainer width="100%" height={180}>
                  <AreaChart data={mockTimeSeries}>
                    <defs>
                      <linearGradient id="reqGrad" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
                        <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(99,102,241,0.1)" />
                    <XAxis dataKey="hour" tick={{ fontSize: 10, fill: '#475569' }} />
                    <YAxis tick={{ fontSize: 10, fill: '#475569' }} />
                    <Tooltip content={<CustomTooltip />} />
                    <Area type="monotone" dataKey="requests" stroke="#6366f1" fill="url(#reqGrad)" strokeWidth={2} />
                  </AreaChart>
                </ResponsiveContainer>
              )}
            </Card>
          </motion.div>

          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.25 }}>
            <Card title="Cost Trends" subtitle="USD spend per hour">
              <ResponsiveContainer width="100%" height={180}>
                <LineChart data={mockTimeSeries}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(6,182,212,0.1)" />
                  <XAxis dataKey="hour" tick={{ fontSize: 10, fill: '#475569' }} />
                  <YAxis tick={{ fontSize: 10, fill: '#475569' }} />
                  <Tooltip content={<CustomTooltip />} />
                  <Line type="monotone" dataKey="cost" stroke="#06b6d4" strokeWidth={2} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </Card>
          </motion.div>
        </div>

        {/* Provider & system status */}
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-4">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }} className="xl:col-span-2">
            <Card title="Provider Status" subtitle="Real-time health & utilization">
              {(['OpenAI', 'Anthropic', 'Gemini', 'Groq'] as const).map((p, i) => (
                <div key={p} className="flex items-center gap-4 py-3 border-b border-slate-800 last:border-0">
                  <div className="w-8 h-8 rounded-lg bg-indigo-500/10 flex items-center justify-center">
                    <Server className="w-4 h-4 text-indigo-400" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-slate-200">{p}</p>
                    <div className="mt-1 h-1.5 rounded-full bg-slate-800 overflow-hidden">
                      <div
                        className="h-full rounded-full gradient-primary"
                        style={{ width: `${[78, 45, 91, 62][i]}%` }}
                      />
                    </div>
                  </div>
                  <Badge variant="success">Online</Badge>
                  <span className="text-xs text-slate-500 font-mono">{[78, 45, 91, 62][i]}%</span>
                </div>
              ))}
            </Card>
          </motion.div>

          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.35 }}>
            <Card title="Quick Stats">
              {[
                { label: 'Token Usage (24h)', value: '2.4M', icon: Zap },
                { label: 'Avg Retry Rate', value: '2.1%', icon: RefreshCcw },
                { label: 'Active Experiments', value: '3', icon: FlaskConical },
                { label: 'Provider Uptime', value: '99.8%', icon: TrendingUp },
              ].map((item) => (
                <div key={item.label} className="flex items-center gap-3 py-2.5 border-b border-slate-800 last:border-0">
                  <div className="w-7 h-7 rounded-md bg-indigo-500/10 flex items-center justify-center">
                    <item.icon className="w-3.5 h-3.5 text-indigo-400" />
                  </div>
                  <span className="flex-1 text-sm text-slate-400">{item.label}</span>
                  <span className="text-sm font-medium text-slate-200">{item.value}</span>
                </div>
              ))}
            </Card>
          </motion.div>
        </div>
      </div>
    </div>
  )
}
