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
  const [statuses, setStatuses] = useState([])
  const [ranks, setRanks] = useState([])
  const [trades, setTrades] = useState([])
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

  useEffect(() => {
    const loadStatuses = async () => {
      try {
        const res = await axios.get('/api/v1/students/statuses')
        if (res.data && res.data.length > 0) {
          setStatuses(res.data)
        }
      } catch (err) {
        console.error('Failed to load student status types from DB', err)
      }
    }
    loadStatuses()

    const loadRanks = async () => {
      try {
        const res = await axios.get('/api/v1/students/ranks')
        if (res.data && res.data.length > 0) {
          setRanks(res.data)
        }
      } catch (err) {
        console.error('Failed to load student ranks from DB', err)
      }
    }
    loadRanks()

    const loadTrades = async () => {
      try {
        const res = await axios.get('/api/v1/students/trades')
        if (res.data && res.data.length > 0) {
          setTrades(res.data)
        }
      } catch (err) {
        console.error('Failed to load student trades from DB', err)
      }
    }
    loadTrades()
  }, [])

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
      <div className="d-flex flex-column flex-sm-row justify-content-between align-items-start align-items-sm-center gap-3 mb-4">
        <div>
          <h2 className="mb-0 text-primary display-font fs-3">Student Registry</h2>
          <p className="text-muted mb-0 small">Master database (Single Source of Truth) for all school trainees</p>
        </div>
        <div className="d-flex gap-2 flex-wrap">
          <button className="btn btn-outline-secondary btn-sm d-flex align-items-center gap-1.5" onClick={exportToCSV}>
            <i className="bi bi-file-earmark-spreadsheet"></i> Export CSV
          </button>
          {hasPermission('personal_occurrence:read') && (
            <Link to="/students/occurrences" className="btn btn-outline-danger btn-sm d-flex align-items-center gap-1.5 fw-bold">
              <i className="bi bi-shield-exclamation"></i> Personal Occurrences
            </Link>
          )}
          {hasPermission('student:write') && (
            <Link to="/students/new" className="btn btn-primary btn-sm d-flex align-items-center gap-1.5">
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
              {ranks.map(r => (
                <option key={r.id} value={r.label}>
                  {r.label}
                </option>
              ))}
            </select>
          </div>
          <div className="col-md-3">
            <select className="form-select" value={trade} onChange={(e) => { setTrade(e.target.value); setSkip(0); }}>
              <option value="">All Trades</option>
              {trades.map(t => (
                <option key={t.id} value={t.label}>
                  {t.label}
                </option>
              ))}
            </select>
          </div>
          <div className="col-md-3">
            <select className="form-select" value={status} onChange={(e) => { setStatus(e.target.value); setSkip(0); }}>
              <option value="">All Statuses</option>
              {statuses.map(st => (
                <option key={st.id || st.code} value={st.label}>
                  {st.label}
                </option>
              ))}
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
                        <div className="d-flex align-items-center gap-2.5">
                          <div className="d-inline-flex bg-primary-subtle text-primary rounded-circle align-items-center justify-content-center flex-shrink-0" style={{ width: '36px', height: '36px' }}>
                            <i className="bi bi-person-fill fs-6"></i>
                          </div>
                          <div>
                            <span className="fw-bold text-dark d-block text-capitalize" style={{ fontSize: '0.925rem', lineHeight: '1.25' }}>
                              {s.full_name || s.initials}
                            </span>
                            <div className="d-flex align-items-center gap-1.5 mt-1">
                              <span className="badge bg-secondary-subtle text-dark border border-secondary-subtle px-2 py-0.5 fw-semibold" style={{ fontSize: '0.725rem' }}>
                                {s.rank}
                              </span>
                              {s.initials && (
                                <span className="text-muted fw-medium" style={{ fontSize: '0.775rem' }}>
                                  • {s.initials}
                                </span>
                              )}
                            </div>
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
                          {hasPermission('personal_occurrence:read') && (
                            <Link to={`/students/occurrences?trainee_id=${s.id}`} className="btn btn-outline-danger btn-sm px-2.5" title="Personal Occurrence Reporting">
                              <i className="bi bi-shield-exclamation"></i>
                            </Link>
                          )}
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
