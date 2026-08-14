import React, { useState, useEffect } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
import axios from 'axios'
import { toast } from 'react-toastify'
import { useAuth } from '../../context/AuthContext'

export const PersonalOccurrenceReporting = ({ initialTraineeId = null }) => {
  const { hasPermission } = useAuth()
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()

  // Master Trainees List for Selection
  const [trainees, setTrainees] = useState([])
  const [selectedTraineeId, setSelectedTraineeId] = useState(initialTraineeId || searchParams.get('trainee_id') || '')

  // Occurrences Data State
  const [occurrences, setOccurrences] = useState([])
  const [loading, setLoading] = useState(true)

  // Filters State
  const [searchQuery, setSearchQuery] = useState('')
  const [filterType, setFilterType] = useState('ALL') // ALL, ACHIEVEMENT, MISCONDUCT_OFFENSE
  const [dateFrom, setDateFrom] = useState('')
  const [dateTo, setDateTo] = useState('')

  // Add / Edit Modal State
  const [showModal, setShowModal] = useState(false)
  const [editingOccurrence, setEditingOccurrence] = useState(null)
  const [submitting, setSubmitting] = useState(false)

  // Delete Modal State
  const [showDeleteModal, setShowDeleteModal] = useState(false)
  const [deletingId, setDeletingId] = useState(null)
  const [deletingTitle, setDeletingTitle] = useState('')

  // Form State
  const defaultForm = {
    trainee_id: '',
    occurrence_type: 'ACHIEVEMENT',
    occurrence_date: new Date().toISOString().split('T')[0],
    title: '',
    description: '',
    remarks: ''
  }
  const [form, setForm] = useState(defaultForm)

  // Fetch Trainees list for dropdown
  useEffect(() => {
    fetchTrainees()
  }, [])

  const fetchTrainees = async () => {
    try {
      const res = await axios.get('/api/v1/students', { params: { limit: 500 } })
      setTrainees(res.data.items || [])
    } catch (err) {
      console.error('Failed to load trainees list', err)
    }
  }

  // Fetch Occurrences
  const fetchOccurrences = async () => {
    setLoading(true)
    try {
      const params = {}
      if (selectedTraineeId) params.trainee_id = selectedTraineeId
      if (filterType && filterType !== 'ALL') params.occurrence_type = filterType
      if (dateFrom) params.date_from = dateFrom
      if (dateTo) params.date_to = dateTo
      if (searchQuery.trim()) params.search = searchQuery.trim()

      const res = await axios.get('/api/v1/personal-occurrences', { params })
      setOccurrences(res.data.items || [])
    } catch (err) {
      console.error('Failed to load personal occurrences', err)
      if (err.response?.status === 403) {
        toast.error('Access Denied: You do not have permission to view Personal Occurrence Reporting.')
      } else {
        toast.error('Failed to load personal occurrence history.')
      }
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchOccurrences()
  }, [selectedTraineeId, filterType, dateFrom, dateTo])

  // Open Create Modal
  const handleOpenCreate = () => {
    setEditingOccurrence(null)
    setForm({
      ...defaultForm,
      trainee_id: selectedTraineeId || (trainees.length > 0 ? trainees[0].id : '')
    })
    setShowModal(true)
  }

  // Open Edit Modal
  const handleOpenEdit = (occ) => {
    setEditingOccurrence(occ)
    setForm({
      trainee_id: occ.trainee_id,
      occurrence_type: occ.occurrence_type,
      occurrence_date: occ.occurrence_date,
      title: occ.title || '',
      description: occ.description || '',
      remarks: occ.remarks || ''
    })
    setShowModal(true)
  }

  // Submit Form (Create / Update)
  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!form.trainee_id) {
      toast.warning('Please select a target trainee.')
      return
    }
    if (!form.title.trim()) {
      toast.warning('Occurrence title is required.')
      return
    }
    if (!form.description.trim()) {
      toast.warning('Detailed description is required.')
      return
    }

    setSubmitting(true)
    try {
      const payload = {
        trainee_id: form.trainee_id,
        occurrence_type: form.occurrence_type,
        occurrence_date: form.occurrence_date,
        title: form.title.trim(),
        description: form.description.trim(),
        remarks: form.remarks ? form.remarks.trim() : null
      }

      if (editingOccurrence) {
        await axios.put(`/api/v1/personal-occurrences/${editingOccurrence.id}`, payload)
        toast.success('Personal occurrence record updated successfully!')
      } else {
        await axios.post(`/api/v1/students/${form.trainee_id}/occurrences`, payload)
        toast.success('Personal occurrence recorded successfully!')
      }

      setShowModal(false)
      fetchOccurrences()
    } catch (err) {
      console.error('Error saving occurrence', err)
      toast.error(err.response?.data?.detail || 'Failed to save occurrence record.')
    } finally {
      setSubmitting(false)
    }
  }

  // Handle Delete
  const handleOpenDelete = (occ) => {
    setDeletingId(occ.id)
    setDeletingTitle(occ.title)
    setShowDeleteModal(true)
  }

  const handleConfirmDelete = async () => {
    if (!deletingId) return
    try {
      await axios.delete(`/api/v1/personal-occurrences/${deletingId}`)
      toast.success('Personal occurrence record deleted successfully.')
      setShowDeleteModal(false)
      fetchOccurrences()
    } catch (err) {
      console.error('Failed to delete occurrence', err)
      toast.error(err.response?.data?.detail || 'Failed to delete occurrence record.')
    }
  }

  const handleResetFilters = () => {
    setSelectedTraineeId('')
    setFilterType('ALL')
    setDateFrom('')
    setDateTo('')
    setSearchQuery('')
  }

  const formatDateDDMMYYYY = (dateStr) => {
    if (!dateStr) return 'N/A'
    const parts = dateStr.split('-')
    if (parts.length === 3) return `${parts[2]}.${parts[1]}.${parts[0]}`
    return dateStr
  }

  return (
    <div className="fade-in-slide">
      {/* Header Banner */}
      <div className="d-flex justify-content-between align-items-center mb-3">
        <div>
          <h4 className="fw-extrabold text-dark mb-0 display-font">Personal Occurrence Reporting</h4>
          <p className="text-muted small mb-0">
            Restricted Personnel Management SSOT for Trainee Achievements & Misconduct Records.
          </p>
        </div>
        {hasPermission('personal_occurrence:write') && (
          <button className="btn btn-primary btn-sm fw-bold shadow-sm" onClick={handleOpenCreate}>
            <i className="bi bi-plus-lg me-1"></i> Add Personal Occurrence
          </button>
        )}
      </div>

      {/* Filter Toolbar */}
      <div className="card slaf-card p-3 mb-4 shadow-sm">
        <div className="row g-2 align-items-end">
          {/* Trainee Dropdown Filter */}
          <div className="col-md-3">
            <label className="form-label text-muted fw-bold mb-1" style={{ fontSize: '0.7rem' }}>TARGET TRAINEE</label>
            <select
              className="form-select form-select-sm"
              value={selectedTraineeId}
              onChange={(e) => setSelectedTraineeId(e.target.value)}
            >
              <option value="">All Trainees</option>
              {trainees.map(t => (
                <option key={t.id} value={t.id}>
                  {t.service_number} - {t.rank} {t.full_name} ({t.trade})
                </option>
              ))}
            </select>
          </div>

          {/* Occurrence Type Filter */}
          <div className="col-md-2.5 col-lg-2">
            <label className="form-label text-muted fw-bold mb-1" style={{ fontSize: '0.7rem' }}>OCCURRENCE TYPE</label>
            <select
              className="form-select form-select-sm"
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
            >
              <option value="ALL">All Categories</option>
              <option value="ACHIEVEMENT">🟢 Achievements</option>
              <option value="MISCONDUCT_OFFENSE">🔴 Misconduct / Offenses</option>
            </select>
          </div>

          {/* Date From */}
          <div className="col-6 col-md-2">
            <label className="form-label text-muted fw-bold mb-1" style={{ fontSize: '0.7rem' }}>DATE FROM</label>
            <input
              type="date"
              className="form-control form-control-sm"
              value={dateFrom}
              onChange={(e) => setDateFrom(e.target.value)}
            />
          </div>

          {/* Date To */}
          <div className="col-6 col-md-2">
            <label className="form-label text-muted fw-bold mb-1" style={{ fontSize: '0.7rem' }}>DATE TO</label>
            <input
              type="date"
              className="form-control form-control-sm"
              value={dateTo}
              onChange={(e) => setDateTo(e.target.value)}
            />
          </div>

          {/* Search Box */}
          <div className="col-md-2.5 col-lg-2">
            <div className="input-group input-group-sm">
              <input
                type="text"
                className="form-control"
                placeholder="Search title/text..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && fetchOccurrences()}
              />
              <button className="btn btn-outline-secondary" type="button" onClick={fetchOccurrences}>
                <i className="bi bi-search"></i>
              </button>
            </div>
          </div>

          {/* Reset Filters */}
          <div className="col-md-1">
            <button className="btn btn-outline-secondary btn-sm w-100 fw-semibold" onClick={handleResetFilters} title="Reset Filters">
              <i className="bi bi-x-circle me-1"></i>Reset
            </button>
          </div>
        </div>
      </div>

      {/* Occurrences List / Timeline Grid */}
      {loading ? (
        <div className="text-center py-5">
          <div className="spinner-border text-primary me-2"></div>
          <span className="fw-semibold text-secondary">Loading personal occurrence records...</span>
        </div>
      ) : occurrences.length === 0 ? (
        <div className="card slaf-card p-5 text-center shadow-sm">
          <i className="bi bi-journal-x display-4 text-muted mb-2"></i>
          <h5 className="fw-bold text-dark">No Personal Occurrence Records Found</h5>
          <p className="text-muted small mb-0">No achievement or misconduct entries match the selected filters.</p>
        </div>
      ) : (
        <div className="d-flex flex-column gap-3">
          {occurrences.map(occ => {
            const isAchievement = occ.occurrence_type === 'ACHIEVEMENT'
            return (
              <div
                key={occ.id}
                className={`card slaf-card shadow-sm border-0 border-start border-4 ${
                  isAchievement ? 'border-success' : 'border-danger'
                }`}
              >
                <div className={`card-header py-2.5 px-3 d-flex justify-content-between align-items-center ${
                  isAchievement ? 'bg-success-subtle text-success-emphasis' : 'bg-danger-subtle text-danger-emphasis'
                }`}>
                  <div className="d-flex align-items-center gap-2">
                    <span style={{ fontSize: '1.2rem' }}>
                      {isAchievement ? '🟢' : '🔴'}
                    </span>
                    <strong className="fw-extrabold text-uppercase" style={{ fontSize: '0.85rem', letterSpacing: '0.5px' }}>
                      {isAchievement ? 'ACHIEVEMENTS' : 'MISCONDUCT / OFFENSES'}
                    </strong>
                  </div>
                  <div className="d-flex align-items-center gap-2">
                    <span className="badge bg-white text-dark border fw-bold">
                      <i className="bi bi-calendar-event me-1 text-primary"></i>
                      {formatDateDDMMYYYY(occ.occurrence_date)}
                    </span>
                  </div>
                </div>

                <div className="card-body p-3">
                  <div className="d-flex justify-content-between align-items-start mb-2">
                    <div>
                      <h5 className="fw-bold text-dark mb-1">{occ.title}</h5>
                      <p className="text-muted small mb-2">
                        Trainee: <strong className="text-dark cursor-pointer" onClick={() => navigate(`/students/${occ.trainee_id}`)}>{occ.trainee_service_number} - {occ.trainee_rank} {occ.trainee_full_name}</strong>
                        {occ.trainee_trade && <span className="ms-2 badge bg-secondary-subtle text-dark border">{occ.trainee_trade}</span>}
                        {occ.trainee_batch && <span className="ms-1 badge bg-light text-dark border">Batch {occ.trainee_batch}</span>}
                      </p>
                    </div>
                    
                    {/* Action buttons if permitted */}
                    <div className="d-flex gap-1">
                      {hasPermission('personal_occurrence:write') && (
                        <button className="btn btn-outline-secondary btn-sm" onClick={() => handleOpenEdit(occ)} title="Edit Occurrence">
                          <i className="bi bi-pencil me-1"></i>Edit
                        </button>
                      )}
                      {hasPermission('personal_occurrence:delete') && (
                        <button className="btn btn-outline-danger btn-sm" onClick={() => handleOpenDelete(occ)} title="Delete Record">
                          <i className="bi bi-trash me-1"></i>Delete
                        </button>
                      )}
                    </div>
                  </div>

                  <div className="p-3 bg-light rounded border mb-2">
                    <p className="mb-0 text-dark small white-space-pre-wrap">{occ.description}</p>
                  </div>

                  {occ.remarks && (
                    <div className="p-2.5 bg-warning-subtle text-dark rounded border border-warning mb-2" style={{ fontSize: '0.8rem' }}>
                      <strong>Remarks:</strong> {occ.remarks}
                    </div>
                  )}

                  <div className="d-flex justify-content-between align-items-center text-muted pt-2 border-top" style={{ fontSize: '0.725rem' }}>
                    <span>
                      <i className="bi bi-person-check me-1"></i>Recorded By: <strong>{occ.creator_name || 'System Admin'}</strong>
                    </span>
                    <span>
                      <i className="bi bi-clock me-1"></i>Recorded Date: {new Date(occ.created_at).toLocaleString()}
                    </span>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      )}

      {/* Add / Edit Modal */}
      {showModal && (
        <div className="modal fade show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)', zIndex: 1060 }} tabIndex="-1">
          <div className="modal-dialog modal-lg modal-dialog-centered">
            <div className="modal-content slaf-card border-0 shadow-lg">
              <div className="modal-header bg-primary text-white py-3">
                <div className="d-flex align-items-center gap-2">
                  <i className="bi bi-journal-plus fs-5"></i>
                  <h5 className="modal-title fw-bold">
                    {editingOccurrence ? 'Edit Personal Occurrence Record' : 'Add Personal Occurrence Record'}
                  </h5>
                </div>
                <button type="button" className="btn-close btn-close-white" onClick={() => setShowModal(false)}></button>
              </div>

              <form onSubmit={handleSubmit}>
                <div className="modal-body p-4">
                  <div className="row g-3">
                    {/* Trainee Selection */}
                    <div className="col-md-7">
                      <label className="form-label fw-bold small text-muted">SELECT TRAINEE*</label>
                      <select
                        className="form-select"
                        value={form.trainee_id}
                        onChange={(e) => setForm({ ...form, trainee_id: e.target.value })}
                        required
                        disabled={Boolean(editingOccurrence)}
                      >
                        <option value="">-- Select Trainee --</option>
                        {trainees.map(t => (
                          <option key={t.id} value={t.id}>
                            {t.service_number} - {t.rank} {t.full_name} ({t.trade})
                          </option>
                        ))}
                      </select>
                    </div>

                    {/* Occurrence Type Select */}
                    <div className="col-md-5">
                      <label className="form-label fw-bold small text-muted">OCCURRENCE CATEGORY*</label>
                      <select
                        className="form-select"
                        value={form.occurrence_type}
                        onChange={(e) => setForm({ ...form, occurrence_type: e.target.value })}
                        required
                      >
                        <option value="ACHIEVEMENT">🟢 Achievements</option>
                        <option value="MISCONDUCT_OFFENSE">🔴 Misconduct / Offenses</option>
                      </select>
                    </div>

                    {/* Occurrence Date */}
                    <div className="col-md-5">
                      <label className="form-label fw-bold small text-muted">OCCURRENCE DATE*</label>
                      <input
                        type="date"
                        className="form-control"
                        value={form.occurrence_date}
                        onChange={(e) => setForm({ ...form, occurrence_date: e.target.value })}
                        required
                      />
                    </div>

                    {/* Title */}
                    <div className="col-md-7">
                      <label className="form-label fw-bold small text-muted">OCCURRENCE TITLE / SUBJECT*</label>
                      <input
                        type="text"
                        className="form-control"
                        placeholder="e.g. Outstanding Academic Performance or Repeated Late Attendance"
                        value={form.title}
                        onChange={(e) => setForm({ ...form, title: e.target.value })}
                        required
                      />
                    </div>

                    {/* Description */}
                    <div className="col-12">
                      <label className="form-label fw-bold small text-muted">DETAILED DESCRIPTION*</label>
                      <textarea
                        className="form-control"
                        rows="3"
                        placeholder="Enter full details of the achievement or misconduct incident..."
                        value={form.description}
                        onChange={(e) => setForm({ ...form, description: e.target.value })}
                        required
                      ></textarea>
                    </div>

                    {/* Remarks */}
                    <div className="col-12">
                      <label className="form-label fw-bold small text-muted">REMARKS / ACTION TAKEN (OPTIONAL)</label>
                      <textarea
                        className="form-control"
                        rows="2"
                        placeholder="Optional supervisory remarks, award details, or disciplinary action..."
                        value={form.remarks}
                        onChange={(e) => setForm({ ...form, remarks: e.target.value })}
                      ></textarea>
                    </div>
                  </div>
                </div>

                <div className="modal-footer bg-light py-2">
                  <button type="button" className="btn btn-secondary btn-sm fw-semibold" onClick={() => setShowModal(false)}>
                    Cancel
                  </button>
                  <button type="submit" className="btn btn-primary btn-sm fw-bold shadow-sm" disabled={submitting}>
                    {submitting ? 'Saving...' : 'Save Occurrence'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {showDeleteModal && (
        <div className="modal fade show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.6)', zIndex: 1070 }} tabIndex="-1">
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content slaf-card border-0 shadow-lg">
              <div className="modal-header bg-danger text-white py-3">
                <div className="d-flex align-items-center gap-2">
                  <i className="bi bi-exclamation-triangle-fill fs-5"></i>
                  <h5 className="modal-title fw-bold">Confirm Delete Record</h5>
                </div>
                <button type="button" className="btn-close btn-close-white" onClick={() => setShowDeleteModal(false)}></button>
              </div>

              <div className="modal-body p-4 text-center">
                <p className="mb-2 text-dark fs-6">
                  Are you sure you want to delete this personal occurrence record?
                </p>
                <strong className="text-danger d-block mb-3">"{deletingTitle}"</strong>
                <p className="text-muted small mb-0">
                  This record will be soft-deleted in accordance with SLAF record-retention policy and logged in system audit trails.
                </p>
              </div>

              <div className="modal-footer bg-light py-2">
                <button type="button" className="btn btn-secondary btn-sm fw-semibold" onClick={() => setShowDeleteModal(false)}>
                  Cancel
                </button>
                <button type="button" className="btn btn-danger btn-sm fw-bold shadow-sm" onClick={handleConfirmDelete}>
                  Yes, Delete Record
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default PersonalOccurrenceReporting
