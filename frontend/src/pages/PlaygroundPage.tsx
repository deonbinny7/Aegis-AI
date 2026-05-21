import { useState, useRef, useEffect, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import ReactMarkdown from 'react-markdown'
import { Send, Square, RefreshCcw, Copy, Check, Settings2, ChevronDown, ChevronUp } from 'lucide-react'
import { Topbar } from '@/components/layout/Topbar'
import { Button, Slider, Badge, Spinner } from '@/components/ui'
import { streamChat } from '@/api/client'
import { usePlaygroundStore } from '@/store'
import { cn } from '@/lib/utils'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  metadata?: Record<string, unknown>
  streaming?: boolean
}

const PROVIDERS = [
  { value: 'openai', label: 'OpenAI', models: ['gpt-4o', 'gpt-4o-mini', 'gpt-3.5-turbo'] },
  { value: 'anthropic', label: 'Anthropic', models: ['claude-3-5-sonnet-20241022', 'claude-3-haiku-20240307'] },
  { value: 'google', label: 'Gemini', models: ['gemini-1.5-pro', 'gemini-1.5-flash'] },
  { value: 'groq', label: 'Groq', models: ['llama3-70b-8192', 'mixtral-8x7b-32768'] },
]

function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false)
  const copy = () => {
    navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }
  return (
    <button onClick={copy} className="opacity-0 group-hover:opacity-100 transition-opacity p-1.5 rounded hover:bg-white/10 text-slate-500 hover:text-slate-300">
      {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
    </button>
  )
}

