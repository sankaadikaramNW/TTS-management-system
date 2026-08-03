import React from 'react'
import { Navigate, Outlet, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export const ProtectedRoute = ({ permissionCode }) => {
  const { token, loading, hasPermission } = useAuth()

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center vh-100 bg-app">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    )
  }

  if (!token) {
    return <Navigate to="/login" replace />
  }

  if (permissionCode && !hasPermission(permissionCode)) {
    return (
      <div className="container py-5 text-center fade-in-slide">
        <div className="card slaf-card p-5 mx-auto" style={{ maxWidth: '600px' }}>
          <div className="text-danger mb-4">
            <i className="bi bi-shield-lock-fill" style={{ fontSize: '4rem' }}></i>
          </div>
          <h2 className="mb-3">Access Denied</h2>
          <p className="text-muted mb-4">
            You do not have the required permissions to access this page. Please contact the administrator if you believe this is in error.
          </p>
          <Link to="/dashboard" className="btn btn-primary px-4 py-2">
            Return to Dashboard
          </Link>
        </div>
      </div>
    )
  }

  return <Outlet />
}
