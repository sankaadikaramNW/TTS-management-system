import React from 'react'
import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import Navbar from './Navbar'

export const Layout = () => {
  return (
    <div className="d-flex bg-app min-vh-100">
      <Sidebar />
      <div className="w-100">
        <Navbar />
        <main className="main-wrapper px-4 pb-4">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
export default Layout
