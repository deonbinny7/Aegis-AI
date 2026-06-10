import { useQuery } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import { Topbar } from '@/components/layout/Topbar'
import { Card, Badge, Spinner } from '@/components/ui'
import { analyticsApi } from '@/api/client'
import { formatCurrency, formatNumber } from '@/lib/utils'
import {
  ResponsiveContainer, BarChart, Bar, AreaChart, Area,
  PieChart, Pie, Cell, XAxis, YAxis, Tooltip, CartesianGrid, Legend
} from 'recharts'

const COLORS = ['#6366f1', '#06b6d4', '#10b981', '#f59e0b']

const mockHourly = Array.from({ length: 24 }, (_, i) => ({
  hour: `${i}:00`,
  requests: Math.floor(Math.random() * 300) + 20,
  errors: Math.floor(Math.random() * 10),
  tokens: Math.floor(Math.random() * 80000) + 5000,
}))

const mockCostByProvider = [
  { name: 'OpenAI', cost: 12.45 },
  { name: 'Anthropic', cost: 7.23 },
  { name: 'Gemini', cost: 3.11 },
  { name: 'Groq', cost: 1.89 },
]

const mockRouting = [
  { name: 'Explicit', value: 45 },
  { name: 'Cheapest', value: 25 },
  { name: 'Fastest', value: 20 },
  { name: 'Smart', value: 10 },
]

const CustomTooltip = ({ active, payload, label }: {active?: boolean; payload?: {value: number; dataKey: string; color: string}[]; label?: string}) => {
  if (!active || !payload?.length) return null
  return (
    <div className="glass-strong rounded-lg p-3 text-xs border border-indigo-500/20">
      <p className="text-slate-400 mb-1">{label}</p>
      {payload.map(p => (
        <p key={p.dataKey} style={{ color: p.color }}>{p.dataKey}: {p.value.toLocaleString()}</p>
      ))}
    </div>
  )
}

export function AnalyticsPage() {
  const { data, isLoading } = useQuery({
    queryKey: ['analytics'],
    queryFn: () => analyticsApi.getOverview().then(r => r.data),
    refetchInterval: 60000,
  })

  return (
    <div className="flex flex-col flex-1 overflow-hidden">
      <Topbar title="Analytics" subtitle="Platform-wide metrics and trends" />
      <div className="flex-1 overflow-y-auto p-6 space-y-6 scrollbar-thin">

        {/* Metrics Row */}
        <div className="grid grid-cols-2 xl:grid-cols-4 gap-4">
          {[
            { label: 'Total Requests', value: formatNumber(data?.total_requests ?? 12847), change: '+12%' },
            { label: 'Success Rate', value: `${data?.success_rate ?? 98.4}%`, change: '+0.2%' },
            { label: 'Retry Rate', value: `${data?.retry_rate ?? 2.1}%`, change: '-0.4%' },
            { label: 'Avg Tokens/Req', value: formatNumber(data?.avg_tokens ?? 1243), change: '+5%' },
          ].map((m, i) => (
            <motion.div key={m.label} initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}
              className="glass rounded-xl p-5">
              <p className="text-xs text-slate-500 uppercase tracking-wider">{m.label}</p>
              <p className="text-2xl font-bold text-slate-100 mt-2">{m.value}</p>
              <Badge variant="success" className="mt-2">{m.change}</Badge>
            </motion.div>
          ))}
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
          <Card title="Request Volume" subtitle="24-hour breakdown">
            {isLoading ? <div className="h-48 flex items-center justify-center"><Spinner /></div> : (
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={mockHourly}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(99,102,241,0.1)" />
                  <XAxis dataKey="hour" tick={{ fontSize: 9, fill: '#475569' }} />
                  <YAxis tick={{ fontSize: 9, fill: '#475569' }} />
                  <Tooltip content={<CustomTooltip />} />
                  <Bar dataKey="requests" fill="#6366f1" radius={[3, 3, 0, 0]} opacity={0.85} />
                  <Bar dataKey="errors" fill="#ef4444" radius={[3, 3, 0, 0]} opacity={0.85} />
                </BarChart>
              </ResponsiveContainer>
            )}
          </Card>

          <Card title="Token Consumption" subtitle="Tokens per hour">
            <ResponsiveContainer width="100%" height={200}>
              <AreaChart data={mockHourly}>
                <defs>
                  <linearGradient id="tokGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#06b6d4" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(6,182,212,0.1)" />
                <XAxis dataKey="hour" tick={{ fontSize: 9, fill: '#475569' }} />
                <YAxis tick={{ fontSize: 9, fill: '#475569' }} />
                <Tooltip content={<CustomTooltip />} />
                <Area type="monotone" dataKey="tokens" stroke="#06b6d4" fill="url(#tokGrad)" strokeWidth={2} />
              </AreaChart>
            </ResponsiveContainer>
          </Card>

          <Card title="Cost by Provider" subtitle="USD spend breakdown">
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={mockCostByProvider} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(99,102,241,0.1)" horizontal={false} />
                <XAxis type="number" tick={{ fontSize: 9, fill: '#475569' }} tickFormatter={v => `$${v}`} />
                <YAxis type="category" dataKey="name" tick={{ fontSize: 10, fill: '#94a3b8' }} width={70} />
                <Tooltip formatter={(v: any) => [`$${Number(v).toFixed(2)}`, 'Cost']} contentStyle={{ background: '#0d1220', border: '1px solid rgba(99,102,241,0.2)', borderRadius: 8 }} />
                <Bar dataKey="cost" radius={[0, 4, 4, 0]}>
                  {mockCostByProvider.map((_, i) => (
                    <Cell key={i} fill={COLORS[i]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </Card>

          <Card title="Routing Distribution" subtitle="Strategy breakdown">
            <div className="flex items-center gap-6">
              <ResponsiveContainer width="50%" height={200}>
                <PieChart>
                  <Pie data={mockRouting} cx="50%" cy="50%" innerRadius={55} outerRadius={80} dataKey="value" strokeWidth={0}>
                    {mockRouting.map((_, i) => (
                      <Cell key={i} fill={COLORS[i]} opacity={0.85} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
              <div className="space-y-2">
                {mockRouting.map((r, i) => (
                  <div key={r.name} className="flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full" style={{ background: COLORS[i] }} />
                    <span className="text-xs text-slate-400">{r.name}</span>
                    <span className="text-xs font-medium text-slate-200 ml-auto">{r.value}%</span>
                  </div>
                ))}
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  )
}

// Code style format review — 2026-06-10T09:12:04
