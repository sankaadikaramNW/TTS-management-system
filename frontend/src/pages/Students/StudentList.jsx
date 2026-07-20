import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'
import { toast } from 'react-toastify'
import { useAuth } from '../../context/AuthContext'

export const StudentList = () => {
  const { hasPermission } = useAuth()
  const [students, setStudents] = useState([])
  const [total, setTotal] = useState(0)
  const [search, setSearch] = useState('')
  const [rank, setRank] = useState('')
  const [trade, setTrade] = useState('')
  const [status, setStatus] = useState('')
  const [skip, setSkip] = useState(0)
  const [limit] = useState(10)
  const [loading, setLoading] = useState(true)

  const fetchStudents = async () => {
    setLoading(true)
    try {
      const res = await axios.get('/api/v1/students', {
        params: { search, rank, trade, status, skip, limit }
      })
      setStudents(res.data.items)
      setTotal(res.data.total)
    } catch (err) {
      toast.error('Failed to load students')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchStudents()
  }, [search, rank, trade, status, skip])

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to soft-delete this student record?')) return
    try {
      await axios.delete(`/api/v1/students/${id}`)
      toast.success('Student record deleted successfully')
      fetchStudents()
    } catch (err) {
      toast.error('Failed to delete student')
    }
  }

  // Export search results to CSV
  const exportToCSV = () => {
    if (students.length === 0) return
    const headers = ['Service Number', 'Rank', 'Initials', 'Full Name', 'NIC', 'Trade', 'Status']
    const rows = students.map(s => [
      s.service_number,
      s.rank,
      s.initials,
      s.full_name,
      s.nic,
      s.trade,
      s.status
    ])

    const csvContent = "data:text/csv;charset=utf-8," 
      + [headers.join(','), ...rows.map(e => e.map(val => `"${val}"`).join(","))].join("\n")
    
    const encodedUri = encodeURI(csvContent)
    const link = document.createElement("a")
    link.setAttribute("href", encodedUri)
    link.setAttribute("download", `slaf_trainees_export.csv`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  return (
    <div className="fade-in-slide">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 className="mb-0 text-primary display-font">Student Registry</h2>
          <p className="text-muted mb-0">Master database (Single Source of Truth) for all school trainees</p>
        </div>
        <div className="d-flex gap-2">
          <button className="btn btn-outline-secondary d-flex align-items-center gap-2" onClick={exportToCSV}>
            <i className="bi bi-file-earmark-spreadsheet"></i> Export CSV
          </button>
          {hasPermission('student:write') && (
            <Link to="/students/new" className="btn btn-primary d-flex align-items-center gap-2">
              <i className="bi bi-plus-circle"></i> Add Trainee
            </Link>
          )}
        </div>
      </div>

      {/* Filter and Search Card */}
      <div className="card slaf-card p-3 mb-4">
        <div className="row g-2">
          <div className="col-md-4">
            <input 
              type="text" 
              className="form-control" 
              placeholder="Search by Service No, Name, NIC..." 
              value={search}
              onChange={(e) => { setSearch(e.target.value); setSkip(0); }}
            />
          </div>
          <div className="col-md-2">
            <select className="form-select" value={rank} onChange={(e) => { setRank(e.target.value); setSkip(0); }}>
              <option value="">All Ranks</option>
              <option value="Aircraftman">Aircraftman (AC)</option>
              <option value="Leading Aircraftman">Leading Aircraftman (LAC)</option>
              <option value="Corporal">Corporal (Cpl)</option>
              <option value="Sergeant">Sergeant (Sgt)</option>
            </select>
          </div>
          <div className="col-md-3">
            <select className="form-select" value={trade} onChange={(e) => { setTrade(e.target.value); setSkip(0); }}>
              <option value="">All Trades</option>
              <option value="Airframe">Airframe Fitters</option>
              <option value="Avionics">Avionics Fitters</option>
              <option value="Safety Equipment">Safety Equipment Fitters</option>
            </select>
          </div>
          <div className="col-md-3">
            <select className="form-select" value={status} onChange={(e) => { setStatus(e.target.value); setSkip(0); }}>
              <option value="">All Statuses</option>
              <option value="Active">Active</option>
              <option value="Sick Report">Sick Report</option>
              <option value="Leave">Leave</option>
              <option value="AWOL">AWOL</option>
              <option value="Passed Out">Passed Out</option>
            </select>
          </div>
        </div>
      </div>

      {/* Trainees Grid/Table */}
      {loading ? (
        <div className="text-center py-5">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading trainees...</span>
          </div>
        </div>
      ) : (
        <div className="card slaf-card p-0 mb-4">
          <div className="table-responsive">
            <table className="table slaf-table mb-0">
              <thead>
                <tr>
                  <th>Service Number</th>
                  <th>Rank & Name</th>
                  <th>NIC</th>
                  <th>Trade</th>
                  <th>Course Status</th>
                  <th>Status</th>
                  <th className="text-end">Actions</th>
                </tr>
              </thead>
              <tbody>
                {students.length === 0 ? (
                  <tr>
                    <td colSpan="7" className="text-center py-5 text-muted">No student profiles found matching filters.</td>
                  </tr>
                ) : (
                  students.map((s) => (
                    <tr key={s.id}>
                      <td className="fw-semibold text-primary">{s.service_number}</td>
                      <td>
                        <div className="d-flex align-items-center gap-2">
                          <div className="d-inline-flex bg-secondary-subtle text-secondary rounded-circle align-items-center justify-content-center" style={{ width: '32px', height: '32px' }}>
                            <i className="bi bi-person-fill"></i>
                          </div>
                          <div>
                            <span className="fw-semibold d-block">{s.rank} {s.initials}</span>
                            <small className="text-muted">{s.full_name}</small>
                          </div>
                        </div>
                      </td>
                      <td>{s.nic}</td>
                      <td>{s.trade}</td>
                      <td>{s.course_name || 'Unassigned'}</td>
                      <td>
                        <span className={`slaf-badge ${s.status.toLowerCase().replace(' ', '-')}`}>
                          {s.status}
                        </span>
                      </td>
                      <td className="text-end">
                        <div className="d-inline-flex gap-1">
                          <Link to={`/students/${s.id}`} className="btn btn-outline-primary btn-sm px-2.5" title="View Profile">
                            <i className="bi bi-eye"></i>
                          </Link>
                          {hasPermission('student:write') && (
                            <>
                              <Link to={`/students/${s.id}/edit`} className="btn btn-outline-secondary btn-sm px-2.5" title="Edit Profile">
                                <i className="bi bi-pencil"></i>
                              </Link>
                              <button className="btn btn-outline-danger btn-sm px-2.5" onClick={() => handleDelete(s.id)} title="Delete Profile">
                                <i className="bi bi-trash"></i>
                              </button>
                            </>
                          )}
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Pagination controls */}
      {total > limit && (
        <div className="d-flex justify-content-between align-items-center mt-3">
          <span className="text-muted" style={{ fontSize: '0.85rem' }}>
            Showing {skip + 1} - {Math.min(skip + limit, total)} of {total} trainees
          </span>
          <div className="d-flex gap-2">
            <button 
              className="btn btn-outline-primary btn-sm px-3" 
              onClick={() => setSkip(prev => Math.max(0, prev - limit))}
              disabled={skip === 0}
            >
              Previous
            </button>
            <button 
              className="btn btn-outline-primary btn-sm px-3" 
              onClick={() => setSkip(prev => prev + limit)}
              disabled={skip + limit >= total}
            >
              Next
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
export default StudentList