export function PlaygroundPage() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [streaming, setStreaming] = useState(false)
  const [showSettings, setShowSettings] = useState(true)
  const abortRef = useRef<AbortController | null>(null)
  const bottomRef = useRef<HTMLDivElement>(null)

  const {
    provider, model, temperature, maxTokens,
    setProvider, setModel, setTemperature, setMaxTokens, sessionId, setSessionId
  } = usePlaygroundStore()

  const selectedProvider = PROVIDERS.find(p => p.value === provider) ?? PROVIDERS[0]

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = useCallback(() => {
    if (!input.trim() || streaming) return

    const userMsg: Message = { id: crypto.randomUUID(), role: 'user', content: input }
    const assistantMsg: Message = { id: crypto.randomUUID(), role: 'assistant', content: '', streaming: true }

    setMessages(prev => [...prev, userMsg, assistantMsg])
    setInput('')
    setStreaming(true)

    const ctrl = new AbortController()
    abortRef.current = ctrl

    streamChat(
      {
        messages: [...messages, userMsg].map(m => ({ role: m.role, content: m.content })),
        model,
        routing_strategy: 'explicit',
        temperature,
        max_tokens: maxTokens,
        session_id: sessionId,
      },
      (token) => {
        setMessages(prev => prev.map(m =>
          m.id === assistantMsg.id ? { ...m, content: m.content + token } : m
        ))
      },
      (meta) => {
        if ((meta as { session_id?: string }).session_id) setSessionId((meta as { session_id?: string }).session_id!)
        setMessages(prev => prev.map(m =>
          m.id === assistantMsg.id ? { ...m, streaming: false, metadata: meta as Record<string, unknown> } : m
        ))
        setStreaming(false)
      },
      (err) => {
        setMessages(prev => prev.map(m =>
          m.id === assistantMsg.id ? { ...m, content: `Error: ${err}`, streaming: false } : m
        ))
        setStreaming(false)
      },
      ctrl.signal
    )
  }, [input, streaming, messages, model, temperature, maxTokens, sessionId, setSessionId])

  const stopStream = () => {
    abortRef.current?.abort()
    setStreaming(false)
    setMessages(prev => prev.map(m => m.streaming ? { ...m, streaming: false } : m))
  }

  return (
    <div className="flex flex-col flex-1 overflow-hidden">
      <Topbar title="AI Playground" subtitle="Interactive chat with live streaming" />
      <div className="flex flex-1 overflow-hidden">

        {/* Settings Panel */}
        <AnimatePresence>
          {showSettings && (
            <motion.aside
              initial={{ width: 0, opacity: 0 }}
              animate={{ width: 280, opacity: 1 }}
              exit={{ width: 0, opacity: 0 }}
              transition={{ duration: 0.2 }}
              className="flex-shrink-0 glass border-r border-[rgba(99,102,241,0.15)] overflow-hidden"
            >
              <div className="p-4 space-y-5 w-[280px]">
                <div>
                  <label className="text-xs text-slate-500 uppercase tracking-wider font-semibold">Provider</label>
                  <div className="mt-2 grid grid-cols-2 gap-1.5">
                    {PROVIDERS.map(p => (
                      <button
                        key={p.value}
                        onClick={() => { setProvider(p.value); setModel(p.models[0]) }}
                        className={cn(
                          'px-2 py-2 rounded-lg text-xs font-medium transition-all border',
                          provider === p.value
                            ? 'bg-indigo-500/20 border-indigo-500/40 text-indigo-300'
                            : 'border-transparent text-slate-500 hover:text-slate-300 hover:bg-white/5'
                        )}
                      >
                        {p.label}
                      </button>
                    ))}
                  </div>
                </div>

                <div>
                  <label className="text-xs text-slate-500 uppercase tracking-wider font-semibold">Model</label>
                  <select
                    value={model}
                    onChange={e => setModel(e.target.value)}
                    className="mt-2 w-full glass rounded-lg px-3 py-2 text-xs text-slate-200 border border-[rgba(99,102,241,0.15)] focus:outline-none focus:border-indigo-500/50 bg-transparent"
                  >
                    {selectedProvider.models.map(m => (
                      <option key={m} value={m} className="bg-slate-900">{m}</option>
                    ))}
                  </select>
                </div>

                <Slider label="Temperature" value={temperature} min={0} max={2} step={0.05} onChange={setTemperature} format={v => v.toFixed(2)} />
                <Slider label="Max Tokens" value={maxTokens} min={64} max={4096} step={64} onChange={setMaxTokens} />

                {sessionId && (
                  <div>
                    <label className="text-xs text-slate-500 uppercase tracking-wider font-semibold">Session</label>
                    <p className="mt-1 text-xs font-mono text-indigo-400 truncate">{sessionId}</p>
                  </div>
                )}

                <button
                  onClick={() => { setMessages([]); setSessionId(null) }}
                  className="w-full flex items-center justify-center gap-2 py-2 rounded-lg text-xs text-slate-500 hover:text-slate-300 hover:bg-white/5 transition-colors border border-slate-800"
                >
                  <RefreshCcw className="w-3.5 h-3.5" /> New Session
                </button>
              </div>
            </motion.aside>
          )}
        </AnimatePresence>

        {/* Chat Area */}
        <div className="flex flex-col flex-1 min-w-0">
          {/* Toggle settings button */}
          <div className="flex items-center gap-2 px-4 py-2 border-b border-[rgba(99,102,241,0.1)]">
            <button
              onClick={() => setShowSettings(!showSettings)}
              className="flex items-center gap-1.5 text-xs text-slate-500 hover:text-slate-300 transition-colors"
            >
              <Settings2 className="w-3.5 h-3.5" />
              {showSettings ? 'Hide Settings' : 'Show Settings'}
              {showSettings ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
            </button>
            <div className="flex-1" />
            <Badge variant="info">{model}</Badge>
            <Badge variant="default">{provider}</Badge>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-6 space-y-4 scrollbar-thin">
            {messages.length === 0 && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="flex flex-col items-center justify-center h-full text-center"
              >
                <div className="w-16 h-16 rounded-2xl gradient-primary flex items-center justify-center mb-4 glow-primary">
                  <Send className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-lg font-semibold text-slate-200 mb-2">Start a conversation</h3>
                <p className="text-slate-500 text-sm max-w-sm">
                  Ask anything. The platform will route your message through the AI Gateway with full token tracking, analytics, and memory.
                </p>
              </motion.div>
            )}

            <AnimatePresence initial={false}>
              {messages.map((msg) => (
                <motion.div
                  key={msg.id}
                  initial={{ opacity: 0, y: 12 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.2 }}
                  className={cn('flex gap-3 group', msg.role === 'user' ? 'flex-row-reverse' : '')}
                >
                  <div className={cn(
                    'w-7 h-7 rounded-full flex-shrink-0 flex items-center justify-center text-xs font-bold',
                    msg.role === 'user' ? 'gradient-primary text-white' : 'bg-indigo-500/15 text-indigo-400'
                  )}>
                    {msg.role === 'user' ? 'U' : 'AI'}
                  </div>
                  <div className={cn(
                    'max-w-[80%] rounded-xl px-4 py-3 text-sm relative',
                    msg.role === 'user'
                      ? 'glass text-slate-200 rounded-tr-sm'
                      : 'glass text-slate-200 rounded-tl-sm'
                  )}>
                    <div className="prose prose-invert prose-sm max-w-none">
                      <ReactMarkdown>{msg.content}</ReactMarkdown>
                    </div>
                    {msg.streaming && (
                      <span className="inline-block w-1.5 h-4 ml-1 bg-indigo-400 rounded-sm animate-pulse" />
                    )}
                    {!msg.streaming && msg.role === 'assistant' && msg.content && (
                      <div className="absolute top-2 right-2"><CopyButton text={msg.content} /></div>
                    )}
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
            <div ref={bottomRef} />
          </div>

          {/* Input */}
          <div className="p-4 border-t border-[rgba(99,102,241,0.1)]">
            <div className="flex gap-3 items-end">
              <textarea
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage() } }}
                placeholder="Type your message… (Enter to send, Shift+Enter for new line)"
                rows={3}
                className="flex-1 glass rounded-xl px-4 py-3 text-sm text-slate-200 placeholder:text-slate-600 border border-[rgba(99,102,241,0.15)] focus:outline-none focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/30 resize-none scrollbar-thin"
              />
              {streaming ? (
                <Button variant="danger" onClick={stopStream} icon={Square} size="lg" className="flex-shrink-0 h-[76px]">Stop</Button>
              ) : (
                <Button onClick={sendMessage} disabled={!input.trim()} icon={Send} size="lg" className="flex-shrink-0 h-[76px]">Send</Button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
