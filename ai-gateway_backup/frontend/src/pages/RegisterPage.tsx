import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Zap, UserPlus } from 'lucide-react'
import { authApi } from '@/api/client'
import { Button, Input } from '@/components/ui'

const schema = z.object({
  username: z.string().min(3, 'At least 3 characters'),
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'At least 8 characters'),
})

type FormData = z.infer<typeof schema>

export function RegisterPage() {
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)
  const navigate = useNavigate()

  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<FormData>({
    resolver: zodResolver(schema),
  })

  const onSubmit = async (data: FormData) => {
    try {
      setError('')
      await authApi.register(data)
      setSuccess(true)
      setTimeout(() => navigate('/login'), 2000)
    } catch (err: unknown) {
      const axiosErr = err as { response?: { data?: { detail?: string } } }
      setError(axiosErr?.response?.data?.detail ?? 'Registration failed.')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4" style={{ background: 'var(--color-background)' }}>
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 right-1/3 w-96 h-96 bg-indigo-500/5 rounded-full blur-3xl" />
      </div>
      <motion.div initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }} className="w-full max-w-md">
        <div className="flex flex-col items-center mb-8">
          <div className="w-14 h-14 rounded-2xl gradient-primary flex items-center justify-center mb-4 glow-primary">
            <Zap className="w-7 h-7 text-white" />
          </div>
          <h1 className="text-2xl font-bold gradient-text">Create Account</h1>
          <p className="text-slate-500 text-sm mt-1">Join PrivGuard AI Platform</p>
        </div>

        <div className="glass-strong rounded-2xl p-8">
          {success ? (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-center py-4">
              <div className="w-12 h-12 rounded-full bg-emerald-500/15 flex items-center justify-center mx-auto mb-3">
                <span className="text-2xl">✓</span>
              </div>
              <p className="text-emerald-400 font-medium">Account created!</p>
              <p className="text-slate-500 text-sm mt-1">Redirecting to login…</p>
            </motion.div>
          ) : (
            <>
              <h2 className="text-lg font-semibold text-slate-100 mb-6">Create your account</h2>
              {error && (
                <div className="mb-4 px-4 py-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm">{error}</div>
              )}
              <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4">
                <Input id="username" label="Username" placeholder="Choose a username" error={errors.username?.message} {...register('username')} />
                <Input id="email" type="email" label="Email" placeholder="Enter your email" error={errors.email?.message} {...register('email')} />
                <Input id="password" type="password" label="Password" placeholder="Create a password" error={errors.password?.message} {...register('password')} />
                <Button type="submit" loading={isSubmitting} icon={UserPlus} size="lg" className="mt-2 w-full">Create Account</Button>
              </form>
              <p className="text-center text-sm text-slate-500 mt-6">
                Already have an account?{' '}
                <Link to="/login" className="text-indigo-400 hover:text-indigo-300">Sign in</Link>
              </p>
            </>
          )}
        </div>
      </motion.div>
    </div>
  )
}
