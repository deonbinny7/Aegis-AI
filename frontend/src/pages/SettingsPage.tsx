import { Topbar } from '@/components/layout/Topbar'
import { Card, Badge, Button, Input, Slider } from '@/components/ui'
import { useUIStore } from '@/store'
import { motion } from 'framer-motion'
import { Sun, Moon, Palette, Key, Bell, User } from 'lucide-react'

export function SettingsPage() {
  const { theme, setTheme } = useUIStore()

  return (
    <div className="flex flex-col flex-1 overflow-hidden">
      <Topbar title="Settings" subtitle="Platform preferences and configuration" />
      <div className="flex-1 overflow-y-auto p-6 space-y-6 max-w-3xl scrollbar-thin">

        <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0 }}>
          <Card title="Appearance" subtitle="Customize the interface theme">
            <div className="flex gap-3">
              {(['dark', 'light'] as const).map(t => (
                <button
                  key={t}
                  onClick={() => setTheme(t)}
                  className={`flex items-center gap-2.5 px-4 py-3 rounded-xl border transition-all ${
                    theme === t
                      ? 'border-indigo-500/40 bg-indigo-500/15 text-indigo-300'
                      : 'border-slate-700 text-slate-500 hover:text-slate-300 hover:border-slate-600'
                  }`}
                >
                  {t === 'dark' ? <Moon className="w-4 h-4" /> : <Sun className="w-4 h-4" />}
                  <span className="text-sm font-medium capitalize">{t} Mode</span>
                  {theme === t && <Badge variant="info">Active</Badge>}
                </button>
              ))}
            </div>
          </Card>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.05 }}>
          <Card title="Profile" subtitle="Your account information">
            <div className="space-y-4">
              <Input id="display-name" label="Display Name" placeholder="Your name" />
              <Input id="email-settings" type="email" label="Email" placeholder="your@email.com" />
              <Button size="sm">Update Profile</Button>
            </div>
          </Card>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
          <Card title="API Keys" subtitle="Manage external API credentials">
            <div className="space-y-3">
              {['OpenAI', 'Anthropic', 'Google AI', 'Groq'].map(provider => (
                <div key={provider} className="flex items-center gap-3">
                  <span className="w-28 text-sm text-slate-400">{provider}</span>
                  <input
                    type="password"
                    placeholder="sk-••••••••••••••••"
                    className="flex-1 glass rounded-lg px-3 py-2 text-sm text-slate-200 border border-[rgba(99,102,241,0.15)] focus:outline-none focus:border-indigo-500/50 font-mono"
                  />
                  <Button size="sm" variant="secondary" icon={Key}>Save</Button>
                </div>
              ))}
            </div>
          </Card>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.15 }}>
          <Card title="Defaults" subtitle="Default model and provider preferences">
            <div className="space-y-4">
              <div>
                <label className="text-xs text-slate-500 font-medium">Default Provider</label>
                <select className="mt-1.5 w-full glass rounded-lg px-3 py-2 text-sm text-slate-200 border border-[rgba(99,102,241,0.15)] focus:outline-none bg-transparent">
                  <option className="bg-slate-900">OpenAI</option>
                  <option className="bg-slate-900">Anthropic</option>
                  <option className="bg-slate-900">Gemini</option>
                  <option className="bg-slate-900">Groq</option>
                </select>
              </div>
              <Button size="sm">Save Defaults</Button>
            </div>
          </Card>
        </motion.div>
      </div>
    </div>
  )
}
