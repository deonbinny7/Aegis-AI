import { Topbar } from '@/components/layout/Topbar'
import { Card, Badge, Button } from '@/components/ui'
import { motion } from 'framer-motion'
import { Shield, Search, Download } from 'lucide-react'

const MOCK_AUDIT = [
  { id: 'a1', user: 'alice@corp.com', provider: 'openai', model: 'gpt-4o', status: 'success', retry_count: 0, session: 'sess_abc123', timestamp: '2026-06-29T12:01:23Z' },
  { id: 'a2', user: 'bob@corp.com', provider: 'anthropic', model: 'claude-3-5-sonnet-20241022', status: 'success', retry_count: 1, session: 'sess_def456', timestamp: '2026-06-29T12:03:11Z' },
  { id: 'a3', user: 'system@corp.com', provider: 'groq', model: 'llama3-70b-8192', status: 'error', retry_count: 3, session: 'sess_ghi789', timestamp: '2026-06-29T12:05:44Z' },
  { id: 'a4', user: 'diana@corp.com', provider: 'google', model: 'gemini-1.5-pro', status: 'success', retry_count: 0, session: 'sess_jkl012', timestamp: '2026-06-29T12:08:02Z' },
]

export function AuditPage() {
  return (
    <div className="flex flex-col flex-1 overflow-hidden">
      <Topbar title="Audit Trail" subtitle="Immutable records of all platform activity" />
      <div className="flex-1 overflow-y-auto p-6 space-y-6 scrollbar-thin">

        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 glass rounded-lg px-3 py-2 border border-[rgba(99,102,241,0.15)] w-72">
            <Search className="w-3.5 h-3.5 text-slate-500" />
            <input placeholder="Search audit logs…" className="flex-1 bg-transparent text-xs text-slate-200 placeholder:text-slate-600 outline-none" />
          </div>
          <Button variant="secondary" size="sm" icon={Download}>Export CSV</Button>
        </div>

        <Card title="Audit Log" subtitle="All records are immutable after creation">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-slate-800">
                  {['Timestamp', 'User', 'Provider', 'Model', 'Status', 'Retries', 'Session'].map(h => (
                    <th key={h} className="text-left text-xs text-slate-500 pb-3 pr-4 font-medium whitespace-nowrap">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {MOCK_AUDIT.map((log, i) => (
                  <motion.tr key={log.id} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: i * 0.05 }}>
                    <td className="py-3 pr-4 text-xs font-mono text-slate-500 whitespace-nowrap">{new Date(log.timestamp).toLocaleTimeString()}</td>
                    <td className="py-3 pr-4 text-xs text-slate-300">{log.user}</td>
                    <td className="py-3 pr-4"><Badge variant="default">{log.provider}</Badge></td>
                    <td className="py-3 pr-4 text-xs font-mono text-slate-400">{log.model}</td>
                    <td className="py-3 pr-4"><Badge variant={log.status === 'success' ? 'success' : 'danger'}>{log.status}</Badge></td>
                    <td className="py-3 pr-4 text-xs text-center text-slate-400">{log.retry_count}</td>
                    <td className="py-3 text-xs font-mono text-slate-500 truncate max-w-[120px]">{log.session}</td>
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

// Code style format review — 2026-05-25T15:58:06

// Code style format review — 2026-06-08T10:13:44

// Code style format review — 2026-06-17T16:55:14
