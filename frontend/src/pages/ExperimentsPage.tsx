import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { motion } from 'framer-motion'
import { Topbar } from '@/components/layout/Topbar'
import { Card, Badge, Button, Input, Spinner } from '@/components/ui'
import { experimentsApi } from '@/api/client'
import { FlaskConical, Plus, TrendingUp, BarChart2 } from 'lucide-react'

export function ExperimentsPage() {
  const qc = useQueryClient()
  const [showCreate, setShowCreate] = useState(false)
  const [newName, setNewName] = useState('')

  const { data, isLoading } = useQuery({
    queryKey: ['experiments'],
    queryFn: () => experimentsApi.list().then(r => r.data),
  })

  const { data: statsData, mutate: fetchStats, isPending: statsPending } = useMutation({
    mutationFn: (id: string) => experimentsApi.getStats(id).then(r => r.data),
  })

  const createMutation = useMutation({
    mutationFn: () => experimentsApi.create({ name: newName, status: 'running' }),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['experiments'] })
      setShowCreate(false)
      setNewName('')
    },
  })

  const mockExperiments = [
    { id: 'exp_1', name: 'GPT-4o vs Claude Sonnet', status: 'running', metric: 'latency', split_pct: 50 },
    { id: 'exp_2', name: 'Cheapest vs Smart Routing', status: 'completed', metric: 'cost', split_pct: 40 },
    { id: 'exp_3', name: 'Prompt Template v2 Test', status: 'running', metric: 'user_rating', split_pct: 30 },
  ]

  const experiments = Array.isArray(data) ? data : mockExperiments

  return (
    <div className="flex flex-col flex-1 overflow-hidden">
      <Topbar title="Experiments" subtitle="A/B testing and statistical analysis" />
      <div className="flex-1 overflow-y-auto p-6 space-y-6 scrollbar-thin">

        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-sm font-medium text-slate-300">Active Experiments</h2>
            <p className="text-xs text-slate-500">Deterministic assignment via hash(user_id + experiment_id) % 100</p>
          </div>
          <Button icon={Plus} onClick={() => setShowCreate(true)} size="sm">New Experiment</Button>
        </div>

        {showCreate && (
          <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }}>
            <Card title="Create Experiment">
              <div className="flex gap-3">
                <Input
                  placeholder="Experiment name"
                  value={newName}
                  onChange={e => setNewName(e.target.value)}
                  className="flex-1"
                />
                <Button onClick={() => createMutation.mutate()} loading={createMutation.isPending} size="md">Create</Button>
                <Button variant="ghost" onClick={() => setShowCreate(false)} size="md">Cancel</Button>
              </div>
            </Card>
          </motion.div>
        )}

        {isLoading ? (
          <div className="flex items-center justify-center py-16"><Spinner /></div>
        ) : (
          <div className="space-y-3">
            {experiments.map((exp: {id: string; name: string; status: string; metric: string; split_pct: number}, i) => (
              <motion.div key={exp.id} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}>
                <Card>
                  <div className="flex items-start gap-4">
                    <div className="w-10 h-10 rounded-xl bg-indigo-500/10 flex items-center justify-center flex-shrink-0">
                      <FlaskConical className="w-5 h-5 text-indigo-400" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="font-medium text-slate-200 text-sm">{exp.name}</h3>
                        <Badge variant={exp.status === 'running' ? 'success' : 'info'}>
                          {exp.status}
                        </Badge>
                      </div>
                      <div className="flex gap-4 text-xs text-slate-500">
                        <span>Metric: <span className="text-slate-300">{exp.metric}</span></span>
                        <span>Traffic split: <span className="text-slate-300">{exp.split_pct}% / {100 - exp.split_pct}%</span></span>
                      </div>
                      {/* Traffic split visual */}
                      <div className="mt-3 h-1.5 rounded-full bg-slate-800 overflow-hidden flex">
                        <div className="h-full bg-indigo-500 rounded-l-full" style={{ width: `${exp.split_pct}%` }} />
                        <div className="h-full bg-cyan-500 rounded-r-full" style={{ width: `${100 - exp.split_pct}%` }} />
                      </div>
                    </div>
                    <Button
                      variant="secondary"
                      size="sm"
                      icon={statsPending ? undefined : BarChart2}
                      loading={statsPending}
                      onClick={() => fetchStats(exp.id)}
                    >
                      Stats
                    </Button>
                  </div>

                  {statsData && (statsData as {experiment_id: string}).experiment_id === exp.id && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      className="mt-4 pt-4 border-t border-slate-800 grid grid-cols-2 gap-4"
                    >
                      {(['latency_t_test', 'success_rate_chi_square'] as const).map(key => {
                        const result = (statsData as Record<string, {t_statistic?: number; chi2_statistic?: number; p_value: number; significant: boolean}>)[key]
                        if (!result) return null
                        return (
                          <div key={key} className="glass rounded-lg p-3">
                            <p className="text-xs font-medium text-slate-400 mb-2">{key.replace(/_/g, ' ')}</p>
                            <div className="space-y-1 text-xs font-mono">
                              {'t_statistic' in result && <p>t-stat: <span className="text-indigo-400">{result.t_statistic}</span></p>}
                              {'chi2_statistic' in result && <p>χ²: <span className="text-indigo-400">{result.chi2_statistic}</span></p>}
                              <p>p-value: <span className="text-cyan-400">{result.p_value}</span></p>
                              <Badge variant={result.significant ? 'success' : 'warning'}>
                                {result.significant ? '✓ Significant' : '— Not Significant'}
                              </Badge>
                            </div>
                          </div>
                        )
                      })}
                    </motion.div>
                  )}
                </Card>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

// Code style format review — 2026-06-06T17:33:26
