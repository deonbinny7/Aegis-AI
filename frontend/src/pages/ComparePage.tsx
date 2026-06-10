import { Topbar } from '@/components/layout/Topbar'
import { Card, Badge, Button, Spinner } from '@/components/ui'
import { motion } from 'framer-motion'
import { useState } from 'react'
import { streamChat } from '@/api/client'
import { Send, Clock, DollarSign, Zap } from 'lucide-react'

const PROVIDERS_LIST = [
  { id: 'openai', name: 'OpenAI GPT-4o', model: 'gpt-4o', color: '#10a37f' },
  { id: 'anthropic', name: 'Claude Sonnet', model: 'claude-3-5-sonnet-20241022', color: '#cc785c' },
  { id: 'google', name: 'Gemini 1.5 Pro', model: 'gemini-1.5-pro', color: '#4285f4' },
  { id: 'groq', name: 'Llama3 (Groq)', model: 'llama3-70b-8192', color: '#f55036' },
]

interface CompareResult {
  providerId: string
  content: string
  duration: number
  tokens: number
  streaming: boolean
}

export function ComparePage() {
  const [prompt, setPrompt] = useState('')
  const [results, setResults] = useState<Record<string, CompareResult>>({})
  const [running, setRunning] = useState(false)
  const [selected, setSelected] = useState<string[]>(['openai', 'anthropic'])

  const toggleProvider = (id: string) => {
    setSelected(prev => prev.includes(id) ? prev.filter(p => p !== id) : [...prev, id])
  }

  const run = () => {
    if (!prompt.trim() || selected.length === 0) return
    setRunning(true)
    const initial: Record<string, CompareResult> = {}
    selected.forEach(id => {
      initial[id] = { providerId: id, content: '', duration: 0, tokens: 0, streaming: true }
    })
    setResults(initial)

    const startTimes: Record<string, number> = {}
    let completed = 0

    selected.forEach(providerId => {
      const provider = PROVIDERS_LIST.find(p => p.id === providerId)!
      startTimes[providerId] = Date.now()

      streamChat(
        { messages: [{ role: 'user', content: prompt }], model: provider.model, routing_strategy: 'explicit', temperature: 0.7 },
        (token) => {
          setResults(prev => ({
            ...prev,
            [providerId]: { ...prev[providerId], content: (prev[providerId]?.content ?? '') + token }
          }))
        },
        (meta) => {
          const dur = Date.now() - startTimes[providerId]
          setResults(prev => ({
            ...prev,
            [providerId]: {
              ...prev[providerId],
              streaming: false,
              duration: dur,
              tokens: (meta as {total_tokens?: number}).total_tokens ?? 0,
            }
          }))
          completed++
          if (completed === selected.length) setRunning(false)
        },
        () => {
          completed++
          setResults(prev => ({
            ...prev,
            [providerId]: { ...prev[providerId], streaming: false, content: (prev[providerId]?.content ?? '') + '\n\n[Error fetching response]' }
          }))
          if (completed === selected.length) setRunning(false)
        }
      )
    })
  }

  return (
    <div className="flex flex-col flex-1 overflow-hidden">
      <Topbar title="Model Comparison" subtitle="Send one prompt to multiple providers simultaneously" />
      <div className="flex-1 overflow-y-auto p-6 space-y-6 scrollbar-thin">

        {/* Prompt input */}
        <Card>
          <div className="space-y-4">
            <div>
              <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold mb-2">Select Providers</p>
              <div className="flex flex-wrap gap-2">
                {PROVIDERS_LIST.map(p => (
                  <button
                    key={p.id}
                    onClick={() => toggleProvider(p.id)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all border ${
                      selected.includes(p.id)
                        ? 'border-transparent text-white'
                        : 'border-slate-700 text-slate-500 hover:text-slate-300'
                    }`}
                    style={selected.includes(p.id) ? { background: `${p.color}30`, borderColor: `${p.color}60`, color: p.color } : {}}
                  >
                    {p.name}
                  </button>
                ))}
              </div>
            </div>
            <textarea
              value={prompt}
              onChange={e => setPrompt(e.target.value)}
              placeholder="Enter a prompt to compare across providers…"
              rows={3}
              className="w-full glass rounded-xl px-4 py-3 text-sm text-slate-200 placeholder:text-slate-600 border border-[rgba(99,102,241,0.15)] focus:outline-none focus:border-indigo-500/50 resize-none"
            />
            <div className="flex justify-end">
              <Button onClick={run} loading={running} icon={Send} disabled={!prompt.trim() || selected.length === 0}>
                Compare Providers
              </Button>
            </div>
          </div>
        </Card>

        {/* Results Grid */}
        {Object.keys(results).length > 0 && (
          <div className={`grid gap-4 ${selected.length === 2 ? 'grid-cols-2' : selected.length >= 3 ? 'grid-cols-2 xl:grid-cols-4' : 'grid-cols-1'}`}>
            {selected.map(id => {
              const provider = PROVIDERS_LIST.find(p => p.id === id)!
              const result = results[id]
              return (
                <motion.div key={id} initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }}>
                  <Card
                    title={provider.name}
                    action={
                      result?.streaming
                        ? <Badge variant="info">Streaming…</Badge>
                        : <Badge variant="success">Complete</Badge>
                    }
                  >
                    <div className="prose prose-invert prose-xs max-w-none text-sm min-h-[120px]">
                      {result?.content || <span className="text-slate-600">Waiting…</span>}
                      {result?.streaming && <span className="inline-block w-1.5 h-4 ml-1 bg-indigo-400 rounded-sm animate-pulse" />}
                    </div>
                    {!result?.streaming && result?.duration > 0 && (
                      <div className="mt-4 pt-3 border-t border-slate-800 flex gap-4 text-xs text-slate-500">
                        <span className="flex items-center gap-1"><Clock className="w-3 h-3" />{(result.duration / 1000).toFixed(2)}s</span>
                        <span className="flex items-center gap-1"><Zap className="w-3 h-3" />{result.tokens} tokens</span>
                      </div>
                    )}
                  </Card>
                </motion.div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}

// Code style format review — 2026-06-10T09:51:01
