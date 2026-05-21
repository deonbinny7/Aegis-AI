import { Topbar } from '@/components/layout/Topbar'
import { Card, Badge, Button } from '@/components/ui'
import { motion } from 'framer-motion'
import Editor from '@monaco-editor/react'
import { useState } from 'react'
import { FileText, Plus, Search, Tag, Clock, Copy, Trash2 } from 'lucide-react'

const MOCK_PROMPTS = [
  {
    id: 'prompt_1',
    name: 'Customer Support',
    description: 'Friendly, professional support assistant',
    template: 'You are a helpful customer support agent for {{company}}.\n\nYour tone should be: {{tone}}\n\nConversation history:\n{{history}}\n\nUser: {{message}}',
    variables: ['company', 'tone', 'history', 'message'],
    version: 3,
    tags: ['support', 'customer-facing'],
    status: 'active',
  },
  {
    id: 'prompt_2',
    name: 'Code Reviewer',
    description: 'Technical code review and feedback',
    template: 'You are an expert {{language}} developer.\n\nReview the following code and provide:\n1. Security issues\n2. Performance improvements\n3. Best practices\n\n```{{language}}\n{{code}}\n```',
    variables: ['language', 'code'],
    version: 1,
    tags: ['code', 'engineering'],
    status: 'active',
  },
  {
    id: 'prompt_3',
    name: 'Document Summarizer',
    description: 'Concise document summarization',
    template: 'Summarize the following document in {{max_words}} words or less.\n\nFocus on: {{focus_areas}}\n\nDocument:\n{{document}}',
    variables: ['max_words', 'focus_areas', 'document'],
    version: 2,
    tags: ['summarization'],
    status: 'draft',
  },
]

export function PromptsPage() {
  const [selected, setSelected] = useState(MOCK_PROMPTS[0])
  const [search, setSearch] = useState('')
  const [editorValue, setEditorValue] = useState(selected.template)

  const filtered = MOCK_PROMPTS.filter(p =>
    p.name.toLowerCase().includes(search.toLowerCase()) ||
    p.tags.some(t => t.includes(search.toLowerCase()))
  )

  const handleSelect = (p: typeof MOCK_PROMPTS[0]) => {
    setSelected(p)
    setEditorValue(p.template)
  }

  return (
    <div className="flex flex-col flex-1 overflow-hidden">
      <Topbar title="Prompt Library" subtitle="Manage and version prompt templates" />
      <div className="flex flex-1 overflow-hidden">

        {/* Sidebar */}
        <div className="w-72 flex-shrink-0 glass border-r border-[rgba(99,102,241,0.15)] flex flex-col overflow-hidden">
          <div className="p-3 border-b border-slate-800 flex gap-2">
            <div className="flex-1 flex items-center gap-2 glass rounded-lg px-3 py-2 border border-[rgba(99,102,241,0.15)]">
              <Search className="w-3.5 h-3.5 text-slate-500" />
              <input
                value={search}
                onChange={e => setSearch(e.target.value)}
                placeholder="Search prompts..."
                className="flex-1 bg-transparent text-xs text-slate-200 placeholder:text-slate-600 outline-none"
              />
            </div>
            <Button size="sm" icon={Plus} variant="secondary">New</Button>
          </div>

          <div className="flex-1 overflow-y-auto p-2 scrollbar-thin space-y-1">
            {filtered.map(prompt => (
              <button
                key={prompt.id}
                onClick={() => handleSelect(prompt)}
                className={`w-full text-left p-3 rounded-lg transition-all ${selected.id === prompt.id ? 'bg-indigo-500/15 border border-indigo-500/20' : 'hover:bg-white/5'}`}
              >
                <div className="flex items-center gap-2 mb-1">
                  <FileText className="w-3.5 h-3.5 text-indigo-400 flex-shrink-0" />
                  <span className="text-sm font-medium text-slate-200 truncate">{prompt.name}</span>
                </div>
                <p className="text-xs text-slate-500 mb-2 truncate">{prompt.description}</p>
                <div className="flex items-center gap-2 flex-wrap">
                  {prompt.tags.map(t => (
                    <span key={t} className="text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-400">{t}</span>
                  ))}
                  <span className="ml-auto flex items-center gap-1 text-[10px] text-slate-600"><Clock className="w-3 h-3" />v{prompt.version}</span>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Editor Panel */}
        <div className="flex-1 flex flex-col overflow-hidden">
          <div className="flex items-center justify-between px-5 py-3 border-b border-slate-800">
            <div>
              <h2 className="text-sm font-semibold text-slate-200">{selected.name}</h2>
              <div className="flex items-center gap-2 mt-0.5">
                <Badge variant={selected.status === 'active' ? 'success' : 'warning'}>{selected.status}</Badge>
                <span className="text-xs text-slate-500">Version {selected.version}</span>
              </div>
            </div>
            <div className="flex gap-2">
              <Button size="sm" variant="secondary" icon={Copy}>Clone</Button>
              <Button size="sm" icon={FileText}>Save Version</Button>
            </div>
          </div>

          <div className="flex flex-1 overflow-hidden">
            <div className="flex-1 overflow-hidden">
              <Editor
                height="100%"
                defaultLanguage="handlebars"
                value={editorValue}
                onChange={v => setEditorValue(v ?? '')}
                theme="vs-dark"
                options={{
                  fontSize: 13,
                  fontFamily: "'JetBrains Mono', monospace",
                  minimap: { enabled: false },
                  lineNumbers: 'on',
                  scrollBeyondLastLine: false,
                  wordWrap: 'on',
                  padding: { top: 16, bottom: 16 },
                  renderLineHighlight: 'gutter',
                  cursorBlinking: 'smooth',
                }}
              />
            </div>

            {/* Variable panel */}
            <div className="w-56 flex-shrink-0 border-l border-slate-800 p-4 overflow-y-auto scrollbar-thin">
              <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3 flex items-center gap-1.5">
                <Tag className="w-3.5 h-3.5" /> Variables
              </p>
              <div className="space-y-2">
                {selected.variables.map(v => (
                  <div key={v} className="glass rounded-lg p-2.5">
                    <p className="text-xs font-mono text-indigo-300">{'{{' + v + '}}'}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
