import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { useAuth } from '../context/AuthContext'
import { useTheme } from '../context/ThemeContext'
import { toast } from 'react-toastify'

export const Navbar = () => {
  const { user, logout } = useAuth()
  const { theme, toggleTheme } = useTheme()
  const [notifications, setNotifications] = useState([])
  const [showNotifications, setShowNotifications] = useState(false)

  // Fetch unread notifications every 30 seconds
  const fetchNotifications = async () => {
    try {
      const res = await axios.get('/api/v1/dashboard/notifications')
      setNotifications(res.data)
    } catch (err) {
      console.error('Failed to load notifications', err)
    }
  }

  useEffect(() => {
    fetchNotifications()
    const timer = setInterval(fetchNotifications, 30000)
    return () => clearInterval(timer)
  }, [])

  const markAsRead = async (id) => {
    try {
      await axios.post(`/api/v1/dashboard/notifications/${id}/read`)
      setNotifications((prev) => prev.filter((n) => n.id !== id))
      toast.info('Notification dismissed')
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <header className="glass-header d-flex align-items-center justify-content-between px-4 py-2 fixed-top" style={{ marginLeft: '260px', height: '70px', zIndex: 900 }}>
      {/* Search Header placeholder / Title */}
      <div className="d-flex align-items-center gap-3">
        <h4 className="mb-0 display-font text-primary">TTS Management Portal</h4>
      </div>

      {/* Control Buttons */}
      <div className="d-flex align-items-center gap-4">
        {/* Toggle Theme */}
        <button className="btn btn-link text-body p-0" onClick={toggleTheme} title="Toggle Light/Dark Theme">
          {theme === 'light' ? (
            <i className="bi bi-moon-stars-fill" style={{ fontSize: '1.25rem' }}></i>
          ) : (
            <i className="bi bi-sun-fill" style={{ fontSize: '1.25rem' }}></i>
          )}
        </button>

        {/* Notifications Icon dropdown */}
        <div className="position-relative">
          <button className="btn btn-link text-body p-0 position-relative" onClick={() => setShowNotifications(!showNotifications)}>
            <i className="bi bi-bell-fill" style={{ fontSize: '1.25rem' }}></i>
            {notifications.length > 0 && (
              <span className="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger" style={{ fontSize: '0.65rem' }}>
                {notifications.length}
              </span>
            )}
          </button>

          {showNotifications && (
            <div className="card slaf-card position-absolute end-0 mt-3 p-0" style={{ width: '320px', zIndex: 1100, maxHeight: '400px', overflowY: 'auto' }}>
              <div className="card-header bg-app d-flex justify-content-between align-items-center py-2 px-3">
                <span className="fw-semibold">Alert Center</span>
                <span className="badge bg-secondary">{notifications.length} new</span>
              </div>
              <div className="list-group list-group-flush">
                {notifications.length === 0 ? (
                  <div className="text-center py-4 text-muted">No pending alerts</div>
                ) : (
                  notifications.map((n) => (
                    <div key={n.id} className="list-group-item p-3 position-relative">
                      <div className="d-flex justify-content-between align-items-start mb-1">
                        <span className={`fw-semibold text-${n.type === 'ALERT' ? 'danger' : 'warning'}`} style={{ fontSize: '0.85rem' }}>
                          {n.title}
                        </span>
                        <button className="btn btn-link p-0 text-muted" onClick={() => markAsRead(n.id)}>
                          <i className="bi bi-x-circle-fill"></i>
                        </button>
                      </div>
                      <p className="mb-0 text-muted" style={{ fontSize: '0.75rem' }}>{n.message}</p>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}
        </div>

        {/* Logged user section */}
        <div className="d-flex align-items-center gap-3">
          <div className="text-end">
            <div className="fw-semibold" style={{ fontSize: '0.9rem' }}>{user?.full_name}</div>
            <div className="text-muted" style={{ fontSize: '0.75rem' }}>{user?.role?.name}</div>
          </div>
          <button className="btn btn-outline-danger btn-sm px-3 py-1.5 rounded-pill" onClick={logout}>
            <i className="bi bi-box-arrow-right me-1"></i> Logout
          </button>
        </div>
      </div>
    </header>
  )
}
export default Navbar
