import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Zap, Eye, EyeOff, LogIn } from 'lucide-react'
import { useAuthStore } from '@/store'
import { authApi } from '@/api/client'
import { Button, Input } from '@/components/ui'

const schema = z.object({
  username: z.string().min(1, 'Username is required'),
  password: z.string().min(6, 'Password must be at least 6 characters'),
})

type FormData = z.infer<typeof schema>

export function LoginPage() {
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()
  const { setToken, setUser } = useAuthStore()

  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<FormData>({
    resolver: zodResolver(schema),
  })

  const onSubmit = async (data: FormData) => {
    try {
      setError('')
      const res = await authApi.login(data.username, data.password)
      setToken(res.data.access_token)
      const meRes = await authApi.me()
      setUser(meRes.data)
      navigate('/dashboard')
    } catch (err: unknown) {
      const axiosErr = err as { response?: { data?: { detail?: string } } }
      setError(axiosErr?.response?.data?.detail ?? 'Login failed. Please check your credentials.')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4" style={{ background: 'var(--color-background)' }}>
      {/* Background glow */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/3 w-96 h-96 bg-indigo-500/5 rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 right-1/3 w-64 h-64 bg-cyan-500/5 rounded-full blur-3xl" />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-md"
      >
        {/* Logo */}
        <div className="flex flex-col items-center mb-8">
          <div className="w-14 h-14 rounded-2xl gradient-primary flex items-center justify-center mb-4 glow-primary">
            <Zap className="w-7 h-7 text-white" />
          </div>
          <h1 className="text-2xl font-bold gradient-text">PrivGuard AI</h1>
          <p className="text-slate-500 text-sm mt-1">Enterprise AI Platform</p>
        </div>

        {/* Card */}
        <div className="glass-strong rounded-2xl p-8">
          <h2 className="text-lg font-semibold text-slate-100 mb-1">Sign in to your account</h2>
          <p className="text-sm text-slate-500 mb-6">Welcome back. Enter your credentials to continue.</p>

          {error && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              className="mb-4 px-4 py-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm"
            >
              {error}
            </motion.div>
          )}

          <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4">
            <Input
              id="username"
              label="Username"
              placeholder="Enter your username"
              error={errors.username?.message}
              {...register('username')}
            />
            <div className="flex flex-col gap-1.5">
              <label className="text-xs font-medium text-slate-400">Password</label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  placeholder="Enter your password"
                  className="w-full glass rounded-lg px-3 py-2 pr-10 text-sm text-slate-200 placeholder:text-slate-600 border border-[rgba(99,102,241,0.15)] focus:outline-none focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/30 transition-all"
                  {...register('password')}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-300"
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
              {errors.password && <p className="text-xs text-red-400">{errors.password.message}</p>}
            </div>

            <Button type="submit" loading={isSubmitting} icon={LogIn} size="lg" className="mt-2 w-full">
              Sign In
            </Button>
          </form>

          <p className="text-center text-sm text-slate-500 mt-6">
            Don't have an account?{' '}
            <Link to="/register" className="text-indigo-400 hover:text-indigo-300 transition-colors">
              Create one
            </Link>
          </p>
        </div>
      </motion.div>
    </div>
  )
}
