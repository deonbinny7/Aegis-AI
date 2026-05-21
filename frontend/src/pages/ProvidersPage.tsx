import { useQuery } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import { Topbar } from '@/components/layout/Topbar'
import { Card, Badge } from '@/components/ui'
import { providersApi } from '@/api/client'
import { Server, Zap, Clock, TrendingUp, AlertCircle, CheckCircle } from 'lucide-react'
import { ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, Radar } from 'recharts'
import { formatNumber } from '@/lib/utils'

const MOCK_PROVIDERS = [
  { name: 'OpenAI', id: 'openai', status: 'operational', latency_ms: 342, availability: 99.9, success_rate: 98.7, cost_efficiency: 7.2, models: ['gpt-4o', 'gpt-4o-mini'], requests: 6234 },
  { name: 'Anthropic', id: 'anthropic', status: 'operational', latency_ms: 521, availability: 99.7, success_rate: 99.1, cost_efficiency: 6.5, models: ['claude-3-5-sonnet-20241022'], requests: 3891 },
  { name: 'Google Gemini', id: 'google', status: 'operational', latency_ms: 287, availability: 99.5, success_rate: 97.8, cost_efficiency: 9.1, models: ['gemini-1.5-pro', 'gemini-1.5-flash'], requests: 1842 },
  { name: 'Groq', id: 'groq', status: 'degraded', latency_ms: 89, availability: 97.2, success_rate: 96.4, cost_efficiency: 9.8, models: ['llama3-70b-8192'], requests: 880 },
]

const radarDataFor = (p: typeof MOCK_PROVIDERS[number]) => [
  { metric: 'Availability', value: p.availability },
  { metric: 'Success Rate', value: p.success_rate },
  { metric: 'Speed Score', value: 100 - (p.latency_ms / 10) },
  { metric: 'Cost Eff.', value: p.cost_efficiency * 10 },
]

export function ProvidersPage() {
  const { data } = useQuery({
    queryKey: ['providers'],
    queryFn: () => providersApi.list().then(r => r.data),
    refetchInterval: 30000,
  })

  const providers = Array.isArray(data) ? data : MOCK_PROVIDERS

  return (
    <div className="flex flex-col flex-1 overflow-hidden">
      <Topbar title="Provider Dashboard" subtitle="Real-time provider health, latency & benchmarks" />
      <div className="flex-1 overflow-y-auto p-6 space-y-6 scrollbar-thin">

        <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
          {MOCK_PROVIDERS.map((provider, i) => (
            <motion.div key={provider.id} initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.08 }}>
              <Card>
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-indigo-500/10 flex items-center justify-center">
                      <Server className="w-5 h-5 text-indigo-400" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-slate-200">{provider.name}</h3>
                      <p className="text-xs text-slate-500">{provider.models.length} model{provider.models.length > 1 ? 's' : ''} active</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    {provider.status === 'operational'
                      ? <><CheckCircle className="w-4 h-4 text-emerald-400" /><Badge variant="success">Operational</Badge></>
                      : <><AlertCircle className="w-4 h-4 text-amber-400" /><Badge variant="warning">Degraded</Badge></>
                    }
                  </div>
                </div>

                <div className="grid grid-cols-4 gap-3 mb-4">
                  {[
                    { label: 'Latency', value: `${provider.latency_ms}ms`, icon: Clock },
                    { label: 'Availability', value: `${provider.availability}%`, icon: TrendingUp },
                    { label: 'Success', value: `${provider.success_rate}%`, icon: CheckCircle },
                    { label: 'Requests', value: formatNumber(provider.requests), icon: Zap },
                  ].map(m => (
                    <div key={m.label} className="glass rounded-lg p-3 text-center">
                      <m.icon className="w-3.5 h-3.5 text-indigo-400 mx-auto mb-1" />
                      <p className="text-xs font-bold text-slate-200">{m.value}</p>
                      <p className="text-[10px] text-slate-600 mt-0.5">{m.label}</p>
                    </div>
                  ))}
                </div>

                <div className="flex items-center gap-4">
                  <div className="flex-1">
                    <ResponsiveContainer width="100%" height={120}>
                      <RadarChart data={radarDataFor(provider)}>
                        <PolarGrid stroke="rgba(99,102,241,0.2)" />
                        <PolarAngleAxis dataKey="metric" tick={{ fontSize: 9, fill: '#475569' }} />
                        <Radar dataKey="value" stroke="#6366f1" fill="#6366f1" fillOpacity={0.15} strokeWidth={1.5} />
                      </RadarChart>
                    </ResponsiveContainer>
                  </div>
                  <div className="flex-1 space-y-2">
                    <p className="text-xs text-slate-500 font-semibold uppercase tracking-wider">Models</p>
                    {provider.models.map(m => (
                      <div key={m} className="glass rounded-lg px-2 py-1.5">
                        <p className="text-xs font-mono text-slate-300 truncate">{m}</p>
                      </div>
                    ))}
                  </div>
                </div>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  )
}
