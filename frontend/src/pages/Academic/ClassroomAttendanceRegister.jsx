import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { toast } from 'react-toastify'

export const ClassroomAttendanceRegister = () => {
  const [courses, setCourses] = useState([])
  const [selectedCourseId, setSelectedCourseId] = useState('')
  const [selectedDate, setSelectedDate] = useState(() => new Date().toISOString().split('T')[0])
  const [timetables, setTimetables] = useState([])
  const [selectedTimetableId, setSelectedTimetableId] = useState('')
  
  const [sessionData, setSessionData] = useState(null)
  const [traineeList, setTraineeList] = useState([])
  const [loadingSession, setLoadingSession] = useState(false)
  const [submitting, setSubmitting] = useState(false)

  // Reporting State
  const [activeMode, setActiveMode] = useState('register') // 'register' | 'class-report' | 'student-report' | 'classroom-report'
  
  // Class-wise report
  const [classReport, setClassReport] = useState([])
  const [loadingClassReport, setLoadingClassReport] = useState(false)

  // Student history report
  const [students, setStudents] = useState([])
  const [selectedStudentId, setSelectedStudentId] = useState('')
  const [studentHistory, setStudentHistory] = useState([])
  const [loadingStudentHistory, setLoadingStudentHistory] = useState(false)
  const [studentCourseFilter, setStudentCourseFilter] = useState('')
  const [svcSearchQuery, setSvcSearchQuery] = useState('')

  // Classroom report
  const [classrooms, setClassrooms] = useState([])
  const [selectedLocation, setSelectedLocation] = useState('')
  const [classroomReport, setClassroomReport] = useState([])
  const [loadingClassroomReport, setLoadingClassroomReport] = useState(false)

  const STATUS_OPTIONS = [
    { value: 'PRESENT', label: 'Present', color: 'success' },
    { value: 'LATE', label: 'Late', color: 'warning' },
    { value: 'ABSENT', label: 'Absent', color: 'danger' },
    { value: 'SICK_REPORT', label: 'Sick Report', color: 'info' },
    { value: 'COURSE_VISIT', label: 'Course Visit', color: 'primary' },
    { value: 'LEAVE', label: 'Leave', color: 'secondary' },
    { value: 'HOSPITAL', label: 'Hospital', color: 'danger' },
    { value: 'EXCUSED', label: 'Excused', color: 'dark' }
  ]

  useEffect(() => {
    fetchInitialData()
  }, [])

  const fetchInitialData = async () => {
    try {
      const [cRes, sRes, rmRes] = await Promise.all([
        axios.get('/api/v1/academic/courses'),
        axios.get('/api/v1/students?limit=200'),
        axios.get('/api/v1/academic/classrooms')
      ])
      const courseData = cRes.data || []
      setCourses(courseData)
      const studentData = sRes.data?.items || sRes.data || []
      setStudents(studentData)
      const rmData = rmRes.data || []
      setClassrooms(rmData)
      if (rmData.length > 0) {
        setSelectedLocation(rmData[0].name || rmData[0].code)
      }
    } catch (err) {
      console.error('Failed to load initial data for attendance', err)
      toast.error('Failed to load courses or students.')
    }
  }

  // Fetch timetables when course or date changes
  useEffect(() => {
    if (selectedCourseId && selectedDate) {
      fetchTimetables(selectedCourseId, selectedDate)
    }
  }, [selectedCourseId, selectedDate])

  const fetchTimetables = async (courseId, dateStr) => {
    try {
      const res = await axios.get('/api/v1/academic/timetables', {
        params: { course_id: courseId, date: dateStr, timetable_date: dateStr }
      })
      const ttList = res.data || []
      setTimetables(ttList)
      setSelectedTimetableId('')
      setSessionData(null)
      setTraineeList([])
    } catch (err) {
      console.error('Error loading timetables', err)
      setTimetables([])
      setSelectedTimetableId('')
      setSessionData(null)
      setTraineeList([])
    }
  }

  const handleApproveParadeState = async () => {
    if (!sessionData) return
    try {
      await axios.post('/api/v1/academic/attendance/approve-parade-state', {
        trade_name: sessionData.trade_name,
        date: sessionData.date
      })
      toast.success('Parade State approved successfully!')
      fetchSessionDetails(selectedTimetableId)
    } catch (err) {
      toast.error('Failed to approve Parade State.')
    }
  }

  // Fetch classroom session details when selectedTimetableId changes
  useEffect(() => {
    if (selectedTimetableId) {
      fetchSessionDetails(selectedTimetableId)
    }
  }, [selectedTimetableId])

  const fetchSessionDetails = async (timetableId) => {
    setLoadingSession(true)
    try {
      const res = await axios.get(`/api/v1/academic/attendance/session/${timetableId}`)
      const data = res.data
      setSessionData(data)
      setTraineeList(data.students || [])
    } catch (err) {
      console.error('Error fetching session details', err)
      toast.error('Failed to load class session attendance.')
      setSessionData(null)
      setTraineeList([])
    } finally {
      setLoadingSession(false)
    }
  }

  const handleStatusChange = (studentId, newStatus) => {
    setTraineeList(prev => prev.map(item => item.student_id === studentId ? { ...item, attendance_status: newStatus } : item))
  }

  const handleRemarksChange = (studentId, newRemarks) => {
    setTraineeList(prev => prev.map(item => item.student_id === studentId ? { ...item, remarks: newRemarks } : item))
  }

  const handleMarkAllPresent = () => {
    setTraineeList(prev => prev.map(item => ({ ...item, attendance_status: 'PRESENT' })))
    toast.info('All trainees set to PRESENT')
  }

  const handleResetToParadeState = () => {
    if (sessionData && sessionData.students) {
      setTraineeList(sessionData.students)
      toast.info('Reset attendance statuses to default Parade State values.')
    }
  }

  const handleSaveAttendance = async () => {
    if (!selectedTimetableId) return
    if (!sessionData?.is_parade_approved) {
      toast.error("Today's Parade State has not been approved. Classroom attendance cannot be finalized until the Parade State is approved.")
      return
    }

    setSubmitting(true)
    try {
      const payload = {
        timetable_id: selectedTimetableId,
        records: traineeList.map(t => ({
          student_id: t.student_id,
          status: t.attendance_status,
          remarks: t.remarks ? t.remarks.trim() : null
        }))
      }
      await axios.post('/api/v1/academic/attendance', payload)
      toast.success('Classroom attendance saved successfully!')
      fetchSessionDetails(selectedTimetableId)
    } catch (err) {
      console.error('Error saving attendance', err)
      const msg = err.response?.data?.detail || 'Failed to save classroom attendance.'
      toast.error(msg)
    } finally {
      setSubmitting(false)
    }
  }

  // Class-wise Report Fetcher
  const fetchClassReport = async () => {
    setLoadingClassReport(true)
    try {
      const res = await axios.get('/api/v1/academic/attendance/reports/class-wise', {
        params: { course_id: selectedCourseId }
      })
      setClassReport(res.data || [])
    } catch (err) {
      console.error('Failed to load class report', err)
      toast.error('Failed to load class attendance report.')
    } finally {
      setLoadingClassReport(false)
    }
  }

  // Student History Fetcher
  const fetchStudentHistory = async (studentId) => {
    if (!studentId) return
    setLoadingStudentHistory(true)
    try {
      const res = await axios.get(`/api/v1/academic/students/${studentId}/attendance`)
      setStudentHistory(res.data || [])
    } catch (err) {
      console.error('Failed to load student history', err)
      toast.error('Failed to load student attendance history.')
    } finally {
      setLoadingStudentHistory(false)
    }
  }

  // Classroom Report Fetcher
  const fetchClassroomReport = async (location) => {
    if (!location) return
    setLoadingClassroomReport(true)
    try {
      const res = await axios.get('/api/v1/academic/attendance/reports/classroom-wise', {
        params: { location }
      })
      setClassroomReport(res.data || [])
    } catch (err) {
      console.error('Failed to load classroom report', err)
      toast.error('Failed to load classroom attendance report.')
    } finally {
      setLoadingClassroomReport(false)
    }
  }

  return (
    <div className="fade-in-slide">
      {/* Header & Sub Navigation */}
      <div className="card slaf-card p-3 mb-4 shadow-sm">
        <div className="d-flex flex-wrap justify-content-between align-items-center gap-3">
          <div>
            <h5 className="fw-extrabold display-font text-dark mb-1">
              <i className="bi bi-calendar-check text-primary me-2"></i>
              Classroom Attendance Register
            </h5>
            <p className="text-muted small mb-0">
              Record period-by-period class attendance synchronized with approved Daily Parade States.
            </p>
          </div>
          <div className="d-flex gap-2">
            <button
              className={`btn btn-sm ${activeMode === 'register' ? 'btn-primary fw-bold' : 'btn-outline-primary'}`}
              onClick={() => setActiveMode('register')}
            >
              <i className="bi bi-clipboard-check me-1"></i> Class Register
            </button>
            <button
              className={`btn btn-sm ${activeMode === 'class-report' ? 'btn-primary fw-bold' : 'btn-outline-primary'}`}
              onClick={() => {
                setActiveMode('class-report')
                fetchClassReport()
              }}
            >
              <i className="bi bi-bar-chart-steps me-1"></i> Class-wise Report
            </button>
            <button
              className={`btn btn-sm ${activeMode === 'student-report' ? 'btn-primary fw-bold' : 'btn-outline-primary'}`}
              onClick={() => {
                setActiveMode('student-report')
                setSelectedStudentId('')
                setStudentHistory([])
              }}
            >
              <i className="bi bi-person-badge me-1"></i> Trainee History
            </button>
            <button
              className={`btn btn-sm ${activeMode === 'classroom-report' ? 'btn-primary fw-bold' : 'btn-outline-primary'}`}
              onClick={() => {
                setActiveMode('classroom-report')
                if (selectedLocation) fetchClassroomReport(selectedLocation)
              }}
            >
              <i className="bi bi-door-open me-1"></i> Classroom Report
            </button>
          </div>
        </div>
      </div>

      {/* MODE 1: CLASSROOM ATTENDANCE REGISTER */}
      {activeMode === 'register' && (
        <>
          {/* Session Picker Bar */}
          <div className="card slaf-card p-3 mb-4 shadow-sm border-primary border-top border-3">
            <div className="row g-3 align-items-center">
              <div className="col-md-4">
                <label className="form-label small fw-bold text-muted text-uppercase mb-1">
                  Course & Batch
                </label>
                <select
                  className="form-select border-primary"
                  value={selectedCourseId}
                  onChange={(e) => setSelectedCourseId(e.target.value)}
                >
                  <option value="">-- Select Ongoing Course & Batch --</option>
                  {courses.map(c => (
                    <option key={c.id} value={c.id}>
                      {c.name} ({c.code}) — {c.trade_name || 'General'}
                    </option>
                  ))}
                </select>
              </div>

              <div className="col-md-3">
                <label className="form-label small fw-bold text-muted text-uppercase mb-1">
                  Session Date
                </label>
                <input
                  type="date"
                  className="form-control"
                  value={selectedDate}
                  onChange={(e) => setSelectedDate(e.target.value)}
                />
              </div>

              <div className="col-md-5">
                <label className="form-label small fw-bold text-primary text-uppercase mb-1">
                  Select Class Session Period <span className="text-danger">*</span>
                </label>
                <select
                  className="form-select border-primary fw-semibold"
                  value={selectedTimetableId}
                  onChange={(e) => setSelectedTimetableId(e.target.value)}
                  disabled={!selectedCourseId || timetables.length === 0}
                >
                  {!selectedCourseId ? (
                    <option value="">-- Select a Course first --</option>
                  ) : timetables.length === 0 ? (
                    <option value="">-- No scheduled class sessions found on this date --</option>
                  ) : (
                    <>
                      <option value="">-- Select Class Session Period --</option>
                      {timetables.map(tt => (
                        <option key={tt.id} value={tt.id}>
                          Period {tt.period_number} — {tt.subject_name || 'Subject'} ({tt.location || 'Hall'})
                        </option>
                      ))}
                    </>
                  )}
                </select>
              </div>
            </div>
          </div>

          {/* Session Details Header Banner */}
          {loadingSession ? (
            <div className="text-center py-5">
              <div className="spinner-border text-primary me-2" role="status"></div>
              <span className="text-muted fw-semibold">Loading class session attendance data...</span>
            </div>
          ) : sessionData ? (
            <>
              <div className="card slaf-card p-3 mb-4 shadow-sm">
                <div className="row align-items-center g-3">
                  <div className="col-lg-8">
                    <div className="d-flex align-items-center gap-2 mb-2">
                      <span className="badge bg-primary-subtle text-primary border fw-bold px-2.5 py-1">
                        {sessionData.course_code}
                      </span>
                      <h6 className="fw-bold text-dark mb-0">{sessionData.course_name}</h6>
                    </div>

                    <div className="d-flex flex-wrap gap-3 text-muted small">
                      <div><strong className="text-dark">Trade:</strong> {sessionData.trade_name}</div>
                      <div><strong className="text-dark">Batch:</strong> {sessionData.batch}</div>
                      <div><strong className="text-dark">Classroom:</strong> {sessionData.classroom_location}</div>
                      <div><strong className="text-dark">Instructor:</strong> {sessionData.instructor_name}</div>
                      <div><strong className="text-dark">Period:</strong> {sessionData.period_number} ({sessionData.subject_name})</div>
                      <div><strong className="text-dark">Date:</strong> {sessionData.date}</div>
                    </div>
                  </div>

                  <div className="col-lg-4 text-lg-end">
                    <div className="d-inline-block text-start text-lg-end">
                      <div className="small text-muted fw-bold text-uppercase mb-1">Parade State Approval</div>
                      {sessionData.is_parade_approved ? (
                        <span className="badge bg-success text-white px-3 py-2 fw-bold">
                          <i className="bi bi-check-circle-fill me-1"></i> APPROVED
                        </span>
                      ) : (
                        <span className="badge bg-warning text-dark px-3 py-2 fw-bold">
                          <i className="bi bi-exclamation-triangle-fill me-1"></i> PENDING / NOT APPROVED
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              </div>

              {/* Unapproved Parade State Warning Banner */}
              {!sessionData.is_parade_approved && (
                <div className="alert alert-warning d-flex align-items-center justify-content-between mb-4 shadow-xs border-start border-warning border-4" role="alert">
                  <div className="d-flex align-items-center">
                    <i className="bi bi-shield-exclamation display-6 me-3 text-warning"></i>
                    <div>
                      <h6 className="fw-bold mb-1">Parade State Pending / Not Approved</h6>
                      <p className="mb-0 small">
                        Parade State for {sessionData.trade_name} on {sessionData.date} has not been marked as approved. You can click to approve & sync the Parade State below to enable class attendance recording.
                      </p>
                    </div>
                  </div>
                  <button
                    className="btn btn-warning btn-sm fw-bold text-dark text-nowrap ms-3 px-3 py-2"
                    onClick={handleApproveParadeState}
                  >
                    <i className="bi bi-check-circle-fill me-1"></i> Approve & Sync Parade State
                  </button>
                </div>
              )}

              {/* Action Toolbar */}
              <div className="card slaf-card p-3 mb-3 shadow-sm">
                <div className="d-flex flex-wrap justify-content-between align-items-center gap-2">
                  <div className="d-flex gap-2">
                    <button
                      className="btn btn-sm btn-outline-success fw-semibold"
                      onClick={handleMarkAllPresent}
                      disabled={!sessionData.is_parade_approved}
                    >
                      <i className="bi bi-check-all me-1"></i> Mark All Present
                    </button>
                    <button
                      className="btn btn-sm btn-outline-secondary fw-semibold"
                      onClick={handleResetToParadeState}
                      disabled={!sessionData.is_parade_approved}
                    >
                      <i className="bi bi-arrow-counterclockwise me-1"></i> Reset to Parade State
                    </button>
                  </div>

                  <div>
                    <button
                      className="btn btn-primary fw-bold px-4 shadow-sm"
                      onClick={handleSaveAttendance}
                      disabled={!sessionData.is_parade_approved || submitting}
                    >
                      {submitting ? (
                        <>
                          <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                          Saving...
                        </>
                      ) : (
                        <>
                          <i className="bi bi-save me-1.5"></i> Save Attendance
                        </>
                      )}
                    </button>
                  </div>
                </div>
              </div>

              {/* Trainee Attendance Register Table */}
              <div className="card slaf-card border-0 shadow-sm overflow-hidden mb-4">
                <div className="table-responsive">
                  <table className="table table-hover align-middle mb-0">
                    <thead className="table-dark text-uppercase small">
                      <tr>
                        <th style={{ width: '120px' }}>Service No</th>
                        <th style={{ width: '90px' }}>Rank</th>
                        <th style={{ minWidth: '180px' }}>Student Name</th>
                        <th style={{ width: '130px' }}>Parade State</th>
                        <th style={{ width: '170px' }}>Classroom Attendance</th>
                        <th style={{ minWidth: '200px' }}>Remarks</th>
                      </tr>
                    </thead>
                    <tbody>
                      {traineeList.length === 0 ? (
                        <tr>
                          <td colSpan="6" className="text-center py-5 text-muted">
                            No trainees enrolled in this course batch.
                          </td>
                        </tr>
                      ) : (
                        traineeList.map((t) => (
                          <tr key={t.student_id}>
                            <td>
                              <span className="fw-bold font-monospace text-dark">{t.service_number}</span>
                            </td>
                            <td>
                              <span className="badge bg-secondary-subtle text-dark border">{t.rank}</span>
                            </td>
                            <td>
                              <div className="fw-bold text-dark">{t.full_name}</div>
                              <div className="text-muted small">{t.trade}</div>
                            </td>
                            <td>
                              <span className={`badge ${
                                t.parade_state === 'Present' ? 'bg-success-subtle text-success border-success' : 'bg-warning-subtle text-dark border-warning'
                              } px-2 py-1`}>
                                {t.parade_state}
                              </span>
                            </td>
                            <td>
                              <select
                                className="form-select form-select-sm fw-semibold"
                                value={t.attendance_status}
                                onChange={(e) => handleStatusChange(t.student_id, e.target.value)}
                                disabled={!sessionData.is_parade_approved}
                              >
                                {STATUS_OPTIONS.map(opt => (
                                  <option key={opt.value} value={opt.value}>
                                    {opt.label}
                                  </option>
                                ))}
                              </select>
                            </td>
                            <td>
                              <input
                                type="text"
                                className="form-control form-control-sm"
                                placeholder="Optional remarks..."
                                value={t.remarks || ''}
                                onChange={(e) => handleRemarksChange(t.student_id, e.target.value)}
                                disabled={!sessionData.is_parade_approved}
                              />
                            </td>
                          </tr>
                        ))
                      )}
                    </tbody>
                  </table>
                </div>
              </div>
            </>
          ) : (
            <div className="card slaf-card text-center p-5 shadow-sm border-dashed">
              <div className="py-4">
                <i className="bi bi-calendar-x display-4 text-muted mb-3 d-block"></i>
                <h5 className="fw-bold text-dark">No Scheduled Session Selected</h5>
                <p className="text-muted small max-w-md mx-auto">
                  Select a course, date, and timetable period session from the selectors above to load classroom attendance.
                </p>
              </div>
            </div>
          )}
        </>
      )}

      {/* MODE 2: CLASS-WISE ATTENDANCE REPORT */}
      {activeMode === 'class-report' && (
        <div className="card slaf-card p-4 shadow-sm">
          <h6 className="fw-bold text-dark mb-3">
            <i className="bi bi-bar-chart-fill me-2 text-primary"></i>
            Class-wise Attendance Summary Report
          </h6>
          {loadingClassReport ? (
            <div className="text-center py-5">
              <div className="spinner-border text-primary me-2"></div>
              <span className="text-muted fw-semibold">Generating report...</span>
            </div>
          ) : (
            <div className="table-responsive">
              <table className="table align-middle table-hover mb-0">
                <thead className="table-dark text-uppercase small">
                  <tr>
                    <th>Date</th>
                    <th>Period</th>
                    <th>Course</th>
                    <th>Classroom</th>
                    <th>Instructor</th>
                    <th>Subject</th>
                    <th className="text-center">Total</th>
                    <th className="text-center text-success">Present</th>
                    <th className="text-center text-warning">Late</th>
                    <th className="text-center text-info">Sick</th>
                    <th className="text-center text-danger">Absent</th>
                  </tr>
                </thead>
                <tbody>
                  {classReport.length === 0 ? (
                    <tr>
                      <td colSpan="11" className="text-center py-4 text-muted">
                        No class attendance records found for this course.
                      </td>
                    </tr>
                  ) : (
                    classReport.map((row, i) => (
                      <tr key={i}>
                        <td className="fw-bold">{row.date}</td>
                        <td>P{row.period_number}</td>
                        <td>{row.course_name}</td>
                        <td>{row.classroom_location}</td>
                        <td>{row.instructor_name}</td>
                        <td>{row.subject_name}</td>
                        <td className="text-center font-monospace fw-bold">{row.total_students}</td>
                        <td className="text-center text-success fw-bold">{row.present_count}</td>
                        <td className="text-center text-warning fw-bold">{row.late_count}</td>
                        <td className="text-center text-info fw-bold">{row.sick_report_count}</td>
                        <td className="text-center text-danger fw-bold">{row.absent_count}</td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* MODE 3: INDIVIDUAL TRAINEE ATTENDANCE HISTORY */}
      {activeMode === 'student-report' && (() => {
        const filteredStudents = students.filter(s => {
          const matchCourse = !studentCourseFilter || s.course_id === studentCourseFilter
          const q = svcSearchQuery.trim().toLowerCase()
          const matchQuery = !q || (s.service_number || '').toLowerCase().includes(q) || (s.full_name || '').toLowerCase().includes(q) || (s.rank || '').toLowerCase().includes(q)
          return matchCourse && matchQuery
        })

        const activeStudent = selectedStudentId ? students.find(s => s.id === selectedStudentId) : null

        const totalClasses = studentHistory.length
        const presentClasses = studentHistory.filter(h => h.status === 'PRESENT').length
        const lateClasses = studentHistory.filter(h => h.status === 'LATE').length
        const absentClasses = studentHistory.filter(h => h.status === 'ABSENT').length
        const excClasses = studentHistory.filter(h => ['SICK_REPORT', 'LEAVE', 'HOSPITAL', 'EXCUSED', 'COURSE_VISIT'].includes(h.status)).length
        const presentRate = totalClasses > 0 ? Math.round(((presentClasses + lateClasses) / totalClasses) * 100) : 0

        return (
          <div className="card slaf-card p-4 shadow-sm">
            {/* Controls Bar: Course Filter, Service No Search, Trainee Picker */}
            <div className="row g-3 align-items-end mb-4">
              <div className="col-md-4">
                <label className="form-label small fw-bold text-muted text-uppercase mb-1">
                  Filter by Ongoing Course
                </label>
                <select
                  className="form-select border-primary"
                  value={studentCourseFilter}
                  onChange={(e) => {
                    setStudentCourseFilter(e.target.value)
                    setSelectedStudentId('')
                    setStudentHistory([])
                  }}
                >
                  <option value="">All Ongoing Courses</option>
                  {courses.map(c => (
                    <option key={c.id} value={c.id}>
                      {c.name} ({c.code}) — {c.trade_name || 'General'}
                    </option>
                  ))}
                </select>
              </div>

              <div className="col-md-3">
                <label className="form-label small fw-bold text-primary text-uppercase mb-1">
                  Search by Service No / Name
                </label>
                <div className="input-group">
                  <span className="input-group-text bg-light text-muted"><i className="bi bi-search"></i></span>
                  <input
                    type="text"
                    className="form-control border-primary"
                    placeholder="Type Svc No (e.g. 50833, 50327)..."
                    value={svcSearchQuery}
                    onChange={(e) => {
                      setSvcSearchQuery(e.target.value)
                    }}
                  />
                </div>
              </div>

              <div className="col-md-5">
                <label className="form-label small fw-bold text-muted text-uppercase mb-1">
                  Select Trainee / Student ({filteredStudents.length} Found)
                </label>
                <select
                  className="form-select border-primary fw-semibold"
                  value={selectedStudentId}
                  onChange={(e) => {
                    setSelectedStudentId(e.target.value)
                    if (e.target.value) {
                      fetchStudentHistory(e.target.value)
                    } else {
                      setStudentHistory([])
                    }
                  }}
                >
                  <option value="">-- Select Trainee / Student --</option>
                  {filteredStudents.map(s => (
                    <option key={s.id} value={s.id}>
                      {s.service_number} — {s.rank} {s.full_name} ({s.trade || 'General'})
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {/* Trainee Profile & Attendance Statistics Card */}
            {activeStudent ? (
              <>
                <div className="card bg-light border-0 p-3 mb-4 rounded-3 shadow-xs">
                  <div className="row align-items-center g-3">
                    <div className="col-md-7">
                      <div className="d-flex align-items-center gap-3">
                        <div className="d-inline-flex bg-primary text-white rounded-circle align-items-center justify-content-center p-3" style={{ width: '48px', height: '48px' }}>
                          <i className="bi bi-person-badge-fill fs-4"></i>
                        </div>
                        <div>
                          <span className="badge bg-primary-subtle text-primary border fw-bold me-2">
                            Svc No: {activeStudent.service_number}
                          </span>
                          <span className="badge bg-secondary-subtle text-dark border me-2">
                            {activeStudent.rank}
                          </span>
                          <h5 className="fw-bold text-dark mb-1 mt-1">{activeStudent.full_name}</h5>
                          <div className="text-muted small">
                            <strong>Trade:</strong> {activeStudent.trade || 'General'} &bull; <strong>Batch:</strong> {activeStudent.batch || '169'}
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className="col-md-5 text-md-end border-start border-md-start-0 border-secondary-subtle ps-md-4">
                      <div className="d-flex justify-content-md-end gap-3 align-items-center">
                        <div>
                          <span className="text-muted small fw-bold text-uppercase d-block">Overall Attendance</span>
                          <h4 className={`mb-0 fw-bold ${presentRate >= 80 ? 'text-success' : presentRate >= 60 ? 'text-warning' : 'text-danger'}`}>
                            {presentRate}%
                          </h4>
                        </div>
                        <div className="vr d-none d-sm-block"></div>
                        <div className="d-flex gap-1">
                          <span className="badge bg-success-subtle text-success border p-2" title="Present Classes">
                            <i className="bi bi-check-circle-fill me-1"></i> {presentClasses}
                          </span>
                          <span className="badge bg-warning-subtle text-warning border p-2" title="Late Classes">
                            <i className="bi bi-clock-history me-1"></i> {lateClasses}
                          </span>
                          <span className="badge bg-danger-subtle text-danger border p-2" title="Absent Classes">
                            <i className="bi bi-x-circle-fill me-1"></i> {absentClasses}
                          </span>
                          <span className="badge bg-secondary-subtle text-secondary border p-2" title="Excused / Parade State Absences">
                            <i className="bi bi-shield-minus me-1"></i> {excClasses}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Attendance Trail Table */}
                {loadingStudentHistory ? (
                  <div className="text-center py-5">
                    <div className="spinner-border text-primary me-2"></div>
                    <span className="text-muted">Loading trainee attendance trail...</span>
                  </div>
                ) : (
                  <div className="table-responsive">
                    <table className="table align-middle table-hover mb-0">
                      <thead className="table-dark text-uppercase small">
                        <tr>
                          <th>Date</th>
                          <th>Period</th>
                          <th>Course</th>
                          <th>Subject</th>
                          <th>Classroom</th>
                          <th>Attendance Status</th>
                          <th>Remarks</th>
                        </tr>
                      </thead>
                      <tbody>
                        {studentHistory.length === 0 ? (
                          <tr>
                            <td colSpan="7" className="text-center py-4 text-muted">
                              No recorded period attendance history for this trainee.
                            </td>
                          </tr>
                        ) : (
                          studentHistory.map((h, idx) => (
                            <tr key={idx}>
                              <td className="fw-bold">{h.date}</td>
                              <td><span className="badge bg-primary-subtle text-primary border fw-bold">Period {h.period_number}</span></td>
                              <td>{h.course_name}</td>
                              <td>{h.subject_name}</td>
                              <td>{h.classroom_location}</td>
                              <td>
                                <span className={`badge px-2.5 py-1.5 fw-bold bg-${
                                  h.status === 'PRESENT' ? 'success' :
                                  h.status === 'LATE' ? 'warning' :
                                  h.status === 'ABSENT' ? 'danger' :
                                  h.status === 'SICK_REPORT' ? 'info' :
                                  h.status === 'COURSE_VISIT' ? 'primary' :
                                  h.status === 'LEAVE' ? 'secondary' : 'dark'
                                }`}>
                                  {h.status}
                                </span>
                              </td>
                              <td className="text-muted small">{h.remarks || '-'}</td>
                            </tr>
                          ))
                        )}
                      </tbody>
                    </table>
                  </div>
                )}
              </>
            ) : (
              <div className="card slaf-card text-center p-5 shadow-sm border-dashed">
                <div className="py-4">
                  <i className="bi bi-person-bounding-box display-4 text-muted mb-3 d-block"></i>
                  <h5 className="fw-bold text-dark">No Trainee Selected</h5>
                  <p className="text-muted small max-w-md mx-auto mb-0">
                    Please select a trainee from the dropdown above or enter a Service Number to view individual attendance trail.
                  </p>
                </div>
              </div>
            )}
          </div>
        )
      })()}

      {/* MODE 4: CLASSROOM-WISE REPORT */}
      {activeMode === 'classroom-report' && (
        <div className="card slaf-card p-4 shadow-sm">
          <div className="row g-3 align-items-center mb-4">
            <div className="col-md-6">
              <label className="form-label small fw-bold text-muted text-uppercase mb-1">
                Select Classroom Location
              </label>
              <select
                className="form-select border-primary"
                value={selectedLocation}
                onChange={(e) => {
                  setSelectedLocation(e.target.value)
                  fetchClassroomReport(e.target.value)
                }}
              >
                {classrooms.map(rm => (
                  <option key={rm.id} value={rm.name || rm.code}>
                    {rm.name || rm.code} ({rm.building || rm.block || 'Main'})
                  </option>
                ))}
              </select>
            </div>
          </div>

          {loadingClassroomReport ? (
            <div className="text-center py-5">
              <div className="spinner-border text-primary me-2"></div>
              <span className="text-muted">Generating classroom utilization report...</span>
            </div>
          ) : (
            <div className="table-responsive">
              <table className="table align-middle table-hover mb-0">
                <thead className="table-dark text-uppercase small">
                  <tr>
                    <th>Classroom Location</th>
                    <th className="text-center">Total Sessions Conducted</th>
                    <th className="text-center">Total Trainee Logs</th>
                    <th className="text-center text-success">Present</th>
                    <th className="text-center text-warning">Late</th>
                    <th className="text-center text-danger">Absent</th>
                    <th className="text-center text-secondary">Excused / Other</th>
                  </tr>
                </thead>
                <tbody>
                  {classroomReport.length === 0 ? (
                    <tr>
                      <td colSpan="7" className="text-center py-4 text-muted">
                        No attendance records logged for this classroom.
                      </td>
                    </tr>
                  ) : (
                    classroomReport.map((r, i) => (
                      <tr key={i}>
                        <td className="fw-bold">{r.location}</td>
                        <td className="text-center font-monospace fw-bold">{r.total_sessions}</td>
                        <td className="text-center font-monospace">{r.total_records}</td>
                        <td className="text-center text-success fw-bold">{r.present_count}</td>
                        <td className="text-center text-warning fw-bold">{r.late_count}</td>
                        <td className="text-center text-danger fw-bold">{r.absent_count}</td>
                        <td className="text-center text-secondary">{r.other_count}</td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
