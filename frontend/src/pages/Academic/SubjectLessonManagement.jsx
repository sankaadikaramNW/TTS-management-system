import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { toast } from 'react-toastify'

export const SubjectLessonManagement = () => {
  const [courses, setCourses] = useState([])
  const [selectedCourseId, setSelectedCourseId] = useState('')
  const [subjects, setSubjects] = useState([])
  const [selectedSubjectId, setSelectedSubjectId] = useState('')
  const [lessons, setLessons] = useState([])
  const [loading, setLoading] = useState(false)

  // Subject Modal
  const [showSubModal, setShowSubModal] = useState(false)
  const [subForm, setSubForm] = useState({ code: '', name: '', periods: 40, description: '' })

  // Lesson Modal
  const [showLesModal, setShowLesModal] = useState(false)
  const [lesForm, setLesForm] = useState({ name: '', description: '' })

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

  const fetchSubjects = async (courseId) => {
    if (!courseId) return
    setLoading(true)
    try {
      const res = await axios.get(`/api/v1/academic/subjects/${courseId}`)
      setSubjects(res.data)
      if (res.data.length > 0) {
        setSelectedSubjectId(res.data[0].id)
      } else {
        setSelectedSubjectId('')
        setLessons([])
      }
    } catch (err) {
      toast.error('Failed to load subjects')
    } finally {
      setLoading(false)
    }
  }

  const fetchLessons = async (subjectId) => {
    if (!subjectId) return
    try {
      const res = await axios.get(`/api/v1/academic/lessons/${subjectId}`)
      setLessons(res.data)
    } catch (err) {
      console.error(err)
    }
  }

  useEffect(() => {
    fetchCourses()
  }, [])

  useEffect(() => {
    if (selectedCourseId) {
      fetchSubjects(selectedCourseId)
    }
  }, [selectedCourseId])

  useEffect(() => {
    if (selectedSubjectId) {
      fetchLessons(selectedSubjectId)
    }
  }, [selectedSubjectId])

  const handleCreateSubject = async (e) => {
    e.preventDefault()
    if (!subForm.code || !subForm.name || !selectedCourseId) return
    try {
      await axios.post('/api/v1/academic/subjects', {
        ...subForm,
        course_id: selectedCourseId
      })
      toast.success(`Subject '${subForm.name}' created`)
      setShowSubModal(false)
      fetchSubjects(selectedCourseId)
    } catch (err) {
      toast.error('Failed to create subject')
    }
  }

  const handleCreateLesson = async (e) => {
    e.preventDefault()
    if (!lesForm.name || !selectedSubjectId) return
    try {
      await axios.post('/api/v1/academic/lessons', {
        ...lesForm,
        subject_id: selectedSubjectId
      })
      toast.success(`Lesson '${lesForm.name}' created`)
      setShowLesModal(false)
      fetchLessons(selectedSubjectId)
    } catch (err) {
      toast.error('Failed to create lesson')
    }
  }

  return (
    <div className="fade-in-slide">
      <div className="d-flex justify-content-between align-items-center mb-3">
        <div>
          <h5 className="fw-bold text-dark mb-0 display-font">Subject & Lesson Curriculum Management</h5>
          <small className="text-muted">Structure course subjects, periods, and instructional lesson plans</small>
        </div>
      </div>

      {/* Course Selection */}
      <div className="card slaf-card p-3 mb-4 shadow-sm">
        <div className="row align-items-center g-2">
          <div className="col-md-3">
            <label className="fw-bold text-dark small">Select Course Syllabus:</label>
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
            <button className="btn btn-primary btn-sm fw-semibold" onClick={() => setShowSubModal(true)}>
              <i className="bi bi-plus-lg me-1"></i> Add Subject
            </button>
          </div>
        </div>
      </div>

      {/* Grid: Subjects and Lessons */}
      <div className="row g-3">
        {/* Subjects List */}
        <div className="col-lg-6">
          <div className="card slaf-card p-3 shadow-sm h-100">
            <h6 className="fw-bold text-dark mb-3"><i className="bi bi-journal-text me-2 text-primary"></i>Course Subjects</h6>
            {loading ? (
              <div className="text-center py-4"><div className="spinner-border text-primary"></div></div>
            ) : subjects.length === 0 ? (
              <p className="text-muted small py-4 text-center">No subjects configured for this course yet.</p>
            ) : (
              <div className="list-group list-group-flush">
                {subjects.map(s => (
                  <button
                    key={s.id}
                    className={`list-group-item list-group-item-action d-flex justify-content-between align-items-center py-3 border-bottom ${selectedSubjectId === s.id ? 'bg-primary-subtle border-primary' : ''}`}
                    onClick={() => setSelectedSubjectId(s.id)}
                  >
                    <div>
                      <span className="badge bg-primary text-white me-2">{s.code}</span>
                      <strong className="text-dark">{s.name}</strong>
                      <small className="text-muted d-block mt-0.5">{s.description || 'No description'}</small>
                    </div>
                    <span className="badge bg-secondary-subtle text-dark border">{s.periods} Periods</span>
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Lessons List */}
        <div className="col-lg-6">
          <div className="card slaf-card p-3 shadow-sm h-100">
            <div className="d-flex justify-content-between align-items-center mb-3">
              <h6 className="fw-bold text-dark mb-0"><i className="bi bi-list-task me-2 text-info"></i>Lessons for Selected Subject</h6>
              {selectedSubjectId && (
                <button className="btn btn-outline-primary btn-sm fw-semibold" onClick={() => setShowLesModal(true)}>
                  <i className="bi bi-plus-lg me-1"></i> Add Lesson
                </button>
              )}
            </div>

            {!selectedSubjectId ? (
              <p className="text-muted small py-4 text-center">Select a subject to manage lessons.</p>
            ) : lessons.length === 0 ? (
              <p className="text-muted small py-4 text-center">No lessons added to this subject yet.</p>
            ) : (
              <div className="d-flex flex-column gap-2">
                {lessons.map((l, idx) => (
                  <div key={l.id} className="p-2.5 bg-light rounded border">
                    <div className="fw-bold text-dark small mb-0.5">Lesson {idx + 1}: {l.name}</div>
                    <small className="text-muted">{l.description || 'Standard training module lesson'}</small>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Add Subject Modal */}
      {showSubModal && (
        <div className="modal fade show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)', zIndex: 1060 }}>
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content slaf-card">
              <div className="modal-header border-bottom">
                <h5 className="modal-title display-font text-primary fw-bold">Add Subject</h5>
                <button type="button" className="btn-close" onClick={() => setShowSubModal(false)}></button>
              </div>
              <form onSubmit={handleCreateSubject}>
                <div className="modal-body">
                  <div className="mb-3">
                    <label className="form-label small fw-semibold">Subject Code*</label>
                    <input type="text" className="form-control" placeholder="e.g. SUB-101" value={subForm.code} onChange={(e) => setSubForm({ ...subForm, code: e.target.value })} required />
                  </div>
                  <div className="mb-3">
                    <label className="form-label small fw-semibold">Subject Name*</label>
                    <input type="text" className="form-control" placeholder="e.g. Electrical Fundamentals" value={subForm.name} onChange={(e) => setSubForm({ ...subForm, name: e.target.value })} required />
                  </div>
                  <div className="mb-3">
                    <label className="form-label small fw-semibold">Total Scheduled Periods</label>
                    <input type="number" className="form-control" value={subForm.periods} onChange={(e) => setSubForm({ ...subForm, periods: parseInt(e.target.value) || 0 })} min="1" />
                  </div>
                </div>
                <div className="modal-footer border-top">
                  <button type="button" className="btn btn-outline-secondary btn-sm" onClick={() => setShowSubModal(false)}>Cancel</button>
                  <button type="submit" className="btn btn-primary btn-sm">Save Subject</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Add Lesson Modal */}
      {showLesModal && (
        <div className="modal fade show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)', zIndex: 1060 }}>
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content slaf-card">
              <div className="modal-header border-bottom">
                <h5 className="modal-title display-font text-primary fw-bold">Add Lesson</h5>
                <button type="button" className="btn-close" onClick={() => setShowLesModal(false)}></button>
              </div>
              <form onSubmit={handleCreateLesson}>
                <div className="modal-body">
                  <div className="mb-3">
                    <label className="form-label small fw-semibold">Lesson Name*</label>
                    <input type="text" className="form-control" placeholder="e.g. Ohm's Law & Circuit Analysis" value={lesForm.name} onChange={(e) => setLesForm({ ...lesForm, name: e.target.value })} required />
                  </div>
                  <div className="mb-3">
                    <label className="form-label small fw-semibold">Description</label>
                    <textarea className="form-control" rows="2" value={lesForm.description} onChange={(e) => setLesForm({ ...lesForm, description: e.target.value })}></textarea>
                  </div>
                </div>
                <div className="modal-footer border-top">
                  <button type="button" className="btn btn-outline-secondary btn-sm" onClick={() => setShowLesModal(false)}>Cancel</button>
                  <button type="submit" className="btn btn-primary btn-sm">Save Lesson</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
