import React, { useEffect, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import axios from 'axios'
import { toast } from 'react-toastify'
import { useAuth } from '../../context/AuthContext'

export const CourseList = () => {
  const { hasPermission } = useAuth()
  const [courses, setCourses] = useState([])
  const [selectedCourse, setSelectedCourse] = useState(null)
  
  // Syllabus & lessons states
  const [subjects, setSubjects] = useState([])
  const [lessons, setLessons] = useState([])
  
  // Timetables and Exams states
  const [timetables, setTimetables] = useState([])
  const [exams, setExams] = useState([])
  const [examMarks, setExamMarks] = useState([])
  const [selectedExam, setSelectedExam] = useState(null)
  
  // Active Tab
  const [activeTab, setActiveTab] = useState('syllabus')
  const [loading, setLoading] = useState(true)

  // Creation form states
  const [newCourseCode, setNewCourseCode] = useState('')
  const [newCourseName, setNewCourseName] = useState('')
  const [newCourseDuration, setNewCourseDuration] = useState(24)

  const [newExamType, setNewExamType] = useState('Phase Test')
  const [newExamSubjectId, setNewExamSubjectId] = useState('')
  const [newExamDate, setNewExamDate] = useState('')
  
  const [selectedTimetableSlot, setSelectedTimetableSlot] = useState(null)
  const [students, setStudents] = useState([])
  const [attendanceRecords, setAttendanceRecords] = useState([])

  // Trade & Rank Management and Statistics states
  const [searchParams, setSearchParams] = useSearchParams()
  const showTradeManagement = searchParams.get('view') === 'trades'
  const showRankManagement = searchParams.get('view') === 'ranks'
  
  const [allTrades, setAllTrades] = useState([])
  const [editingTrade, setEditingTrade] = useState(null)
  const [tradeForm, setTradeForm] = useState({ code: '', label: '', is_active: true })

  const [allRanks, setAllRanks] = useState([])
  const [editingRank, setEditingRank] = useState(null)
  const [rankForm, setRankForm] = useState({ code: '', label: '', is_active: true })

  const [academicStats, setAcademicStats] = useState({
    course_count: 0,
    active_students: 0,
    average_pass_rate: 0,
    active_timetables_today: 0
  })

  const fetchAllTrades = async () => {
    try {
      const res = await axios.get('/api/v1/students/trades', {
        params: { include_inactive: true }
      })
      setAllTrades(res.data)
    } catch (err) {
      console.error('Failed to fetch trades', err)
      toast.error('Failed to load trades list')
    }
  }

  const fetchAllRanks = async () => {
    try {
      const res = await axios.get('/api/v1/students/ranks', {
        params: { include_inactive: true }
      })
      setAllRanks(res.data)
    } catch (err) {
      console.error('Failed to fetch ranks', err)
      toast.error('Failed to load ranks list')
    }
  }

  useEffect(() => {
    if (showTradeManagement) {
      fetchAllTrades()
    }
  }, [showTradeManagement])

  useEffect(() => {
    if (showRankManagement) {
      fetchAllRanks()
    }
  }, [showRankManagement])

  const fetchCourses = async () => {
    setLoading(true)
    try {
      const res = await axios.get('/api/v1/academic/courses')
      setCourses(res.data)
    } catch (err) {
      toast.error('Failed to load courses')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchCourses()

    // Fetch overview statistics for the landing view
    const fetchAcademicStats = async () => {
      try {
        const res = await axios.get('/api/v1/dashboard/summary')
        const studentsRes = await axios.get('/api/v1/students', { params: { limit: 1 } })
        setAcademicStats({
          course_count: res.data.academic.course_count,
          active_students: studentsRes.data.total,
          average_pass_rate: res.data.academic.average_pass_rate,
          active_timetables_today: res.data.academic.active_timetables_today
        })
      } catch (err) {
        console.error('Failed to load statistics', err)
      }
    }
    fetchAcademicStats()
  }, [])

  // Sync details when course or tab changes
  useEffect(() => {
    if (!selectedCourse) return

    const loadCourseDetails = async () => {
      try {
        if (activeTab === 'syllabus') {
          const subRes = await axios.get(`/api/v1/academic/subjects/${selectedCourse.id}`)
          setSubjects(subRes.data)
          if (subRes.data.length > 0) {
            const lesRes = await axios.get(`/api/v1/academic/lessons/${subRes.data[0].id}`)
            setLessons(lesRes.data)
          } else {
            setLessons([])
          }
        } else if (activeTab === 'timetable') {
          const ttRes = await axios.get('/api/v1/academic/timetables', {
            params: { course_id: selectedCourse.id, timetable_date: new Date().toISOString().substring(0, 10) }
          })
          setTimetables(ttRes.data)
        } else if (activeTab === 'marks') {
          const exRes = await axios.get(`/api/v1/academic/exams/${selectedCourse.id}`)
          setExams(exRes.data)
          if (exRes.data.length > 0) {
            setSelectedExam(exRes.data[0])
          } else {
            setSelectedExam(null)
          }
        } else if (activeTab === 'trainees') {
          const stRes = await axios.get('/api/v1/students', {
            params: { course_id: selectedCourse.id, limit: 100 }
          })
          setStudents(stRes.data.items)
        }
      } catch (err) {
        console.error(err)
      }
    }
    loadCourseDetails()
  }, [selectedCourse, activeTab])

  // Sync exam marks when exam selection updates
  useEffect(() => {
    if (!selectedExam) {
      setExamMarks([])
      return
    }
    const loadMarks = async () => {
      try {
        const res = await axios.get(`/api/v1/academic/exam-marks/${selectedExam.id}`)
        setExamMarks(res.data)
      } catch (err) {
        console.error(err)
      }
    }
    loadMarks()
  }, [selectedExam])

  const handleAddCourse = async (e) => {
    e.preventDefault()
    try {
      await axios.post('/api/v1/academic/courses', {
        code: newCourseCode,
        name: newCourseName,
        duration_weeks: newCourseDuration
      })
      toast.success('Course created successfully')
      setNewCourseCode('')
      setNewCourseName('')
      fetchCourses()
    } catch (err) {
      toast.error('Failed to create course')
    }
  }

  const handleSaveTrade = async (e) => {
    e.preventDefault()
    try {
      if (editingTrade) {
        await axios.put(`/api/v1/students/trades/${editingTrade.id}`, {
          code: tradeForm.code,
          label: tradeForm.label,
          is_active: tradeForm.is_active
        })
        toast.success('Trade updated successfully')
      } else {
        await axios.post('/api/v1/students/trades', {
          code: tradeForm.code,
          label: tradeForm.label,
          is_active: tradeForm.is_active
        })
        toast.success('Trade created successfully')
      }
      setEditingTrade(null)
      setTradeForm({ code: '', label: '', is_active: true })
      fetchAllTrades()
    } catch (err) {
      console.error(err)
      const detail = err.response?.data?.detail || 'Failed to save trade'
      toast.error(detail)
    }
  }

  const handleEditTradeClick = (trade) => {
    setEditingTrade(trade)
    setTradeForm({ code: trade.code, label: trade.label, is_active: trade.is_active })
  }

  const handleDeleteTrade = async (tradeId) => {
    if (!window.confirm('Are you sure you want to delete this trade?')) return
    try {
      await axios.delete(`/api/v1/students/trades/${tradeId}`)
      toast.success('Trade deleted successfully')
      fetchAllTrades()
    } catch (err) {
      console.error(err)
      const detail = err.response?.data?.detail || 'Failed to delete trade'
      toast.error(detail)
    }
  }

  const handleCancelTradeEdit = () => {
    setEditingTrade(null)
    setTradeForm({ code: '', label: '', is_active: true })
  }

  const handleSaveRank = async (e) => {
    e.preventDefault()
    try {
      if (editingRank) {
        await axios.put(`/api/v1/students/ranks/${editingRank.id}`, {
          label: rankForm.label,
          is_active: rankForm.is_active
        })
        toast.success('Rank updated successfully')
      } else {
        await axios.post('/api/v1/students/ranks', {
          code: rankForm.code,
          label: rankForm.label,
          is_active: rankForm.is_active
        })
        toast.success('Rank added successfully')
      }
      setRankForm({ code: '', label: '', is_active: true })
      setEditingRank(null)
      fetchAllRanks()
    } catch (err) {
      console.error(err)
      const detail = err.response?.data?.detail || 'Failed to save rank'
      toast.error(detail)
    }
  }

  const handleEditRankClick = (rank) => {
    setEditingRank(rank)
    setRankForm({ code: rank.code, label: rank.label, is_active: rank.is_active })
  }

  const handleDeleteRank = async (rankId) => {
    if (!window.confirm('Are you sure you want to delete this rank?')) return
    try {
      await axios.delete(`/api/v1/students/ranks/${rankId}`)
      toast.success('Rank deleted successfully')
      fetchAllRanks()
    } catch (err) {
      console.error(err)
      const detail = err.response?.data?.detail || 'Failed to delete rank'
      toast.error(detail)
    }
  }

  const handleCancelRankEdit = () => {
    setEditingRank(null)
    setRankForm({ code: '', label: '', is_active: true })
  }

  const handleAddExam = async (e) => {
    e.preventDefault()
    if (!newExamSubjectId || !newExamDate) return
    try {
      await axios.post('/api/v1/academic/exams', {
        course_id: selectedCourse.id,
        subject_id: newExamSubjectId,
        type: newExamType,
        date: newExamDate
      })
      toast.success('Examination slot scheduled')
      setNewExamDate('')
      // Refresh list
      const exRes = await axios.get(`/api/v1/academic/exams/${selectedCourse.id}`)
      setExams(exRes.data)
    } catch (err) {
      toast.error('Failed to create examination slot')
    }
  }

  return (
    <div className="fade-in-slide">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 className="mb-0 text-primary display-font">Academic Dashboard</h2>
          <p className="text-muted mb-0">Record exam marks, syllabus lessons, and schedules</p>
        </div>
      </div>

      <div className="row g-4">
        {/* Left Side: Course Selection List – only shown in Course Syllabus view */}
        {!showTradeManagement && !showRankManagement && (
        <div className="col-lg-3 col-md-12">
          <div className="card slaf-card p-3 mb-4">
            <h5 className="display-font text-muted mb-3 border-bottom pb-2">Active Courses</h5>
            {loading ? (
              <div className="spinner-border spinner-border-sm text-primary" role="status"></div>
            ) : (
              <div className="list-group list-group-flush mb-4">
                {courses.map(c => (
                  <button 
                    key={c.id} 
                    className={`list-group-item list-group-item-action border-0 px-2 py-2.5 rounded-3 mb-1 text-start fw-semibold ${(selectedCourse?.id === c.id) ? 'bg-primary-subtle text-primary' : ''}`}
                    onClick={() => {
                      setSelectedCourse(c);
                      setSearchParams({});
                    }}
                  >
                    <i className="bi bi-mortarboard me-2"></i> {c.name} ({c.code})
                  </button>
                ))}
              </div>
            )}

            {hasPermission('academic:write') && (
              <form onSubmit={handleAddCourse} className="border-top pt-3">
                <h6 className="fw-semibold mb-2" style={{ fontSize: '0.85rem' }}>Create New Course</h6>
                <div className="mb-2">
                  <input type="text" className="form-control form-control-sm" placeholder="Code (e.g. BA-AV-02)" value={newCourseCode} onChange={e => setNewCourseCode(e.target.value)} required />
                </div>
                <div className="mb-2">
                  <input type="text" className="form-control form-control-sm" placeholder="Course Name" value={newCourseName} onChange={e => setNewCourseName(e.target.value)} required />
                </div>
                <button type="submit" className="btn btn-primary btn-sm w-100 fw-semibold">Add Course</button>
              </form>
            )}
          </div>
        </div>
        )}

        {/* Right Side: Tabular Course Workspace / Trade & Rank Management Panel */}
        <div className={`${(showTradeManagement || showRankManagement) ? 'col-12' : 'col-lg-9 col-md-12'}`}>
          {showTradeManagement ? (
            <div className="card slaf-card p-4">
              <div className="d-flex justify-content-between align-items-center mb-4 border-bottom pb-2">
                <div>
                  <h3 className="display-font mb-0 text-primary">Trade Management</h3>
                  <p className="text-muted mb-0">Create, update, and manage student trade options</p>
                </div>
              </div>

              <div className="row g-4">
                {/* Form to Add/Edit Trade */}
                <div className="col-xl-4 col-lg-12">
                  <div className="card border-0 shadow-sm p-4 bg-light">
                    <h5 className="fw-semibold mb-3">{editingTrade ? 'Edit Trade' : 'Add New Trade'}</h5>
                    <form onSubmit={handleSaveTrade}>
                      <div className="mb-3">
                        <label className="form-label fw-semibold">Trade Code *</label>
                        <input
                          type="text"
                          className="form-control"
                          placeholder="e.g. COMPUTER_TECHNICIAN"
                          value={tradeForm.code}
                          onChange={e => setTradeForm({ ...tradeForm, code: e.target.value.toUpperCase() })}
                          required
                          disabled={!!editingTrade}
                        />
                        <small className="text-muted">A unique uppercase identifier.</small>
                      </div>
                      <div className="mb-3">
                        <label className="form-label fw-semibold">Trade Name (Label) *</label>
                        <input
                          type="text"
                          className="form-control"
                          placeholder="e.g. Computer Technician"
                          value={tradeForm.label}
                          onChange={e => setTradeForm({ ...tradeForm, label: e.target.value })}
                          required
                        />
                      </div>
                      <div className="mb-3 form-check form-switch">
                        <input
                          className="form-check-input"
                          type="checkbox"
                          id="tradeActiveSwitch"
                          checked={tradeForm.is_active}
                          onChange={e => setTradeForm({ ...tradeForm, is_active: e.target.checked })}
                        />
                        <label className="form-check-label fw-semibold" htmlFor="tradeActiveSwitch">
                          Active Status
                        </label>
                      </div>
                      <div className="d-flex gap-2">
                        <button type="submit" className="btn btn-primary w-100 fw-semibold">
                          {editingTrade ? 'Update' : 'Save'}
                        </button>
                        {editingTrade && (
                          <button type="button" className="btn btn-secondary w-100 fw-semibold" onClick={handleCancelTradeEdit}>
                            Cancel
                          </button>
                        )}
                      </div>
                    </form>
                  </div>
                </div>

                {/* Table of Trades */}
                <div className="col-xl-8 col-lg-12">
                  <div className="card border-0 shadow-sm p-4">
                    <div className="table-responsive">
                      <table className="table slaf-table align-middle mb-0">
                        <thead>
                          <tr>
                            <th style={{ width: '35%' }}>Code</th>
                            <th style={{ width: '35%' }}>Label</th>
                            <th style={{ width: '15%' }}>Status</th>
                            <th className="text-end" style={{ width: '15%' }}>Actions</th>
                          </tr>
                        </thead>
                        <tbody>
                          {allTrades.length === 0 ? (
                            <tr>
                              <td colSpan="4" className="text-center py-4 text-muted">
                                No trades loaded.
                              </td>
                            </tr>
                          ) : (
                            allTrades.map(t => (
                              <tr key={t.id}>
                                <td className="fw-bold">{t.code}</td>
                                <td>{t.label}</td>
                                <td>
                                  <span className={`slaf-badge ${t.is_active ? 'active' : 'awol'}`}>
                                    {t.is_active ? 'Active' : 'Inactive'}
                                  </span>
                                </td>
                                <td className="text-end">
                                  <button
                                    className="btn btn-outline-primary btn-sm px-2 me-1"
                                    onClick={() => handleEditTradeClick(t)}
                                    title="Edit Trade"
                                  >
                                    <i className="bi bi-pencil"></i>
                                  </button>
                                  <button
                                    className="btn btn-outline-danger btn-sm px-2"
                                    onClick={() => handleDeleteTrade(t.id)}
                                    title="Delete Trade"
                                  >
                                    <i className="bi bi-trash"></i>
                                  </button>
                                </td>
                              </tr>
                            ))
                          )}
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ) : showRankManagement ? (
            <div className="card slaf-card p-4">
              <div className="d-flex justify-content-between align-items-center mb-4 border-bottom pb-2">
                <div>
                  <h3 className="display-font mb-0 text-primary">Rank Management</h3>
                  <p className="text-muted mb-0">Create, update, and manage student rank options</p>
                </div>
              </div>

              <div className="row g-4">
                {/* Form to Add/Edit Rank */}
                <div className="col-xl-4 col-lg-12">
                  <div className="card border-0 shadow-sm p-4 bg-light">
                    <h5 className="fw-semibold mb-3">{editingRank ? 'Edit Rank' : 'Add New Rank'}</h5>
                    <form onSubmit={handleSaveRank}>
                      <div className="mb-3">
                        <label className="form-label fw-semibold">Rank Code *</label>
                        <input
                          type="text"
                          className="form-control"
                          placeholder="e.g. CPL"
                          value={rankForm.code}
                          onChange={e => setRankForm({ ...rankForm, code: e.target.value.toUpperCase() })}
                          required
                          disabled={!!editingRank}
                        />
                        <small className="text-muted">A unique uppercase identifier.</small>
                      </div>
                      <div className="mb-3">
                        <label className="form-label fw-semibold">Rank Name (Label) *</label>
                        <input
                          type="text"
                          className="form-control"
                          placeholder="e.g. Corporal"
                          value={rankForm.label}
                          onChange={e => setRankForm({ ...rankForm, label: e.target.value })}
                          required
                        />
                      </div>
                      <div className="mb-3 form-check form-switch">
                        <input
                          className="form-check-input"
                          type="checkbox"
                          id="rankActiveSwitch"
                          checked={rankForm.is_active}
                          onChange={e => setRankForm({ ...rankForm, is_active: e.target.checked })}
                        />
                        <label className="form-check-label fw-semibold" htmlFor="rankActiveSwitch">
                          Active Status
                        </label>
                      </div>
                      <div className="d-flex gap-2">
                        <button type="submit" className="btn btn-primary w-100 fw-semibold">
                          {editingRank ? 'Update' : 'Save'}
                        </button>
                        {editingRank && (
                          <button type="button" className="btn btn-secondary w-100 fw-semibold" onClick={handleCancelRankEdit}>
                            Cancel
                          </button>
                        )}
                      </div>
                    </form>
                  </div>
                </div>

                {/* Table of Ranks */}
                <div className="col-xl-8 col-lg-12">
                  <div className="card border-0 shadow-sm p-4">
                    <div className="table-responsive">
                      <table className="table slaf-table align-middle mb-0">
                        <thead>
                          <tr>
                            <th style={{ width: '35%' }}>Code</th>
                            <th style={{ width: '35%' }}>Label</th>
                            <th style={{ width: '15%' }}>Status</th>
                            <th className="text-end" style={{ width: '15%' }}>Actions</th>
                          </tr>
                        </thead>
                        <tbody>
                          {allRanks.length === 0 ? (
                            <tr>
                              <td colSpan="4" className="text-center py-4 text-muted">
                                No ranks loaded.
                              </td>
                            </tr>
                          ) : (
                            allRanks.map(r => (
                              <tr key={r.id}>
                                <td className="fw-bold">{r.code}</td>
                                <td>{r.label}</td>
                                <td>
                                  <span className={`slaf-badge ${r.is_active ? 'active' : 'awol'}`}>
                                    {r.is_active ? 'Active' : 'Inactive'}
                                  </span>
                                </td>
                                <td className="text-end">
                                  <button
                                    className="btn btn-outline-primary btn-sm px-2 me-1"
                                    onClick={() => handleEditRankClick(r)}
                                    title="Edit Rank"
                                  >
                                    <i className="bi bi-pencil"></i>
                                  </button>
                                  <button
                                    className="btn btn-outline-danger btn-sm px-2"
                                    onClick={() => handleDeleteRank(r.id)}
                                    title="Delete Rank"
                                  >
                                    <i className="bi bi-trash"></i>
                                  </button>
                                </td>
                              </tr>
                            ))
                          )}
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ) : selectedCourse ? (
            <div className="card slaf-card p-4">
              <div className="d-flex justify-content-between align-items-center mb-4 border-bottom pb-2">
                <div>
                  <h3 className="display-font mb-0 text-primary">{selectedCourse.name}</h3>
                  <small className="text-muted">Duration: {selectedCourse.duration_weeks} Weeks</small>
                </div>
                {/* Tabs */}
                <div className="nav nav-pills gap-1">
                  <button className={`nav-link px-3 py-1.5 fw-semibold ${activeTab === 'syllabus' ? 'active bg-primary' : 'text-body'}`} onClick={() => setActiveTab('syllabus')}>
                    Syllabus
                  </button>
                  <button className={`nav-link px-3 py-1.5 fw-semibold ${activeTab === 'timetable' ? 'active bg-primary' : 'text-body'}`} onClick={() => setActiveTab('timetable')}>
                    Timetable
                  </button>
                  <button className={`nav-link px-3 py-1.5 fw-semibold ${activeTab === 'marks' ? 'active bg-primary' : 'text-body'}`} onClick={() => setActiveTab('marks')}>
                    Grade Sheet
                  </button>
                  <button className={`nav-link px-3 py-1.5 fw-semibold ${activeTab === 'trainees' ? 'active bg-primary' : 'text-body'}`} onClick={() => setActiveTab('trainees')}>
                    Trainees
                  </button>
                </div>
              </div>

              {/* Tab Content 1: Syllabus */}
              {activeTab === 'syllabus' && (
                <div>
                  <h5 className="fw-semibold mb-3">Course Subjects</h5>
                  <div className="row g-3">
                    <div className="col-md-6">
                      <div className="list-group">
                        {subjects.length === 0 ? (
                          <div className="text-muted">No subjects added to syllabus.</div>
                        ) : (
                          subjects.map(s => (
                            <div key={s.id} className="list-group-item d-flex justify-content-between align-items-center p-3 mb-2 border rounded">
                              <div>
                                <strong className="text-secondary">{s.code}</strong> - {s.name}
                                <small className="text-muted d-block">{s.periods} Periods</small>
                              </div>
                            </div>
                          ))
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Tab Content 2: Timetable */}
              {activeTab === 'timetable' && (
                <div>
                  <h5 className="fw-semibold mb-3">Today's Timetable</h5>
                  <div className="table-responsive">
                    <table className="table slaf-table mb-0">
                      <thead>
                        <tr>
                          <th>Period</th>
                          <th>Subject</th>
                          <th>Lesson</th>
                          <th>Location</th>
                        </tr>
                      </thead>
                      <tbody>
                        {timetables.length === 0 ? (
                          <tr>
                            <td colSpan="4" className="text-center py-4 text-muted">No lectures scheduled for today.</td>
                          </tr>
                        ) : (
                          timetables.map(slot => (
                            <tr key={slot.id}>
                              <td><strong>Period {slot.period_number}</strong></td>
                              <td>{slot.subject_name}</td>
                              <td>{slot.lesson_name}</td>
                              <td>{slot.location}</td>
                            </tr>
                          ))
                        )}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              {/* Tab Content 3: Exam Marks */}
              {activeTab === 'marks' && (
                <div>
                  <div className="d-flex justify-content-between align-items-center mb-4">
                    <h5 className="fw-semibold mb-0">Exam Grading sheets</h5>
                    <select className="form-select w-auto" value={selectedExam?.id || ''} onChange={e => setSelectedExam(exams.find(ex => ex.id === e.target.value))}>
                      {exams.map(e => (
                        <option key={e.id} value={e.id}>{e.type} - {e.subject_name} ({new Date(e.date).toLocaleDateString()})</option>
                      ))}
                    </select>
                  </div>

                  {selectedExam ? (
                    <div className="table-responsive">
                      <table className="table slaf-table mb-0">
                        <thead>
                          <tr>
                            <th>Service Number</th>
                            <th>Trainee</th>
                            <th>Marks Obtained %</th>
                            <th>Grade Result</th>
                          </tr>
                        </thead>
                        <tbody>
                          {examMarks.length === 0 ? (
                            <tr>
                              <td colSpan="4" className="text-center py-4 text-muted">No student marks recorded for this examination yet.</td>
                            </tr>
                          ) : (
                            examMarks.map(mark => (
                              <tr key={mark.id}>
                                <td className="fw-semibold">{mark.student_service_number}</td>
                                <td>{mark.student_name}</td>
                                <td><span className="fw-bold">{mark.marks_obtained}%</span></td>
                                <td>
                                  <span className={`badge bg-${mark.status === 'Pass' ? 'success' : 'danger'}`}>
                                    {mark.status}
                                  </span>
                                </td>
                              </tr>
                            ))
                          )}
                        </tbody>
                      </table>
                    </div>
                  ) : (
                    <div className="text-muted">No examinations scheduled yet for this course.</div>
                  )}

                  {hasPermission('academic:write') && subjects.length > 0 && (
                    <form onSubmit={handleAddExam} className="row g-2 align-items-end mt-4 p-3 bg-light rounded-3">
                      <h6 className="fw-semibold mb-2">Schedule Examination Slot</h6>
                      <div className="col-md-3">
                        <select className="form-select" value={newExamType} onChange={e => setNewExamType(e.target.value)} required>
                          <option value="Phase Test">Phase Test</option>
                          <option value="Final Exam">Final Exam</option>
                        </select>
                      </div>
                      <div className="col-md-5">
                        <select className="form-select" value={newExamSubjectId} onChange={e => setNewExamSubjectId(e.target.value)} required>
                          <option value="">Select Subject</option>
                          {subjects.map(s => (
                            <option key={s.id} value={s.id}>{s.name}</option>
                          ))}
                        </select>
                      </div>
                      <div className="col-md-3">
                        <input type="date" className="form-control" value={newExamDate} onChange={e => setNewExamDate(e.target.value)} required />
                      </div>
                      <div className="col-md-1">
                        <button type="submit" className="btn btn-primary w-100"><i className="bi bi-check-circle"></i></button>
                      </div>
                    </form>
                  )}
                </div>
              )}

              {/* Tab Content 4: Trainees */}
              {activeTab === 'trainees' && (
                <div>
                  <h5 className="fw-semibold mb-3">Enrolled Trainees</h5>
                  <div className="table-responsive">
                    <table className="table slaf-table mb-0">
                      <thead>
                        <tr>
                          <th>Service Number</th>
                          <th>Rank & Full Name</th>
                          <th>Batch</th>
                          <th>Status</th>
                          <th className="text-end">Actions</th>
                        </tr>
                      </thead>
                      <tbody>
                        {students.length === 0 ? (
                          <tr>
                            <td colSpan="5" className="text-center py-4 text-muted">
                              No trainees are assigned to this course.
                            </td>
                          </tr>
                        ) : (
                          students.map(s => (
                            <tr key={s.id}>
                              <td className="fw-semibold text-primary">{s.service_number}</td>
                               <td>
                                 <span className="fw-bold text-dark d-block text-capitalize" style={{ fontSize: '0.9rem', lineHeight: '1.25' }}>
                                   {s.full_name || s.initials}
                                 </span>
                                 <div className="d-flex align-items-center gap-1.5 mt-1">
                                   <span className="badge bg-secondary-subtle text-dark border border-secondary-subtle px-2 py-0.5 fw-semibold" style={{ fontSize: '0.725rem' }}>
                                     {s.rank}
                                   </span>
                                   {s.initials && (
                                     <span className="text-muted fw-medium" style={{ fontSize: '0.75rem' }}>
                                       • {s.initials}
                                     </span>
                                   )}
                                 </div>
                               </td>
                              <td>{s.batch}</td>
                              <td>
                                <span className={`slaf-badge ${s.status.toLowerCase().replace(' ', '-')}`}>
                                  {s.status}
                                </span>
                              </td>
                              <td className="text-end">
                                <Link to={`/students/${s.id}`} className="btn btn-outline-primary btn-sm px-2.5" title="View Profile">
                                  <i className="bi bi-eye"></i>
                                </Link>
                              </td>
                            </tr>
                          ))
                        )}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="card slaf-card p-4">
              <h3 className="display-font text-primary mb-4 border-bottom pb-2">Academic Activities Overview</h3>
              <div className="row g-4 mb-4">
                <div className="col-md-6 col-xl-3">
                  <div className="card border-0 shadow-sm p-4 text-center bg-primary-subtle text-primary">
                    <i className="bi bi-mortarboard-fill mb-2" style={{ fontSize: '2.5rem' }}></i>
                    <h5 className="text-muted fw-semibold">Active Courses</h5>
                    <h2 className="display-font fw-bold mb-0">{academicStats.course_count}</h2>
                  </div>
                </div>
                <div className="col-md-6 col-xl-3">
                  <div className="card border-0 shadow-sm p-4 text-center bg-success-subtle text-success">
                    <i className="bi bi-people-fill mb-2" style={{ fontSize: '2.5rem' }}></i>
                    <h5 className="text-muted fw-semibold">Enrolled Trainees</h5>
                    <h2 className="display-font fw-bold mb-0">{academicStats.active_students}</h2>
                  </div>
                </div>
                <div className="col-md-6 col-xl-3">
                  <div className="card border-0 shadow-sm p-4 text-center bg-warning-subtle text-warning">
                    <i className="bi bi-calendar3 mb-2" style={{ fontSize: '2.5rem' }}></i>
                    <h5 className="text-muted fw-semibold">Classes Today</h5>
                    <h2 className="display-font fw-bold mb-0">{academicStats.active_timetables_today}</h2>
                  </div>
                </div>
                <div className="col-md-6 col-xl-3">
                  <div className="card border-0 shadow-sm p-4 text-center bg-info-subtle text-info">
                    <i className="bi bi-graph-up-arrow mb-2" style={{ fontSize: '2.5rem' }}></i>
                    <h5 className="text-muted fw-semibold">Avg Pass Rate</h5>
                    <h2 className="display-font fw-bold mb-0">{academicStats.average_pass_rate}%</h2>
                  </div>
                </div>
              </div>
              <div className="text-center py-4 bg-light rounded-3 text-muted">
                Please select an active course from the directory list to manage syllabus, timetables, grades, and assigned trainees.
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
export default CourseList
