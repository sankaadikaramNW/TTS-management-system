import React, { useState, useEffect, useCallback } from 'react'
import axios from 'axios'
import { toast } from 'react-toastify'
import { useAuth } from '../../context/AuthContext'
import { LessonPlanUploadModal } from './LessonPlanUploadModal'
import { LessonPlanPreviewModal } from './LessonPlanPreviewModal'
import { LessonPlanEditModal } from './LessonPlanEditModal'

export const LessonPlanDocuments = () => {
  const { hasPermission } = useAuth()
  const canWrite = hasPermission('academic:write')

  // Data state
  const [trades, setTrades] = useState([])
  const [courses, setCourses] = useState([])
  const [documents, setDocuments] = useState([])
  const [loading, setLoading] = useState(false)
  const [loadingCourses, setLoadingCourses] = useState(false)

  // Filters
  const [selectedTradeId, setSelectedTradeId] = useState('')
  const [selectedCourseId, setSelectedCourseId] = useState('')
  const [statusFilter, setStatusFilter] = useState('Active')
  const [searchQuery, setSearchQuery] = useState('')

  // Modals
  const [showUploadModal, setShowUploadModal] = useState(false)
  const [showPreviewModal, setShowPreviewModal] = useState(false)
  const [showEditModal, setShowEditModal] = useState(false)
  const [selectedDocument, setSelectedDocument] = useState(null)
  const [editMode, setEditMode] = useState('edit') // 'edit' or 'replace'

  // Confirmation
  const [confirmAction, setConfirmAction] = useState(null)

  // Load trades on mount
  useEffect(() => {
    const fetchTrades = async () => {
      try {
        const res = await axios.get('/api/v1/academic/trades')
        setTrades(res.data)
      } catch (err) {
        toast.error('Failed to load trades')
      }
    }
    fetchTrades()
  }, [])

  // Load courses when trade changes
  useEffect(() => {
    if (!selectedTradeId) {
      setCourses([])
      setSelectedCourseId('')
      return
    }
    const fetchCourses = async () => {
      setLoadingCourses(true)
      try {
        const res = await axios.get(`/api/v1/academic/courses?trade_id=${selectedTradeId}`)
        setCourses(res.data)
      } catch (err) {
        toast.error('Failed to load courses')
      } finally {
        setLoadingCourses(false)
      }
    }
    fetchCourses()
    setSelectedCourseId('')
  }, [selectedTradeId])

  // Load documents
  const fetchDocuments = useCallback(async () => {
    setLoading(true)
    try {
      const params = new URLSearchParams()
      if (selectedCourseId) params.append('course_id', selectedCourseId)
      if (selectedTradeId && !selectedCourseId) params.append('trade_id', selectedTradeId)
      if (statusFilter && statusFilter !== 'All') params.append('status', statusFilter)
      if (searchQuery.trim()) params.append('search', searchQuery.trim())

      const res = await axios.get(`/api/v1/academic/lesson-plans?${params.toString()}`)
      setDocuments(res.data)
    } catch (err) {
      toast.error('Failed to load lesson plan documents')
    } finally {
      setLoading(false)
    }
  }, [selectedCourseId, selectedTradeId, statusFilter, searchQuery])

  useEffect(() => {
    fetchDocuments()
  }, [fetchDocuments])

  // Handlers
  const handlePreview = (doc) => {
    setSelectedDocument(doc)
    setShowPreviewModal(true)
  }

  const handleEdit = (doc) => {
    setSelectedDocument(doc)
    setEditMode('edit')
    setShowEditModal(true)
  }

  const handleReplace = (doc) => {
    setSelectedDocument(doc)
    setEditMode('replace')
    setShowEditModal(true)
  }

  const handleDownload = (doc) => {
    window.open(doc.cloudinary_url, '_blank')
  }

  const handleArchive = (doc) => {
    setConfirmAction({
      type: 'archive',
      doc,
      title: 'Archive Lesson Plan',
      message: `Are you sure you want to archive "${doc.title}"? It will no longer appear in the active document list.`
    })
  }

  const handleDelete = (doc) => {
    setConfirmAction({
      type: 'delete',
      doc,
      title: 'Permanently Delete Lesson Plan',
      message: `Are you sure you want to permanently delete "${doc.title}"? This action cannot be undone and will remove the file from cloud storage.`
    })
  }

  const executeConfirmAction = async () => {
    if (!confirmAction) return
    const { type, doc } = confirmAction
    try {
      if (type === 'archive') {
        await axios.patch(`/api/v1/academic/lesson-plans/${doc.id}/archive`)
        toast.success(`"${doc.title}" has been archived.`)
      } else if (type === 'delete') {
        await axios.delete(`/api/v1/academic/lesson-plans/${doc.id}`)
        toast.success(`"${doc.title}" has been permanently deleted.`)
      }
      fetchDocuments()
    } catch (err) {
      toast.error(err.response?.data?.detail || `Failed to ${type} document.`)
    } finally {
      setConfirmAction(null)
    }
  }

  const handleClearFilters = () => {
    setSelectedTradeId('')
    setSelectedCourseId('')
    setStatusFilter('Active')
    setSearchQuery('')
  }

  const formatFileSize = (bytes) => {
    if (!bytes) return 'N/A'
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`
  }

  const formatDate = (dateStr) => {
    if (!dateStr) return 'N/A'
    return new Date(dateStr).toLocaleDateString('en-GB', {
      day: '2-digit', month: 'short', year: 'numeric'
    })
  }

  return (
    <div className="lesson-plan-documents">
      {/* Header */}
      <div className="d-flex flex-wrap justify-content-between align-items-center mb-4 gap-2">
        <div>
          <h4 className="fw-bold text-dark mb-1">
            <i className="bi bi-file-earmark-pdf-fill text-danger me-2"></i>
            Lesson Plan Documents
          </h4>
          <p className="text-muted small mb-0">
            Upload, manage, and preview PDF lesson plan documents for courses
          </p>
        </div>
        {canWrite && (
          <button
            className="btn btn-primary d-flex align-items-center gap-2 px-4 py-2 shadow-sm"
            onClick={() => setShowUploadModal(true)}
            id="btn-upload-lesson-plan"
          >
            <i className="bi bi-cloud-upload-fill"></i>
            Upload Lesson Plan
          </button>
        )}
      </div>

      {/* Filters Row */}
      <div className="card shadow-sm border-0 mb-4">
        <div className="card-body py-3">
          <div className="row g-3 align-items-end">
            {/* Trade Filter */}
            <div className="col-md-3 col-sm-6">
              <label className="form-label small fw-semibold text-muted mb-1">
                <i className="bi bi-wrench me-1"></i>Trade
              </label>
              <select
                className="form-select form-select-sm"
                value={selectedTradeId}
                onChange={(e) => setSelectedTradeId(e.target.value)}
                id="filter-trade"
              >
                <option value="">All Trades</option>
                {trades.map(t => (
                  <option key={t.id} value={t.id}>{t.label}</option>
                ))}
              </select>
            </div>

            {/* Course Filter */}
            <div className="col-md-3 col-sm-6">
              <label className="form-label small fw-semibold text-muted mb-1">
                <i className="bi bi-book-half me-1"></i>Course
              </label>
              <select
                className="form-select form-select-sm"
                value={selectedCourseId}
                onChange={(e) => setSelectedCourseId(e.target.value)}
                disabled={!selectedTradeId || loadingCourses}
                id="filter-course"
              >
                <option value="">
                  {!selectedTradeId 
                    ? 'Select a Trade first' 
                    : loadingCourses 
                    ? 'Loading...' 
                    : courses.length === 0 
                    ? 'No courses available for this Trade' 
                    : 'All Courses'}
                </option>
                {courses.map(c => (
                  <option key={c.id} value={c.id}>{c.name}</option>
                ))}
              </select>
            </div>

            {/* Status Filter */}
            <div className="col-md-2 col-sm-6">
              <label className="form-label small fw-semibold text-muted mb-1">
                <i className="bi bi-funnel me-1"></i>Status
              </label>
              <select
                className="form-select form-select-sm"
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                id="filter-status"
              >
                <option value="Active">Active</option>
                <option value="Archived">Archived</option>
                <option value="All">All</option>
              </select>
            </div>

            {/* Search */}
            <div className="col-md-3 col-sm-6">
              <label className="form-label small fw-semibold text-muted mb-1">
                <i className="bi bi-search me-1"></i>Search
              </label>
              <input
                type="text"
                className="form-control form-control-sm"
                placeholder="Search by title, filename..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                id="filter-search"
              />
            </div>

            {/* Clear */}
            <div className="col-md-1 col-sm-6 d-flex align-items-end">
              <button
                className="btn btn-outline-secondary btn-sm w-100"
                onClick={handleClearFilters}
                title="Clear all filters"
                id="btn-clear-filters"
              >
                <i className="bi bi-x-circle"></i>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Document Count */}
      <div className="d-flex justify-content-between align-items-center mb-3">
        <span className="text-muted small">
          <i className="bi bi-file-earmark me-1"></i>
          {documents.length} document{documents.length !== 1 ? 's' : ''} found
        </span>
        {loading && (
          <div className="spinner-border spinner-border-sm text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
        )}
      </div>

      {/* Documents Table */}
      {loading && documents.length === 0 ? (
        <div className="card shadow-sm border-0">
          <div className="card-body text-center py-5">
            <div className="spinner-border text-primary mb-3" role="status">
              <span className="visually-hidden">Loading...</span>
            </div>
            <p className="text-muted">Loading lesson plan documents...</p>
          </div>
        </div>
      ) : documents.length === 0 ? (
        <div className="card shadow-sm border-0">
          <div className="card-body text-center py-5">
            <div className="mb-3">
              <i className="bi bi-file-earmark-x display-1 text-muted opacity-25"></i>
            </div>
            <h5 className="fw-bold text-dark mb-2">No Lesson Plans Found</h5>
            <p className="text-muted mb-3">
              {selectedCourseId
                ? 'No lesson plan documents have been uploaded for this course yet.'
                : 'No lesson plan documents match the current filters.'}
            </p>
            {canWrite && (
              <button
                className="btn btn-primary btn-sm px-4"
                onClick={() => setShowUploadModal(true)}
              >
                <i className="bi bi-cloud-upload me-1"></i> Upload First Lesson Plan
              </button>
            )}
          </div>
        </div>
      ) : (
        <div className="card shadow-sm border-0">
          <div className="table-responsive">
            <table className="table table-hover align-middle mb-0">
              <thead className="bg-light">
                <tr>
                  <th className="fw-semibold small text-muted ps-3" style={{ width: '25%' }}>Lesson Plan</th>
                  <th className="fw-semibold small text-muted">Course</th>
                  <th className="fw-semibold small text-muted">Subject</th>
                  <th className="fw-semibold small text-muted text-center">Version</th>
                  <th className="fw-semibold small text-muted">Uploaded By</th>
                  <th className="fw-semibold small text-muted">Date</th>
                  <th className="fw-semibold small text-muted text-center">Size</th>
                  <th className="fw-semibold small text-muted text-center">Status</th>
                  <th className="fw-semibold small text-muted text-end pe-3">Actions</th>
                </tr>
              </thead>
              <tbody>
                {documents.map(doc => (
                  <tr key={doc.id}>
                    {/* Title + filename */}
                    <td className="ps-3">
                      <div className="d-flex align-items-center gap-2">
                        <div className="bg-danger bg-opacity-10 text-danger rounded d-flex align-items-center justify-content-center flex-shrink-0"
                          style={{ width: '36px', height: '36px' }}>
                          <i className="bi bi-file-earmark-pdf-fill fs-5"></i>
                        </div>
                        <div>
                          <div className="fw-semibold small text-dark">{doc.title}</div>
                          <div className="text-muted" style={{ fontSize: '0.7rem' }}>
                            {doc.original_file_name}
                          </div>
                        </div>
                      </div>
                    </td>

                    {/* Course */}
                    <td>
                      <div className="small">{doc.course_name || 'N/A'}</div>
                      {doc.trade_name && (
                        <div className="text-muted" style={{ fontSize: '0.7rem' }}>{doc.trade_name}</div>
                      )}
                    </td>

                    {/* Subject */}
                    <td className="small text-muted">{doc.subject_name || '—'}</td>

                    {/* Version */}
                    <td className="text-center">
                      {doc.version ? (
                        <span className="badge bg-secondary bg-opacity-10 text-secondary small">v{doc.version}</span>
                      ) : '—'}
                    </td>

                    {/* Uploaded By */}
                    <td>
                      <div className="small">{doc.uploader_name || 'N/A'}</div>
                      {doc.uploader_service_number && (
                        <div className="text-muted" style={{ fontSize: '0.7rem' }}>{doc.uploader_service_number}</div>
                      )}
                    </td>

                    {/* Date */}
                    <td className="small text-muted">{formatDate(doc.uploaded_at)}</td>

                    {/* Size */}
                    <td className="text-center small text-muted">{formatFileSize(doc.file_size)}</td>

                    {/* Status */}
                    <td className="text-center">
                      <span className={`badge ${doc.status === 'Active' ? 'bg-success' : 'bg-warning text-dark'} bg-opacity-75`}>
                        {doc.status}
                      </span>
                    </td>

                    {/* Actions */}
                    <td className="text-end pe-3">
                      <div className="btn-group btn-group-sm">
                        <button
                          className="btn btn-outline-primary btn-sm"
                          title="Preview PDF"
                          onClick={() => handlePreview(doc)}
                        >
                          <i className="bi bi-eye-fill"></i>
                        </button>
                        <button
                          className="btn btn-outline-secondary btn-sm"
                          title="Download"
                          onClick={() => handleDownload(doc)}
                        >
                          <i className="bi bi-download"></i>
                        </button>
                        {canWrite && (
                          <>
                            <button
                              className="btn btn-outline-info btn-sm"
                              title="Edit Metadata"
                              onClick={() => handleEdit(doc)}
                            >
                              <i className="bi bi-pencil"></i>
                            </button>
                            <button
                              className="btn btn-outline-warning btn-sm"
                              title="Replace PDF"
                              onClick={() => handleReplace(doc)}
                            >
                              <i className="bi bi-arrow-repeat"></i>
                            </button>
                            {doc.status === 'Active' ? (
                              <button
                                className="btn btn-outline-danger btn-sm"
                                title="Archive"
                                onClick={() => handleArchive(doc)}
                              >
                                <i className="bi bi-archive"></i>
                              </button>
                            ) : (
                              <button
                                className="btn btn-outline-danger btn-sm"
                                title="Delete Permanently"
                                onClick={() => handleDelete(doc)}
                              >
                                <i className="bi bi-trash3"></i>
                              </button>
                            )}
                          </>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Upload Modal */}
      {showUploadModal && (
        <LessonPlanUploadModal
          show={showUploadModal}
          onClose={() => setShowUploadModal(false)}
          onSuccess={() => {
            setShowUploadModal(false)
            fetchDocuments()
          }}
          trades={trades}
        />
      )}

      {/* Preview Modal */}
      {showPreviewModal && selectedDocument && (
        <LessonPlanPreviewModal
          show={showPreviewModal}
          document={selectedDocument}
          onClose={() => {
            setShowPreviewModal(false)
            setSelectedDocument(null)
          }}
        />
      )}

      {/* Edit/Replace Modal */}
      {showEditModal && selectedDocument && (
        <LessonPlanEditModal
          show={showEditModal}
          document={selectedDocument}
          mode={editMode}
          onClose={() => {
            setShowEditModal(false)
            setSelectedDocument(null)
          }}
          onSuccess={() => {
            setShowEditModal(false)
            setSelectedDocument(null)
            fetchDocuments()
          }}
        />
      )}

      {/* Confirmation Modal */}
      {confirmAction && (
        <div className="modal show d-block" tabIndex="-1" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content shadow-lg border-0">
              <div className="modal-header border-0 pb-0">
                <h5 className="modal-title fw-bold">
                  <i className={`bi ${confirmAction.type === 'delete' ? 'bi-exclamation-triangle-fill text-danger' : 'bi-archive-fill text-warning'} me-2`}></i>
                  {confirmAction.title}
                </h5>
                <button type="button" className="btn-close" onClick={() => setConfirmAction(null)}></button>
              </div>
              <div className="modal-body">
                <p className="text-muted">{confirmAction.message}</p>
              </div>
              <div className="modal-footer border-0 pt-0">
                <button className="btn btn-light" onClick={() => setConfirmAction(null)}>Cancel</button>
                <button
                  className={`btn ${confirmAction.type === 'delete' ? 'btn-danger' : 'btn-warning'}`}
                  onClick={executeConfirmAction}
                >
                  <i className={`bi ${confirmAction.type === 'delete' ? 'bi-trash3' : 'bi-archive'} me-1`}></i>
                  {confirmAction.type === 'delete' ? 'Delete Permanently' : 'Archive'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default LessonPlanDocuments
