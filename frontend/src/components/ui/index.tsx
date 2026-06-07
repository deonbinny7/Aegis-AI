import { motion } from 'framer-motion'
import { cn } from '@/lib/utils'

interface StatCardProps {
  label: string
  value: string | number
  icon: React.ElementType
  trend?: string
  trendUp?: boolean
  className?: string
  delay?: number
}

export function StatCard({ label, value, icon: Icon, trend, trendUp, className, delay = 0 }: StatCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay }}
      className={cn(
        'glass rounded-xl p-5 group hover:border-indigo-500/30 transition-all duration-300',
        className
      )}
    >
      <div className="flex items-start justify-between mb-3">
        <p className="text-xs font-medium text-slate-500 uppercase tracking-wider">{label}</p>
        <div className="w-8 h-8 rounded-lg bg-indigo-500/10 flex items-center justify-center group-hover:bg-indigo-500/20 transition-colors">
          <Icon className="w-4 h-4 text-indigo-400" />
        </div>
      </div>
      <p className="text-2xl font-bold text-slate-100 mb-1">{value}</p>
      {trend && (
        <p className={cn('text-xs font-medium', trendUp ? 'text-emerald-400' : 'text-red-400')}>
          {trendUp ? '↑' : '↓'} {trend}
        </p>
      )}
    </motion.div>
  )
}

// Generic glassmorphism card
interface CardProps {
  children: React.ReactNode
  className?: string
  title?: string
  subtitle?: string
  action?: React.ReactNode
}

export function Card({ children, className, title, subtitle, action }: CardProps) {
  return (
    <div className={cn('glass rounded-xl', className)}>
      {(title || action) && (
        <div className="flex items-center justify-between px-5 pt-5 pb-4 border-b border-[rgba(99,102,241,0.1)]">
          <div>
            {title && <h3 className="font-semibold text-slate-100 text-sm">{title}</h3>}
            {subtitle && <p className="text-xs text-slate-500 mt-0.5">{subtitle}</p>}
          </div>
          {action}
        </div>
      )}
      <div className="p-5">{children}</div>
    </div>
  )
}

// Badge
interface BadgeProps {
  children: React.ReactNode
  variant?: 'default' | 'success' | 'warning' | 'danger' | 'info'
  className?: string
}

const badgeVariants = {
  default: 'bg-indigo-500/15 text-indigo-400 border-indigo-500/20',
  success: 'bg-emerald-500/15 text-emerald-400 border-emerald-500/20',
  warning: 'bg-amber-500/15 text-amber-400 border-amber-500/20',
  danger: 'bg-red-500/15 text-red-400 border-red-500/20',
  info: 'bg-cyan-500/15 text-cyan-400 border-cyan-500/20',
}

export function Badge({ children, variant = 'default', className }: BadgeProps) {
  return (
    <span className={cn('inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium border', badgeVariants[variant], className)}>
      {children}
    </span>
  )
}

// Spinner
export function Spinner({ className }: { className?: string }) {
  return (
    <div className={cn('w-5 h-5 rounded-full border-2 border-indigo-500/30 border-t-indigo-500 animate-spin', className)} />
  )
}

// Button
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  loading?: boolean
  icon?: React.ElementType
}

const buttonVariants = {
  primary: 'gradient-primary text-white hover:opacity-90 shadow-lg shadow-indigo-500/20',
  secondary: 'glass border border-indigo-500/20 text-slate-300 hover:text-white hover:border-indigo-500/40',
  ghost: 'text-slate-400 hover:text-slate-200 hover:bg-white/5',
  danger: 'bg-red-500/15 border border-red-500/20 text-red-400 hover:bg-red-500/25',
}

const buttonSizes = {
  sm: 'px-3 py-1.5 text-xs gap-1.5',
  md: 'px-4 py-2 text-sm gap-2',
  lg: 'px-6 py-2.5 text-sm gap-2',
}

export function Button({ variant = 'primary', size = 'md', loading, icon: Icon, children, className, disabled, ...props }: ButtonProps) {
  return (
    <button
      className={cn(
        'flex items-center justify-center rounded-lg font-medium transition-all duration-150 disabled:opacity-50 disabled:cursor-not-allowed',
        buttonVariants[variant],
        buttonSizes[size],
        className
      )}
      disabled={disabled || loading}
      {...props}
    >
      {loading ? <Spinner className="w-4 h-4" /> : Icon && <Icon className="w-4 h-4" />}
      {children}
    </button>
  )
}

// Input
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
}

export function Input({ label, error, className, id, ...props }: InputProps) {
  return (
    <div className="flex flex-col gap-1.5">
      {label && <label htmlFor={id} className="text-xs font-medium text-slate-400">{label}</label>}
      <input
        id={id}
        className={cn(
          'glass rounded-lg px-3 py-2 text-sm text-slate-200 placeholder:text-slate-600',
          'border border-[rgba(99,102,241,0.15)] focus:outline-none focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/30',
          'transition-all duration-150',
          error && 'border-red-500/50',
          className
        )}
        {...props}
      />
      {error && <p className="text-xs text-red-400">{error}</p>}
    </div>
  )
}

// Slider
interface SliderProps {
  label: string
  value: number
  min: number
  max: number
  step: number
  onChange: (v: number) => void
  format?: (v: number) => string
}

export function Slider({ label, value, min, max, step, onChange, format }: SliderProps) {
  return (
    <div className="flex flex-col gap-2">
      <div className="flex items-center justify-between">
        <label className="text-xs text-slate-500">{label}</label>
        <span className="text-xs font-mono text-indigo-400">{format ? format(value) : value}</span>
      </div>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        className="w-full h-1 rounded-full appearance-none cursor-pointer bg-slate-700 [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-3 [&::-webkit-slider-thumb]:h-3 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-indigo-500"
      />
    </div>
  )
}

// Code style format review — 2026-06-07T21:35:59
