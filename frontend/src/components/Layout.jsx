import React, { useState, useEffect } from 'react'
import { Outlet, useLocation } from 'react-router-dom'
import Sidebar from './Sidebar'
import Navbar from './Navbar'

export const Layout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const location = useLocation()

  // Close mobile sidebar automatically whenever location changes
  useEffect(() => {
    setSidebarOpen(false)
  }, [location])

  return (
    <div className="d-flex bg-app min-vh-100 position-relative overflow-x-hidden">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      <div className="w-100 min-vh-100 d-flex flex-column">
        <Navbar onToggleSidebar={() => setSidebarOpen(prev => !prev)} />
        <main className="main-wrapper px-3 px-md-4 pb-4 flex-grow-1">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
export default Layout
