import React, { useEffect, useState, useRef } from 'react'
import axios from 'axios'
import { toast } from 'react-toastify'

export const SubjectLessonManagement = () => {
  const [courses, setCourses] = useState([])
  const [selectedCourseId, setSelectedCourseId] = useState('')
  const [subjects, setSubjects] = useState([])
  const [selectedSubjectId, setSelectedSubjectId] = useState('')
  const [lessons, setLessons] = useState([])
  const [loading, setLoading] = useState(false)
  const [savingSubject, setSavingSubject] = useState(false)
  const [savingLesson, setSavingLesson] = useState(false)
  const [subjectSearch, setSubjectSearch] = useState('')

  // Subject Modal
  const [showSubModal, setShowSubModal] = useState(false)
  const [subForm, setSubForm] = useState({ code: '', name: '', periods: 40, description: '' })
  const subCodeInputRef = useRef(null)

  // Lesson Modal
  const [showLesModal, setShowLesModal] = useState(false)
  const [lesForm, setLesForm] = useState({ subject_id: '', name: '', description: '' })
  const lesNameInputRef = useRef(null)

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
        // Keep selected subject if it still exists in the new list, else pick first
        setSelectedSubjectId((prev) => {
          const exists = res.data.some(s => s.id === prev)
          return exists ? prev : res.data[0].id
        })
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

  const handleOpenAddSubjectModal = () => {
    setSubForm({ code: '', name: '', periods: 40, description: '' })
    setShowSubModal(true)
    setTimeout(() => {
      subCodeInputRef.current?.focus()
    }, 100)
  }

  const handleOpenAddLessonModal = (targetSubjectId = null) => {
    const subjId = targetSubjectId || selectedSubjectId || (subjects.length > 0 ? subjects[0].id : '')
    if (subjId) {
      setSelectedSubjectId(subjId)
    }
    setLesForm({ subject_id: subjId, name: '', description: '' })
    setShowLesModal(true)
    setTimeout(() => {
      lesNameInputRef.current?.focus()
    }, 100)
  }

  const handleCreateSubject = async (e, addAnother = false) => {
    if (e) e.preventDefault()
    if (!subForm.code.trim() || !subForm.name.trim() || !selectedCourseId) {
      toast.warning('Please fill in both Subject Code and Subject Name')
      return
    }

    setSavingSubject(true)
    try {
      const res = await axios.post('/api/v1/academic/subjects', {
        code: subForm.code.trim(),
        name: subForm.name.trim(),
        periods: subForm.periods || 40,
        description: subForm.description.trim(),
        course_id: selectedCourseId
      })
      toast.success(`Subject '${subForm.name}' (${subForm.code}) added successfully`)
      await fetchSubjects(selectedCourseId)

      if (res.data?.id) {
        setSelectedSubjectId(res.data.id)
      }

      if (addAnother) {
        setSubForm({ code: '', name: '', periods: 40, description: '' })
        setTimeout(() => {
          subCodeInputRef.current?.focus()
        }, 50)
      } else {
        setShowSubModal(false)
        setSubForm({ code: '', name: '', periods: 40, description: '' })
      }
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to create subject')
    } finally {
      setSavingSubject(false)
    }
  }

  const handleCreateLesson = async (e, addAnother = false) => {
    if (e) e.preventDefault()
    const targetSubjectId = lesForm.subject_id || selectedSubjectId
    if (!targetSubjectId) {
      toast.warning('Please select a subject first')
      return
    }
    if (!lesForm.name.trim()) {
      toast.warning('Please enter a lesson name')
      return
    }

    setSavingLesson(true)
    try {
      await axios.post('/api/v1/academic/lessons', {
        name: lesForm.name.trim(),
        description: lesForm.description.trim(),
        subject_id: targetSubjectId
      })
      toast.success(`Lesson '${lesForm.name}' created successfully`)
      await fetchLessons(targetSubjectId)

      if (addAnother) {
        setLesForm(prev => ({ ...prev, name: '', description: '' }))
        setTimeout(() => {
          lesNameInputRef.current?.focus()
        }, 50)
      } else {
        setShowLesModal(false)
        setLesForm({ subject_id: targetSubjectId, name: '', description: '' })
      }
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to create lesson')
    } finally {
      setSavingLesson(false)
    }
  }

  const filteredSubjects = subjects.filter(s => {
    if (!subjectSearch.trim()) return true
    const term = subjectSearch.toLowerCase()
    return (
      (s.code && s.code.toLowerCase().includes(term)) ||
      (s.name && s.name.toLowerCase().includes(term))
    )
  })

  const selectedCourse = courses.find(c => String(c.id) === String(selectedCourseId))
  const selectedSubject = subjects.find(s => String(s.id) === String(selectedSubjectId))

  return (
    <div className="fade-in-slide">
      {/* Page Header */}
      <div className="d-flex justify-content-between align-items-center mb-3">
        <div>
          <h5 className="fw-bold text-dark mb-0 display-font">
            <i className="bi bi-book-half me-2 text-primary"></i>
            Subject &amp; Lesson Curriculum Management
          </h5>
          <small className="text-muted">Structure course subjects, scheduled periods, and instructional lesson plans</small>
        </div>
      </div>

      {/* Course Selection Toolbar */}
      <div className="card slaf-card p-3 mb-4 shadow-sm border-0">
        <div className="row align-items-center g-3">
          <div className="col-lg-3 col-md-4">
            <label className="fw-bold text-dark small d-flex align-items-center mb-1">
              <i className="bi bi-mortarboard me-1.5 text-primary"></i>
              Select Course Syllabus:
            </label>
          </div>
          <div className="col-lg-6 col-md-5">
            <select 
              className="form-select form-select-sm border-primary-subtle fw-medium shadow-none"
              value={selectedCourseId}
              onChange={(e) => setSelectedCourseId(e.target.value)}
            >
              {courses.map(c => (
                <option key={c.id} value={c.id}>{c.name} ({c.code})</option>
              ))}
            </select>
          </div>
          <div className="col-lg-3 col-md-3 text-md-end">
            <button 
              className="btn btn-primary btn-sm fw-semibold shadow-sm w-100 w-md-auto d-inline-flex align-items-center justify-content-center"
              onClick={handleOpenAddSubjectModal}
              disabled={!selectedCourseId}
            >
              <i className="bi bi-plus-circle me-1.5 fs-6"></i> Add Subject
            </button>
          </div>
        </div>
      </div>

      {/* Grid: Subjects and Lessons */}
      <div className="row g-3">
        {/* Subjects List */}
        <div className="col-lg-6">
          <div className="card slaf-card shadow-sm border-0 h-100 d-flex flex-column">
            {/* Subject Card Header - Sticky at the top of the subject list */}
            <div className="card-header bg-white border-bottom p-3">
              <div className="d-flex justify-content-between align-items-center flex-wrap gap-2">
                <div className="d-flex align-items-center">
                  <h6 className="fw-bold text-dark mb-0 d-flex align-items-center">
                    <i className="bi bi-journal-text me-2 text-primary fs-5"></i>
                    Course Subjects
                  </h6>
                  <span className="badge bg-primary-subtle text-primary border border-primary-subtle rounded-pill ms-2 fw-semibold">
                    {subjects.length} {subjects.length === 1 ? 'Subject' : 'Subjects'}
                  </span>
                </div>
                <button 
                  className="btn btn-primary btn-sm fw-semibold shadow-sm d-inline-flex align-items-center"
                  onClick={handleOpenAddSubjectModal}
                  disabled={!selectedCourseId}
                >
                  <i className="bi bi-plus-lg me-1"></i> Add Subject
                </button>
              </div>

              {/* Subject Search / Filter */}
              {subjects.length > 4 && (
                <div className="mt-2.5">
                  <div className="input-group input-group-sm">
                    <span className="input-group-text bg-light border-end-0 text-muted">
                      <i className="bi bi-search"></i>
                    </span>
                    <input
                      type="text"
                      className="form-control bg-light border-start-0 ps-0 shadow-none"
                      placeholder="Filter subjects by code or name..."
                      value={subjectSearch}
                      onChange={(e) => setSubjectSearch(e.target.value)}
                    />
                    {subjectSearch && (
                      <button 
                        className="btn btn-outline-secondary border-start-0" 
                        type="button"
                        onClick={() => setSubjectSearch('')}
                      >
                        <i className="bi bi-x"></i>
                      </button>
                    )}
                  </div>
                </div>
              )}
            </div>

            {/* Subject List Body - Scrollable */}
            <div className="card-body p-2 flex-grow-1" style={{ maxHeight: '560px', overflowY: 'auto' }}>
              {loading ? (
                <div className="text-center py-5">
                  <div className="spinner-border text-primary spinner-border-sm me-2"></div>
                  <span className="text-muted small">Loading subjects...</span>
                </div>
              ) : filteredSubjects.length === 0 ? (
                <div className="text-center py-5">
                  <div className="p-3 bg-light rounded-circle d-inline-block mb-3 text-muted">
                    <i className="bi bi-journal-x fs-2"></i>
                  </div>
                  <p className="text-muted small mb-2">
                    {subjectSearch ? 'No subjects match your filter.' : 'No subjects configured for this course yet.'}
                  </p>
                  {!subjectSearch && selectedCourseId && (
                    <button className="btn btn-outline-primary btn-sm fw-semibold mt-1" onClick={handleOpenAddSubjectModal}>
                      <i className="bi bi-plus-circle me-1"></i> Add First Subject
                    </button>
                  )}
                </div>
              ) : (
                <div className="list-group list-group-flush gap-1">
                  {filteredSubjects.map(s => {
                    const isSelected = selectedSubjectId === s.id
                    return (
                      <div
                        key={s.id}
                        className={`list-group-item list-group-item-action rounded-2 border d-flex justify-content-between align-items-center p-3 mb-1 transition-all cursor-pointer ${
                          isSelected ? 'bg-primary text-white border-primary shadow-sm' : 'bg-white text-dark hover-bg-light'
                        }`}
                        onClick={() => setSelectedSubjectId(s.id)}
                        role="button"
                      >
                        <div className="text-start me-2">
                          <div className="d-flex align-items-center gap-2 mb-1">
                            <span className={`badge ${isSelected ? 'bg-white text-primary fw-bold' : 'bg-primary-subtle text-primary border border-primary-subtle'}`}>
                              {s.code}
                            </span>
                            <strong className={`small ${isSelected ? 'text-white' : 'text-dark'}`}>{s.name}</strong>
                          </div>
                          {s.description && (
                            <small className={`d-block ${isSelected ? 'text-white-50' : 'text-muted'}`} style={{ fontSize: '0.78rem' }}>
                              {s.description}
                            </small>
                          )}
                        </div>
                        <div className="d-flex align-items-center gap-2">
                          <span className={`badge rounded-pill border text-nowrap ${isSelected ? 'bg-white text-primary' : 'bg-light text-secondary'}`}>
                            {s.periods} Periods
                          </span>
                          <button
                            type="button"
                            className={`btn btn-sm py-0.5 px-2 rounded-pill fw-semibold ${
                              isSelected ? 'btn-light text-primary' : 'btn-outline-primary'
                            }`}
                            style={{ fontSize: '0.75rem' }}
                            title={`Add lesson to ${s.name}`}
                            onClick={(e) => {
                              e.stopPropagation()
                              handleOpenAddLessonModal(s.id)
                            }}
                          >
                            <i className="bi bi-plus me-0.5"></i>Lesson
                          </button>
                        </div>
                      </div>
                    )
                  })}
                </div>
              )}
            </div>

            {/* Subject Footer Quick Stats */}
            {subjects.length > 0 && (
              <div className="card-footer bg-light border-top py-2 px-3 d-flex justify-content-between align-items-center">
                <small className="text-muted">
                  Total Course Periods: <strong className="text-dark">{subjects.reduce((sum, s) => sum + (s.periods || 0), 0)} hrs</strong>
                </small>
                <button 
                  className="btn btn-link btn-sm p-0 text-decoration-none fw-semibold text-primary"
                  onClick={handleOpenAddSubjectModal}
                >
                  <i className="bi bi-plus-circle me-1"></i>Add Another
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Lessons List */}
        <div className="col-lg-6">
          <div className="card slaf-card shadow-sm border-0 h-100 d-flex flex-column">
            <div className="card-header bg-white border-bottom p-3 d-flex justify-content-between align-items-center flex-wrap gap-2">
              <div>
                <h6 className="fw-bold text-dark mb-0 d-flex align-items-center">
                  <i className="bi bi-list-task me-2 text-info fs-5"></i>
                  Lessons for Selected Subject
                </h6>
                {selectedSubject ? (
                  <small className="text-muted d-block mt-0.5">
                    [{selectedSubject.code}] <strong className="text-dark">{selectedSubject.name}</strong> &bull; {lessons.length} {lessons.length === 1 ? 'Lesson' : 'Lessons'}
                  </small>
                ) : (
                  <small className="text-muted d-block mt-0.5">Select a subject on the left or click Add Lesson</small>
                )}
              </div>
              <button 
                className="btn btn-outline-primary btn-sm fw-semibold d-inline-flex align-items-center" 
                onClick={() => handleOpenAddLessonModal(selectedSubjectId)}
                disabled={subjects.length === 0}
              >
                <i className="bi bi-plus-lg me-1"></i> Add Lesson
              </button>
            </div>

            <div className="card-body p-3 flex-grow-1" style={{ maxHeight: '560px', overflowY: 'auto' }}>
              {subjects.length === 0 ? (
                <div className="text-center py-5">
                  <div className="p-3 bg-light rounded-circle d-inline-block mb-3 text-muted">
                    <i className="bi bi-journal-plus fs-2"></i>
                  </div>
                  <p className="text-muted small mb-2">Please add subjects to this course first before creating lesson plans.</p>
                  <button className="btn btn-primary btn-sm fw-semibold" onClick={handleOpenAddSubjectModal}>
                    <i className="bi bi-plus-circle me-1"></i> Add Subject Now
                  </button>
                </div>
              ) : !selectedSubjectId ? (
                <div className="text-center py-5">
                  <div className="p-3 bg-light rounded-circle d-inline-block mb-3 text-muted">
                    <i className="bi bi-arrow-left-circle fs-2"></i>
                  </div>
                  <p className="text-muted small">Select a subject from the left panel to view and manage its lesson units.</p>
                </div>
              ) : lessons.length === 0 ? (
                <div className="text-center py-5">
                  <div className="p-3 bg-light rounded-circle d-inline-block mb-3 text-muted">
                    <i className="bi bi-card-list fs-2"></i>
                  </div>
                  <p className="text-muted small mb-2">No lesson units added to <strong>{selectedSubject?.name}</strong> yet.</p>
                  <button className="btn btn-outline-primary btn-sm fw-semibold" onClick={() => handleOpenAddLessonModal(selectedSubjectId)}>
                    <i className="bi bi-plus-circle me-1"></i> Add First Lesson
                  </button>
                </div>
              ) : (
                <div className="d-flex flex-column gap-2">
                  {lessons.map((l, idx) => (
                    <div key={l.id} className="p-3 bg-light rounded border border-light-subtle shadow-none">
                      <div className="d-flex justify-content-between align-items-start">
                        <div className="fw-bold text-dark small mb-1">
                          <span className="badge bg-secondary-subtle text-dark border me-1.5">Lesson {idx + 1}</span>
                          {l.name}
                        </div>
                      </div>
                      <small className="text-muted d-block" style={{ fontSize: '0.8rem' }}>
                        {l.description || 'Standard training curriculum lesson topic.'}
                      </small>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Add Subject Modal */}
      {showSubModal && (
        <div className="modal fade show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.55)', zIndex: 1060 }} tabIndex="-1">
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content slaf-card border-0 shadow-lg">
              <div className="modal-header border-bottom bg-light py-3">
                <div>
                  <h5 className="modal-title display-font text-primary fw-bold mb-0">
                    <i className="bi bi-journal-plus me-2"></i>
                    Add Subject
                  </h5>
                  <small className="text-muted">
                    Course: <span className="fw-semibold text-dark">{selectedCourse?.name || 'Selected Course'}</span>
                  </small>
                </div>
                <button type="button" className="btn-close" onClick={() => setShowSubModal(false)}></button>
              </div>
              <form onSubmit={(e) => handleCreateSubject(e, false)}>
                <div className="modal-body p-4">
                  <div className="mb-3">
                    <label className="form-label small fw-semibold text-dark">Subject Code <span className="text-danger">*</span></label>
                    <input 
                      ref={subCodeInputRef}
                      type="text" 
                      className="form-control form-control-sm" 
                      placeholder="e.g. SUB-101 or 09" 
                      value={subForm.code} 
                      onChange={(e) => setSubForm({ ...subForm, code: e.target.value })} 
                      required 
                    />
                  </div>
                  <div className="mb-3">
                    <label className="form-label small fw-semibold text-dark">Subject Name <span className="text-danger">*</span></label>
                    <input 
                      type="text" 
                      className="form-control form-control-sm" 
                      placeholder="e.g. Electrical Fundamentals" 
                      value={subForm.name} 
                      onChange={(e) => setSubForm({ ...subForm, name: e.target.value })} 
                      required 
                    />
                  </div>
                  <div className="mb-3">
                    <label className="form-label small fw-semibold text-dark">Total Scheduled Periods</label>
                    <input 
                      type="number" 
                      className="form-control form-control-sm" 
                      value={subForm.periods} 
                      onChange={(e) => setSubForm({ ...subForm, periods: parseInt(e.target.value) || 0 })} 
                      min="1" 
                    />
                    <div className="form-text text-muted" style={{ fontSize: '0.75rem' }}>
                      Allocated training periods/hours for syllabus completion.
                    </div>
                  </div>
                  <div className="mb-2">
                    <label className="form-label small fw-semibold text-dark">Description (Optional)</label>
                    <textarea 
                      className="form-control form-control-sm" 
                      rows="2" 
                      placeholder="Optional brief overview of subject syllabus..." 
                      value={subForm.description} 
                      onChange={(e) => setSubForm({ ...subForm, description: e.target.value })}
                    ></textarea>
                  </div>
                </div>
                <div className="modal-footer border-top bg-light py-2.5 px-4 d-flex justify-content-between align-items-center">
                  <button type="button" className="btn btn-outline-secondary btn-sm px-3" onClick={() => setShowSubModal(false)}>
                    Cancel
                  </button>
                  <div className="d-flex gap-2">
                    <button 
                      type="button" 
                      className="btn btn-outline-primary btn-sm fw-semibold"
                      disabled={savingSubject}
                      onClick={(e) => handleCreateSubject(e, true)}
                    >
                      {savingSubject ? (
                        <>
                          <span className="spinner-border spinner-border-sm me-1" role="status"></span>
                          Saving...
                        </>
                      ) : (
                        <>
                          <i className="bi bi-plus-circle me-1"></i> Save &amp; Add Another
                        </>
                      )}
                    </button>
                    <button 
                      type="submit" 
                      className="btn btn-primary btn-sm fw-semibold px-3"
                      disabled={savingSubject}
                    >
                      {savingSubject ? (
                        <>
                          <span className="spinner-border spinner-border-sm me-1" role="status"></span>
                          Saving...
                        </>
                      ) : (
                        'Save Subject'
                      )}
                    </button>
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Add Lesson Modal */}
      {showLesModal && (
        <div className="modal fade show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.55)', zIndex: 1060 }} tabIndex="-1">
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content slaf-card border-0 shadow-lg">
              <div className="modal-header border-bottom bg-light py-3">
                <div>
                  <h5 className="modal-title display-font text-primary fw-bold mb-0">
                    <i className="bi bi-journal-bookmark-fill me-2"></i>
                    Add Lesson
                  </h5>
                  <small className="text-muted">
                    Course: <span className="fw-semibold text-dark">{selectedCourse?.name || 'Selected Course'}</span>
                  </small>
                </div>
                <button type="button" className="btn-close" onClick={() => setShowLesModal(false)}></button>
              </div>
              <form onSubmit={(e) => handleCreateLesson(e, false)}>
                <div className="modal-body p-4">
                  {/* Select Subject of Relevant Course */}
                  <div className="mb-3">
                    <label className="form-label small fw-semibold text-dark">
                      Select Subject <span className="text-danger">*</span>
                    </label>
                    <select
                      className="form-select form-select-sm border-primary-subtle fw-medium"
                      value={lesForm.subject_id || selectedSubjectId || ''}
                      onChange={(e) => {
                        const newSubjId = e.target.value
                        setLesForm({ ...lesForm, subject_id: newSubjId })
                        setSelectedSubjectId(newSubjId)
                      }}
                      required
                    >
                      <option value="">-- Select Subject from {selectedCourse?.code || 'Course'} --</option>
                      {subjects.map(s => (
                        <option key={s.id} value={s.id}>
                          {s.code ? `[${s.code}] ` : ''}{s.name} ({s.periods || 0} Periods)
                        </option>
                      ))}
                    </select>
                    <div className="form-text text-muted" style={{ fontSize: '0.75rem' }}>
                      Choose which subject syllabus this lesson plan belongs to.
                    </div>
                  </div>

                  <div className="mb-3">
                    <label className="form-label small fw-semibold text-dark">Lesson Name <span className="text-danger">*</span></label>
                    <input 
                      ref={lesNameInputRef}
                      type="text" 
                      className="form-control form-control-sm" 
                      placeholder="e.g. Ohm's Law &amp; Circuit Analysis" 
                      value={lesForm.name} 
                      onChange={(e) => setLesForm({ ...lesForm, name: e.target.value })} 
                      required 
                    />
                  </div>
                  <div className="mb-2">
                    <label className="form-label small fw-semibold text-dark">Description</label>
                    <textarea 
                      className="form-control form-control-sm" 
                      rows="3" 
                      placeholder="Outline instructional objectives and key topics covered..."
                      value={lesForm.description} 
                      onChange={(e) => setLesForm({ ...lesForm, description: e.target.value })}
                    ></textarea>
                  </div>
                </div>
                <div className="modal-footer border-top bg-light py-2.5 px-4 d-flex justify-content-between align-items-center">
                  <button type="button" className="btn btn-outline-secondary btn-sm px-3" onClick={() => setShowLesModal(false)}>
                    Cancel
                  </button>
                  <div className="d-flex gap-2">
                    <button 
                      type="button" 
                      className="btn btn-outline-primary btn-sm fw-semibold"
                      disabled={savingLesson}
                      onClick={(e) => handleCreateLesson(e, true)}
                    >
                      {savingLesson ? (
                        <>
                          <span className="spinner-border spinner-border-sm me-1" role="status"></span>
                          Saving...
                        </>
                      ) : (
                        <>
                          <i className="bi bi-plus-circle me-1"></i> Save &amp; Add Another
                        </>
                      )}
                    </button>
                    <button 
                      type="submit" 
                      className="btn btn-primary btn-sm fw-semibold px-3"
                      disabled={savingLesson}
                    >
                      {savingLesson ? (
                        <>
                          <span className="spinner-border spinner-border-sm me-1" role="status"></span>
                          Saving...
                        </>
                      ) : (
                        'Save Lesson'
                      )}
                    </button>
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

