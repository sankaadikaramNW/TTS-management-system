import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export const Login = () => {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!username || !password) return
    
    setLoading(true)
    const success = await login(username, password)
    setLoading(false)
    
    if (success) {
      navigate('/')
    }
  }

  return (
    <div className="d-flex justify-content-center align-items-center vh-100 bg-app fade-in-slide">
      <div className="card slaf-card p-4 shadow-lg w-100" style={{ maxWidth: '420px' }}>
        <div className="text-center mb-4">
          <div className="d-inline-flex align-items-center justify-content-center bg-primary text-white rounded-circle p-3 mb-2" style={{ width: '60px', height: '60px' }}>
            <i className="bi bi-airplane-fill" style={{ fontSize: '1.75rem' }}></i>
          </div>
          <h3 className="mb-1 display-font fw-bold">SLAF TTS Portal</h3>
          <p className="text-muted" style={{ fontSize: '0.85rem' }}>Sri Lanka Air Force Trade Training School</p>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label fw-semibold">Username</label>
            <div className="input-group">
              <span className="input-group-text"><i className="bi bi-person"></i></span>
              <input 
                type="text" 
                className="form-control" 
                placeholder="Enter username" 
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="mb-4">
            <label className="form-label fw-semibold">Password</label>
            <div className="input-group">
              <span className="input-group-text"><i className="bi bi-lock"></i></span>
              <input 
                type="password" 
                className="form-control" 
                placeholder="Enter password" 
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
          </div>

          <button 
            type="submit" 
            className="btn btn-primary w-100 py-2.5 rounded-3 fw-semibold"
            disabled={loading}
          >
            {loading ? (
              <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
            ) : 'Sign In'}
          </button>
        </form>
      </div>
    </div>
  )
}
export default Login
