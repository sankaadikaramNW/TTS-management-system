import React, { useEffect, useState, useMemo } from 'react'
import axios from 'axios'
import { toast } from 'react-toastify'
import { ClassroomAttendanceRegister } from './ClassroomAttendanceRegister'
import { ClassicalReportModal } from '../../components/ClassicalReportModal'

export const AssessmentManagement = ({ initialTab = 'attendance' }) => {
  const [activeSubTab, setActiveSubTab] = useState(initialTab)
  const [courses, setCourses] = useState([])
  const [selectedCourseId, setSelectedCourseId] = useState('')
  const [exams, setExams] = useState([])
  const [subjects, setSubjects] = useState([])
  const [loading, setLoading] = useState(false)

  // Exam Creation Modal
  const [showExamModal, setShowExamModal] = useState(false)
  const [examForm, setExamForm] = useState({
    subject_id: '',
    type: 'Phase Test',
    date: new Date().toISOString().split('T')[0],
    max_marks: 100,
    pass_marks: 50
  })

  // Integrated Result Sheet / Marks Modal
  const [selectedExam, setSelectedExam] = useState(null)
  const [showReportModal, setShowReportModal] = useState(false)
  const [resultSheetData, setResultSheetData] = useState(null)
  const [examMarks, setExamMarks] = useState([])
  const [showMarksModal, setShowMarksModal] = useState(false)
  const [modalFilter, setModalFilter] = useState('ALL')
  const [modalSearch, setModalSearch] = useState('')
  const [savingMarks, setSavingMarks] = useState(false)

  // Controlled Override Modal
  const [showOverrideModal, setShowOverrideModal] = useState(false)
  const [overrideStudent, setOverrideStudent] = useState(null)
  const [overrideForm, setOverrideForm] = useState({
    reason: '',
    remarks: ''
  })
  const [submittingOverride, setSubmittingOverride] = useState(false)

  const fetchCourses = async () => {
    try {
      const res = await axios.get('/api/v1/academic/courses')
      setCourses(res.data)
      if (res.data.length > 0) {
        setSelectedCourseId(res.data[0].id)
      }
    } catch (err) {
      console.error(err)
    }
  }

  const fetchExamsAndSubjects = async (courseId) => {
    if (!courseId) return
    setLoading(true)
    try {
      const [eRes, sRes] = await Promise.all([
        axios.get(`/api/v1/academic/exams/${courseId}`),
        axios.get(`/api/v1/academic/subjects/${courseId}`)
      ])
      setExams(eRes.data || [])
      setSubjects(sRes.data || [])
    } catch (err) {
      toast.error('Failed to load assessment details')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchCourses()
  }, [])

  useEffect(() => {
    if (selectedCourseId) {
      fetchExamsAndSubjects(selectedCourseId)
    }
  }, [selectedCourseId])

  useEffect(() => {
    setActiveSubTab(initialTab)
  }, [initialTab])

  const handleCreateExam = async (e) => {
    e.preventDefault()
    if (!examForm.subject_id || !selectedCourseId) return
    try {
      await axios.post('/api/v1/academic/exams', {
        ...examForm,
        course_id: selectedCourseId
      })
      toast.success(`${examForm.type} scheduled successfully`)
      setShowExamModal(false)
      fetchExamsAndSubjects(selectedCourseId)
    } catch (err) {
      toast.error('Failed to schedule examination')
    }
  }

  // Load comprehensive result sheet integrated with parade state
  const handleOpenResultSheet = async (ex) => {
    setSelectedExam(ex)
    setModalFilter('ALL')
    setModalSearch('')
    try {
      const res = await axios.get(`/api/v1/academic/exams/${ex.id}/result-sheet`)
      const data = res.data
      setResultSheetData(data)
      // Initialize local marks state for editing
      const studentRecords = (data.students || []).map(st => ({
        student_id: st.student_id,
        service_number: st.service_number,
        student_name: st.student_name,
        rank: st.rank,
        trade: st.trade,
        batch: st.batch,
        parade_state_status: st.parade_state_status,
        is_parade_approved: st.is_parade_approved,
        can_sit_exam: st.can_sit_exam,
        marks_entry_allowed: st.marks_entry_allowed,
        marks_obtained: st.marks_obtained !== null && st.marks_obtained !== undefined ? st.marks_obtained : '',
        result_status: st.result_status,
        remarks: st.remarks || '',
        is_overridden: st.is_overridden,
        override_reason: st.override_reason,
        overridden_by_name: st.overridden_by_name,
        overridden_at: st.overridden_at,
        original_parade_status: st.original_parade_status
      }))
      setExamMarks(studentRecords)
      setShowMarksModal(true)
    } catch (err) {
      console.error('Error loading result sheet:', err)
      toast.error('Failed to load examination result sheet')
    }
  }

  const handleSaveMarks = async (e) => {
    e.preventDefault()
    if (!selectedExam) return
    setSavingMarks(true)
    try {
      // Only submit records that are eligible or have values
      const payload = {
        exam_id: selectedExam.id,
        records: examMarks
          .filter(m => m.marks_entry_allowed || m.is_overridden)
          .map(m => ({
            student_id: m.student_id,
            marks_obtained: m.marks_obtained !== '' && m.marks_obtained !== null ? parseFloat(m.marks_obtained) : null,
            remarks: m.remarks
          }))
      }

      await axios.post('/api/v1/academic/exam-marks', payload)
      toast.success('Official examination results saved successfully')
      
      // Refresh result sheet data
      const res = await axios.get(`/api/v1/academic/exams/${selectedExam.id}/result-sheet`)
      setResultSheetData(res.data)
      setShowMarksModal(false)
      fetchExamsAndSubjects(selectedCourseId)
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Failed to save exam results'
      toast.error(errorMsg)
    } finally {
      setSavingMarks(false)
    }
  }

  // Handle Controlled Officer Override
  const handleOpenOverrideModal = (student) => {
    setOverrideStudent(student)
    setOverrideForm({
      reason: '',
      remarks: ''
    })
    setShowOverrideModal(true)
  }

  const handleSubmitOverride = async (e) => {
    e.preventDefault()
    if (!overrideStudent || !selectedExam) return
    if (!overrideForm.reason.trim()) {
      toast.warning('Please enter a valid override justification reason')
      return
    }

    setSubmittingOverride(true)
    try {
      const res = await axios.post(`/api/v1/academic/exams/${selectedExam.id}/override-eligibility`, {
        student_id: overrideStudent.student_id,
        reason: overrideForm.reason.trim(),
        remarks: overrideForm.remarks.trim() || undefined
      })

      toast.success(`Override authorized for ${overrideStudent.service_number} (${overrideStudent.student_name})`)
      setResultSheetData(res.data)

      // Sync local marks state
      const updatedStudents = (res.data.students || []).map(st => ({
        student_id: st.student_id,
        service_number: st.service_number,
        student_name: st.student_name,
        rank: st.rank,
        trade: st.trade,
        batch: st.batch,
        parade_state_status: st.parade_state_status,
        is_parade_approved: st.is_parade_approved,
        can_sit_exam: st.can_sit_exam,
        marks_entry_allowed: st.marks_entry_allowed,
        marks_obtained: st.marks_obtained !== null && st.marks_obtained !== undefined ? st.marks_obtained : '',
        result_status: st.result_status,
        remarks: st.remarks || '',
        is_overridden: st.is_overridden,
        override_reason: st.override_reason,
        overridden_by_name: st.overridden_by_name,
        overridden_at: st.overridden_at,
        original_parade_status: st.original_parade_status
      }))
      setExamMarks(updatedStudents)
      setShowOverrideModal(false)
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Failed to authorize override'
      toast.error(errorMsg)
    } finally {
      setSubmittingOverride(false)
    }
  }

  // Print Marksheet — Open Classical Official Institutional Result Sheet Modal
  const handlePrintMarksheet = () => {
    setShowReportModal(true)
  }

  // Filtered list of exams for main tabs
  const filteredExams = exams.filter(ex => {
    if (activeSubTab === 'phase-tests') return ex.type === 'Phase Test'
    if (activeSubTab === 'final-exams') return ex.type === 'Final Exam'
    return true
  })

  // Dynamic real-time metrics computed live from user mark inputs
  const liveSummary = useMemo(() => {
    const total = examMarks.length
    const eligible = examMarks.filter(m => m.can_sit_exam || m.is_overridden).length
    const entered = examMarks.filter(m => m.marks_obtained !== '' && m.marks_obtained !== null && !isNaN(parseFloat(m.marks_obtained)))
    const enteredCount = entered.length
    const passMarks = selectedExam?.pass_marks || 50
    const maxMarks = selectedExam?.max_marks || 100
    
    let passedCount = 0
    let failedCount = 0
    let totalMarksSum = 0

    entered.forEach(m => {
      const val = parseFloat(m.marks_obtained)
      totalMarksSum += val
      if (val >= passMarks) {
        passedCount++
      } else {
        failedCount++
      }
    })

    const avgScore = enteredCount > 0 ? (totalMarksSum / enteredCount).toFixed(1) : '0.0'
    const pendingCount = Math.max(0, eligible - enteredCount)
    const passRate = enteredCount > 0 ? Math.round((passedCount / enteredCount) * 100) : 0
    const progressPct = eligible > 0 ? Math.round((enteredCount / eligible) * 100) : 0
    const ineligibleCount = examMarks.filter(m => !m.can_sit_exam && !m.is_overridden).length
    const overriddenCount = examMarks.filter(m => m.is_overridden).length

    return {
      total,
      eligible,
      enteredCount,
      passedCount,
      failedCount,
      pendingCount,
      avgScore,
      passRate,
      progressPct,
      ineligibleCount,
      overriddenCount
    }
  }, [examMarks, selectedExam])

  // Grade classification helper
  const getGradeInfo = (marks, maxMarks, passMarks) => {
    if (marks === '' || marks === null || isNaN(parseFloat(marks))) {
      return null
    }
    const num = parseFloat(marks)
    const pct = maxMarks > 0 ? (num / maxMarks) * 100 : num
    const isPass = num >= passMarks

    if (!isPass) {
      return { grade: 'F', label: 'Fail', color: '#dc2626', bg: '#fef2f2', border: '#fecaca', isPass: false }
    }
    if (pct >= 85) {
      return { grade: 'A+', label: 'Distinction', color: '#15803d', bg: '#dcfce7', border: '#bbf7d0', isPass: true }
    }
    if (pct >= 75) {
      return { grade: 'A', label: 'Distinction', color: '#16a34a', bg: '#dcfce7', border: '#bbf7d0', isPass: true }
    }
    if (pct >= 65) {
      return { grade: 'B', label: 'Credit', color: '#2563eb', bg: '#dbeafe', border: '#bfdbfe', isPass: true }
    }
    return { grade: 'C', label: 'Pass', color: '#4f46e5', bg: '#e0e7ff', border: '#c7d2fe', isPass: true }
  }

  // Batch helper: Auto-fill blank eligible trainees with pass marks
  const handleBatchFillPassMarks = () => {
    if (!selectedExam) return
    const updated = examMarks.map(m => {
      if ((m.can_sit_exam || m.is_overridden) && (m.marks_obtained === '' || m.marks_obtained === null)) {
        return { ...m, marks_obtained: String(selectedExam.pass_marks) }
      }
      return m
    })
    setExamMarks(updated)
    toast.info(`Auto-filled eligible blank entries with pass mark (${selectedExam.pass_marks})`)
  }

  // Batch helper: Clear all entered marks
  const handleClearAllMarks = () => {
    if (window.confirm('Are you sure you want to clear all entered marks?')) {
      const updated = examMarks.map(m => ({ ...m, marks_obtained: '' }))
      setExamMarks(updated)
      toast.info('All marks cleared')
    }
  }

  // Filtered students in modal result sheet
  const filteredModalStudents = useMemo(() => {
    return examMarks.filter(st => {
      // Status filter
      if (modalFilter === 'ELIGIBLE' && !st.can_sit_exam && !st.is_overridden) return false
      if (modalFilter === 'INELIGIBLE' && (st.can_sit_exam || st.is_overridden)) return false
      if (modalFilter === 'ENTERED' && (st.marks_obtained === '' || st.marks_obtained === null)) return false
      if (modalFilter === 'PENDING' && (st.marks_obtained !== '' && st.marks_obtained !== null || (!st.can_sit_exam && !st.is_overridden))) return false
      if (modalFilter === 'PASSED') {
        const num = parseFloat(st.marks_obtained)
        if (isNaN(num) || num < (selectedExam?.pass_marks || 50)) return false
      }
      if (modalFilter === 'FAILED') {
        const num = parseFloat(st.marks_obtained)
        if (isNaN(num) || num >= (selectedExam?.pass_marks || 50)) return false
      }
      if (modalFilter === 'LEAVE' && !st.parade_state_status?.toUpperCase().includes('LEAVE')) return false
      if (modalFilter === 'HOSPITAL' && !st.parade_state_status?.toUpperCase().includes('HOSPITAL')) return false
      if (modalFilter === 'AWOL' && !st.parade_state_status?.toUpperCase().includes('AWOL')) return false
      if (modalFilter === 'COURSE_VISIT' && !st.parade_state_status?.toUpperCase().includes('COURSE') && !st.parade_state_status?.toUpperCase().includes('VISIT')) return false
      if (modalFilter === 'OVERRIDDEN' && !st.is_overridden) return false

      // Search query filter
      if (modalSearch.trim()) {
        const query = modalSearch.toLowerCase()
        const matchNo = st.service_number?.toLowerCase().includes(query)
        const matchName = st.student_name?.toLowerCase().includes(query)
        const matchTrade = st.trade?.toLowerCase().includes(query)
        if (!matchNo && !matchName && !matchTrade) return false
      }

      return true
    })
  }, [examMarks, modalFilter, modalSearch, selectedExam])

  // Badge helpers
  const getParadeStatusBadge = (status, isApproved) => {
    const s = (status || 'Present').toUpperCase()
    let bgClass = 'bg-success-subtle text-success border-success-subtle'
    let icon = 'bi-check-circle-fill'

    if (s.includes('LEAVE')) {
      bgClass = 'bg-warning-subtle text-warning-emphasis border-warning-subtle'
      icon = 'bi-box-arrow-right'
    } else if (s.includes('HOSPITAL')) {
      bgClass = 'bg-danger-subtle text-danger border-danger-subtle'
      icon = 'bi-hospital-fill'
    } else if (s.includes('AWOL')) {
      bgClass = 'bg-danger text-white'
      icon = 'bi-exclamation-triangle-fill'
    } else if (s.includes('COURSE') || s.includes('VISIT')) {
      bgClass = 'bg-info-subtle text-info-emphasis border-info-subtle'
      icon = 'bi-compass-fill'
    } else if (s.includes('SICK')) {
      bgClass = 'bg-warning-subtle text-warning border-warning-subtle'
      icon = 'bi-heart-pulse-fill'
    }

    return (
      <span className={`badge ${bgClass} border d-inline-flex align-items-center text-nowrap px-2.5 py-1`} style={{ gap: '6px' }}>
        <i className={`bi ${icon}`}></i>
        <span className="fw-semibold">{status || 'Present'}</span>
        {isApproved ? (
          <i className="bi bi-shield-fill-check text-success ms-1" title="Approved Parade State"></i>
        ) : (
          <i className="bi bi-clock-history text-muted ms-1" title="Pending Approval"></i>
        )}
      </span>
    )
  }

  const getResultBadge = (resultStatus, isPass, marksVal) => {
    const r = (resultStatus || '').toUpperCase()
    if (r === 'PASS') {
      return <span className="badge bg-success text-white px-2.5 py-1 fw-bold"><i className="bi bi-check2 me-1"></i>PASS</span>
    }
    if (r === 'FAIL') {
      return <span className="badge bg-danger text-white px-2.5 py-1 fw-bold"><i className="bi bi-x me-1"></i>FAIL</span>
    }
    if (r === 'LEAVE') {
      return <span className="badge bg-warning text-dark px-2.5 py-1 fw-semibold"><i className="bi bi-person-x me-1"></i>LEAVE</span>
    }
    if (r === 'IN HOSPITAL' || r === 'HOSPITAL') {
      return <span className="badge bg-danger-subtle text-danger border px-2.5 py-1 fw-semibold"><i className="bi bi-hospital me-1"></i>IN HOSPITAL</span>
    }
    if (r === 'AWOL') {
      return <span className="badge bg-dark text-white px-2.5 py-1 fw-bold"><i className="bi bi-exclamation-diamond me-1"></i>AWOL</span>
    }
    if (r === 'COURSE VISIT') {
      return <span className="badge bg-info text-dark px-2.5 py-1 fw-semibold"><i className="bi bi-geo-alt me-1"></i>COURSE VISIT</span>
    }
    if (r === 'SICK REPORT') {
      return <span className="badge bg-warning-subtle text-dark border px-2.5 py-1 fw-semibold"><i className="bi bi-bandaid me-1"></i>SICK REPORT</span>
    }
    return <span className="badge bg-secondary-subtle text-muted border px-2 py-1">{r || 'ELIGIBLE'}</span>
  }

  return (
    <div className="fade-in-slide">
      {/* Header */}
      <div className="d-flex justify-content-between align-items-center mb-3">
        <div>
          <h5 className="fw-bold text-dark mb-0 display-font">Assessment & Examination Center</h5>
          <small className="text-muted">Integrated Attendance Registers, Phase Tests, Final Examinations & Official Marksheets</small>
        </div>
      </div>

      {/* Course Selector & Actions */}
      <div className="card slaf-card p-3 mb-3 shadow-sm border-0 bg-white">
        <div className="row align-items-center g-2">
          <div className="col-md-3">
            <label className="fw-bold text-dark small">Select Course / Specialization:</label>
          </div>
          <div className="col-md-6">
            <select 
              className="form-select form-select-sm fw-semibold"
              value={selectedCourseId}
              onChange={(e) => setSelectedCourseId(e.target.value)}
            >
              {courses.map(c => (
                <option key={c.id} value={c.id}>{c.name} ({c.code})</option>
              ))}
            </select>
          </div>
          <div className="col-md-3 text-end">
            {(activeSubTab === 'phase-tests' || activeSubTab === 'final-exams') && (
              <button className="btn btn-primary btn-sm fw-semibold shadow-sm" onClick={() => setShowExamModal(true)}>
                <i className="bi bi-journal-plus me-1"></i> Schedule Exam
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Sub Tabs */}
      <ul className="nav nav-pills custom-pills mb-3 border-bottom pb-2">
        <li className="nav-item">
          <button className={`nav-link btn-sm ${activeSubTab === 'attendance' ? 'active fw-bold' : ''}`} onClick={() => setActiveSubTab('attendance')}>
            <i className="bi bi-calendar-check me-1.5"></i> Class Attendance
          </button>
        </li>
        <li className="nav-item">
          <button className={`nav-link btn-sm ${activeSubTab === 'phase-tests' ? 'active fw-bold' : ''}`} onClick={() => setActiveSubTab('phase-tests')}>
            <i className="bi bi-file-earmark-code me-1.5"></i> Phase Tests
          </button>
        </li>
        <li className="nav-item">
          <button className={`nav-link btn-sm ${activeSubTab === 'final-exams' ? 'active fw-bold' : ''}`} onClick={() => setActiveSubTab('final-exams')}>
            <i className="bi bi-award me-1.5"></i> Final Examinations
          </button>
        </li>
        <li className="nav-item">
          <button className={`nav-link btn-sm ${activeSubTab === 'results' ? 'active fw-bold' : ''}`} onClick={() => setActiveSubTab('results')}>
            <i className="bi bi-bar-chart-line me-1.5"></i> Result Sheets & Marksheets
          </button>
        </li>
      </ul>

      {/* Sub Tab 1: Attendance */}
      {activeSubTab === 'attendance' && (
        <ClassroomAttendanceRegister />
      )}

      {/* Sub Tab 2 & 3: Phase Tests & Final Exams */}
      {(activeSubTab === 'phase-tests' || activeSubTab === 'final-exams') && (
        <div className="card slaf-card p-0 shadow-sm border-0">
          <div className="table-responsive">
            <table className="table slaf-table align-middle mb-0">
              <thead className="bg-light">
                <tr>
                  <th>Exam Title / Type</th>
                  <th>Subject</th>
                  <th>Scheduled Date</th>
                  <th>Max Marks</th>
                  <th>Pass Marks</th>
                  <th className="text-end">Action</th>
                </tr>
              </thead>
              <tbody>
                {loading ? (
                  <tr><td colSpan="6" className="text-center py-5"><div className="spinner-border spinner-border-sm text-primary"></div></td></tr>
                ) : filteredExams.length === 0 ? (
                  <tr><td colSpan="6" className="text-center py-5 text-muted">No examinations scheduled for this course view.</td></tr>
                ) : (
                  filteredExams.map(ex => (
                    <tr key={ex.id}>
                      <td><span className="badge bg-primary-subtle text-primary border fw-bold">{ex.type}</span></td>
                      <td><strong className="text-dark">{ex.subject_name}</strong></td>
                      <td><small className="text-muted"><i className="bi bi-calendar-event me-1 text-primary"></i>{ex.date}</small></td>
                      <td><span className="badge bg-secondary-subtle text-dark border">{ex.max_marks} Marks</span></td>
                      <td><span className="badge bg-success-subtle text-success border">{ex.pass_marks} Pass</span></td>
                      <td className="text-end">
                        <button className="btn btn-primary btn-sm fw-semibold shadow-sm" onClick={() => handleOpenResultSheet(ex)}>
                          <i className="bi bi-pencil-square me-1"></i> Result Sheet
                        </button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Sub Tab 4: Results & Marksheets */}
      {activeSubTab === 'results' && (
        <div className="card slaf-card p-3 shadow-sm border-0">
          <div className="d-flex justify-content-between align-items-center mb-3">
            <div>
              <h6 className="fw-bold text-dark mb-0"><i className="bi bi-bar-chart-fill me-2 text-success"></i>Official Academic Marksheets & Performance Registers</h6>
              <small className="text-muted">Seamlessly integrated with Trade Daily Parade State attendance authorizations</small>
            </div>
          </div>
          <div className="table-responsive">
            <table className="table slaf-table align-middle mb-0">
              <thead className="bg-light">
                <tr>
                  <th>Exam Title</th>
                  <th>Subject</th>
                  <th>Scheduled Date</th>
                  <th>Status Integration</th>
                  <th className="text-end">Action</th>
                </tr>
              </thead>
              <tbody>
                {exams.length === 0 ? (
                  <tr><td colSpan="5" className="text-center py-4 text-muted">No exams available for result viewing.</td></tr>
                ) : (
                  exams.map(ex => (
                    <tr key={ex.id}>
                      <td>
                        <strong className="text-dark d-block">{ex.type}</strong>
                        <small className="text-muted">Course ID: {ex.course_id.substring(0, 8)}...</small>
                      </td>
                      <td><span className="fw-semibold text-primary">{ex.subject_name}</span></td>
                      <td><small className="text-muted"><i className="bi bi-calendar3 me-1"></i>{ex.date}</small></td>
                      <td>
                        <span className="badge bg-info-subtle text-info border">
                          <i className="bi bi-shield-check me-1"></i>Parade State Linked
                        </span>
                      </td>
                      <td className="text-end">
                        <button className="btn btn-outline-primary btn-sm fw-semibold" onClick={() => handleOpenResultSheet(ex)}>
                          <i className="bi bi-journal-text me-1"></i> Open Result Sheet
                        </button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Create Exam Modal */}
      {showExamModal && (
        <div className="modal fade show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)', zIndex: 1060 }}>
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content slaf-card shadow-lg border-0">
              <div className="modal-header border-bottom bg-light">
                <h5 className="modal-title display-font text-primary fw-bold">
                  <i className="bi bi-calendar-plus me-2"></i>Schedule Examination
                </h5>
                <button type="button" className="btn-close" onClick={() => setShowExamModal(false)}></button>
              </div>
              <form onSubmit={handleCreateExam}>
                <div className="modal-body p-4">
                  <div className="mb-3">
                    <label className="form-label small fw-bold text-dark">Exam Type*</label>
                    <select className="form-select" value={examForm.type} onChange={(e) => setExamForm({ ...examForm, type: e.target.value })}>
                      <option value="Phase Test">Phase Test</option>
                      <option value="Final Exam">Final Examination</option>
                    </select>
                  </div>
                  <div className="mb-3">
                    <label className="form-label small fw-bold text-dark">Select Subject / Module*</label>
                    <select className="form-select" value={examForm.subject_id} onChange={(e) => setExamForm({ ...examForm, subject_id: e.target.value })} required>
                      <option value="">-- Select Subject --</option>
                      {subjects.map(s => (
                        <option key={s.id} value={s.id}>{s.name} ({s.code})</option>
                      ))}
                    </select>
                  </div>
                  <div className="mb-3">
                    <label className="form-label small fw-bold text-dark">Exam Date*</label>
                    <input type="date" className="form-control" value={examForm.date} onChange={(e) => setExamForm({ ...examForm, date: e.target.value })} required />
                    <small className="text-muted" style={{ fontSize: '0.75rem' }}>
                      <i className="bi bi-info-circle me-1"></i>Trainees' approved Parade State on this specific date will automatically dictate exam eligibility.
                    </small>
                  </div>
                  <div className="row g-2">
                    <div className="col-6">
                      <label className="form-label small fw-bold text-dark">Max Marks</label>
                      <input type="number" className="form-control" value={examForm.max_marks} onChange={(e) => setExamForm({ ...examForm, max_marks: parseFloat(e.target.value) || 0 })} />
                    </div>
                    <div className="col-6">
                      <label className="form-label small fw-bold text-dark">Pass Marks</label>
                      <input type="number" className="form-control" value={examForm.pass_marks} onChange={(e) => setExamForm({ ...examForm, pass_marks: parseFloat(e.target.value) || 0 })} />
                    </div>
                  </div>
                </div>
                <div className="modal-footer border-top bg-light">
                  <button type="button" className="btn btn-outline-secondary btn-sm" onClick={() => setShowExamModal(false)}>Cancel</button>
                  <button type="submit" className="btn btn-primary btn-sm fw-semibold shadow-sm">Schedule Exam</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Comprehensive Result Sheet Modal */}
      {showMarksModal && selectedExam && resultSheetData && (
        <div className="modal fade show d-block" style={{ backgroundColor: 'rgba(15, 23, 42, 0.75)', zIndex: 1060, overflowY: 'auto' }}>
          <div className="modal-dialog modal-dialog-centered modal-xl" style={{ maxWidth: 'min(98vw, 1500px)', width: '98%', height: '92vh', margin: '4vh auto' }}>
            <div className="modal-content slaf-card shadow-2xl border-0 overflow-hidden" style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              {/* Header */}
              <div className="modal-header bg-dark text-white py-3 px-4 border-bottom border-secondary flex-shrink-0 d-flex flex-wrap align-items-center justify-content-between gap-3">
                <div className="d-flex align-items-center gap-3">
                  <div className="bg-primary bg-opacity-25 text-primary rounded-3 p-2 d-flex align-items-center justify-content-center flex-shrink-0" style={{ width: '44px', height: '44px' }}>
                    <i className="bi bi-journal-check fs-4 text-info"></i>
                  </div>
                  <div>
                    <div className="d-flex align-items-center flex-wrap gap-2">
                      <h5 className="modal-title fw-bold text-white mb-0" style={{ letterSpacing: '0.2px' }}>
                        {resultSheetData.exam_type}: {resultSheetData.subject_name}
                      </h5>
                      <span className="badge bg-primary text-white border border-primary-subtle px-2.5 py-1">
                        {resultSheetData.course_name} {resultSheetData.course_code ? `(${resultSheetData.course_code})` : ''}
                      </span>
                      <span className="badge bg-secondary text-white border border-secondary px-2.5 py-1">
                        Batch: {selectedExam.batch_name || 'All'}
                      </span>
                    </div>
                    <div className="d-flex align-items-center flex-wrap gap-3 mt-1 text-white-50" style={{ fontSize: '0.8rem' }}>
                      <span><i className="bi bi-calendar-event text-info me-1"></i>Exam Date: <strong className="text-light">{resultSheetData.exam_date}</strong></span>
                      <span><i className="bi bi-award text-warning me-1"></i>Max Marks: <strong className="text-light">{resultSheetData.max_marks}</strong></span>
                      <span><i className="bi bi-check2-circle text-success me-1"></i>Pass Marks: <strong className="text-light">{resultSheetData.pass_marks}</strong></span>
                      <span>
                        {resultSheetData.is_parade_approved ? (
                          <span className="badge bg-success bg-opacity-25 text-success border border-success px-2 py-0.5">
                            <i className="bi bi-shield-fill-check me-1"></i>Parade State Approved (SSOT Linked)
                          </span>
                        ) : (
                          <span className="badge bg-warning bg-opacity-25 text-warning border border-warning px-2 py-0.5">
                            <i className="bi bi-exclamation-triangle-fill me-1"></i>Parade State: {resultSheetData.parade_submission_status}
                          </span>
                        )}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="d-flex align-items-center gap-2 ms-auto flex-shrink-0">
                  <button type="button" className="btn btn-outline-light btn-sm fw-semibold d-inline-flex align-items-center gap-1.5 shadow-xs" onClick={handlePrintMarksheet} title="Print Formal Marksheet">
                    <i className="bi bi-printer"></i>
                    <span>Formal Report</span>
                  </button>
                  <button
                    type="button"
                    className="btn btn-sm btn-outline-light border-0 ms-1 flex-shrink-0 d-flex align-items-center justify-content-center"
                    onClick={() => setShowMarksModal(false)}
                    title="Close Modal"
                    style={{ width: '34px', height: '34px', borderRadius: '6px' }}
                  >
                    <i className="bi bi-x-lg fs-6"></i>
                  </button>
                </div>
              </div>

              {/* Live Metric Strip */}
              <div className="px-4 py-2.5 bg-light border-bottom flex-shrink-0">
                <div className="row g-2 align-items-center text-center">
                  <div className="col-6 col-sm-4 col-md-2">
                    <div className="p-2 rounded bg-white border shadow-xs">
                      <small className="text-muted d-block fw-semibold" style={{ fontSize: '0.68rem', letterSpacing: '0.5px' }}>TOTAL TRAINEES</small>
                      <strong className="fs-5 text-dark">{liveSummary.total}</strong>
                    </div>
                  </div>
                  <div className="col-6 col-sm-4 col-md-2">
                    <div className="p-2 rounded bg-white border shadow-xs">
                      <small className="text-success d-block fw-semibold" style={{ fontSize: '0.68rem', letterSpacing: '0.5px' }}>ELIGIBLE TO SIT</small>
                      <strong className="fs-5 text-success">{liveSummary.eligible}</strong>
                    </div>
                  </div>
                  <div className="col-6 col-sm-4 col-md-2">
                    <div className="p-2 rounded bg-white border shadow-xs">
                      <small className="text-primary d-block fw-semibold" style={{ fontSize: '0.68rem', letterSpacing: '0.5px' }}>MARKS ENTERED</small>
                      <strong className="fs-5 text-primary">{liveSummary.enteredCount} <small className="fs-7 text-muted fw-normal">/ {liveSummary.eligible}</small></strong>
                    </div>
                  </div>
                  <div className="col-6 col-sm-4 col-md-2">
                    <div className="p-2 rounded bg-white border shadow-xs">
                      <small className="text-success d-block fw-semibold" style={{ fontSize: '0.68rem', letterSpacing: '0.5px' }}>PASSED</small>
                      <strong className="fs-5 text-success">{liveSummary.passedCount} <small className="fs-7 text-muted fw-normal">({liveSummary.passRate}%)</small></strong>
                    </div>
                  </div>
                  <div className="col-6 col-sm-4 col-md-2">
                    <div className="p-2 rounded bg-white border shadow-xs">
                      <small className="text-danger d-block fw-semibold" style={{ fontSize: '0.68rem', letterSpacing: '0.5px' }}>FAILED</small>
                      <strong className="fs-5 text-danger">{liveSummary.failedCount}</strong>
                    </div>
                  </div>
                  <div className="col-6 col-sm-4 col-md-2">
                    <div className="p-2 rounded bg-white border shadow-xs">
                      <small className="text-muted d-block fw-semibold" style={{ fontSize: '0.68rem', letterSpacing: '0.5px' }}>AVG SCORE</small>
                      <strong className="fs-5 text-dark">{liveSummary.avgScore}%</strong>
                    </div>
                  </div>
                </div>
              </div>

              {/* Filter Controls & Search */}
              <div className="px-4 py-2 bg-white border-bottom d-flex flex-wrap justify-content-between align-items-center gap-2 flex-shrink-0">
                <div className="d-flex flex-wrap align-items-center gap-1.5">
                  <small className="text-muted fw-bold me-1">View:</small>
                  <button 
                    type="button" 
                    className={`btn btn-xs rounded-pill px-2.5 py-1 ${modalFilter === 'ALL' ? 'btn-primary fw-bold' : 'btn-outline-secondary'}`}
                    onClick={() => setModalFilter('ALL')}
                    style={{ fontSize: '0.75rem' }}
                  >
                    All ({examMarks.length})
                  </button>
                  <button 
                    type="button" 
                    className={`btn btn-xs rounded-pill px-2.5 py-1 ${modalFilter === 'ELIGIBLE' ? 'btn-success text-white fw-bold' : 'btn-outline-success'}`}
                    onClick={() => setModalFilter('ELIGIBLE')}
                    style={{ fontSize: '0.75rem' }}
                  >
                    Eligible ({liveSummary.eligible})
                  </button>
                  <button 
                    type="button" 
                    className={`btn btn-xs rounded-pill px-2.5 py-1 ${modalFilter === 'ENTERED' ? 'btn-primary text-white fw-bold' : 'btn-outline-primary'}`}
                    onClick={() => setModalFilter('ENTERED')}
                    style={{ fontSize: '0.75rem' }}
                  >
                    Entered ({liveSummary.enteredCount})
                  </button>
                  {liveSummary.pendingCount > 0 && (
                    <button 
                      type="button" 
                      className={`btn btn-xs rounded-pill px-2.5 py-1 ${modalFilter === 'PENDING' ? 'btn-warning text-dark fw-bold' : 'btn-outline-warning text-dark'}`}
                      onClick={() => setModalFilter('PENDING')}
                      style={{ fontSize: '0.75rem' }}
                    >
                      Pending ({liveSummary.pendingCount})
                    </button>
                  )}
                  <button 
                    type="button" 
                    className={`btn btn-xs rounded-pill px-2.5 py-1 ${modalFilter === 'PASSED' ? 'btn-success text-white fw-bold' : 'btn-outline-success'}`}
                    onClick={() => setModalFilter('PASSED')}
                    style={{ fontSize: '0.75rem' }}
                  >
                    Passed ({liveSummary.passedCount})
                  </button>
                  <button 
                    type="button" 
                    className={`btn btn-xs rounded-pill px-2.5 py-1 ${modalFilter === 'FAILED' ? 'btn-danger text-white fw-bold' : 'btn-outline-danger'}`}
                    onClick={() => setModalFilter('FAILED')}
                    style={{ fontSize: '0.75rem' }}
                  >
                    Failed ({liveSummary.failedCount})
                  </button>
                  {liveSummary.ineligibleCount > 0 && (
                    <button 
                      type="button" 
                      className={`btn btn-xs rounded-pill px-2.5 py-1 ${modalFilter === 'INELIGIBLE' ? 'btn-danger text-white fw-bold' : 'btn-outline-danger'}`}
                      onClick={() => setModalFilter('INELIGIBLE')}
                      style={{ fontSize: '0.75rem' }}
                    >
                      Ineligible ({liveSummary.ineligibleCount})
                    </button>
                  )}
                  {liveSummary.overriddenCount > 0 && (
                    <button 
                      type="button" 
                      className={`btn btn-xs rounded-pill px-2.5 py-1 ${modalFilter === 'OVERRIDDEN' ? 'btn-info text-dark fw-bold' : 'btn-outline-info'}`}
                      onClick={() => setModalFilter('OVERRIDDEN')}
                      style={{ fontSize: '0.75rem' }}
                    >
                      Overridden ({liveSummary.overriddenCount})
                    </button>
                  )}
                </div>

                <div className="d-flex align-items-center gap-2 ms-auto flex-wrap">
                  {/* Quick Auto Fill Button */}
                  <button 
                    className="btn btn-outline-secondary btn-sm py-1 px-2.5 d-inline-flex align-items-center gap-1 shadow-xs" 
                    style={{ fontSize: '0.78rem' }} 
                    type="button" 
                    onClick={handleBatchFillPassMarks}
                    title={`Auto-fill eligible blanks with pass marks (${selectedExam.pass_marks})`}
                  >
                    <i className="bi bi-magic text-primary"></i>
                    <span>Fill Pass Mark</span>
                  </button>

                  {/* Search Box */}
                  <div className="input-group input-group-sm" style={{ width: '220px' }}>
                    <span className="input-group-text bg-white border-end-0 text-muted"><i className="bi bi-search"></i></span>
                    <input 
                      type="text" 
                      className="form-control border-start-0" 
                      placeholder="Filter trainee name / no..."
                      value={modalSearch}
                      onChange={(e) => setModalSearch(e.target.value)}
                    />
                    {modalSearch && (
                      <button className="btn btn-outline-secondary border-start-0 bg-white" type="button" onClick={() => setModalSearch('')}>
                        <i className="bi bi-x"></i>
                      </button>
                    )}
                  </div>
                </div>
              </div>

              {/* Marksheet Form & Interactive Table */}
              <form onSubmit={handleSaveMarks} style={{ display: 'flex', flexDirection: 'column', flex: 1, minHeight: 0, overflow: 'hidden' }}>
                <div className="table-responsive" style={{ flex: 1, minHeight: 0, overflowY: 'auto', overflowX: 'auto', width: '100%' }}>
                  <table className="table table-hover align-middle mb-0" style={{ fontSize: '0.875rem' }}>
                    <thead className="table-light sticky-top shadow-xs" style={{ zIndex: 10 }}>
                      <tr>
                        <th style={{ minWidth: '100px', width: '110px', padding: '12px 14px' }}>Service No</th>
                        <th style={{ minWidth: '220px', padding: '12px 14px' }}>Trainee Full Name</th>
                        <th style={{ minWidth: '130px', padding: '12px 14px' }}>Trade / Batch</th>
                        <th style={{ minWidth: '160px', padding: '12px 14px' }}>Parade State</th>
                        <th style={{ minWidth: '130px', padding: '12px 14px' }}>Eligibility</th>
                        <th style={{ minWidth: '150px', width: '160px', padding: '12px 14px', textAlign: 'center' }}>Marks Obtained</th>
                        <th style={{ minWidth: '150px', padding: '12px 14px', textAlign: 'center' }}>Result & Grade</th>
                        <th style={{ minWidth: '220px', padding: '12px 14px' }}>Remarks & Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {filteredModalStudents.length === 0 ? (
                        <tr>
                          <td colSpan="8" className="text-center py-5 text-muted">
                            <i className="bi bi-inbox fs-2 d-block mb-2 text-muted"></i>
                            No trainees match the selected filter criteria.
                          </td>
                        </tr>
                      ) : (
                        filteredModalStudents.map((st) => {
                          const originalIdx = examMarks.findIndex(m => m.student_id === st.student_id)
                          const marksNum = parseFloat(st.marks_obtained)
                          const hasValidMarks = !isNaN(marksNum) && st.marks_obtained !== '' && st.marks_obtained !== null
                          const isPass = hasValidMarks && marksNum >= selectedExam.pass_marks
                          const isOverMax = hasValidMarks && marksNum > selectedExam.max_marks
                          const isUnderZero = hasValidMarks && marksNum < 0
                          const isInvalidInput = isOverMax || isUnderZero
                          const gradeInfo = getGradeInfo(st.marks_obtained, selectedExam.max_marks, selectedExam.pass_marks)

                          return (
                            <tr key={st.student_id} className={`marks-row-active ${!st.can_sit_exam && !st.is_overridden ? 'marks-row-disabled' : ''}`}>
                              {/* 1. Service No */}
                              <td className="px-3 py-2.5">
                                <span className="badge bg-primary-subtle text-primary border font-monospace px-2 py-1 fw-bold" style={{ fontSize: '0.82rem' }}>
                                  {st.service_number}
                                </span>
                              </td>

                              {/* 2. Trainee Name */}
                              <td className="px-3 py-2.5">
                                <div className="d-flex align-items-center gap-2">
                                  <div className="bg-light rounded-circle d-flex align-items-center justify-content-center border flex-shrink-0 text-dark fw-bold" style={{ width: '28px', height: '28px', fontSize: '0.72rem' }}>
                                    {st.rank || 'LAC'}
                                  </div>
                                  <div>
                                    <div className="fw-bold text-dark" style={{ lineHeight: '1.2' }}>{st.student_name}</div>
                                    <small className="text-muted" style={{ fontSize: '0.72rem' }}>Rank: {st.rank || 'LAC'}</small>
                                  </div>
                                </div>
                              </td>

                              {/* 3. Trade & Batch */}
                              <td className="px-3 py-2.5">
                                <div className="fw-medium text-dark" style={{ fontSize: '0.82rem' }}>{st.trade || 'General'}</div>
                                <span className="badge bg-light text-muted border" style={{ fontSize: '0.675rem' }}>Batch {st.batch || '26/1'}</span>
                              </td>

                              {/* 4. Parade State Status */}
                              <td className="px-3 py-2.5">
                                {getParadeStatusBadge(st.parade_state_status, st.is_parade_approved)}
                              </td>

                              {/* 5. Exam Eligibility */}
                              <td className="px-3 py-2.5">
                                {st.is_overridden ? (
                                  <div>
                                    <span className="badge bg-primary-subtle text-primary border" title={st.override_reason}>
                                      <i className="bi bi-key-fill me-1"></i>Overridden
                                    </span>
                                    <small className="d-block text-muted" style={{ fontSize: '0.675rem' }}>
                                      by {st.overridden_by_name || 'Officer'}
                                    </small>
                                  </div>
                                ) : st.can_sit_exam ? (
                                  <span className="badge bg-success-subtle text-success border px-2 py-1">
                                    <i className="bi bi-check-circle-fill me-1"></i>Eligible
                                  </span>
                                ) : (
                                  <span className="badge bg-danger-subtle text-danger border px-2 py-1" title={`Trainee recorded as ${st.parade_state_status} in approved Parade State`}>
                                    <i className="bi bi-x-circle-fill me-1"></i>Ineligible
                                  </span>
                                )}
                              </td>

                              {/* 6. Marks Obtained Input (Modern, keyboard-optimized) */}
                              <td className="px-3 py-2.5 text-center">
                                {st.marks_entry_allowed || st.is_overridden ? (
                                  <div className="d-inline-block" style={{ width: '120px' }}>
                                    <div className="input-group input-group-sm shadow-xs">
                                      <input 
                                        type="number"
                                        id={`mark-input-${originalIdx}`}
                                        step="0.5"
                                        min="0"
                                        max={selectedExam.max_marks}
                                        placeholder="—"
                                        className={`form-control form-control-sm text-center fw-bold marks-input-modern ${isInvalidInput ? 'is-invalid-mark' : ''}`}
                                        style={{
                                          fontSize: '1rem',
                                          backgroundColor: hasValidMarks ? (isPass ? '#f0fdf4' : '#fef2f2') : '#f8fafc',
                                          borderColor: hasValidMarks ? (isPass ? '#86efac' : '#fca5a5') : '#cbd5e1'
                                        }}
                                        value={st.marks_obtained}
                                        onChange={(e) => {
                                          const updated = [...examMarks]
                                          updated[originalIdx].marks_obtained = e.target.value
                                          setExamMarks(updated)
                                        }}
                                        onKeyDown={(e) => {
                                          if (e.key === 'Enter') {
                                            e.preventDefault()
                                            const nextInput = document.getElementById(`mark-input-${originalIdx + 1}`)
                                            if (nextInput) nextInput.focus()
                                          }
                                        }}
                                      />
                                      <span className="input-group-text bg-light text-muted border-start-0 px-1.5" style={{ fontSize: '0.72rem' }}>
                                        /{selectedExam.max_marks}
                                      </span>
                                    </div>
                                    {isOverMax && (
                                      <small className="text-danger d-block fw-semibold" style={{ fontSize: '0.675rem' }}>
                                        Max is {selectedExam.max_marks}
                                      </small>
                                    )}
                                  </div>
                                ) : (
                                  <div className="text-center">
                                    <span className="badge bg-secondary-subtle text-muted border px-2.5 py-1 font-monospace">--</span>
                                    <small className="d-block text-muted" style={{ fontSize: '0.675rem' }}>
                                      Locked ({st.parade_state_status})
                                    </small>
                                  </div>
                                )}
                              </td>

                              {/* 7. Result Status & Grade Badge */}
                              <td className="px-3 py-2.5 text-center">
                                {hasValidMarks && gradeInfo ? (
                                  <div className="d-inline-flex flex-column align-items-center gap-0.5">
                                    <span
                                      className="badge fw-bold px-2.5 py-1 d-inline-flex align-items-center gap-1 shadow-xs"
                                      style={{
                                        backgroundColor: gradeInfo.bg,
                                        color: gradeInfo.color,
                                        border: `1px solid ${gradeInfo.border}`,
                                        fontSize: '0.8rem'
                                      }}
                                    >
                                      <i className={`bi ${gradeInfo.isPass ? 'bi-check2-circle' : 'bi-x-circle'}`}></i>
                                      {gradeInfo.isPass ? 'PASS' : 'FAIL'} ({gradeInfo.grade})
                                    </span>
                                    <small className="text-muted" style={{ fontSize: '0.7rem' }}>
                                      {((marksNum / selectedExam.max_marks) * 100).toFixed(0)}% • {gradeInfo.label}
                                    </small>
                                  </div>
                                ) : (
                                  <div>
                                    {st.can_sit_exam || st.is_overridden ? (
                                      <span className="badge bg-light text-muted border px-2 py-1" style={{ fontSize: '0.75rem' }}>
                                        <i className="bi bi-clock me-1"></i>Awaiting Marks
                                      </span>
                                    ) : (
                                      getResultBadge(st.result_status || st.parade_state_status, false, null)
                                    )}
                                  </div>
                                )}
                              </td>

                              {/* 8. Remarks & Controlled Override Action */}
                              <td className="px-3 py-2.5">
                                <div className="d-flex align-items-center gap-1.5">
                                  <input 
                                    type="text" 
                                    className="form-control form-control-sm" 
                                    placeholder="Optional remarks..."
                                    value={st.remarks}
                                    onChange={(e) => {
                                      const updated = [...examMarks]
                                      updated[originalIdx].remarks = e.target.value
                                      setExamMarks(updated)
                                    }}
                                    style={{ minWidth: '120px' }}
                                  />
                                  {!st.can_sit_exam && !st.is_overridden && (
                                    <button 
                                      type="button" 
                                      className="btn btn-outline-warning btn-sm text-nowrap px-2.5 py-1 fw-semibold d-inline-flex align-items-center gap-1 shadow-xs"
                                      onClick={() => handleOpenOverrideModal(st)}
                                      title="Authorize officer override for this trainee"
                                      style={{ fontSize: '0.75rem' }}
                                    >
                                      <i className="bi bi-shield-lock-fill"></i> Override
                                    </button>
                                  )}
                                </div>
                              </td>
                            </tr>
                          )
                        })
                      )}
                    </tbody>
                  </table>
                </div>

                {/* Modal Footer (Sticky, Perfectly Visible, Uncut) */}
                <div className="modal-footer border-top bg-white py-2.5 px-4 d-flex flex-wrap align-items-center justify-content-between gap-3 flex-shrink-0 shadow-lg">
                  <div className="d-flex align-items-center flex-wrap gap-3">
                    <div className="small text-muted d-flex align-items-center gap-1.5">
                      <i className="bi bi-shield-check text-primary fs-6"></i>
                      <span>Parade State SSOT: <strong>{resultSheetData.exam_date}</strong></span>
                    </div>

                    <div className="vr d-none d-md-block" style={{ height: '18px' }}></div>

                    <div className="d-flex align-items-center gap-2">
                      <span className="small text-dark fw-semibold">
                        Progress: {liveSummary.enteredCount} / {liveSummary.eligible} ({liveSummary.progressPct}%)
                      </span>
                      <div className="progress" style={{ width: '100px', height: '6px' }}>
                        <div 
                          className={`progress-bar ${liveSummary.progressPct === 100 ? 'bg-success' : 'bg-primary'}`} 
                          role="progressbar" 
                          style={{ width: `${liveSummary.progressPct}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>

                  <div className="d-flex align-items-center gap-2 ms-auto">
                    <button type="button" className="btn btn-outline-secondary btn-sm px-3 fw-semibold" onClick={() => setShowMarksModal(false)}>
                      Close
                    </button>
                    <button 
                      type="submit" 
                      className="btn btn-primary btn-sm fw-bold shadow-sm px-4 py-1.5 d-inline-flex align-items-center gap-2"
                      disabled={savingMarks}
                      style={{
                        background: 'linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%)',
                        border: 'none'
                      }}
                    >
                      {savingMarks ? (
                        <>
                          <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                          <span>Saving Official Marksheet...</span>
                        </>
                      ) : (
                        <>
                          <i className="bi bi-cloud-check-fill fs-6"></i>
                          <span>Save Official Marksheet</span>
                          {liveSummary.enteredCount > 0 && (
                            <span className="badge bg-white text-primary rounded-pill px-2 py-0.5" style={{ fontSize: '0.72rem' }}>
                              {liveSummary.enteredCount} Records
                            </span>
                          )}
                        </>
                      )}
                    </button>
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Controlled Officer Override Modal */}
      {showOverrideModal && overrideStudent && (
        <div className="modal fade show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.65)', zIndex: 1070 }}>
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content slaf-card shadow-lg border-0">
              <div className="modal-header border-bottom bg-warning-subtle py-2.5 px-3">
                <h6 className="modal-title display-font text-dark fw-bold mb-0">
                  <i className="bi bi-shield-lock-fill text-warning me-2"></i>Authorize Examination Eligibility Override
                </h6>
                <button type="button" className="btn-close" onClick={() => setShowOverrideModal(false)}></button>
              </div>
              <form onSubmit={handleSubmitOverride}>
                <div className="modal-body p-3">
                  <div className="alert alert-warning py-2 px-3 mb-3 border" style={{ fontSize: '0.8rem' }}>
                    <i className="bi bi-exclamation-triangle-fill me-1.5"></i>
                    <strong>Official Audit Notice:</strong> This action allows an ineligible trainee (status: <strong>{overrideStudent.parade_state_status}</strong>) to sit the examination. All overrides are permanently recorded in the system audit trail.
                  </div>

                  <div className="bg-light p-2.5 rounded mb-3 border">
                    <div className="row g-1 text-sm">
                      <div className="col-5 text-muted small">Trainee:</div>
                      <div className="col-7 fw-bold">{overrideStudent.rank} {overrideStudent.student_name}</div>
                      <div className="col-5 text-muted small">Service Number:</div>
                      <div className="col-7 font-monospace fw-bold text-primary">{overrideStudent.service_number}</div>
                      <div className="col-5 text-muted small">Parade Status on Exam Date:</div>
                      <div className="col-7 fw-bold text-danger">{overrideStudent.parade_state_status}</div>
                    </div>
                  </div>

                  <div className="mb-3">
                    <label className="form-label small fw-bold text-dark">
                      Mandatory Justification Reason*
                    </label>
                    <textarea 
                      className="form-control form-control-sm"
                      rows="3"
                      placeholder="Enter official justification (e.g. Special medical clearance granted by Senior Medical Officer, Executive approval by OC Training)..."
                      value={overrideForm.reason}
                      onChange={(e) => setOverrideForm({ ...overrideForm, reason: e.target.value })}
                      required
                    ></textarea>
                  </div>

                  <div className="mb-2">
                    <label className="form-label small fw-bold text-dark">
                      Optional Remarks
                    </label>
                    <input 
                      type="text" 
                      className="form-control form-control-sm"
                      placeholder="Additional notes..."
                      value={overrideForm.remarks}
                      onChange={(e) => setOverrideForm({ ...overrideForm, remarks: e.target.value })}
                    />
                  </div>
                </div>
                <div className="modal-footer border-top bg-light py-2">
                  <button type="button" className="btn btn-outline-secondary btn-sm" onClick={() => setShowOverrideModal(false)}>
                    Cancel
                  </button>
                  <button 
                    type="submit" 
                    className="btn btn-warning btn-sm fw-bold shadow-sm px-3 text-dark"
                    disabled={submittingOverride}
                  >
                    {submittingOverride ? (
                      <>
                        <span className="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span>
                        Authorizing...
                      </>
                    ) : (
                      <>
                        <i className="bi bi-check-circle-fill me-1"></i> Authorize & Grant Eligibility
                      </>
                    )}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Classical Formal Academic Examination Result Sheet Modal */}
      <ClassicalReportModal
        show={showReportModal}
        onClose={() => setShowReportModal(false)}
        title={selectedExam ? `EXAMINATION RESULT SHEET — ${selectedExam.subject_name || 'Subject'} (${selectedExam.type})` : 'EXAMINATION RESULT SHEET'}
        endpoint="/api/v1/reports/academic-results"
        params={{
          course_id: selectedExam?.course_id || selectedCourseId,
          subject_id: selectedExam?.subject_id,
          batch: selectedExam?.batch_name,
          exam_id: selectedExam?.id
        }}
        defaultOrientation="landscape"
      />
    </div>
  )
}


