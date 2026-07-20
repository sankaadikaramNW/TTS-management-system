import React, { useEffect, useState } from 'react'
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

  const fetchCourses = async () => {
    setLoading(true)
    try {
      const res = await axios.get('/api/v1/academic/courses')
      setCourses(res.data)
      if (res.data.length > 0 && !selectedCourse) {
        setSelectedCourse(res.data[0])
      }
    } catch (err) {
      toast.error('Failed to load courses')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchCourses()
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
        {/* Left Side: Course Selection List */}
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
                    className={`list-group-item list-group-item-action border-0 px-2 py-2.5 rounded-3 mb-1 text-start fw-semibold ${selectedCourse?.id === c.id ? 'bg-primary-subtle text-primary' : ''}`}
                    onClick={() => setSelectedCourse(c)}
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

        {/* Right Side: Tabular Course Workspace */}
        <div className="col-lg-9 col-md-12">
          {selectedCourse ? (
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
                  <h5 className="fw-semibold mb-3">Today's Class Schedule</h5>
                  <div className="table-responsive">
                    <table className="table slaf-table mb-0">
                      <thead>
                        <tr>
                          <th>Period</th>
                          <th>Subject</th>
                          <th>Topic</th>
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
                    <div className="text-center py-4 text-muted">No examinations scheduled yet for this course.</div>
                  )}

                  {hasPermission('academic:write') && (
                    <form onSubmit={handleAddExam} className="border-top pt-4 mt-4 row g-3">
                      <div className="col-12">
                        <h6 className="fw-semibold mb-0">Schedule New Exam Slot</h6>
                      </div>
                      <div className="col-md-3">
                        <select className="form-select" value={newExamType} onChange={e => setNewExamType(e.target.value)}>
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
            </div>
          ) : (
            <div className="text-center py-5 card slaf-card text-muted">Please select or add a course to start managing academics.</div>
          )}
        </div>
      </div>
    </div>
  )
}
export default CourseList
