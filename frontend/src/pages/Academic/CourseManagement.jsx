import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { toast } from 'react-toastify'

export const CourseManagement = () => {
  const [courses, setCourses] = useState([])
  const [trades, setTrades] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedTradeFilter, setSelectedTradeFilter] = useState('')
  const [query, setQuery] = useState('')

  const [showModal, setShowModal] = useState(false)
  const [editingCourse, setEditingCourse] = useState(null)
  
  const [form, setForm] = useState({
    code: '',
    name: '',
    trade_id: '',
    course_type: 'Basic',
    duration_weeks: 24,
    intake_capacity: 30,
    start_date: '',
    end_date: '',
    description: '',
    is_active: true
  })

  const fetchTrades = async () => {
    try {
      const res = await axios.get('/api/v1/academic/trades')
      setTrades(res.data)
    } catch (err) {
      console.error(err)
    }
  }

  const fetchCourses = async () => {
    setLoading(true)
    try {
      const params = {}
      if (selectedTradeFilter) params.trade_id = selectedTradeFilter
      const res = await axios.get('/api/v1/academic/courses', { params })
      setCourses(res.data)
    } catch (err) {
      toast.error('Failed to load courses')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchTrades()
  }, [])

  useEffect(() => {
    fetchCourses()
  }, [selectedTradeFilter])

  const handleOpenCreate = () => {
    setEditingCourse(null)
    setForm({
      code: '',
      name: '',
      trade_id: trades.length > 0 ? trades[0].id : '',
      course_type: 'Basic',
      duration_weeks: 24,
      intake_capacity: 30,
      start_date: '',
      end_date: '',
      description: '',
      is_active: true
    })
    setShowModal(true)
  }

  const handleOpenEdit = (c) => {
    setEditingCourse(c)
    setForm({
      code: c.code,
      name: c.name,
      trade_id: c.trade_id || '',
      course_type: c.course_type || 'Basic',
      duration_weeks: c.duration_weeks || 24,
      intake_capacity: c.intake_capacity || 30,
      start_date: c.start_date || '',
      end_date: c.end_date || '',
      description: c.description || '',
      is_active: c.is_active
    })
    setShowModal(true)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!form.code.trim() || !form.name.trim()) {
      toast.error('Course Number and Course Name are required')
      return
    }

    try {
      if (editingCourse) {
        await axios.put(`/api/v1/academic/courses/${editingCourse.id}`, form)
        toast.success(`Course '${form.name}' updated successfully`)
      } else {
        await axios.post('/api/v1/academic/courses', form)
        toast.success(`Course '${form.name}' created successfully`)
      }
      setShowModal(false)
      fetchCourses()
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to save course')
    }
  }

  const filteredCourses = courses.filter(c => 
    c.code.toLowerCase().includes(query.toLowerCase()) ||
    c.name.toLowerCase().includes(query.toLowerCase())
  )

  return (
    <div className="fade-in-slide">
      <div className="d-flex justify-content-between align-items-center mb-3">
        <div>
          <h5 className="fw-bold text-dark mb-0 display-font">Course Management Master Data</h5>
          <small className="text-muted">Manage training courses linked to Trades (Basic, Advance, Special)</small>
        </div>
        <button className="btn btn-primary btn-sm fw-semibold" onClick={handleOpenCreate}>
          <i className="bi bi-plus-lg me-1"></i> Add New Course
        </button>
      </div>

      {/* Filters */}
      <div className="card slaf-card p-3 mb-3 shadow-sm">
        <div className="row g-2">
          <div className="col-md-4">
            <select 
              className="form-select form-select-sm"
              value={selectedTradeFilter}
              onChange={(e) => setSelectedTradeFilter(e.target.value)}
            >
              <option value="">All Trades Filter</option>
              {trades.map(t => (
                <option key={t.id} value={t.id}>{t.label} ({t.code})</option>
              ))}
            </select>
          </div>
          <div className="col-md-5">
            <div className="input-group input-group-sm">
              <span className="input-group-text bg-light"><i className="bi bi-search text-muted"></i></span>
              <input 
                type="text" 
                className="form-control" 
                placeholder="Search Course Number or Name..." 
                value={query}
                onChange={(e) => setQuery(e.target.value)}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Course Table */}
      <div className="card slaf-card p-0 shadow-sm">
        <div className="table-responsive">
          <table className="table slaf-table align-middle mb-0">
            <thead>
              <tr>
                <th>Course No</th>
                <th>Course Name</th>
                <th>Trade</th>
                <th>Type</th>
                <th>Duration</th>
                <th>Capacity</th>
                <th>Batches</th>
                <th>Status</th>
                <th className="text-end">Actions</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr><td colSpan="9" className="text-center py-5"><div className="spinner-border text-primary"></div></td></tr>
              ) : filteredCourses.length === 0 ? (
                <tr><td colSpan="9" className="text-center py-5 text-muted">No course records found.</td></tr>
              ) : (
                filteredCourses.map(c => (
                  <tr key={c.id}>
                    <td><span className="badge bg-primary-subtle text-primary border fw-bold">{c.code}</span></td>
                    <td><strong className="text-dark">{c.name}</strong></td>
                    <td><span className="badge bg-secondary-subtle text-dark border">{c.trade_name || 'General'}</span></td>
                    <td><span className="badge bg-info-subtle text-info border">{c.course_type || 'Basic'}</span></td>
                    <td><small className="fw-semibold text-dark">{c.duration_weeks} Weeks</small></td>
                    <td><small className="text-muted">{c.intake_capacity} Trainees</small></td>
                    <td><span className="badge bg-success-subtle text-success border">{c.batches_count || 0} Batches</span></td>
                    <td>
                      <span className={`badge bg-${c.is_active ? 'success' : 'danger'}-subtle text-${c.is_active ? 'success' : 'danger'} border px-2 py-0.5`}>
                        {c.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                    <td className="text-end">
                      <button className="btn btn-outline-secondary btn-sm" onClick={() => handleOpenEdit(c)}>
                        <i className="bi bi-pencil me-1"></i> Edit
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Modal */}
      {showModal && (
        <div className="modal fade show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)', zIndex: 1060 }}>
          <div className="modal-dialog modal-lg modal-dialog-centered">
            <div className="modal-content slaf-card">
              <div className="modal-header border-bottom">
                <h5 className="modal-title display-font text-primary fw-bold">
                  {editingCourse ? `Edit Course: ${editingCourse.code}` : 'Create New Training Course'}
                </h5>
                <button type="button" className="btn-close" onClick={() => setShowModal(false)}></button>
              </div>
              <form onSubmit={handleSubmit}>
                <div className="modal-body">
                  <div className="row g-3">
                    <div className="col-md-6">
                      <label className="form-label fw-semibold small text-muted">Select Trade Category*</label>
                      <select 
                        className="form-select"
                        value={form.trade_id}
                        onChange={(e) => setForm({ ...form, trade_id: e.target.value })}
                        required
                      >
                        <option value="">-- Select Trade --</option>
                        {trades.map(t => (
                          <option key={t.id} value={t.id}>{t.label} ({t.code})</option>
                        ))}
                      </select>
                    </div>

                    <div className="col-md-6">
                      <label className="form-label fw-semibold small text-muted">Course Number / Code (Unique)*</label>
                      <input 
                        type="text" 
                        className="form-control" 
                        placeholder="e.g. 26/1, 174-A, 175-C" 
                        value={form.code}
                        onChange={(e) => setForm({ ...form, code: e.target.value })}
                        required
                      />
                    </div>

                    <div className="col-md-8">
                      <label className="form-label fw-semibold small text-muted">Course Full Name*</label>
                      <input 
                        type="text" 
                        className="form-control" 
                        placeholder="e.g. Computer Technician 26/1 Advance Course" 
                        value={form.name}
                        onChange={(e) => setForm({ ...form, name: e.target.value })}
                        required
                      />
                    </div>

                    <div className="col-md-4">
                      <label className="form-label fw-semibold small text-muted">Course Type</label>
                      <select 
                        className="form-select"
                        value={form.course_type}
                        onChange={(e) => setForm({ ...form, course_type: e.target.value })}
                      >
                        <option value="Basic">Basic Course</option>
                        <option value="Advance">Advance Course</option>
                        <option value="Special">Specialized Training</option>
                      </select>
                    </div>

                    <div className="col-md-4">
                      <label className="form-label fw-semibold small text-muted">Duration (Weeks)</label>
                      <input 
                        type="number" 
                        className="form-control" 
                        value={form.duration_weeks}
                        onChange={(e) => setForm({ ...form, duration_weeks: parseInt(e.target.value) || 0 })}
                        min="1"
                      />
                    </div>

                    <div className="col-md-4">
                      <label className="form-label fw-semibold small text-muted">Intake Capacity</label>
                      <input 
                        type="number" 
                        className="form-control" 
                        value={form.intake_capacity}
                        onChange={(e) => setForm({ ...form, intake_capacity: parseInt(e.target.value) || 0 })}
                        min="1"
                      />
                    </div>

                    <div className="col-md-4">
                      <label className="form-label fw-semibold small text-muted">Status</label>
                      <div className="form-check form-switch mt-2">
                        <input 
                          className="form-check-input" 
                          type="checkbox" 
                          id="cActive"
                          checked={form.is_active}
                          onChange={(e) => setForm({ ...form, is_active: e.target.checked })}
                        />
                        <label className="form-check-label fw-semibold small text-dark" htmlFor="cActive">Active Course</label>
                      </div>
                    </div>

                    <div className="col-md-12">
                      <label className="form-label fw-semibold small text-muted">Course Syllabus / Description</label>
                      <textarea 
                        className="form-control" 
                        rows="2"
                        value={form.description}
                        onChange={(e) => setForm({ ...form, description: e.target.value })}
                      ></textarea>
                    </div>
                  </div>
                </div>
                <div className="modal-footer border-top">
                  <button type="button" className="btn btn-outline-secondary btn-sm" onClick={() => setShowModal(false)}>Cancel</button>
                  <button type="submit" className="btn btn-primary btn-sm fw-semibold">Save Course</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
