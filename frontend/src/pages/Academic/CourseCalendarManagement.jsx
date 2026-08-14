import React, { useState, useEffect, useMemo } from 'react'
import { useSearchParams } from 'react-router-dom'
import axios from 'axios'
import { toast } from 'react-toastify'
import { CourseCalendarPrintView } from './CourseCalendarPrintView'

export const CourseCalendarManagement = () => {
  const [searchParams] = useSearchParams()

  // Master data states
  const [trades, setTrades] = useState([])
  const [courses, setCourses] = useState([])
  const [instructors, setInstructors] = useState([])
  
  // Selection states
  const [selectedTradeId, setSelectedTradeId] = useState('')
  const [selectedCourseId, setSelectedCourseId] = useState('')
  const [selectedCourse, setSelectedCourse] = useState(null)
  
  // Calendar data states
  const [calendarEntries, setCalendarEntries] = useState([])
  const [loading, setLoading] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  
  // Modal & Print states
  const [showModal, setShowModal] = useState(false)
  const [showPrintModal, setShowPrintModal] = useState(false)
  const [isEditing, setIsEditing] = useState(false)
  const [editingEntryId, setEditingEntryId] = useState(null)
  const [submitting, setSubmitting] = useState(false)

  // Form states with auto-sum
  const defaultFormData = {
    phase_name: '',
    theory_periods: 0,
    practical_periods: 0,
    working_days: 0,
    commencement_date: '',
    completion_date: '',
    instructor_selection: 'NOT_ASSIGNED',
    remarks: ''
  }
  const [formData, setFormData] = useState(defaultFormData)

  // Fetch initial master data
  useEffect(() => {
    fetchTradesAndCourses()
    fetchInstructors()
  }, [])

  const fetchTradesAndCourses = async () => {
    try {
      const [tRes, cRes] = await Promise.all([
        axios.get('/api/v1/academic/trades'),
        axios.get('/api/v1/academic/courses')
      ])
      setTrades(tRes.data || [])
      setCourses(cRes.data || [])
    } catch (err) {
      console.error('Error loading trade/course master data', err)
      toast.error('Failed to load courses list.')
    }
  }

  const fetchInstructors = async () => {
    try {
      const res = await axios.get('/api/v1/academic/instructors/active')
      setInstructors(res.data || [])
    } catch (err) {
      console.error('Error loading instructors list', err)
    }
  }

  // Filter courses by selected trade
  const filteredCourses = useMemo(() => {
    if (!selectedTradeId) return courses
    return courses.filter(c => c.trade_id === selectedTradeId)
  }, [courses, selectedTradeId])

  // Load calendar when selected course changes
  useEffect(() => {
    if (selectedCourseId) {
      const foundCourse = courses.find(c => c.id === selectedCourseId)
      setSelectedCourse(foundCourse || null)
      fetchCalendarEntries(selectedCourseId)
    } else {
      setSelectedCourse(null)
      setCalendarEntries([])
    }
  }, [selectedCourseId, courses])

  // Handle URL query parameters from landing page redirection (course_id & edit_id)
  useEffect(() => {
    const paramCourseId = searchParams.get('course_id')
    if (paramCourseId && courses.length > 0 && paramCourseId !== selectedCourseId) {
      setSelectedCourseId(paramCourseId)
    }
  }, [searchParams, courses])

  useEffect(() => {
    const paramEditId = searchParams.get('edit_id')
    if (paramEditId && calendarEntries.length > 0) {
      const entryToEdit = calendarEntries.find(e => e.id === paramEditId)
      if (entryToEdit) {
        handleOpenEditModal(entryToEdit)
      }
    }
  }, [searchParams, calendarEntries])


  const fetchCalendarEntries = async (courseId) => {
    setLoading(true)
    try {
      const res = await axios.get(`/api/v1/academic/courses/${courseId}/calendar`)
      setCalendarEntries(res.data || [])
    } catch (err) {
      console.error('Failed to fetch course calendar entries', err)
      toast.error('Failed to load course calendar.')
    } finally {
      setLoading(false)
    }
  }

  // Filtered calendar entries by search
  const displayedEntries = useMemo(() => {
    if (!searchTerm.trim()) return calendarEntries
    const term = searchTerm.toLowerCase()
    return calendarEntries.filter(item => 
      (item.phase_name && item.phase_name.toLowerCase().includes(term)) ||
      (item.instructor_name && item.instructor_name.toLowerCase().includes(term)) ||
      (item.remarks && item.remarks.toLowerCase().includes(term))
    )
  }, [calendarEntries, searchTerm])

  // Totals calculations
  const totalTheory = useMemo(() => calendarEntries.reduce((acc, c) => acc + (Number(c.theory_periods) || 0), 0), [calendarEntries])
  const totalPractical = useMemo(() => calendarEntries.reduce((acc, c) => acc + (Number(c.practical_periods) || 0), 0), [calendarEntries])
  const totalPeriods = useMemo(() => calendarEntries.reduce((acc, c) => acc + (Number(c.total_periods) || 0), 0), [calendarEntries])
  const totalWorkingDays = useMemo(() => calendarEntries.reduce((acc, c) => acc + (Number(c.working_days) || 0), 0), [calendarEntries])

  // Real-time calculated total periods for form
  const calculatedFormTotal = (Number(formData.theory_periods) || 0) + (Number(formData.practical_periods) || 0)

  // Handlers for modal opening
  const handleOpenAddModal = () => {
    if (!selectedCourseId) {
      toast.warning('Please select a course first.')
      return
    }
    setIsEditing(false)
    setEditingEntryId(null)
    setFormData(defaultFormData)
    setShowModal(true)
  }

  const handleOpenEditModal = (entry) => {
    setIsEditing(true)
    setEditingEntryId(entry.id)
    const isAssigned = entry.instructor_status === 'ASSIGNED' && entry.instructor_id
    setFormData({
      phase_name: entry.phase_name || '',
      theory_periods: entry.theory_periods || 0,
      practical_periods: entry.practical_periods || 0,
      working_days: entry.working_days || 0,
      commencement_date: entry.commencement_date || '',
      completion_date: entry.completion_date || '',
      instructor_selection: isAssigned ? entry.instructor_id : 'NOT_ASSIGNED',
      remarks: entry.remarks || ''
    })
    setShowModal(true)
  }

  const handleSubmitForm = async (e) => {
    e.preventDefault()
    if (!formData.phase_name.trim()) {
      toast.warning('Phase Name is required.')
      return
    }
    if (!formData.commencement_date || !formData.completion_date) {
      toast.warning('Commencement and Completion dates are required.')
      return
    }
    if (new Date(formData.completion_date) < new Date(formData.commencement_date)) {
      toast.error('Completion date cannot be earlier than commencement date.')
      return
    }
    if (formData.instructor_selection === 'NOT_ASSIGNED' && !formData.remarks.trim()) {
      toast.warning('Remarks are mandatory when Instructor is NOT ASSIGNED (Record nomination status & responsible person).')
      return
    }

    setSubmitting(true)
    try {
      const isSystemInstructor = formData.instructor_selection !== 'NOT_ASSIGNED' && Boolean(formData.instructor_selection)
      const payload = {
        phase_name: formData.phase_name.trim(),
        theory_periods: Number(formData.theory_periods) || 0,
        practical_periods: Number(formData.practical_periods) || 0,
        working_days: Number(formData.working_days) || 0,
        commencement_date: formData.commencement_date,
        completion_date: formData.completion_date,
        instructor_id: isSystemInstructor ? formData.instructor_selection : null,
        instructor_status: isSystemInstructor ? 'ASSIGNED' : 'NOT_ASSIGNED',
        remarks: formData.remarks ? formData.remarks.trim() : null
      }

      if (isEditing) {
        await axios.put(`/api/v1/academic/course-calendar/${editingEntryId}`, payload)
        toast.success('Calendar entry updated successfully!')
      } else {
        await axios.post(`/api/v1/academic/courses/${selectedCourseId}/calendar`, payload)
        toast.success('Calendar entry added successfully!')
      }

      setShowModal(false)
      fetchCalendarEntries(selectedCourseId)
    } catch (err) {
      console.error('Error saving calendar entry', err)
      if (err.response?.status === 409 && err.response?.data?.detail?.message) {
        const d = err.response.data.detail
        toast.error(`Date Conflict: "${d.conflicting_activity}" (${d.conflicting_start_date} to ${d.conflicting_end_date}) overlaps with selected dates!`, { autoClose: 6000 })
      } else {
        const msg = typeof err.response?.data?.detail === 'string'
          ? err.response.data.detail
          : err.response?.data?.detail?.message || 'Failed to save calendar entry.'
        toast.error(msg)
      }
    } finally {
      setSubmitting(false)
    }
  }

  const handleDeleteEntry = async (id, phaseName) => {
    if (!window.confirm(`Are you sure you want to delete calendar entry "${phaseName}"?`)) return
    try {
      await axios.delete(`/api/v1/academic/course-calendar/${id}`)
      toast.success('Calendar entry deleted successfully.')
      fetchCalendarEntries(selectedCourseId)
    } catch (err) {
      console.error('Error deleting calendar entry', err)
      toast.error('Failed to delete calendar entry.')
    }
  }

  // Reorder phase entries up or down
  const handleMoveEntry = async (index, direction) => {
    const newEntries = [...calendarEntries]
    const targetIdx = direction === 'up' ? index - 1 : index + 1
    if (targetIdx < 0 || targetIdx >= newEntries.length) return

    // Swap elements
    const temp = newEntries[index]
    newEntries[index] = newEntries[targetIdx]
    newEntries[targetIdx] = temp

    setCalendarEntries(newEntries)

    try {
      const orderedIds = newEntries.map(e => e.id)
      await axios.post(`/api/v1/academic/courses/${selectedCourseId}/calendar/reorder`, { ordered_ids: orderedIds })
    } catch (err) {
      console.error('Failed to save entry reordering', err)
      toast.error('Failed to reorder entries.')
      fetchCalendarEntries(selectedCourseId)
    }
  }

  // Format Date helper: YYYY-MM-DD -> DD.MM.YYYY
  const formatDateDisplay = (dateStr) => {
    if (!dateStr) return '-'
    const parts = dateStr.split('-')
    if (parts.length === 3) return `${parts[2]}.${parts[1]}.${parts[0]}`
    return dateStr
  }

  // Export to Excel / CSV
  const handleExportExcel = () => {
    if (!calendarEntries.length) {
      toast.warning('No calendar data to export.')
      return
    }

    let csvContent = "data:text/csv;charset=utf-8,"
    csvContent += "S/No,Phase,Theory Periods,Practical Periods,Total Periods,Working Days,Commencement,Completion,Instructor,Remarks\n"

    calendarEntries.forEach(item => {
      const row = [
        String(item.serial_number || '').padStart(2, '0'),
        `"${(item.phase_name || '').replace(/"/g, '""')}"`,
        item.theory_periods || 0,
        item.practical_periods || 0,
        item.total_periods || 0,
        item.working_days || 0,
        formatDateDisplay(item.commencement_date),
        formatDateDisplay(item.completion_date),
        `"${(item.instructor_name || '').replace(/"/g, '""')}"`,
        `"${(item.remarks || '').replace(/"/g, '""')}"`
      ]
      csvContent += row.join(",") + "\n"
    })

    const encodedUri = encodeURI(csvContent)
    const link = document.createElement("a")
    link.setAttribute("href", encodedUri)
    const courseCode = selectedCourse?.code || 'Course'
    link.setAttribute("download", `Course_Calendar_${courseCode}.csv`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    toast.success('Course Calendar exported to CSV successfully.')
  }

  return (
    <div className="fade-in-slide">
      {/* Page Header */}
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h4 className="fw-extrabold display-font text-dark mb-1">
            <i className="bi bi-calendar-range text-primary me-2"></i>
            Course Calendar Management
          </h4>
          <p className="text-muted small mb-0">
            Define course phases, theory/practical periods, working days, and instructor assignments for training schedules.
          </p>
        </div>
      </div>

      {/* Course Selection Search Bar */}
      <div className="card slaf-card p-3 mb-4 shadow-sm">
        <div className="row g-3 align-items-center">
          <div className="col-md-4">
            <label className="form-label small fw-bold text-muted text-uppercase mb-1">
              Filter by Trade Category
            </label>
            <select
              className="form-select"
              value={selectedTradeId}
              onChange={(e) => {
                setSelectedTradeId(e.target.value)
                setSelectedCourseId('')
              }}
            >
              <option value="">All Technical Trades</option>
              {trades.map(t => (
                <option key={t.id} value={t.id}>{t.label}</option>
              ))}
            </select>
          </div>

          <div className="col-md-8">
            <label className="form-label small fw-bold text-primary text-uppercase mb-1">
              Select Course Calendar <span className="text-danger">*</span>
            </label>
            <select
              className="form-select form-select-lg border-primary fw-bold"
              value={selectedCourseId}
              onChange={(e) => setSelectedCourseId(e.target.value)}
            >
              <option value="">-- Choose a Course to View Calendar --</option>
              {filteredCourses.map(c => (
                <option key={c.id} value={c.id}>
                  {c.code} — {c.name} ({c.trade_name || 'General'})
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Main Content Area */}
      {!selectedCourseId ? (
        <div className="card slaf-card text-center p-5 shadow-sm border-dashed">
          <div className="py-4">
            <div className="bg-primary-subtle text-primary rounded-circle d-inline-flex p-3 mb-3">
              <i className="bi bi-calendar-check display-5"></i>
            </div>
            <h5 className="fw-bold text-dark mb-2">No Course Selected</h5>
            <p className="text-muted small max-w-md mx-auto mb-4">
              Select a course from the dropdown above to view, create, edit, or print the complete phase-by-phase course calendar schedule.
            </p>
            {filteredCourses.length > 0 && (
              <div className="d-flex justify-content-center flex-wrap gap-2">
                <span className="text-muted small align-self-center me-2">Quick Select:</span>
                {filteredCourses.slice(0, 4).map(c => (
                  <button 
                    key={c.id} 
                    className="btn btn-sm btn-outline-primary fw-semibold"
                    onClick={() => setSelectedCourseId(c.id)}
                  >
                    <i className="bi bi-journal-text me-1"></i> {c.code}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      ) : (
        <>
          {/* Selected Course Header Banner */}
          {selectedCourse && (
            <div className="card slaf-card bg-light border-start border-4 border-primary p-4 mb-4 shadow-sm">
              <div className="row g-3 align-items-center">
                <div className="col-lg-6">
                  <span className="badge bg-primary text-white text-uppercase px-2.5 py-1 mb-1">
                    {selectedCourse.trade_name || 'Technical Course'}
                  </span>
                  <h4 className="fw-extrabold display-font text-dark mb-1">
                    {selectedCourse.name}
                  </h4>
                  <div className="d-flex flex-wrap gap-3 small text-muted">
                    <span><i className="bi bi-barcode me-1"></i><strong>Code:</strong> {selectedCourse.code}</span>
                    <span><i className="bi bi-clock me-1"></i><strong>Duration:</strong> {selectedCourse.duration_weeks || 24} Weeks</span>
                    <span><i className="bi bi-calendar3 me-1"></i><strong>Dates:</strong> {formatDateDisplay(selectedCourse.start_date)} to {formatDateDisplay(selectedCourse.end_date)}</span>
                  </div>
                </div>

                <div className="col-lg-6">
                  {/* KPI Summary Cards */}
                  <div className="row g-2 text-center">
                    <div className="col-4 col-sm-2.4 col-md">
                      <div className="bg-white rounded p-2 border shadow-xs">
                        <span className="text-muted extra-small fw-bold text-uppercase d-block">Phases</span>
                        <h5 className="fw-extrabold mb-0 text-dark">{calendarEntries.length}</h5>
                      </div>
                    </div>
                    <div className="col-4 col-sm-2.4 col-md">
                      <div className="bg-white rounded p-2 border shadow-xs">
                        <span className="text-muted extra-small fw-bold text-uppercase d-block">Theory</span>
                        <h5 className="fw-extrabold mb-0 text-primary">{totalTheory}</h5>
                      </div>
                    </div>
                    <div className="col-4 col-sm-2.4 col-md">
                      <div className="bg-white rounded p-2 border shadow-xs">
                        <span className="text-muted extra-small fw-bold text-uppercase d-block">Practical</span>
                        <h5 className="fw-extrabold mb-0 text-info">{totalPractical}</h5>
                      </div>
                    </div>
                    <div className="col-6 col-sm-2.4 col-md">
                      <div className="bg-primary text-white rounded p-2 border shadow-xs">
                        <span className="text-white-50 extra-small fw-bold text-uppercase d-block">Total Periods</span>
                        <h5 className="fw-extrabold mb-0 text-white">{totalPeriods}</h5>
                      </div>
                    </div>
                    <div className="col-6 col-sm-2.4 col-md">
                      <div className="bg-white rounded p-2 border shadow-xs">
                        <span className="text-muted extra-small fw-bold text-uppercase d-block">W/Days</span>
                        <h5 className="fw-extrabold mb-0 text-success">{totalWorkingDays}</h5>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Action Toolbar */}
          <div className="card slaf-card p-3 mb-3 shadow-sm">
            <div className="row g-2 align-items-center justify-content-between">
              <div className="col-md-5 col-lg-4">
                <div className="input-group">
                  <span className="input-group-text bg-white text-muted border-end-0">
                    <i className="bi bi-search"></i>
                  </span>
                  <input
                    type="text"
                    className="form-select-sm form-control border-start-0 ps-0"
                    placeholder="Search phase name or instructor..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                  />
                  {searchTerm && (
                    <button className="btn btn-sm btn-outline-secondary" onClick={() => setSearchTerm('')}>
                      <i className="bi bi-x"></i>
                    </button>
                  )}
                </div>
              </div>

              <div className="col-md-7 col-lg-8 text-md-end d-flex flex-wrap justify-content-md-end gap-2">
                <button className="btn btn-primary fw-semibold shadow-xs" onClick={handleOpenAddModal}>
                  <i className="bi bi-plus-circle me-1"></i> Add Calendar Entry
                </button>
                <button className="btn btn-outline-dark fw-semibold shadow-xs" onClick={() => setShowPrintModal(true)}>
                  <i className="bi bi-printer me-1"></i> Print Calendar
                </button>
                <button className="btn btn-outline-success fw-semibold shadow-xs" onClick={handleExportExcel}>
                  <i className="bi bi-file-earmark-excel me-1"></i> Export Excel
                </button>
              </div>
            </div>
          </div>

          {/* Course Calendar Data Table */}
          <div className="card slaf-card border-0 shadow-sm overflow-hidden mb-4">
            <div className="table-responsive">
              <table className="table table-hover align-middle mb-0">
                <thead className="table-dark text-uppercase small align-middle">
                  <tr>
                    <th style={{ width: '60px' }} className="text-center">S/No</th>
                    <th style={{ minWidth: '220px' }}>Phase / Subject Activity</th>
                    <th style={{ width: '120px' }} className="text-center">Theory Periods</th>
                    <th style={{ width: '120px' }} className="text-center">Practical Periods</th>
                    <th style={{ width: '110px' }} className="text-center">Total Periods</th>
                    <th style={{ width: '110px' }} className="text-center">Working Days</th>
                    <th style={{ width: '130px' }} className="text-center">Commencement</th>
                    <th style={{ width: '130px' }} className="text-center">Completion</th>
                    <th style={{ minWidth: '160px' }}>Instructor</th>
                    <th style={{ minWidth: '180px' }}>Remarks</th>
                    <th style={{ width: '130px' }} className="text-end pe-3">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {loading ? (
                    <tr>
                      <td colSpan="11" className="text-center py-5">
                        <div className="spinner-border text-primary me-2" role="status"></div>
                        <span className="text-muted fw-semibold">Loading course calendar phases...</span>
                      </td>
                    </tr>
                  ) : displayedEntries.length > 0 ? (
                    displayedEntries.map((item, index) => (
                      <tr key={item.id}>
                        <td className="text-center fw-bold text-secondary">
                          {String(item.serial_number || index + 1).padStart(2, '0')}
                        </td>
                        <td>
                          <div className="fw-bold text-dark">{item.phase_name}</div>
                        </td>
                        <td className="text-center fw-semibold">
                          {item.theory_periods > 0 ? item.theory_periods : <span className="text-muted">-</span>}
                        </td>
                        <td className="text-center fw-semibold">
                          {item.practical_periods > 0 ? item.practical_periods : <span className="text-muted">-</span>}
                        </td>
                        <td className="text-center">
                          <span className="badge bg-primary-subtle text-primary fw-extrabold px-2.5 py-1">
                            {item.total_periods}
                          </span>
                        </td>
                        <td className="text-center fw-semibold text-dark">
                          {item.working_days > 0 ? item.working_days : <span className="text-muted">-</span>}
                        </td>
                        <td className="text-center small font-monospace">
                          {formatDateDisplay(item.commencement_date)}
                        </td>
                        <td className="text-center small font-monospace">
                          {formatDateDisplay(item.completion_date)}
                        </td>
                        <td>
                          {item.instructor_status === 'ASSIGNED' && item.instructor_name ? (
                            <div>
                              <span className="badge bg-success-subtle text-success me-1">Assigned</span>
                              <span className="small text-dark fw-bold">
                                <i className="bi bi-person-badge text-primary me-1"></i>
                                {item.instructor_name}
                              </span>
                            </div>
                          ) : (
                            <div>
                              <span className="badge bg-warning text-dark fw-extrabold px-2 py-1">
                                <i className="bi bi-person-x-fill me-1"></i>INSTRUCTOR NOT ASSIGNED
                              </span>
                            </div>
                          )}
                        </td>
                        <td>
                          {item.remarks ? (
                            <span className="small text-dark d-block text-wrap" style={{ maxWidth: '240px' }}>
                              {item.remarks}
                            </span>
                          ) : (
                            <span className="text-muted small">-</span>
                          )}
                        </td>
                        <td className="text-end pe-3">
                          <div className="btn-group btn-group-sm">
                            <button
                              className="btn btn-outline-secondary p-1"
                              disabled={index === 0}
                              onClick={() => handleMoveEntry(index, 'up')}
                              title="Move Up"
                            >
                              <i className="bi bi-arrow-up"></i>
                            </button>
                            <button
                              className="btn btn-outline-secondary p-1"
                              disabled={index === calendarEntries.length - 1}
                              onClick={() => handleMoveEntry(index, 'down')}
                              title="Move Down"
                            >
                              <i className="bi bi-arrow-down"></i>
                            </button>
                            <button
                              className="btn btn-outline-primary p-1"
                              onClick={() => handleOpenEditModal(item)}
                              title="Edit Phase"
                            >
                              <i className="bi bi-pencil-fill"></i>
                            </button>
                            <button
                              className="btn btn-outline-danger p-1"
                              onClick={() => handleDeleteEntry(item.id, item.phase_name)}
                              title="Delete Phase"
                            >
                              <i className="bi bi-trash-fill"></i>
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="11" className="text-center py-5 text-muted">
                        <i className="bi bi-inbox display-6 d-block mb-2 text-secondary opacity-50"></i>
                        No phase entries found. Click <strong>"Add Calendar Entry"</strong> to add course activities.
                      </td>
                    </tr>
                  )}
                </tbody>
                {calendarEntries.length > 0 && (
                  <tfoot className="table-light fw-bold">
                    <tr className="border-top border-2 border-secondary">
                      <td colSpan="2" className="text-end text-uppercase pe-3">Summary Totals:</td>
                      <td className="text-center text-primary fs-6">{totalTheory}</td>
                      <td className="text-center text-info fs-6">{totalPractical}</td>
                      <td className="text-center">
                        <span className="badge bg-primary text-white fs-6 px-2.5 py-1">
                          {totalPeriods}
                        </span>
                      </td>
                      <td className="text-center text-success fs-6">{totalWorkingDays}</td>
                      <td colSpan="5" className="small text-muted ps-3">
                        Total Phases: {calendarEntries.length}
                      </td>
                    </tr>
                  </tfoot>
                )}
              </table>
            </div>
          </div>
        </>
      )}

      {/* Add / Edit Phase Modal */}
      {showModal && (
        <div className="modal fade show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)', zIndex: 1050 }} tabIndex="-1">
          <div className="modal-dialog modal-lg modal-dialog-centered">
            <div className="modal-content shadow-lg border-0">
              <div className="modal-header bg-primary text-white p-3">
                <h5 className="modal-title fw-bold">
                  <i className={`bi bi-${isEditing ? 'pencil-square' : 'plus-circle'} me-2`}></i>
                  {isEditing ? 'Edit Calendar Phase Entry' : 'Add New Calendar Phase Entry'}
                </h5>
                <button type="button" className="btn-close btn-close-white" onClick={() => setShowModal(false)}></button>
              </div>

              <form onSubmit={handleSubmitForm}>
                <div className="modal-body p-4">
                  {/* Selected Course Indicator */}
                  <div className="alert alert-primary py-2 px-3 mb-3 small d-flex align-items-center">
                    <i className="bi bi-info-circle-fill me-2 fs-5"></i>
                    <div>
                      <strong>Course:</strong> {selectedCourse?.name} ({selectedCourse?.code})
                    </div>
                  </div>

                  <div className="row g-3">
                    {/* Phase Name */}
                    <div className="col-12">
                      <label className="form-label fw-bold small text-dark">
                        Phase / Subject Activity Name <span className="text-danger">*</span>
                      </label>
                      <input
                        type="text"
                        className="form-control"
                        placeholder="e.g. English Intensive Period, Practical Flight Line Training..."
                        value={formData.phase_name}
                        onChange={(e) => setFormData({ ...formData, phase_name: e.target.value })}
                        required
                      />
                    </div>

                    {/* Periods Breakdown & Auto-Sum */}
                    <div className="col-md-4">
                      <label className="form-label fw-bold small text-dark">
                        No. of Theory Periods
                      </label>
                      <input
                        type="number"
                        min="0"
                        className="form-control"
                        value={formData.theory_periods}
                        onChange={(e) => setFormData({ ...formData, theory_periods: Math.max(0, parseInt(e.target.value) || 0) })}
                      />
                    </div>

                    <div className="col-md-4">
                      <label className="form-label fw-bold small text-dark">
                        No. of Practical Periods
                      </label>
                      <input
                        type="number"
                        min="0"
                        className="form-control"
                        value={formData.practical_periods}
                        onChange={(e) => setFormData({ ...formData, practical_periods: Math.max(0, parseInt(e.target.value) || 0) })}
                      />
                    </div>

                    <div className="col-md-4">
                      <label className="form-label fw-bold small text-primary">
                        Total Periods (Auto-Sum)
                      </label>
                      <input
                        type="number"
                        className="form-control bg-primary-subtle border-primary text-primary fw-extrabold"
                        value={calculatedFormTotal}
                        disabled
                      />
                    </div>

                    {/* Working Days */}
                    <div className="col-md-4">
                      <label className="form-label fw-bold small text-dark">
                        No. of Working Days
                      </label>
                      <input
                        type="number"
                        min="0"
                        className="form-control"
                        value={formData.working_days}
                        onChange={(e) => setFormData({ ...formData, working_days: Math.max(0, parseInt(e.target.value) || 0) })}
                      />
                    </div>

                    {/* Commencement Date */}
                    <div className="col-md-4">
                      <label className="form-label fw-bold small text-dark">
                        Commencement Date <span className="text-danger">*</span>
                      </label>
                      <input
                        type="date"
                        className="form-control"
                        value={formData.commencement_date}
                        onChange={(e) => setFormData({ ...formData, commencement_date: e.target.value })}
                        required
                      />
                    </div>

                    {/* Completion Date */}
                    <div className="col-md-4">
                      <label className="form-label fw-bold small text-dark">
                        Completion Date <span className="text-danger">*</span>
                      </label>
                      <input
                        type="date"
                        className="form-control"
                        value={formData.completion_date}
                        onChange={(e) => setFormData({ ...formData, completion_date: e.target.value })}
                        required
                      />
                    </div>

                    {/* Instructor Selection */}
                    <div className="col-md-12">
                      <label className="form-label fw-bold small text-dark">
                        Assigned Instructor <span className="text-danger">*</span>
                      </label>
                      <select
                        className={`form-select ${formData.instructor_selection === 'NOT_ASSIGNED' ? 'border-warning text-dark fw-semibold' : 'border-primary'}`}
                        value={formData.instructor_selection}
                        onChange={(e) => setFormData({ ...formData, instructor_selection: e.target.value })}
                      >
                        {instructors.map(inst => (
                          <option key={inst.id} value={inst.id}>
                            {inst.display_name}
                          </option>
                        ))}
                        <option value="NOT_ASSIGNED">INSTRUCTOR NOT ASSIGNED</option>
                      </select>
                      {formData.instructor_selection === 'NOT_ASSIGNED' ? (
                        <div className="alert alert-warning py-2 px-3 mt-2 mb-0 small border-warning">
                          <i className="bi bi-exclamation-triangle-fill me-2 text-warning"></i>
                          <strong>Instructor Nomination Pending:</strong> Please record nomination status & responsible person details in <strong>Remarks *</strong>.
                        </div>
                      ) : (
                        <small className="text-muted extra-small">Loaded dynamically from active Instructor/User management records.</small>
                      )}
                    </div>

                    {/* Remarks */}
                    <div className="col-12">
                      <label className="form-label fw-bold small text-dark">
                        Remarks / Nomination Details {formData.instructor_selection === 'NOT_ASSIGNED' && <span className="text-danger">*</span>}
                      </label>
                      <textarea
                        className={`form-control ${formData.instructor_selection === 'NOT_ASSIGNED' ? 'border-warning' : ''}`}
                        rows="2"
                        placeholder={formData.instructor_selection === 'NOT_ASSIGNED' 
                          ? 'e.g. Instructor nomination pending. Responsible Person: Flt Lt Silva, Academic Section.' 
                          : 'Optional phase details, exam schedule notes, or ceremony details...'}
                        value={formData.remarks}
                        onChange={(e) => setFormData({ ...formData, remarks: e.target.value })}
                        required={formData.instructor_selection === 'NOT_ASSIGNED'}
                      ></textarea>
                    </div>
                  </div>
                </div>

                <div className="modal-footer bg-light p-3">
                  <button type="button" className="btn btn-secondary fw-semibold" onClick={() => setShowModal(false)}>
                    Cancel
                  </button>
                  <button type="submit" className="btn btn-primary fw-bold" disabled={submitting}>
                    {submitting ? (
                      <>
                        <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                        Saving...
                      </>
                    ) : (
                      <>
                        <i className="bi bi-check-circle me-1"></i>
                        {isEditing ? 'Update Entry' : 'Save Calendar Entry'}
                      </>
                    )}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Printable SLAF Course Calendar View Modal */}
      {showPrintModal && (
        <CourseCalendarPrintView
          course={selectedCourse}
          entries={calendarEntries}
          onClose={() => setShowPrintModal(false)}
        />
      )}
    </div>
  )
}

export default CourseCalendarManagement
