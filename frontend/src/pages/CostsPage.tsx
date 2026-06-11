import { Topbar } from '@/components/layout/Topbar'
import { Card, Badge, Button } from '@/components/ui'
import { motion } from 'framer-motion'
import { useQuery } from '@tanstack/react-query'
import { analyticsApi } from '@/api/client'
import { formatCurrency } from '@/lib/utils'
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, Cell, LineChart, Line } from 'recharts'
import { DollarSign, TrendingDown, CreditCard, Calendar } from 'lucide-react'

const COLORS = ['#6366f1', '#06b6d4', '#10b981', '#f59e0b']

const mockDailySpend = Array.from({ length: 30 }, (_, i) => ({
  day: `Jun ${i + 1}`,
  cost: parseFloat((Math.random() * 3 + 0.5).toFixed(3)),
}))

const mockUserCosts = [
  { user: 'alice@corp.com', cost: 8.42, requests: 1231 },
  { user: 'bob@corp.com', cost: 5.17, requests: 892 },
  { user: 'charlie@corp.com', cost: 3.94, requests: 654 },
  { user: 'diana@corp.com', cost: 2.88, requests: 421 },
  { user: 'system@corp.com', cost: 4.27, requests: 2100 },
]

const mockProviderCost = [
  { name: 'OpenAI', cost: 12.45 },
  { name: 'Anthropic', cost: 7.23 },
  { name: 'Gemini', cost: 3.11 },
  { name: 'Groq', cost: 1.89 },
]

const CustomTooltip = ({ active, payload, label }: { active?: boolean; payload?: { value: number }[]; label?: string }) => {
  if (!active || !payload?.length) return null
  return (
    <div className="glass-strong rounded-lg p-3 text-xs border border-indigo-500/20">
      <p className="text-slate-400 mb-1">{label}</p>
      <p className="text-emerald-400 font-mono">{formatCurrency(payload[0].value)}</p>
    </div>
  )
}

export function CostsPage() {
  const { data } = useQuery({
    queryKey: ['costs'],
    queryFn: () => analyticsApi.getCosts().then(r => r.data),
    refetchInterval: 60000,
  })

  const totalMonthly = data?.total_cost ?? mockDailySpend.reduce((a, b) => a + b.cost, 0)

  return (
    <div className="flex flex-col flex-1 overflow-hidden">
      <Topbar title="Cost Dashboard" subtitle="Spend analysis across providers and users" />
      <div className="flex-1 overflow-y-auto p-6 space-y-6 scrollbar-thin">

        {/* Summary Row */}
        <div className="grid grid-cols-2 xl:grid-cols-4 gap-4">
          {[
            { label: 'Today', value: formatCurrency(1.24), icon: DollarSign, delay: 0 },
            { label: 'This Month', value: formatCurrency(totalMonthly), icon: Calendar, delay: 0.05 },
            { label: 'Avg / Request', value: formatCurrency(0.00192), icon: CreditCard, delay: 0.1 },
            { label: 'MoM Change', value: '-8.4%', icon: TrendingDown, delay: 0.15 },
          ].map(s => (
            <motion.div key={s.label} initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: s.delay }} className="glass rounded-xl p-5">
              <div className="flex items-center gap-2 mb-2">
                <s.icon className="w-4 h-4 text-indigo-400" />
                <p className="text-xs text-slate-500 uppercase tracking-wider">{s.label}</p>
              </div>
              <p className="text-2xl font-bold text-slate-100">{s.value}</p>
            </motion.div>
          ))}
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
          <Card title="Daily Spend" subtitle="Last 30 days">
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={mockDailySpend}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(99,102,241,0.1)" />
                <XAxis dataKey="day" tick={{ fontSize: 8, fill: '#475569' }} interval={4} />
                <YAxis tick={{ fontSize: 9, fill: '#475569' }} tickFormatter={v => `$${v}`} />
                <Tooltip content={<CustomTooltip />} />
                <Bar dataKey="cost" fill="#6366f1" radius={[3, 3, 0, 0]} opacity={0.85} />
              </BarChart>
            </ResponsiveContainer>
          </Card>

          <Card title="Cost by Provider">
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={mockProviderCost} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(99,102,241,0.08)" horizontal={false} />
                <XAxis type="number" tick={{ fontSize: 9, fill: '#475569' }} tickFormatter={v => `$${v}`} />
                <YAxis type="category" dataKey="name" tick={{ fontSize: 10, fill: '#94a3b8' }} width={70} />
                <Tooltip formatter={(v: any) => [`$${Number(v).toFixed(2)}`, 'Cost']} contentStyle={{ background: '#0d1220', border: '1px solid rgba(99,102,241,0.2)', borderRadius: 8 }} />
                <Bar dataKey="cost" radius={[0, 4, 4, 0]}>
                  {mockProviderCost.map((_, i) => <Cell key={i} fill={COLORS[i]} />)}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </Card>
        </div>

        {/* User cost table */}
        <Card title="Top Spenders" subtitle="Cost and requests per user this month">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-slate-800">
                  <th className="text-left text-xs text-slate-500 pb-3 font-medium">User</th>
                  <th className="text-right text-xs text-slate-500 pb-3 font-medium">Requests</th>
                  <th className="text-right text-xs text-slate-500 pb-3 font-medium">Cost</th>
                  <th className="text-right text-xs text-slate-500 pb-3 font-medium">Avg/Req</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {mockUserCosts.map((u, i) => (
                  <motion.tr key={u.user} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.3 + i * 0.04 }}>
                    <td className="py-3 text-sm text-slate-300">{u.user}</td>
                    <td className="py-3 text-right text-sm font-mono text-slate-400">{u.requests.toLocaleString()}</td>
                    <td className="py-3 text-right text-sm font-mono text-emerald-400">{formatCurrency(u.cost)}</td>
                    <td className="py-3 text-right text-sm font-mono text-slate-500">{formatCurrency(u.cost / u.requests)}</td>
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      </div>
    </div>
  )
}

// Code style format review — 2026-05-25T19:04:14

// Code style format review — 2026-06-11T16:18:07
