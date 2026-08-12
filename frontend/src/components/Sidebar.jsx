import React from 'react'
import { NavLink, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export const Sidebar = ({ isOpen, onClose, isCollapsed, onToggleCollapse }) => {
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
          <div className="sidebar-module-header px-4 py-2 text-white-50 small fw-bold text-uppercase border-bottom border-secondary mb-3 d-flex align-items-center">
            <i className="bi bi-house-door me-2"></i>
            <span className="module-header-text">Housing Module</span>
          </div>
          <NavLink to="/accommodation" end className="nav-link" title="Dashboard">
            <i className="bi bi-speedometer2"></i>
            <span>Dashboard</span>
          </NavLink>
          <NavLink to="/accommodation/billets" className="nav-link" title="Billet Management">
            <i className="bi bi-building"></i>
            <span>Billet Management</span>
          </NavLink>
          <NavLink to="/accommodation/bunks" className="nav-link" title="Bunk Bed Management">
            <i className="bi bi-layout-three-columns"></i>
            <span>Bunk Bed Management</span>
          </NavLink>
          <NavLink to="/accommodation/allocate" className="nav-link" title="Bed Allocation">
            <i className="bi bi-door-closed"></i>
            <span>Bed Allocation</span>
          </NavLink>
          <NavLink to="/accommodation/trainees" className="nav-link" title="Trainee Accommodation">
            <i className="bi bi-people-fill"></i>
            <span>Trainee Accommodation</span>
          </NavLink>
          <NavLink to="/accommodation/transfers" className="nav-link" title="Transfer & Release">
            <i className="bi bi-arrow-left-right"></i>
            <span>Transfer / Release</span>
          </NavLink>
          <NavLink to="/accommodation/history" className="nav-link" title="Accommodation History">
            <i className="bi bi-clock-history"></i>
            <span>Accommodation History</span>
          </NavLink>
          <NavLink to="/accommodation/reports" className="nav-link" title="Reports & Analytics">
            <i className="bi bi-file-earmark-bar-graph"></i>
            <span>Reports & Analytics</span>
          </NavLink>
          <NavLink to="/accommodation/map" className="nav-link" title="Visual Bunk Map">
            <i className="bi bi-geo-alt"></i>
            <span>Visual Bunk Map</span>
          </NavLink>
          
          <hr className="mx-3 opacity-25" style={{ color: '#fff' }} />
          <NavLink to="/dashboard" className="nav-link text-info" title="Back to Portal Home">
            <i className="bi bi-arrow-left-square"></i>
            <span>Back to Portal Home</span>
          </NavLink>
        </>
      )
    }

    if (isStudent) {
      return (
        <>
          <div className="sidebar-module-header px-4 py-2 text-white-50 small fw-bold text-uppercase border-bottom border-secondary mb-3 d-flex align-items-center">
            <i className="bi bi-people me-2"></i>
            <span className="module-header-text">Trainees Module</span>
          </div>
          <NavLink to="/students" end className="nav-link" title="Trainee Directory">
            <i className="bi bi-people-fill"></i>
            <span>Trainee Directory</span>
          </NavLink>
          {hasPermission('student:write') && (
            <NavLink to="/students/new" className="nav-link" title="Add New Trainee">
              <i className="bi bi-person-plus-fill"></i>
              <span>Add New Trainee</span>
            </NavLink>
          )}
          
          <hr className="mx-3 opacity-25" style={{ color: '#fff' }} />
          <NavLink to="/dashboard" className="nav-link text-info" title="Back to Portal Home">
            <i className="bi bi-arrow-left-square"></i>
            <span>Back to Portal Home</span>
          </NavLink>
        </>
      )
    }

    if (isParade) {
      return (
        <>
          <div className="sidebar-module-header px-4 py-2 text-white-50 small fw-bold text-uppercase border-bottom border-secondary mb-3 d-flex align-items-center">
            <i className="bi bi-clipboard2-check me-2"></i>
            <span className="module-header-text">Parade Module</span>
          </div>
          <NavLink to="/parade" className="nav-link" title="Parade Board">
            <i className="bi bi-clipboard2-check-fill"></i>
            <span>Parade Board</span>
          </NavLink>
          
          <hr className="mx-3 opacity-25" style={{ color: '#fff' }} />
          <NavLink to="/dashboard" className="nav-link text-info" title="Back to Portal Home">
            <i className="bi bi-arrow-left-square"></i>
            <span>Back to Portal Home</span>
          </NavLink>
        </>
      )
    }

    if (isAcademic) {
      const queryParams = new URLSearchParams(location.search)
      const isTrades = queryParams.get('view') === 'trades'
      const isCalendar = queryParams.get('view') === 'calendar'
      return (
        <>
          <div className="sidebar-module-header px-4 py-2 text-white-50 small fw-bold text-uppercase border-bottom border-secondary mb-3 d-flex align-items-center">
            <i className="bi bi-journal-bookmark me-2"></i>
            <span className="module-header-text">Academic Module</span>
          </div>
          <NavLink 
            to="/academic" 
            end 
            className={`nav-link ${(!isTrades && !isCalendar && path === '/academic') ? 'active' : ''}`}
            title="Course Syllabus"
          >
            <i className="bi bi-journal-bookmark-fill"></i>
            <span>Course Syllabus</span>
          </NavLink>
          <NavLink 
            to="/academic?view=calendar" 
            className={`nav-link ${isCalendar ? 'active' : ''}`}
            title="Course Calendar"
          >
            <i className="bi bi-calendar-range-fill"></i>
            <span>Course Calendar</span>
          </NavLink>
          {hasPermission('academic:write') && (
            <NavLink 
              to="/academic?view=trades" 
              className={`nav-link ${isTrades ? 'active' : ''}`}
              title="Trade Management"
            >
              <i className="bi bi-gear-fill"></i>
              <span>Trade Management</span>
            </NavLink>
          )}
          
          <hr className="mx-3 opacity-25" style={{ color: '#fff' }} />
          <NavLink to="/dashboard" className="nav-link text-info" title="Back to Portal Home">
            <i className="bi bi-arrow-left-square"></i>
            <span>Back to Portal Home</span>
          </NavLink>
        </>
      )
    }

    if (isReport) {
      return (
        <>
          <div className="sidebar-module-header px-4 py-2 text-white-50 small fw-bold text-uppercase border-bottom border-secondary mb-3 d-flex align-items-center">
            <i className="bi bi-bar-chart-line me-2"></i>
            <span className="module-header-text">Analytics Module</span>
          </div>
          <NavLink to="/reports" className="nav-link" title="General Reports">
            <i className="bi bi-file-earmark-bar-graph"></i>
            <span>General Reports</span>
          </NavLink>
          
          <hr className="mx-3 opacity-25" style={{ color: '#fff' }} />
          <NavLink to="/dashboard" className="nav-link text-info" title="Back to Portal Home">
            <i className="bi bi-arrow-left-square"></i>
            <span>Back to Portal Home</span>
          </NavLink>
        </>
      )
    }

    if (isAdmin) {
      return (
        <>
          <div className="sidebar-module-header px-4 py-2 text-white-50 small fw-bold text-uppercase border-bottom border-secondary mb-3 d-flex align-items-center">
            <i className="bi bi-shield-lock me-2"></i>
            <span className="module-header-text">Security Module</span>
          </div>
          <NavLink to="/admin" className="nav-link" title="User Accounts">
            <i className="bi bi-gear-fill"></i>
            <span>User Accounts</span>
          </NavLink>
          
          <hr className="mx-3 opacity-25" style={{ color: '#fff' }} />
          <NavLink to="/dashboard" className="nav-link text-info" title="Back to Portal Home">
            <i className="bi bi-arrow-left-square"></i>
            <span>Back to Portal Home</span>
          </NavLink>
        </>
      )
    }

    // Default main dashboard navigation (Central gateway selector)
    return (
      <>
        <div className="sidebar-module-header px-4 py-2 text-white-50 small fw-bold text-uppercase border-bottom border-secondary mb-3 d-flex align-items-center">
          <i className="bi bi-grid-3x3-gap me-2"></i>
          <span className="module-header-text">System Navigation</span>
        </div>
        <NavLink to="/dashboard" className="nav-link" title="Executive Overview">
          <i className="bi bi-grid-1x2"></i>
          <span>Executive Overview</span>
        </NavLink>

        {hasPermission('student:read') && (
          <NavLink to="/students" className="nav-link" title="Student Details">
            <i className="bi bi-people"></i>
            <span>Student Details</span>
          </NavLink>
        )}

        {hasPermission('parade:read') && (
          <NavLink to="/parade" className="nav-link" title="Parade State">
            <i className="bi bi-clipboard2-check"></i>
            <span>Parade State</span>
          </NavLink>
        )}

        {hasPermission('room:read') && (
          <NavLink to="/accommodation" className="nav-link" title="Accommodation">
            <i className="bi bi-house-door"></i>
            <span>Accommodation</span>
          </NavLink>
        )}

        {hasPermission('academic:read') && (
          <NavLink to="/academic" className="nav-link" title="Academic Activities">
            <i className="bi bi-journal-bookmark-fill"></i>
            <span>Academic Activities</span>
          </NavLink>
        )}

        {hasPermission('reports:read') && (
          <NavLink to="/reports" className="nav-link" title="Reports & Analytics">
            <i className="bi bi-file-earmark-bar-graph"></i>
            <span>Reports & Analytics</span>
          </NavLink>
        )}

        {(hasRole('Super Administrator') || hasRole('System Administrator') || hasPermission('system:audit')) && (
          <NavLink to="/admin" className="nav-link" title="System Admin">
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
      <aside className={`slaf-sidebar d-flex flex-column justify-content-between py-4 ${isOpen ? 'show-mobile' : ''} ${isCollapsed ? 'collapsed' : ''}`}>
        <div className="position-relative">
          {/* Desktop Collapse Toggle Button (Image 2 style chevron dropdown toggle) */}
          <div className={`d-none d-lg-flex px-3 mb-2 ${isCollapsed ? 'justify-content-center' : 'justify-content-end'}`}>
            <button 
              className="sidebar-toggle-btn"
              onClick={onToggleCollapse}
              title={isCollapsed ? "Expand Sidebar" : "Collapse Sidebar"}
              aria-label="Toggle Sidebar Navigation"
            >
              <i className={`bi ${isCollapsed ? 'bi-chevron-right' : 'bi-chevron-left'}`}></i>
            </button>
          </div>

          {/* Mobile Close Button */}
          <button className="btn btn-link text-white-50 d-lg-none position-absolute top-0 end-0 me-3 mt-1 p-1" onClick={onClose} title="Close Menu">
            <i className="bi bi-x-lg fs-5"></i>
          </button>

          {/* Sidebar Header Logo */}
          <div className="px-3 mb-4 text-center">
            <div 
              className="d-inline-flex align-items-center justify-content-center bg-primary text-white rounded-circle p-2 mb-2" 
              style={{ width: isCollapsed ? '42px' : '50px', height: isCollapsed ? '42px' : '50px', transition: 'all 0.3s ease' }}
            >
              <i className="bi bi-airplane-engines" style={{ fontSize: isCollapsed ? '1.25rem' : '1.5rem' }}></i>
            </div>
            <div className="sidebar-header-text">
              <h5 className="mb-0 text-white display-font">SLAF TTS</h5>
              <span className="text-muted" style={{ fontSize: '0.75rem' }}>Management Portal</span>
            </div>
          </div>

          <hr className="mx-3 opacity-25" style={{ color: '#fff' }} />

          {/* Dynamic Navigation list */}
          <nav className="nav flex-column">
            {renderSidebarContent()}
          </nav>
        </div>

        <div className="px-3 mt-auto text-center">
          <span className="sidebar-footer-text text-muted" style={{ fontSize: '0.7rem' }}>SLAF TTS v1.0.0 © 2026</span>
        </div>
      </aside>
    </>
  )
}
export default Sidebar
