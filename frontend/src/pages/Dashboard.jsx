import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { useAuth } from '../context/AuthContext'
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
  Title
} from 'chart.js'
import { Pie, Bar } from 'react-chartjs-2'

// Register Chart.js models
ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title)

export const Dashboard = () => {
  const { hasPermission, hasRole } = useAuth()
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(true)

  const fetchSummary = async () => {
    try {
      const res = await axios.get('/api/v1/dashboard/summary')
      setSummary(res.data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchSummary()
  }, [])

  if (loading || !summary) {
    return (
      <div className="d-flex justify-content-center align-items-center py-5">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading Dashboard Summary...</span>
        </div>
      </div>
    )
  }

  const { parade, accommodation, academic, recent_activities } = summary

  // Pie Chart Data: Parade State Distribution
  const pieData = {
    labels: ['Present', 'Sick Report', 'Hospital', 'Leave', 'TDY', 'Course Visit', 'Detached', 'AWOL'],
    datasets: [
      {
        data: [
          parade.present,
          parade.sick_report,
          parade.hospital,
          parade.leave,
          parade.temp_duty,
          parade.course_visit,
          parade.detached_duty,
          parade.awol,
        ],
        backgroundColor: [
          '#10b981', // green
          '#f59e0b', // orange
          '#f87171', // light red
          '#3b82f6', // blue
          '#8b5cf6', // purple
          '#ec4899', // pink
          '#6b7280', // gray
          '#ef4444', // bold red
        ],
        borderWidth: 1,
      },
    ],
  }

  // Bar Chart Data: Performance Analysis
  const barData = {
    labels: ['Class Pass Rate', 'Bed Occupancy', 'Active Courses'],
    datasets: [
      {
        label: 'System Performance %',
        data: [academic.average_pass_rate, accommodation.occupancy_rate, academic.course_count * 10], // scaled
        backgroundColor: 'rgba(59, 130, 246, 0.7)',
        borderColor: 'rgba(59, 130, 246, 1)',
        borderWidth: 1,
      },
    ],
  }

  return (
    <div className="fade-in-slide">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 className="mb-0 text-primary display-font">Executive Overview</h2>
          <p className="text-muted mb-0">Daily status updates for Sri Lanka Air Force Trade Training School</p>
        </div>
        <button className="btn btn-primary d-flex align-items-center gap-2" onClick={fetchSummary}>
          <i className="bi bi-arrow-clockwise"></i> Refresh
        </button>
      </div>

      {/* KPI Cards Row */}
      <div className="row g-3 mb-4">
        <div className="col-md-3 col-sm-6">
          <div className="card slaf-card kpi-card p-3 d-flex flex-column h-100">
            <span className="text-muted text-uppercase fw-semibold" style={{ fontSize: '0.75rem' }}>Total Enrolled</span>
            <h3 className="mb-0 mt-2 fw-bold">{parade.total_enrolled}</h3>
            <span className="text-muted mt-1" style={{ fontSize: '0.7rem' }}>Registered trainees</span>
          </div>
        </div>
        <div className="col-md-3 col-sm-6">
          <div className="card slaf-card kpi-card success p-3 d-flex flex-column h-100">
            <span className="text-muted text-uppercase fw-semibold" style={{ fontSize: '0.75rem' }}>Present Strength</span>
            <h3 className="mb-0 mt-2 fw-bold text-success">{parade.present}</h3>
            <span className="text-muted mt-1" style={{ fontSize: '0.7rem' }}>On-duty strength</span>
          </div>
        </div>
        <div className="col-md-3 col-sm-6">
          <div className="card slaf-card kpi-card warning p-3 d-flex flex-column h-100">
            <span className="text-muted text-uppercase fw-semibold" style={{ fontSize: '0.75rem' }}>Sick Report / Hospital</span>
            <h3 className="mb-0 mt-2 fw-bold text-warning">{parade.sick_report + parade.hospital}</h3>
            <span className="text-muted mt-1" style={{ fontSize: '0.7rem' }}>Medical category</span>
          </div>
        </div>
        <div className="col-md-3 col-sm-6">
          <div className="card slaf-card kpi-card danger p-3 d-flex flex-column h-100">
            <span className="text-muted text-uppercase fw-semibold" style={{ fontSize: '0.75rem' }}>Absent / AWOL</span>
            <h3 className="mb-0 mt-2 fw-bold text-danger">{parade.leave + parade.awol}</h3>
            <span className="text-muted mt-1" style={{ fontSize: '0.7rem' }}>Out of camp limits</span>
          </div>
        </div>
      </div>

      {/* Main Graphs Layout */}
      <div className="row g-4 mb-4">
        <div className="col-lg-6 col-md-12">
          <div className="card slaf-card p-4 h-100">
            <h5 className="card-title mb-3">Trainee Strength Distribution</h5>
            <div className="mx-auto" style={{ maxWidth: '300px' }}>
              <Pie data={pieData} />
            </div>
          </div>
        </div>
        <div className="col-lg-6 col-md-12">
          <div className="card slaf-card p-4 h-100">
            <h5 className="card-title mb-3">Performance & Accommodation</h5>
            <Bar data={barData} />
          </div>
        </div>
      </div>

      {/* Dashboard Sub-layouts */}
      <div className="row g-4">
        {/* Recent Audit Logs (Only visible to System Administrators & Security Officers) */}
        {(hasPermission('system:audit') || hasRole('Super Administrator') || hasRole('System Administrator')) && (
          <div className="col-lg-7 col-md-12">
            <div className="card slaf-card p-4 h-100">
              <h5 className="card-title mb-3">Recent Security & Audit Logs</h5>
              <div className="table-responsive">
                <table className="table slaf-table mb-0">
                  <thead>
                    <tr>
                      <th>User</th>
                      <th>Action</th>
                      <th>Date</th>
                    </tr>
                  </thead>
                  <tbody>
                    {recent_activities.length === 0 ? (
                      <tr>
                        <td colSpan="3" className="text-center text-muted">No audit trails recorded</td>
                      </tr>
                    ) : (
                      recent_activities.map((log) => (
                        <tr key={log.id}>
                          <td><span className="fw-semibold">{log.username}</span></td>
                          <td>{log.action}</td>
                          <td><small className="text-muted">{new Date(log.created_at).toLocaleString()}</small></td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* Accommodation Occupancy Card */}
        <div className={(hasPermission('system:audit') || hasRole('Super Administrator') || hasRole('System Administrator')) ? 'col-lg-5 col-md-12' : 'col-12'}>
          <div className="card slaf-card p-4 h-100">
            <h5 className="card-title mb-3">Accommodation Summary</h5>
            <div className="d-flex flex-column gap-3">
              <div className="d-flex justify-content-between align-items-center">
                <span>Total beds configured</span>
                <span className="fw-bold">{accommodation.total_beds}</span>
              </div>
              <div className="d-flex justify-content-between align-items-center">
                <span>Currently occupied</span>
                <span className="fw-bold text-primary">{accommodation.occupied_beds}</span>
              </div>
              <div className="d-flex justify-content-between align-items-center">
                <span>Bed occupancy rate</span>
                <span className="fw-bold text-success">{accommodation.occupancy_rate}%</span>
              </div>
              <div className="progress mt-2" style={{ height: '10px' }}>
                <div 
                  className="progress-bar bg-success" 
                  role="progressbar" 
                  style={{ width: `${accommodation.occupancy_rate}%` }} 
                  aria-valuenow={accommodation.occupancy_rate} 
                  aria-valuemin="0" 
                  aria-valuemax="100"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
export default Dashboard
