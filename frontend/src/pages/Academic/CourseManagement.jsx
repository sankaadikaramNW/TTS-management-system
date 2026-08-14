import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { toast } from 'react-toastify'
import PersonalOccurrenceReporting from '../Students/PersonalOccurrenceReporting'


export const CourseManagement = () => {
  const [courses, setCourses] = useState([])
  const [trades, setTrades] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedTradeFilter, setSelectedTradeFilter] = useState('')
  const [query, setQuery] = useState('')

  const [showModal, setShowModal] = useState(false)
  const [editingCourse, setEditingCourse] = useState(null)

  // Enrolled Trainees List Modal state
  const [showStudentsModal, setShowStudentsModal] = useState(false)
  const [selectedCourseForStudents, setSelectedCourseForStudents] = useState(null)
  const [courseStudents, setCourseStudents] = useState([])
  const [loadingStudents, setLoadingStudents] = useState(false)
  const [studentSearchQuery, setStudentSearchQuery] = useState('')

  // Student Personal Profile Details Modal state
  const [showStudentDetailModal, setShowStudentDetailModal] = useState(false)
  const [selectedStudentDetail, setSelectedStudentDetail] = useState(null)
  const [loadingStudentDetail, setLoadingStudentDetail] = useState(false)
  
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
      if (selectedTradeFilter && selectedTradeFilter.trim()) {
        params.trade_id = selectedTradeFilter.trim()
      }
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

  const handleViewCourseStudents = async (course) => {
    setSelectedCourseForStudents(course)
    setShowStudentsModal(true)
    setLoadingStudents(true)
    setStudentSearchQuery('')
    try {
      const res = await axios.get('/api/v1/students', { params: { course_id: course.id, limit: 200 } })
      setCourseStudents(res.data.items || [])
    } catch (err) {
      console.error(err)
      toast.error('Failed to load trainees for this course')
    } finally {
      setLoadingStudents(false)
    }
  }

  const handleViewStudentDetail = async (studentId) => {
    setLoadingStudentDetail(true)
    setShowStudentDetailModal(true)
    try {
      const res = await axios.get(`/api/v1/students/${studentId}`)
      setSelectedStudentDetail(res.data)
    } catch (err) {
      console.error(err)
      toast.error('Failed to load student personal profile details')
    } finally {
      setLoadingStudentDetail(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!form.code.trim() || !form.name.trim()) {
      toast.error('Course Number and Course Name are required')
      return
    }

    const payload = {
      ...form,
      trade_id: form.trade_id ? form.trade_id : null,
      start_date: form.start_date ? form.start_date : null,
      end_date: form.end_date ? form.end_date : null,
      description: form.description ? form.description : null,
    }

    try {
      if (editingCourse) {
        await axios.put(`/api/v1/academic/courses/${editingCourse.id}`, payload)
        toast.success(`Course '${form.name}' updated successfully`)
      } else {
        await axios.post('/api/v1/academic/courses', payload)
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

  const filteredStudents = courseStudents.filter(s => 
    (s.full_name && s.full_name.toLowerCase().includes(studentSearchQuery.toLowerCase())) ||
    (s.service_number && s.service_number.toLowerCase().includes(studentSearchQuery.toLowerCase())) ||
    (s.rank && s.rank.toLowerCase().includes(studentSearchQuery.toLowerCase())) ||
    (s.batch && s.batch.toLowerCase().includes(studentSearchQuery.toLowerCase()))
  )

  const formatDate = (dateStr) => {
    if (!dateStr) return 'N/A'
    const parts = dateStr.split('-')
    if (parts.length === 3) return `${parts[2]}.${parts[1]}.${parts[0]}`
    return dateStr
  }

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
                    <td>
                      <button 
                        className="btn btn-link p-0 fw-bold text-decoration-none" 
                        onClick={() => handleViewCourseStudents(c)}
                        title="Click to view enrolled trainees list"
                      >
                        <span className="badge bg-primary-subtle text-primary border fw-bold">{c.code}</span>
                      </button>
                    </td>
                    <td>
                      <button 
                        className="btn btn-link p-0 text-start fw-bold text-decoration-none" 
                        onClick={() => handleViewCourseStudents(c)}
                        title="Click to view enrolled trainees list"
                      >
                        <strong className="text-primary text-decoration-underline">{c.name}</strong>
                      </button>
                    </td>
                    <td><span className="badge bg-secondary-subtle text-dark border">{c.trade_name || 'General'}</span></td>
                    <td><span className="badge bg-info-subtle text-info border">{c.course_type || 'Basic'}</span></td>
                    <td><small className="fw-semibold text-dark">{c.duration_weeks} Weeks</small></td>
                    <td><small className="text-muted">{c.intake_capacity} Trainees</small></td>
                    <td>
                      <button 
                        className="btn btn-link p-0 text-decoration-none" 
                        onClick={() => handleViewCourseStudents(c)}
                        title="Click to view enrolled trainees list"
                      >
                        <span className="badge bg-success-subtle text-success border">{c.batches_count || 0} Batches</span>
                      </button>
                    </td>
                    <td>
                      <span className={`badge bg-${c.is_active ? 'success' : 'danger'}-subtle text-${c.is_active ? 'success' : 'danger'} border px-2 py-0.5`}>
                        {c.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                    <td className="text-end">
                      <button className="btn btn-outline-primary btn-sm me-1" onClick={() => handleViewCourseStudents(c)} title="View Enrolled Trainees">
                        <i className="bi bi-people me-1"></i> Trainees
                      </button>
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

      {/* Enrolled Trainees List Modal */}
      {showStudentsModal && selectedCourseForStudents && (
        <div className="modal fade show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)', zIndex: 1050 }} tabIndex="-1">
          <div className="modal-dialog modal-xl modal-dialog-centered modal-dialog-scrollable">
            <div className="modal-content shadow-lg border-0">
              <div className="modal-header bg-primary text-white py-3">
                <div className="d-flex align-items-center gap-2">
                  <div className="bg-white text-primary rounded p-1.5 d-inline-flex align-items-center justify-content-center" style={{ width: '32px', height: '32px' }}>
                    <i className="bi bi-mortarboard-fill fs-6"></i>
                  </div>
                  <div>
                    <h5 className="modal-title fw-bold mb-0">Enrolled Trainees List</h5>
                    <small className="text-white-50">{selectedCourseForStudents.code} - {selectedCourseForStudents.name} ({selectedCourseForStudents.trade_name || 'General'})</small>
                  </div>
                </div>
                <button type="button" className="btn-close btn-close-white" onClick={() => setShowStudentsModal(false)}></button>
              </div>

              <div className="modal-body p-4">
                {/* Modal Toolbar */}
                <div className="row align-items-center g-3 mb-3">
                  <div className="col-md-6">
                    <div className="input-group input-group-sm">
                      <span className="input-group-text bg-light"><i className="bi bi-search text-muted"></i></span>
                      <input 
                        type="text" 
                        className="form-control" 
                        placeholder="Search by Service No, Rank, Name, or Batch..." 
                        value={studentSearchQuery}
                        onChange={(e) => setStudentSearchQuery(e.target.value)}
                      />
                    </div>
                  </div>
                  <div className="col-md-6 text-md-end">
                    <span className="badge bg-primary-subtle text-primary border px-3 py-2 fw-bold">
                      Total Enrolled Trainees: {filteredStudents.length}
                    </span>
                  </div>
                </div>

                {/* Trainees List Table */}
                <div className="table-responsive border rounded bg-white">
                  <table className="table slaf-table align-middle mb-0">
                    <thead>
                      <tr>
                        <th>#</th>
                        <th>Service No</th>
                        <th>Rank</th>
                        <th>Full Name</th>
                        <th>Trade</th>
                        <th>Batch</th>
                        <th>Status</th>
                        <th className="text-end">Action</th>
                      </tr>
                    </thead>
                    <tbody>
                      {loadingStudents ? (
                        <tr><td colSpan="8" className="text-center py-5"><div className="spinner-border text-primary me-2"></div> Loading trainees...</td></tr>
                      ) : filteredStudents.length === 0 ? (
                        <tr><td colSpan="8" className="text-center py-5 text-muted"><i className="bi bi-person-x fs-3 d-block mb-1"></i>No enrolled trainees found for this course.</td></tr>
                      ) : (
                        filteredStudents.map((s, idx) => (
                          <tr key={s.id || idx}>
                            <td><small className="text-muted">{idx + 1}</small></td>
                            <td>
                              <button 
                                className="btn btn-link p-0 fw-bold text-primary text-decoration-none"
                                onClick={() => handleViewStudentDetail(s.id)}
                              >
                                {s.service_number}
                              </button>
                            </td>
                            <td><span className="badge bg-secondary-subtle text-dark border">{s.rank || 'Trainee'}</span></td>
                            <td>
                              <button 
                                className="btn btn-link p-0 text-start fw-bold text-primary text-decoration-underline"
                                onClick={() => handleViewStudentDetail(s.id)}
                                title="Click to view full personal profile"
                              >
                                {s.full_name}
                              </button>
                            </td>
                            <td><small className="text-dark fw-semibold">{s.trade || 'Airframe'}</small></td>
                            <td><span className="badge bg-light text-dark border">{s.batch || 'N/A'}</span></td>
                            <td>
                              <span className={`badge bg-${s.status === 'Active' ? 'success' : 'secondary'}-subtle text-${s.status === 'Active' ? 'success' : 'secondary'} border px-2 py-0.5`}>
                                {s.status}
                              </span>
                            </td>
                            <td className="text-end">
                              <button 
                                className="btn btn-primary btn-sm fw-semibold shadow-sm"
                                onClick={() => handleViewStudentDetail(s.id)}
                              >
                                <i className="bi bi-person-badge me-1"></i> View Profile
                              </button>
                            </td>
                          </tr>
                        ))
                      )}
                    </tbody>
                  </table>
                </div>
              </div>

              <div className="modal-footer bg-light py-2">
                <button type="button" className="btn btn-secondary btn-sm fw-semibold" onClick={() => setShowStudentsModal(false)}>
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Student Personal Profile Details Modal */}
      {showStudentDetailModal && (
        <div className="modal fade show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.6)', zIndex: 1070 }} tabIndex="-1">
          <div className="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable">
            <div className="modal-content shadow-lg border-0">
              <div className="modal-header bg-dark text-white py-3">
                <div className="d-flex align-items-center gap-2">
                  <i className="bi bi-person-vcard-fill fs-5 text-warning"></i>
                  <h5 className="modal-title fw-bold">Trainee Personal & Academic Profile</h5>
                </div>
                <button type="button" className="btn-close btn-close-white" onClick={() => setShowStudentDetailModal(false)}></button>
              </div>

              <div className="modal-body p-4">
                {loadingStudentDetail || !selectedStudentDetail ? (
                  <div className="text-center py-5">
                    <div className="spinner-border text-primary me-2"></div>
                    <span className="fw-semibold text-secondary">Loading trainee personal details...</span>
                  </div>
                ) : (
                  <div>
                    {/* Header Profile Card */}
                    <div className="card border-0 bg-primary text-white p-3 mb-4 rounded-3 shadow-sm">
                      <div className="d-flex align-items-center gap-3">
                        <div className="bg-white rounded-circle p-2 text-primary d-flex align-items-center justify-content-center shadow-sm" style={{ width: '64px', height: '64px' }}>
                          {selectedStudentDetail.profile_photo_path ? (
                            <img src={selectedStudentDetail.profile_photo_path} alt="Profile" className="rounded-circle w-100 h-100 object-fit-cover" />
                          ) : (
                            <i className="bi bi-person-fill display-6"></i>
                          )}
                        </div>
                        <div className="flex-grow-1">
                          <div className="d-flex align-items-center gap-2">
                            <span className="badge bg-warning text-dark fw-bold px-2 py-0.5">{selectedStudentDetail.service_number}</span>
                            <span className="badge bg-white text-primary fw-bold px-2 py-0.5">{selectedStudentDetail.rank}</span>
                          </div>
                          <h4 className="fw-extrabold display-font mb-0 mt-1">{selectedStudentDetail.full_name}</h4>
                          <small className="text-white-50">{selectedStudentDetail.trade} Trade | Batch {selectedStudentDetail.batch}</small>
                        </div>
                        <div>
                          <span className={`badge bg-${selectedStudentDetail.status === 'Active' ? 'success' : 'warning'} text-white px-3 py-1.5 fw-bold fs-6 shadow-sm`}>
                            {selectedStudentDetail.status}
                          </span>
                        </div>
                      </div>
                    </div>

                    {/* Information Sections */}
                    <div className="row g-3">
                      {/* Personal & Identification */}
                      <div className="col-md-6">
                        <div className="p-3 bg-light rounded border h-100">
                          <h6 className="fw-bold text-dark border-bottom pb-2 mb-3">
                            <i className="bi bi-person-lines-fill me-2 text-primary"></i>Personal & Identification
                          </h6>
                          <div className="row g-2 small">
                            <div className="col-6">
                              <span className="text-muted d-block">NIC Number:</span>
                              <strong className="text-dark">{selectedStudentDetail.nic || 'N/A'}</strong>
                            </div>
                            <div className="col-6">
                              <span className="text-muted d-block">Date of Birth:</span>
                              <strong className="text-dark">{formatDate(selectedStudentDetail.dob)}</strong>
                            </div>
                            <div className="col-6">
                              <span className="text-muted d-block">Gender:</span>
                              <strong className="text-dark">{selectedStudentDetail.gender || 'Male'}</strong>
                            </div>
                            <div className="col-6">
                              <span className="text-muted d-block">Religion:</span>
                              <strong className="text-dark">{selectedStudentDetail.religion || 'Buddhist'}</strong>
                            </div>
                            <div className="col-6">
                              <span className="text-muted d-block">Blood Group:</span>
                              <span className="badge bg-danger-subtle text-danger border fw-bold">{selectedStudentDetail.blood_group || 'O+'}</span>
                            </div>
                            <div className="col-6">
                              <span className="text-muted d-block">Medical Category:</span>
                              <span className="badge bg-info-subtle text-info border fw-bold">{selectedStudentDetail.medical_category || 'A4G4'}</span>
                            </div>
                          </div>
                        </div>
                      </div>

                      {/* Military & Academic Details */}
                      <div className="col-md-6">
                        <div className="p-3 bg-light rounded border h-100">
                          <h6 className="fw-bold text-dark border-bottom pb-2 mb-3">
                            <i className="bi bi-shield-lock me-2 text-primary"></i>Military & Academic Deployment
                          </h6>
                          <div className="row g-2 small">
                            <div className="col-6">
                              <span className="text-muted d-block">Rank:</span>
                              <strong className="text-dark">{selectedStudentDetail.rank}</strong>
                            </div>
                            <div className="col-6">
                              <span className="text-muted d-block">Trade:</span>
                              <strong className="text-dark">{selectedStudentDetail.trade}</strong>
                            </div>
                            <div className="col-12">
                              <span className="text-muted d-block">Assigned Course:</span>
                              <strong className="text-primary">{selectedStudentDetail.course_name || selectedCourseForStudents?.name || 'N/A'}</strong>
                            </div>
                            <div className="col-6">
                              <span className="text-muted d-block">Squadron:</span>
                              <strong className="text-dark">{selectedStudentDetail.squadron || 'Training Squadron'}</strong>
                            </div>
                            <div className="col-6">
                              <span className="text-muted d-block">Station / Unit:</span>
                              <strong className="text-dark">{selectedStudentDetail.unit || 'SLAF TTS Ekala'}</strong>
                            </div>
                            <div className="col-6">
                              <span className="text-muted d-block">Joining Date:</span>
                              <strong className="text-dark">{formatDate(selectedStudentDetail.joining_date)}</strong>
                            </div>
                            <div className="col-6">
                              <span className="text-muted d-block">Passing Out Date:</span>
                              <strong className="text-dark">{formatDate(selectedStudentDetail.passing_out_date)}</strong>
                            </div>
                          </div>
                        </div>
                      </div>

                      {/* Contact & Address Information */}
                      <div className="col-12">
                        <div className="p-3 bg-light rounded border">
                          <h6 className="fw-bold text-dark border-bottom pb-2 mb-3">
                            <i className="bi bi-telephone-outbound me-2 text-primary"></i>Contact Information & Address
                          </h6>
                          <div className="row g-3 small">
                            <div className="col-md-6">
                              <span className="text-muted d-block">Mobile Number:</span>
                              <strong className="text-dark">{selectedStudentDetail.phone || 'N/A'}</strong>
                            </div>
                            <div className="col-md-6">
                              <span className="text-muted d-block">Email Address:</span>
                              <strong className="text-dark">{selectedStudentDetail.email || 'N/A'}</strong>
                            </div>
                            <div className="col-md-6">
                              <span className="text-muted d-block">Permanent Address:</span>
                              <span className="text-dark">{selectedStudentDetail.permanent_address || 'N/A'}</span>
                            </div>
                            <div className="col-md-6">
                              <span className="text-muted d-block">Temporary / Present Address:</span>
                              <span className="text-dark">{selectedStudentDetail.temporary_address || 'N/A'}</span>
                            </div>
                          </div>
                        </div>
                      </div>

                      {/* Emergency Contact */}
                      <div className="col-12">
                        <div className="p-3 bg-warning-subtle rounded border border-warning">
                          <h6 className="fw-bold text-dark mb-2">
                            <i className="bi bi-exclamation-octagon me-2 text-warning"></i>Emergency Contact Person
                          </h6>
                          <div className="row g-2 small">
                            <div className="col-md-6">
                              <span className="text-muted d-block">Contact Name:</span>
                              <strong className="text-dark">{selectedStudentDetail.emergency_contact_name || 'N/A'}</strong>
                            </div>
                            <div className="col-md-6">
                              <span className="text-muted d-block">Emergency Phone Number:</span>
                              <strong className="text-dark">{selectedStudentDetail.emergency_contact_phone || 'N/A'}</strong>
                            </div>
                          </div>
                        </div>
                      </div>

                      {/* Personal Occurrence Reporting Section */}
                      <div className="col-12 mt-3">
                        <PersonalOccurrenceReporting initialTraineeId={selectedStudentDetail.id} />
                      </div>
                    </div>
                  </div>
                )}

              </div>

              <div className="modal-footer bg-light py-2">
                <button type="button" className="btn btn-outline-secondary btn-sm fw-semibold" onClick={() => setShowStudentDetailModal(false)}>
                  <i className="bi bi-arrow-left me-1"></i> Back to Trainees List
                </button>
                <button type="button" className="btn btn-secondary btn-sm fw-semibold" onClick={() => setShowStudentDetailModal(false)}>
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Edit / Create Course Modal */}
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
                      <label className="form-label fw-semibold small text-muted">Course Type</label>
                      <select 
                        className="form-select"
                        value={form.course_type}
                        onChange={(e) => setForm({ ...form, course_type: e.target.value })}
                      >
                        <option value="Basic">Basic Training</option>
                        <option value="Advance">Advance Training</option>
                        <option value="Special">Specialized Training</option>
                        <option value="Refresher">Refresher Course</option>
                      </select>
                    </div>

                    <div className="col-md-4">
                      <label className="form-label fw-semibold small text-muted">Course Number / Code*</label>
                      <input 
                        type="text" 
                        className="form-control" 
                        value={form.code}
                        onChange={(e) => setForm({ ...form, code: e.target.value.toUpperCase() })}
                        placeholder="e.g. 26/1 or CRS-AV-01"
                        required
                      />
                    </div>

                    <div className="col-md-8">
                      <label className="form-label fw-semibold small text-muted">Course Title / Name*</label>
                      <input 
                        type="text" 
                        className="form-control" 
                        value={form.name}
                        onChange={(e) => setForm({ ...form, name: e.target.value })}
                        placeholder="e.g. Computer Technician Advance Course"
                        required
                      />
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

export default CourseManagement
