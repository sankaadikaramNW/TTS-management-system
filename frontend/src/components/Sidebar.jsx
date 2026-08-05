import React from 'react'
import { NavLink, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export const Sidebar = ({ isOpen, onClose }) => {
  const { hasPermission, hasRole } = useAuth()
  const location = useLocation()
  const path = location.pathname

  // Determine which module layout to display
  const isAccommodation = path.startsWith('/accommodation')
  const isStudent = path.startsWith('/students')
  const isParade = path.startsWith('/parade')
  const isAcademic = path.startsWith('/academic')
  const isReport = path.startsWith('/reports')
  const isAdmin = path.startsWith('/admin')

  const renderSidebarContent = () => {
    if (isAccommodation) {
      return (
        <>
          <div className="px-4 py-2 text-white-50 small fw-bold text-uppercase border-bottom border-secondary mb-3">
            <i className="bi bi-house-door me-2"></i>Housing Module
          </div>
          <NavLink to="/accommodation" end className="nav-link">
            <i className="bi bi-speedometer2"></i>
            <span>Dashboard</span>
          </NavLink>
          <NavLink to="/accommodation/map" className="nav-link">
            <i className="bi bi-geo-alt"></i>
            <span>Placement Map</span>
          </NavLink>
          <NavLink to="/accommodation/buildings" className="nav-link">
            <i className="bi bi-building"></i>
            <span>Building Management</span>
          </NavLink>
          <NavLink to="/accommodation/billets" className="nav-link">
            <i className="bi bi-layout-three-columns"></i>
            <span>Billet Management</span>
          </NavLink>
          <NavLink to="/accommodation/beds" className="nav-link">
            <i className="bi bi-door-closed"></i>
            <span>Bed Management</span>
          </NavLink>
          <NavLink to="/accommodation/reports" className="nav-link">
            <i className="bi bi-file-earmark-bar-graph"></i>
            <span>Reports & History</span>
          </NavLink>
          
          <hr className="mx-3 opacity-25" style={{ color: '#fff' }} />
          <NavLink to="/dashboard" className="nav-link text-info">
            <i className="bi bi-arrow-left-square"></i>
            <span>Back to Portal Home</span>
          </NavLink>
        </>
      )
    }

    if (isStudent) {
      return (
        <>
          <div className="px-4 py-2 text-white-50 small fw-bold text-uppercase border-bottom border-secondary mb-3">
            <i className="bi bi-people me-2"></i>Trainees Module
          </div>
          <NavLink to="/students" end className="nav-link">
            <i className="bi bi-people-fill"></i>
            <span>Trainee Directory</span>
          </NavLink>
          {hasPermission('student:write') && (
            <NavLink to="/students/new" className="nav-link">
              <i className="bi bi-person-plus-fill"></i>
              <span>Add New Trainee</span>
            </NavLink>
          )}
          
          <hr className="mx-3 opacity-25" style={{ color: '#fff' }} />
          <NavLink to="/dashboard" className="nav-link text-info">
            <i className="bi bi-arrow-left-square"></i>
            <span>Back to Portal Home</span>
          </NavLink>
        </>
      )
    }

    if (isParade) {
      return (
        <>
          <div className="px-4 py-2 text-white-50 small fw-bold text-uppercase border-bottom border-secondary mb-3">
            <i className="bi bi-clipboard2-check me-2"></i>Parade Module
          </div>
          <NavLink to="/parade" className="nav-link">
            <i className="bi bi-clipboard2-check-fill"></i>
            <span>Parade Board</span>
          </NavLink>
          
          <hr className="mx-3 opacity-25" style={{ color: '#fff' }} />
          <NavLink to="/dashboard" className="nav-link text-info">
            <i className="bi bi-arrow-left-square"></i>
            <span>Back to Portal Home</span>
          </NavLink>
        </>
      )
    }

    if (isAcademic) {
      const queryParams = new URLSearchParams(location.search)
      const isTrades = queryParams.get('view') === 'trades'
      return (
        <>
          <div className="px-4 py-2 text-white-50 small fw-bold text-uppercase border-bottom border-secondary mb-3">
            <i className="bi bi-journal-bookmark me-2"></i>Academic Module
          </div>
          <NavLink 
            to="/academic" 
            end 
            className={`nav-link ${(!isTrades && path === '/academic') ? 'active' : ''}`}
          >
            <i className="bi bi-journal-bookmark-fill"></i>
            <span>Course Syllabus</span>
          </NavLink>
          {hasPermission('academic:write') && (
            <NavLink 
              to="/academic?view=trades" 
              className={`nav-link ${isTrades ? 'active' : ''}`}
            >
              <i className="bi bi-gear-fill"></i>
              <span>Trade Management</span>
            </NavLink>
          )}
          
          <hr className="mx-3 opacity-25" style={{ color: '#fff' }} />
          <NavLink to="/dashboard" className="nav-link text-info">
            <i className="bi bi-arrow-left-square"></i>
            <span>Back to Portal Home</span>
          </NavLink>
        </>
      )
    }

    if (isReport) {
      return (
        <>
          <div className="px-4 py-2 text-white-50 small fw-bold text-uppercase border-bottom border-secondary mb-3">
            <i className="bi bi-bar-chart-line me-2"></i>Analytics Module
          </div>
          <NavLink to="/reports" className="nav-link">
            <i className="bi bi-file-earmark-bar-graph"></i>
            <span>General Reports</span>
          </NavLink>
          
          <hr className="mx-3 opacity-25" style={{ color: '#fff' }} />
          <NavLink to="/dashboard" className="nav-link text-info">
            <i className="bi bi-arrow-left-square"></i>
            <span>Back to Portal Home</span>
          </NavLink>
        </>
      )
    }

    if (isAdmin) {
      return (
        <>
          <div className="px-4 py-2 text-white-50 small fw-bold text-uppercase border-bottom border-secondary mb-3">
            <i className="bi bi-shield-lock me-2"></i>Security Module
          </div>
          <NavLink to="/admin" className="nav-link">
            <i className="bi bi-gear-fill"></i>
            <span>User Accounts</span>
          </NavLink>
          
          <hr className="mx-3 opacity-25" style={{ color: '#fff' }} />
          <NavLink to="/dashboard" className="nav-link text-info">
            <i className="bi bi-arrow-left-square"></i>
            <span>Back to Portal Home</span>
          </NavLink>
        </>
      )
    }

    // Default main dashboard navigation (Central gateway selector)
    return (
      <>
        <div className="px-4 py-2 text-white-50 small fw-bold text-uppercase border-bottom border-secondary mb-3">
          <i className="bi bi-grid-3x3-gap me-2"></i>System Navigation
        </div>
        <NavLink to="/dashboard" className="nav-link">
          <i className="bi bi-grid-1x2"></i>
          <span>Executive Overview</span>
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
      </>
    )
  }

  return (
    <>
      {isOpen && (
        <div className="sidebar-backdrop d-lg-none" onClick={onClose} />
      )}
      <aside className={`slaf-sidebar d-flex flex-column justify-content-between py-4 ${isOpen ? 'show-mobile' : ''}`}>
        <div className="position-relative">
          {/* Mobile Close Button */}
          <button className="btn btn-link text-white-50 d-lg-none position-absolute top-0 end-0 me-3 mt-1 p-1" onClick={onClose} title="Close Menu">
            <i className="bi bi-x-lg fs-5"></i>
          </button>

          {/* Sidebar Header Logo */}
          <div className="px-4 mb-4 text-center">
            <div className="d-inline-flex align-items-center justify-content-center bg-primary text-white rounded-circle p-2 mb-2" style={{ width: '50px', height: '50px' }}>
              <i className="bi bi-airplane-engines" style={{ fontSize: '1.5rem' }}></i>
            </div>
            <h5 className="mb-0 text-white display-font">SLAF TTS</h5>
            <span className="text-muted" style={{ fontSize: '0.75rem' }}>Management Portal</span>
          </div>

          <hr className="mx-3 opacity-25" style={{ color: '#fff' }} />

          {/* Dynamic Navigation list */}
          <nav className="nav flex-column">
            {renderSidebarContent()}
          </nav>
        </div>

        <div className="px-4 mt-auto text-center">
          <span className="text-muted" style={{ fontSize: '0.7rem' }}>SLAF TTS v1.0.0 © 2026</span>
        </div>
      </aside>
    </>
  )
}
export default Sidebar
