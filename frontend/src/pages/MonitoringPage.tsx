import { Topbar } from '@/components/layout/Topbar'
import { Card, Badge } from '@/components/ui'
import { motion } from 'framer-motion'
import { Cpu, HardDrive, Database, Activity, Server, Clock } from 'lucide-react'
import { useQuery } from '@tanstack/react-query'
import { healthApi } from '@/api/client'
import { ResponsiveContainer, AreaChart, Area, CartesianGrid, XAxis, YAxis, Tooltip } from 'recharts'

const MOCK_METRICS = Array.from({ length: 30 }, (_, i) => ({
  t: `${i * 2}m`,
  cpu: Math.floor(Math.random() * 40 + 15),
  memory: Math.floor(Math.random() * 30 + 40),
  latency: Math.floor(Math.random() * 200 + 200),
}))

const SystemMetricCard = ({ label, value, icon: Icon, color, status }: {
  label: string; value: string; icon: React.ElementType; color: string; status: 'healthy' | 'warning' | 'error'
}) => (
  <div className="glass rounded-xl p-5">
    <div className="flex items-center justify-between mb-3">
      <div className="w-8 h-8 rounded-lg flex items-center justify-center" style={{ background: `${color}20` }}>
        <Icon className="w-4 h-4" style={{ color }} />
      </div>
      <Badge variant={status === 'healthy' ? 'success' : status === 'warning' ? 'warning' : 'danger'}>
        {status}
      </Badge>
    </div>
    <p className="text-2xl font-bold text-slate-100">{value}</p>
    <p className="text-xs text-slate-500 mt-1">{label}</p>
  </div>
)

export function MonitoringPage() {
  const { data } = useQuery({
    queryKey: ['health'],
    queryFn: () => healthApi.check().then(r => r.data),
    refetchInterval: 15000,
  })

  return (
    <div className="flex flex-col flex-1 overflow-hidden">
      <Topbar title="System Monitoring" subtitle="Infrastructure health and performance metrics" />
      <div className="flex-1 overflow-y-auto p-6 space-y-6 scrollbar-thin">

        <div className="grid grid-cols-2 xl:grid-cols-3 gap-4">
          <SystemMetricCard label="CPU Usage" value="28%" icon={Cpu} color="#6366f1" status="healthy" />
          <SystemMetricCard label="Memory Usage" value="62%" icon={HardDrive} color="#06b6d4" status="healthy" />
          <SystemMetricCard label="PostgreSQL" value={data?.postgres ?? 'Connected'} icon={Database} color="#10b981" status="healthy" />
          <SystemMetricCard label="Redis" value={data?.redis ?? 'Connected'} icon={Server} color="#f59e0b" status="healthy" />
          <SystemMetricCard label="Celery Workers" value="4 Active" icon={Activity} color="#8b5cf6" status="healthy" />
          <SystemMetricCard label="Avg Response" value="342ms" icon={Clock} color="#06b6d4" status="healthy" />
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
          {[
            { key: 'cpu', label: 'CPU Usage (%)', color: '#6366f1', gradient: 'cpuGrad' },
            { key: 'memory', label: 'Memory Usage (%)', color: '#06b6d4', gradient: 'memGrad' },
          ].map(({ key, label, color, gradient }) => (
            <motion.div key={key} initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
              <Card title={label} subtitle="Last 60 minutes">
                <ResponsiveContainer width="100%" height={160}>
                  <AreaChart data={MOCK_METRICS}>
                    <defs>
                      <linearGradient id={gradient} x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor={color} stopOpacity={0.25} />
                        <stop offset="95%" stopColor={color} stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(99,102,241,0.08)" />
                    <XAxis dataKey="t" tick={{ fontSize: 9, fill: '#475569' }} />
                    <YAxis tick={{ fontSize: 9, fill: '#475569' }} domain={[0, 100]} />
                    <Tooltip contentStyle={{ background: '#0d1220', border: `1px solid ${color}40`, borderRadius: 8, fontSize: 11 }} />
                    <Area type="monotone" dataKey={key} stroke={color} fill={`url(#${gradient})`} strokeWidth={2} />
                  </AreaChart>
                </ResponsiveContainer>
              </Card>
            </motion.div>
          ))}
        </div>

        {/* Celery Queue */}
        <Card title="Celery Worker Queue" subtitle="Background task status">
          <div className="space-y-3">
            {[
              { queue: 'analytics', pending: 12, running: 2, status: 'healthy' },
              { queue: 'webhooks', pending: 0, running: 0, status: 'idle' },
              { queue: 'benchmarking', pending: 3, running: 1, status: 'healthy' },
            ].map(q => (
              <div key={q.queue} className="flex items-center gap-4 py-2 border-b border-slate-800 last:border-0">
                <span className="w-24 text-xs font-mono text-slate-400">{q.queue}</span>
                <div className="flex-1">
                  <div className="h-1.5 rounded-full bg-slate-800 overflow-hidden">
                    <div className="h-full gradient-primary rounded-full transition-all" style={{ width: `${Math.min((q.pending / 20) * 100, 100)}%` }} />
                  </div>
                </div>
                <span className="text-xs text-slate-500">{q.pending} pending / {q.running} running</span>
                <Badge variant={q.status === 'healthy' ? 'success' : 'info'}>{q.status}</Badge>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  )
}

// Code style format review — 2026-06-17T14:34:38
