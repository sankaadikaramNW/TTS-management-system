import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { toast } from 'react-toastify'

export const InstructorAssignment = () => {
  const [instructors, setInstructors] = useState([])
  const [loading, setLoading] = useState(true)
  const [query, setQuery] = useState('')

  const fetchInstructors = async () => {
    setLoading(true)
    try {
      const res = await axios.get('/api/v1/academic/instructors')
      setInstructors(res.data)
    } catch (err) {
      toast.error('Failed to load instructor records from User Management')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchInstructors()
  }, [])

  const filtered = instructors.filter(i => 
    i.full_name.toLowerCase().includes(query.toLowerCase()) ||
    (i.service_number && i.service_number.toLowerCase().includes(query.toLowerCase())) ||
    (i.rank && i.rank.toLowerCase().includes(query.toLowerCase())) ||
    (i.department && i.department.toLowerCase().includes(query.toLowerCase()))
  )

  return (
    <div className="fade-in-slide">
      <div className="d-flex justify-content-between align-items-center mb-3">
        <div>
          <h5 className="fw-bold text-dark mb-0 display-font">SSOT Instructor Assignments</h5>
          <small className="text-muted">Dynamically retrieved from User Management Module (No manual duplication)</small>
        </div>
        <button className="btn btn-outline-primary btn-sm fw-semibold" onClick={fetchInstructors}>
          <i className="bi bi-arrow-clockwise me-1"></i> Sync User Portal
        </button>
      </div>

      <div className="alert alert-info py-2.5 px-3 mb-3 d-flex align-items-center gap-2.5 shadow-sm small">
        <i className="bi bi-shield-lock-fill fs-5 text-primary"></i>
        <div>
          <strong>Single Source of Truth Rule:</strong> Instructor profiles are read-only views retrieved directly from the User Management module (Users with the <strong>Instructor</strong> role).
        </div>
      </div>

      <div className="card slaf-card p-3 mb-3 shadow-sm">
        <div className="row g-2">
          <div className="col-md-6">
            <div className="input-group input-group-sm">
              <span className="input-group-text bg-light"><i className="bi bi-search text-muted"></i></span>
              <input 
                type="text" 
                className="form-control" 
                placeholder="Search Instructor by Name, Rank or Service No..." 
                value={query}
                onChange={(e) => setQuery(e.target.value)}
              />
            </div>
          </div>
        </div>
      </div>

      <div className="card slaf-card p-0 shadow-sm">
        <div className="table-responsive">
          <table className="table slaf-table align-middle mb-0">
            <thead>
              <tr>
                <th>Instructor Name</th>
                <th>Service No / Rank</th>
                <th>Department / Appointment</th>
                <th>Contact Details</th>
                <th>Assigned Batches</th>
                <th>User Portal Status</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr><td colSpan="6" className="text-center py-5"><div className="spinner-border text-primary"></div></td></tr>
              ) : filtered.length === 0 ? (
                <tr><td colSpan="6" className="text-center py-5 text-muted">No instructors found matching search criteria.</td></tr>
              ) : (
                filtered.map(i => (
                  <tr key={i.id}>
                    <td>
                      <strong className="text-dark d-block">{i.full_name}</strong>
                      <small className="text-muted">@{i.username}</small>
                    </td>
                    <td>
                      <span className="fw-semibold text-primary d-block">{i.service_number || 'N/A'}</span>
                      <span className="badge bg-secondary-subtle text-dark border px-2 py-0.5" style={{ fontSize: '0.725rem' }}>{i.rank || 'N/A'}</span>
                    </td>
                    <td>
                      <div className="fw-semibold text-dark" style={{ fontSize: '0.85rem' }}>{i.department || 'Training Section'}</div>
                      <small className="text-muted">{i.designation || 'Instructor'}</small>
                    </td>
                    <td>
                      <div className="small"><i className="bi bi-envelope me-1.5 text-muted"></i>{i.email || 'N/A'}</div>
                      <div className="small text-muted"><i className="bi bi-telephone me-1.5"></i>{i.mobile_number || 'N/A'}</div>
                    </td>
                    <td>
                      <span className="badge bg-primary-subtle text-primary border px-2.5 py-1 fw-bold">
                        {i.assigned_batches_count || 0} Batches Assigned
                      </span>
                    </td>
                    <td>
                      <span className="badge bg-success-subtle text-success border px-2 py-0.5">
                        <i className="bi bi-check-circle-fill me-1"></i>Active User
                      </span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
