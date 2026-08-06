import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { toast } from 'react-toastify'

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

  // Exam Marks Modal
  const [selectedExam, setSelectedExam] = useState(null)
  const [examMarks, setExamMarks] = useState([])
  const [students, setStudents] = useState([])
  const [showMarksModal, setShowMarksModal] = useState(false)

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
      const [eRes, sRes, stRes] = await Promise.all([
        axios.get(`/api/v1/academic/exams/${courseId}`),
        axios.get(`/api/v1/academic/subjects/${courseId}`),
        axios.get('/api/v1/students', { params: { course_id: courseId } })
      ])
      setExams(eRes.data)
      setSubjects(sRes.data)
      setStudents(stRes.data)
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
      toast.success(`${examForm.type} created successfully`)
      setShowExamModal(false)
      fetchExamsAndSubjects(selectedCourseId)
    } catch (err) {
      toast.error('Failed to create examination')
    }
  }

  const handleOpenMarksModal = async (ex) => {
    setSelectedExam(ex)
    try {
      const res = await axios.get(`/api/v1/academic/exam-marks/${ex.id}`)
      // Prepare marks list for all course students
      const existingMap = new Map(res.data.map(m => [m.student_id, m]))
      const markRecords = students.map(st => ({
        student_id: st.id,
        student_name: st.full_name,
        service_number: st.service_number,
        marks_obtained: existingMap.get(st.id)?.marks_obtained ?? 0,
        remarks: existingMap.get(st.id)?.remarks ?? ''
      }))
      setExamMarks(markRecords)
      setShowMarksModal(true)
    } catch (err) {
      toast.error('Failed to load student exam marks')
    }
  }

  const handleSaveMarks = async (e) => {
    e.preventDefault()
    if (!selectedExam) return
    try {
      await axios.post('/api/v1/academic/exam-marks', {
        exam_id: selectedExam.id,
        records: examMarks.map(m => ({
          student_id: m.student_id,
          marks_obtained: parseFloat(m.marks_obtained) || 0,
          remarks: m.remarks
        }))
      })
      toast.success('Exam results saved successfully')
      setShowMarksModal(false)
    } catch (err) {
      toast.error('Failed to save exam results')
    }
  }

  const filteredExams = exams.filter(ex => {
    if (activeSubTab === 'phase-tests') return ex.type === 'Phase Test'
    if (activeSubTab === 'final-exams') return ex.type === 'Final Exam'
    return true
  })

  return (
    <div className="fade-in-slide">
      {/* Navigation Sub-Tabs */}
      <div className="d-flex justify-content-between align-items-center mb-3">
        <div>
          <h5 className="fw-bold text-dark mb-0 display-font">Assessment & Examination Center</h5>
          <small className="text-muted">Attendance Registers, Phase Tests, Final Examinations & Trainee Results</small>
        </div>
      </div>

      <div className="card slaf-card p-3 mb-3 shadow-sm">
        <div className="row align-items-center g-2">
          <div className="col-md-3">
            <label className="fw-bold text-dark small">Select Course:</label>
          </div>
          <div className="col-md-6">
            <select 
              className="form-select form-select-sm"
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
              <button className="btn btn-primary btn-sm fw-semibold" onClick={() => setShowExamModal(true)}>
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
            <i className="bi bi-bar-chart-line me-1.5"></i> Results & Marksheets
          </button>
        </li>
      </ul>

      {/* Sub Tab 1: Attendance */}
      {activeSubTab === 'attendance' && (
        <div className="card slaf-card p-4 text-center shadow-sm">
          <div className="py-4">
            <i className="bi bi-calendar-check-fill display-3 text-primary mb-3 d-block"></i>
            <h5 className="fw-bold text-dark">Academic Class Attendance Registry</h5>
            <p className="text-muted small max-w-lg mx-auto">
              Attendance records are synchronized per daily scheduled timetable period slot. Trainee attendance status (Present, Absent, Excused) is recorded directly by assigned instructors.
            </p>
            <button className="btn btn-outline-primary btn-sm fw-semibold" onClick={() => toast.info('Select a Timetable Slot from Timetable Schedule to mark daily attendance')}>
              <i className="bi bi-clock me-1"></i> View Scheduled Timetable Registry
            </button>
          </div>
        </div>
      )}

      {/* Sub Tab 2 & 3: Phase Tests & Final Exams */}
      {(activeSubTab === 'phase-tests' || activeSubTab === 'final-exams') && (
        <div className="card slaf-card p-0 shadow-sm">
          <div className="table-responsive">
            <table className="table slaf-table align-middle mb-0">
              <thead>
                <tr>
                  <th>Exam Title / Type</th>
                  <th>Subject</th>
                  <th>Date</th>
                  <th>Max Marks</th>
                  <th>Pass Marks</th>
                  <th className="text-end">Action</th>
                </tr>
              </thead>
              <tbody>
                {loading ? (
                  <tr><td colSpan="6" className="text-center py-5"><div className="spinner-border text-primary"></div></td></tr>
                ) : filteredExams.length === 0 ? (
                  <tr><td colSpan="6" className="text-center py-5 text-muted">No examinations scheduled for this course view.</td></tr>
                ) : (
                  filteredExams.map(ex => (
                    <tr key={ex.id}>
                      <td><span className="badge bg-primary-subtle text-primary border fw-bold">{ex.type}</span></td>
                      <td><strong className="text-dark">{ex.subject_name}</strong></td>
                      <td><small className="text-muted"><i className="bi bi-calendar-event me-1"></i>{ex.date}</small></td>
                      <td><span className="badge bg-secondary-subtle text-dark border">{ex.max_marks} Marks</span></td>
                      <td><span className="badge bg-success-subtle text-success border">{ex.pass_marks} Pass</span></td>
                      <td className="text-end">
                        <button className="btn btn-primary btn-sm fw-semibold" onClick={() => handleOpenMarksModal(ex)}>
                          <i className="bi bi-pencil-square me-1"></i> Enter Results
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

      {/* Sub Tab 4: Results */}
      {activeSubTab === 'results' && (
        <div className="card slaf-card p-3 shadow-sm">
          <h6 className="fw-bold text-dark mb-3"><i className="bi bi-bar-chart-fill me-2 text-success"></i>Trainee Performance Marksheets</h6>
          <div className="table-responsive">
            <table className="table slaf-table align-middle mb-0">
              <thead>
                <tr>
                  <th>Exam Title</th>
                  <th>Subject</th>
                  <th>Scheduled Date</th>
                  <th>Trainees Registered</th>
                  <th className="text-end">Action</th>
                </tr>
              </thead>
              <tbody>
                {exams.length === 0 ? (
                  <tr><td colSpan="5" className="text-center py-4 text-muted">No exams available for result viewing.</td></tr>
                ) : (
                  exams.map(ex => (
                    <tr key={ex.id}>
                      <td><strong className="text-dark">{ex.type}</strong></td>
                      <td><span className="text-muted small">{ex.subject_name}</span></td>
                      <td><small className="text-muted">{ex.date}</small></td>
                      <td><span className="badge bg-primary-subtle text-primary border">{students.length} Trainees</span></td>
                      <td className="text-end">
                        <button className="btn btn-outline-primary btn-sm" onClick={() => handleOpenMarksModal(ex)}>
                          <i className="bi bi-eye me-1"></i> View Marksheet
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
            <div className="modal-content slaf-card">
              <div className="modal-header border-bottom">
                <h5 className="modal-title display-font text-primary fw-bold">Schedule Examination</h5>
                <button type="button" className="btn-close" onClick={() => setShowExamModal(false)}></button>
              </div>
              <form onSubmit={handleCreateExam}>
                <div className="modal-body">
                  <div className="mb-3">
                    <label className="form-label small fw-semibold">Exam Type*</label>
                    <select className="form-select" value={examForm.type} onChange={(e) => setExamForm({ ...examForm, type: e.target.value })}>
                      <option value="Phase Test">Phase Test</option>
                      <option value="Final Exam">Final Examination</option>
                    </select>
                  </div>
                  <div className="mb-3">
                    <label className="form-label small fw-semibold">Select Subject*</label>
                    <select className="form-select" value={examForm.subject_id} onChange={(e) => setExamForm({ ...examForm, subject_id: e.target.value })} required>
                      <option value="">-- Select Subject --</option>
                      {subjects.map(s => (
                        <option key={s.id} value={s.id}>{s.name} ({s.code})</option>
                      ))}
                    </select>
                  </div>
                  <div className="mb-3">
                    <label className="form-label small fw-semibold">Exam Date*</label>
                    <input type="date" className="form-control" value={examForm.date} onChange={(e) => setExamForm({ ...examForm, date: e.target.value })} required />
                  </div>
                  <div className="row g-2">
                    <div className="col-6">
                      <label className="form-label small fw-semibold">Max Marks</label>
                      <input type="number" className="form-control" value={examForm.max_marks} onChange={(e) => setExamForm({ ...examForm, max_marks: parseFloat(e.target.value) || 0 })} />
                    </div>
                    <div className="col-6">
                      <label className="form-label small fw-semibold">Pass Marks</label>
                      <input type="number" className="form-control" value={examForm.pass_marks} onChange={(e) => setExamForm({ ...examForm, pass_marks: parseFloat(e.target.value) || 0 })} />
                    </div>
                  </div>
                </div>
                <div className="modal-footer border-top">
                  <button type="button" className="btn btn-outline-secondary btn-sm" onClick={() => setShowExamModal(false)}>Cancel</button>
                  <button type="submit" className="btn btn-primary btn-sm fw-semibold">Schedule Exam</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Enter Marks Modal */}
      {showMarksModal && selectedExam && (
        <div className="modal fade show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)', zIndex: 1060 }}>
          <div className="modal-dialog modal-lg modal-dialog-centered">
            <div className="modal-content slaf-card">
              <div className="modal-header border-bottom">
                <h5 className="modal-title display-font text-primary fw-bold">
                  Enter Results: {selectedExam.type} ({selectedExam.subject_name})
                </h5>
                <button type="button" className="btn-close" onClick={() => setShowMarksModal(false)}></button>
              </div>
              <form onSubmit={handleSaveMarks}>
                <div className="modal-body" style={{ maxHeight: '65vh', overflowY: 'auto' }}>
                  <table className="table table-sm align-middle">
                    <thead>
                      <tr>
                        <th>Service No</th>
                        <th>Student Name</th>
                        <th>Marks Obtained</th>
                        <th>Pass/Fail</th>
                        <th>Remarks</th>
                      </tr>
                    </thead>
                    <tbody>
                      {examMarks.map((m, idx) => {
                        const marksNum = parseFloat(m.marks_obtained) || 0
                        const isPass = marksNum >= selectedExam.pass_marks
                        return (
                          <tr key={m.student_id}>
                            <td><strong className="text-primary small">{m.service_number}</strong></td>
                            <td><small className="fw-semibold">{m.student_name}</small></td>
                            <td style={{ width: '130px' }}>
                              <input 
                                type="number" 
                                className="form-control form-control-sm" 
                                value={m.marks_obtained}
                                min="0"
                                max={selectedExam.max_marks}
                                onChange={(e) => {
                                  const newArr = [...examMarks]
                                  newArr[idx].marks_obtained = e.target.value
                                  setExamMarks(newArr)
                                }}
                              />
                            </td>
                            <td>
                              <span className={`badge bg-${isPass ? 'success' : 'danger'}-subtle text-${isPass ? 'success' : 'danger'} border`}>
                                {isPass ? 'Pass' : 'Fail'}
                              </span>
                            </td>
                            <td>
                              <input 
                                type="text" 
                                className="form-control form-control-sm" 
                                placeholder="Remarks..."
                                value={m.remarks}
                                onChange={(e) => {
                                  const newArr = [...examMarks]
                                  newArr[idx].remarks = e.target.value
                                  setExamMarks(newArr)
                                }}
                              />
                            </td>
                          </tr>
                        )
                      })}
                    </tbody>
                  </table>
                </div>
                <div className="modal-footer border-top">
                  <button type="button" className="btn btn-outline-secondary btn-sm" onClick={() => setShowMarksModal(false)}>Cancel</button>
                  <button type="submit" className="btn btn-primary btn-sm fw-semibold">Save Results</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
