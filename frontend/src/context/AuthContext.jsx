import React, { createContext, useContext, useState, useEffect } from 'react'
import axios from 'axios'
import { toast } from 'react-toastify'

const AuthContext = createContext()

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(() => localStorage.getItem('access_token'))
  const [loading, setLoading] = useState(true)

  // Configure Axios defaults when token is loaded or changed
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

  // Get current user profile details on load
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
        console.error('Failed to load user profile on startup', err)
        logout()
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
      toast.success(`Welcome back, ${loggedUser.full_name}!`)
      return true
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Invalid username or password'
      toast.error(errorMsg)
      return false
    }
  }

  const logout = () => {
    setToken(null)
    setUser(null)
    toast.info('Logged out successfully.')
  }

  // Permission helper check: checks code e.g. student:read
  const hasPermission = (code) => {
    if (!user) return false
    if (user.role.name === 'Super Administrator') return true
    return user.role.permissions.some(p => p.code === code)
  }

  const hasRole = (roleName) => {
    return user?.role?.name === roleName
  }

  return (
    <AuthContext.Provider value={{ user, token, loading, login, logout, hasPermission, hasRole }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)
