import React from 'react'
import { NavLink } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export const Sidebar = () => {
  const { hasPermission, hasRole } = useAuth()

  return (
    <aside className="slaf-sidebar d-flex flex-column justify-content-between py-4">
      <div>
        {/* Header Header */}
        <div className="px-4 mb-4 text-center">
          <div className="d-inline-flex align-items-center justify-content-center bg-primary text-white rounded-circle p-2 mb-2" style={{ width: '50px', height: '50px' }}>
            <i className="bi bi-airplane-engines" style={{ fontSize: '1.5rem' }}></i>
          </div>
          <h5 className="mb-0 text-white display-font">SLAF TTS</h5>
          <span className="text-muted" style={{ fontSize: '0.75rem' }}>Management Portal</span>
        </div>

        <hr className="mx-3 opacity-25" style={{ color: '#fff' }} />

        {/* Navigation list */}
        <nav className="nav flex-column">
          <NavLink to="/" className="nav-link">
            <i className="bi bi-grid-1x2"></i>
            <span>Dashboard</span>
          </NavLink>

          {hasPermission('student:read') && (
            <NavLink to="/students" className="nav-link">
              <i className="bi bi-people"></i>
              <span>Student Details</span>
            </NavLink>
          )}

          {hasPermission('parade:read') && (
            <NavLink to="/parade" className="nav-link">
              <i className="bi bi-clipboard2-check"></i>
              <span>Parade State</span>
            </NavLink>
          )}

          {hasPermission('room:read') && (
            <NavLink to="/accommodation" className="nav-link">
              <i className="bi bi-house-door"></i>
              <span>Accommodation</span>
            </NavLink>
          )}

          {hasPermission('academic:read') && (
            <NavLink to="/academic" className="nav-link">
              <i className="bi bi-journal-bookmark-fill"></i>
              <span>Academic Activities</span>
            </NavLink>
          )}

          {hasPermission('student:read') && (
            <NavLink to="/reports" className="nav-link">
              <i className="bi bi-file-earmark-bar-graph"></i>
              <span>Reports & Analytics</span>
            </NavLink>
          )}

          {(hasRole('Super Administrator') || hasRole('System Administrator')) && (
            <NavLink to="/admin" className="nav-link">
              <i className="bi bi-gear-fill"></i>
              <span>System Admin</span>
            </NavLink>
          )}
        </nav>
      </div>

      <div className="px-4 mt-auto text-center">
        <span className="text-muted" style={{ fontSize: '0.7rem' }}>SLAF TTS v1.0.0 © 2026</span>
      </div>
    </aside>
  )
}
export default Sidebar
