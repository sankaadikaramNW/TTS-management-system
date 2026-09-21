import React from 'react'
import { Navigate, Outlet } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { AccessDenied } from './AccessDenied'

export const ProtectedRoute = ({ permissionCode, moduleName }) => {
  const { token, loading, hasPermission } = useAuth()

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center vh-100 bg-app">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading authenticated session...</span>
        </div>
      </div>
    )
  }

  // If token does not exist or expired, redirect to existing login page
  if (!token) {
    return <Navigate to="/login" replace />
  }

  // If permission code is specified and user lacks the permission (and is not Admin)
  if (permissionCode && !hasPermission(permissionCode)) {
    return <AccessDenied moduleTitle={moduleName} permissionCode={permissionCode} />
  }

  return <Outlet />
}

export default ProtectedRoute
