import React, { createContext, useContext, useState, useEffect, useCallback, useRef } from 'react'
import axios from 'axios'
import { toast } from 'react-toastify'

const AuthContext = createContext()

// ─── SYNCHRONOUS BOOTSTRAP ───────────────────────────────────────────────────
// Set the Authorization header IMMEDIATELY at module load time so that any
// component which fires an axios call during its first-render useEffect already
// has the correct token in the header (avoids the race condition where the
// AuthContext useEffect runs too late).
const _bootstrapToken = localStorage.getItem('access_token')
if (_bootstrapToken) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${_bootstrapToken}`
}

// ─── GLOBAL 401 INTERCEPTOR ──────────────────────────────────────────────────
// Single interceptor instance – we store its ID so we can eject it if needed.
let _interceptorId = null
let _logoutFn = null   // will be wired up once AuthProvider mounts

const wire401Interceptor = () => {
  if (_interceptorId !== null) return   // already registered
  _interceptorId = axios.interceptors.response.use(
    res => res,
    err => {
      if (err.response?.status === 401 && typeof _logoutFn === 'function') {
        // Only fire logout once per session – avoid toast storm
        if (localStorage.getItem('access_token')) {
          _logoutFn()
          toast.error('Session expired. Please log in again.')
        }
      }
      return Promise.reject(err)
    }
  )
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(() => localStorage.getItem('access_token'))
  const [loading, setLoading] = useState(true)
  const logoutCalledRef = useRef(false)

  const logout = useCallback(() => {
    setToken(null)
    setUser(null)
    delete axios.defaults.headers.common['Authorization']
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    if (!logoutCalledRef.current) {
      logoutCalledRef.current = true
      toast.info('Logged out successfully.')
      setTimeout(() => { logoutCalledRef.current = false }, 2000)
    }
  }, [])

  // Wire the global 401 interceptor so it can call our logout
  useEffect(() => {
    _logoutFn = logout
    wire401Interceptor()
    return () => { _logoutFn = null }
  }, [logout])

  // Keep axios header in sync when token changes at runtime (login / logout)
  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
      localStorage.setItem('access_token', token)
    } else {
      delete axios.defaults.headers.common['Authorization']
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    }
  }, [token])

  // Load current user profile on mount (or when token changes)
  useEffect(() => {
    const loadCurrentUser = async () => {
      if (!token) {
        setLoading(false)
        return
      }
      try {
        const res = await axios.get('/api/v1/auth/me')
        setUser(res.data)
      } catch (err) {
        // 401 is handled by the interceptor above; other errors still call logout
        if (err.response?.status !== 401) {
          console.error('Failed to load user profile on startup', err)
          logout()
        }
      } finally {
        setLoading(false)
      }
    }
    loadCurrentUser()
  }, [token])

  const login = async (username, password) => {
    try {
      const res = await axios.post('/api/v1/auth/login', { username, password })
      const { access_token, refresh_token, user: loggedUser } = res.data
      localStorage.setItem('refresh_token', refresh_token)
      setToken(access_token)
      setUser(loggedUser)
      logoutCalledRef.current = false
      toast.success(`Welcome back, ${loggedUser.full_name}!`)
      return true
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Invalid username or password'
      toast.error(errorMsg)
      return false
    }
  }

  const hasPermission = (code) => {
    if (!user) return false
    const roleName = (user.role?.name || '').toLowerCase()
    const roleId = (user.role?.id || '').toLowerCase()
    if (
      roleName.includes('admin') || 
      roleId.includes('admin') ||
      user.role?.name === 'Super Administrator' || 
      user.role?.name === 'System Administrator' || 
      user.role?.id === 'role-super-admin' || 
      user.role?.id === 'role-sys-admin'
    ) return true
    
    const perms = user.effective_permissions || user.role?.permissions || []
    return perms.some(p => p.code === code)
  }


  const hasRole = (roleName) => user?.role?.name === roleName

  return (
    <AuthContext.Provider value={{ user, token, loading, login, logout, hasPermission, hasRole }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)
