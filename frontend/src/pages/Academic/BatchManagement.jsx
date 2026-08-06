import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { toast } from 'react-toastify'

export const BatchManagement = () => {
  const [batches, setBatches] = useState([])
  const [trades, setTrades] = useState([])
  const [courses, setCourses] = useState([])
  const [classrooms, setClassrooms] = useState([])
  const [instructors, setInstructors] = useState([])
  const [loading, setLoading] = useState(true)

  const [showModal, setShowModal] = useState(false)
  const [editingBatch, setEditingBatch] = useState(null)

  // Cascading Selection Workflow state
  const [form, setForm] = useState({
    name: '',
    trade_id: '',
    course_id: '',
    intake_date: '',
    passing_out_date: '',
    capacity: 30,
    classroom_id: '',
    instructor_id: '',
    status: 'Active'
  })

  const loadAllMasterData = async () => {
    setLoading(true)
    try {
      const [tRes, cRes, clRes, iRes, bRes] = await Promise.all([
        axios.get('/api/v1/academic/trades'),
        axios.get('/api/v1/academic/courses'),
        axios.get('/api/v1/academic/classrooms'),
        axios.get('/api/v1/academic/instructors'),
        axios.get('/api/v1/academic/batches')
      ])
      setTrades(tRes.data)
      setCourses(cRes.data)
      setClassrooms(clRes.data.filter(c => c.is_active))
      setInstructors(iRes.data)
      setBatches(bRes.data)
    } catch (err) {
      toast.error('Failed to load batch management data')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadAllMasterData()
  }, [])

  // Filter courses by selected trade in form
  const availableCourses = form.trade_id 
    ? courses.filter(c => c.trade_id === form.trade_id)
    : courses

  const handleOpenCreate = () => {
    setEditingBatch(null)
    const initialTradeId = trades.length > 0 ? trades[0].id : ''
    const initialCourses = initialTradeId ? courses.filter(c => c.trade_id === initialTradeId) : courses
    setForm({
      name: '',
      trade_id: initialTradeId,
      course_id: initialCourses.length > 0 ? initialCourses[0].id : '',
      intake_date: new Date().toISOString().split('T')[0],
      passing_out_date: '',
      capacity: 30,
      classroom_id: classrooms.length > 0 ? classrooms[0].id : '',
      instructor_id: instructors.length > 0 ? instructors[0].id : '',
      status: 'Active'
    })
    setShowModal(true)
  }

  const handleOpenEdit = (b) => {
    setEditingBatch(b)
    setForm({
      name: b.name,
      trade_id: b.trade_id || '',
      course_id: b.course_id,
      intake_date: b.intake_date || '',
      passing_out_date: b.passing_out_date || '',
      capacity: b.capacity || 30,
      classroom_id: b.classroom_id || '',
      instructor_id: b.instructor_id || '',
      status: b.status || 'Active'
    })
    setShowModal(true)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!form.name.trim() || !form.course_id) {
      toast.error('Batch Name and Course Selection are required')
      return
    }

    try {
      if (editingBatch) {
        await axios.put(`/api/v1/academic/batches/${editingBatch.id}`, form)
        toast.success(`Batch '${form.name}' updated successfully`)
      } else {
        await axios.post('/api/v1/academic/batches', form)
        toast.success(`Batch '${form.name}' created & assigned successfully`)
      }
      setShowModal(false)
      loadAllMasterData()
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to save batch')
    }
  }

  return (
    <div className="fade-in-slide">
      <div className="d-flex justify-content-between align-items-center mb-3">
        <div>
          <h5 className="fw-bold text-dark mb-0 display-font">Training Batch Management</h5>
          <small className="text-muted">Configure & Assign Batches with Classrooms and SSOT Instructors</small>
        </div>
        <button className="btn btn-primary btn-sm fw-semibold" onClick={handleOpenCreate}>
          <i className="bi bi-layers-plus me-1.5"></i> Configure New Batch
        </button>
      </div>

      {/* Batch Cards / Table */}
      <div className="card slaf-card p-0 shadow-sm">
        <div className="table-responsive">
          <table className="table slaf-table align-middle mb-0">
            <thead>
              <tr>
                <th>Batch Name</th>
                <th>Trade & Course</th>
                <th>Assigned Classroom</th>
                <th>Assigned Instructor</th>
                <th>Intake Date</th>
                <th>Passing Out Date</th>
                <th>Status</th>
                <th className="text-end">Actions</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr><td colSpan="8" className="text-center py-5"><div className="spinner-border text-primary"></div></td></tr>
              ) : batches.length === 0 ? (
                <tr><td colSpan="8" className="text-center py-5 text-muted">No training batches configured.</td></tr>
              ) : (
                batches.map(b => (
                  <tr key={b.id}>
                    <td>
                      <strong className="text-dark d-block">{b.name}</strong>
                      <small className="text-muted">Capacity: {b.capacity} Trainees</small>
                    </td>
                    <td>
                      <span className="fw-semibold text-primary d-block">{b.course_name}</span>
                      <span className="badge bg-secondary-subtle text-dark border px-2 py-0.5" style={{ fontSize: '0.725rem' }}>{b.trade_name}</span>
                    </td>
                    <td>
                      <span className="badge bg-primary-subtle text-primary border"><i className="bi bi-door-open me-1"></i>{b.classroom_name}</span>
                    </td>
                    <td>
                      <div>
                        <strong className="text-dark d-block small">{b.instructor_name}</strong>
                        <small className="text-muted">{b.instructor_rank ? `${b.instructor_rank} • ${b.instructor_service_number || ''}` : 'Instructor'}</small>
                      </div>
                    </td>
                    <td><small className="text-muted">{b.intake_date || 'N/A'}</small></td>
                    <td><small className="text-muted">{b.passing_out_date || 'N/A'}</small></td>
                    <td>
                      <span className={`badge bg-${b.status === 'Active' ? 'success' : 'secondary'}-subtle text-${b.status === 'Active' ? 'success' : 'secondary'} border px-2 py-0.5`}>
                        {b.status}
                      </span>
                    </td>
                    <td className="text-end">
                      <button className="btn btn-outline-secondary btn-sm" onClick={() => handleOpenEdit(b)}>
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

      {/* Batch Workflow Modal */}
      {showModal && (
        <div className="modal fade show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)', zIndex: 1060 }}>
          <div className="modal-dialog modal-lg modal-dialog-centered">
            <div className="modal-content slaf-card">
              <div className="modal-header border-bottom">
                <h5 className="modal-title display-font text-primary fw-bold">
                  {editingBatch ? `Edit Batch: ${editingBatch.name}` : 'Configure New Training Batch (Workflow)'}
                </h5>
                <button type="button" className="btn-close" onClick={() => setShowModal(false)}></button>
              </div>
              <form onSubmit={handleSubmit}>
                <div className="modal-body" style={{ maxHeight: '75vh', overflowY: 'auto' }}>
                  {/* Workflow Breadcrumb Indicator */}
                  <div className="alert alert-primary py-2 px-3 mb-3 d-flex align-items-center gap-2 small">
                    <i className="bi bi-diagram-3-fill fs-5"></i>
                    <div>
                      <strong>Batch Configuration Workflow:</strong> Select Trade → Select Course → Assign Classroom → Assign Instructor → Save
                    </div>
                  </div>

                  <div className="row g-3">
                    {/* Step 1: Select Trade */}
                    <div className="col-md-6">
                      <label className="form-label fw-semibold small text-muted">Step 1: Select Trade*</label>
                      <select 
                        className="form-select"
                        value={form.trade_id}
                        onChange={(e) => {
                          const newTradeId = e.target.value
                          const filteredC = courses.filter(c => c.trade_id === newTradeId)
                          setForm({
                            ...form,
                            trade_id: newTradeId,
                            course_id: filteredC.length > 0 ? filteredC[0].id : ''
                          })
                        }}
                        required
                      >
                        <option value="">-- Select Trade --</option>
                        {trades.map(t => (
                          <option key={t.id} value={t.id}>{t.label} ({t.code})</option>
                        ))}
                      </select>
                    </div>

                    {/* Step 2: Select Course */}
                    <div className="col-md-6">
                      <label className="form-label fw-semibold small text-muted">Step 2: Select Course*</label>
                      <select 
                        className="form-select"
                        value={form.course_id}
                        onChange={(e) => setForm({ ...form, course_id: e.target.value })}
                        required
                      >
                        <option value="">-- Select Course --</option>
                        {availableCourses.map(c => (
                          <option key={c.id} value={c.id}>{c.name} ({c.code})</option>
                        ))}
                      </select>
                    </div>

                    {/* Step 3: Batch Name & Capacity */}
                    <div className="col-md-8">
                      <label className="form-label fw-semibold small text-muted">Batch Name*</label>
                      <input 
                        type="text" 
                        className="form-control" 
                        placeholder="e.g. Batch 2026-A, Intake 174-A" 
                        value={form.name}
                        onChange={(e) => setForm({ ...form, name: e.target.value })}
                        required
                      />
                    </div>

                    <div className="col-md-4">
                      <label className="form-label fw-semibold small text-muted">Batch Capacity</label>
                      <input 
                        type="number" 
                        className="form-control" 
                        value={form.capacity}
                        onChange={(e) => setForm({ ...form, capacity: parseInt(e.target.value) || 0 })}
                        min="1"
                      />
                    </div>

                    {/* Step 4: Assign Classroom */}
                    <div className="col-md-6">
                      <label className="form-label fw-semibold small text-muted">Step 3: Assign Active Classroom*</label>
                      <select 
                        className="form-select"
                        value={form.classroom_id}
                        onChange={(e) => setForm({ ...form, classroom_id: e.target.value })}
                      >
                        <option value="">-- Select Active Classroom --</option>
                        {classrooms.map(cl => (
                          <option key={cl.id} value={cl.id}>{cl.code} - {cl.name} (Cap: {cl.capacity})</option>
                        ))}
                      </select>
                      <small className="text-muted">Only active classrooms are displayed.</small>
                    </div>

                    {/* Step 5: Assign Instructor (SSOT) */}
                    <div className="col-md-6">
                      <label className="form-label fw-semibold small text-muted">Step 4: Assign Instructor (User Management SSOT)*</label>
                      <select 
                        className="form-select"
                        value={form.instructor_id}
                        onChange={(e) => setForm({ ...form, instructor_id: e.target.value })}
                      >
                        <option value="">-- Select Active Instructor --</option>
                        {instructors.map(inst => (
                          <option key={inst.id} value={inst.id}>
                            {inst.rank || ''} {inst.full_name} ({inst.service_number || 'Staff'})
                          </option>
                        ))}
                      </select>
                      <small className="text-muted">Dynamically loaded from User Management Portal.</small>
                    </div>

                    {/* Dates */}
                    <div className="col-md-6">
                      <label className="form-label fw-semibold small text-muted">Intake Date</label>
                      <input 
                        type="date" 
                        className="form-control" 
                        value={form.intake_date}
                        onChange={(e) => setForm({ ...form, intake_date: e.target.value })}
                      />
                    </div>

                    <div className="col-md-6">
                      <label className="form-label fw-semibold small text-muted">Passing Out Date</label>
                      <input 
                        type="date" 
                        className="form-control" 
                        value={form.passing_out_date}
                        onChange={(e) => setForm({ ...form, passing_out_date: e.target.value })}
                      />
                    </div>
                  </div>
                </div>
                <div className="modal-footer border-top">
                  <button type="button" className="btn btn-outline-secondary btn-sm" onClick={() => setShowModal(false)}>Cancel</button>
                  <button type="submit" className="btn btn-primary btn-sm fw-semibold">Save & Assign Batch</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
