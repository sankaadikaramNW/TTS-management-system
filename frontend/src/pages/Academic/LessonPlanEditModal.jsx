import React, { useState, useRef } from 'react'
import axios from 'axios'
import { toast } from 'react-toastify'

export const LessonPlanEditModal = ({ show, document: doc, mode, onClose, onSuccess }) => {
  const fileInputRef = useRef(null)

  // Metadata form
  const [formData, setFormData] = useState({
    title: doc?.title || '',
    description: doc?.description || '',
    subject_name: doc?.subject_name || '',
    version: doc?.version || '',
    academic_year: doc?.academic_year || '',
    remarks: doc?.remarks || ''
  })

  // Replace file
  const [selectedFile, setSelectedFile] = useState(null)
  const [submitting, setSubmitting] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [errors, setErrors] = useState({})

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }))
    if (errors[field]) setErrors(prev => ({ ...prev, [field]: null }))
  }

  const validatePdfFile = (file) => {
    const ext = file.name.toLowerCase().split('.').pop()
    if (ext !== 'pdf') return 'Only PDF lesson plan documents are allowed.'
    if (file.type && file.type !== 'application/pdf') return 'Only PDF lesson plan documents are allowed.'
    const maxSize = 20 * 1024 * 1024
    if (file.size > maxSize) return 'File size exceeds the maximum allowed size of 20 MB.'
    return null
  }

  const handleFileSelect = (e) => {
    const file = e.target.files?.[0]
    if (!file) return
    const error = validatePdfFile(file)
    if (error) {
      toast.error(error)
      setSelectedFile(null)
      if (fileInputRef.current) fileInputRef.current.value = ''
      return
    }
    setSelectedFile(file)
    if (errors.file) setErrors(prev => ({ ...prev, file: null }))
  }

  const handleSubmitEdit = async () => {
    // Validate
    if (!formData.title.trim()) {
      setErrors({ title: 'Title is required' })
      return
    }

    setSubmitting(true)
    try {
      const updatePayload = {}
      if (formData.title.trim() !== (doc.title || '')) updatePayload.title = formData.title.trim()
      if (formData.description.trim() !== (doc.description || '')) updatePayload.description = formData.description.trim()
      if (formData.subject_name.trim() !== (doc.subject_name || '')) updatePayload.subject_name = formData.subject_name.trim()
      if (formData.version.trim() !== (doc.version || '')) updatePayload.version = formData.version.trim()
      if (formData.academic_year.trim() !== (doc.academic_year || '')) updatePayload.academic_year = formData.academic_year.trim()
      if (formData.remarks.trim() !== (doc.remarks || '')) updatePayload.remarks = formData.remarks.trim()

      if (Object.keys(updatePayload).length === 0) {
        toast.info('No changes detected.')
        onClose()
        return
      }

      await axios.put(`/api/v1/academic/lesson-plans/${doc.id}`, updatePayload)
      toast.success(`Lesson plan "${formData.title}" updated successfully!`)
      onSuccess()
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to update lesson plan metadata.')
    } finally {
      setSubmitting(false)
    }
  }

  const handleSubmitReplace = async () => {
    if (!selectedFile) {
      setErrors({ file: 'Please select a new PDF file' })
      return
    }

    setSubmitting(true)
    setUploadProgress(0)

    try {
      const replaceData = new FormData()
      replaceData.append('file', selectedFile)

      await axios.post(`/api/v1/academic/lesson-plans/${doc.id}/replace`, replaceData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: (progressEvent) => {
          const percent = Math.round((progressEvent.loaded * 100) / progressEvent.total)
          setUploadProgress(percent)
        }
      })

      toast.success(`PDF file for "${doc.title}" replaced successfully!`)
      onSuccess()
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to replace the PDF file.')
    } finally {
      setSubmitting(false)
      setUploadProgress(0)
    }
  }

  const formatFileSize = (bytes) => {
    if (!bytes) return ''
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`
  }

  if (!show || !doc) return null

  return (
    <div className="modal show d-block" tabIndex="-1" style={{ backgroundColor: 'rgba(0,0,0,0.6)', zIndex: 1055 }}>
      <div className="modal-dialog modal-lg modal-dialog-centered">
        <div className="modal-content shadow-lg border-0" style={{ maxHeight: '85vh', display: 'flex', flexDirection: 'column' }}>
          {/* Header */}
          <div className={`modal-header border-0 flex-shrink-0 ${mode === 'replace' ? 'bg-warning bg-opacity-10' : 'bg-info bg-opacity-10'}`}>
            <h5 className={`modal-title fw-bold ${mode === 'replace' ? 'text-warning' : 'text-info'}`}>
              <i className={`bi ${mode === 'replace' ? 'bi-arrow-repeat' : 'bi-pencil-square'} me-2`}></i>
              {mode === 'replace' ? 'Replace Lesson Plan PDF' : 'Edit Lesson Plan Metadata'}
            </h5>
            <button type="button" className="btn-close" onClick={onClose} disabled={submitting}></button>
          </div>

          <div className="modal-body px-4 py-3" style={{ overflowY: 'auto', flex: '1 1 auto' }}>
            {/* Current Document Info */}
            <div className="bg-light rounded-3 p-3 mb-4 border">
              <div className="d-flex align-items-center gap-3">
                <div className="bg-danger bg-opacity-10 text-danger rounded d-flex align-items-center justify-content-center flex-shrink-0"
                  style={{ width: '44px', height: '44px' }}>
                  <i className="bi bi-file-earmark-pdf-fill fs-4"></i>
                </div>
                <div>
                  <div className="fw-semibold text-dark">{doc.title}</div>
                  <div className="text-muted small">
                    {doc.original_file_name} • {formatFileSize(doc.file_size)}
                    {doc.course_name && ` • ${doc.course_name}`}
                  </div>
                </div>
              </div>
            </div>

            {mode === 'edit' ? (
              /* Edit Metadata Form */
              <div className="row g-3">
                <div className="col-12">
                  <label className="form-label small fw-semibold">
                    Title <span className="text-danger">*</span>
                  </label>
                  <input
                    type="text"
                    className={`form-control ${errors.title ? 'is-invalid' : ''}`}
                    value={formData.title}
                    onChange={(e) => handleChange('title', e.target.value)}
                    disabled={submitting}
                    id="edit-title"
                  />
                  {errors.title && <div className="invalid-feedback">{errors.title}</div>}
                </div>

                <div className="col-md-6">
                  <label className="form-label small fw-semibold text-muted">Subject / Lesson</label>
                  <input
                    type="text"
                    className="form-control"
                    value={formData.subject_name}
                    onChange={(e) => handleChange('subject_name', e.target.value)}
                    disabled={submitting}
                    id="edit-subject"
                  />
                </div>

                <div className="col-md-3">
                  <label className="form-label small fw-semibold text-muted">Version</label>
                  <input
                    type="text"
                    className="form-control"
                    value={formData.version}
                    onChange={(e) => handleChange('version', e.target.value)}
                    disabled={submitting}
                    id="edit-version"
                  />
                </div>

                <div className="col-md-3">
                  <label className="form-label small fw-semibold text-muted">Academic Year</label>
                  <input
                    type="text"
                    className="form-control"
                    value={formData.academic_year}
                    onChange={(e) => handleChange('academic_year', e.target.value)}
                    disabled={submitting}
                    id="edit-academic-year"
                  />
                </div>

                <div className="col-12">
                  <label className="form-label small fw-semibold text-muted">Description</label>
                  <textarea
                    className="form-control"
                    rows="2"
                    value={formData.description}
                    onChange={(e) => handleChange('description', e.target.value)}
                    disabled={submitting}
                    id="edit-description"
                  ></textarea>
                </div>

                <div className="col-12">
                  <label className="form-label small fw-semibold text-muted">Remarks</label>
                  <input
                    type="text"
                    className="form-control"
                    value={formData.remarks}
                    onChange={(e) => handleChange('remarks', e.target.value)}
                    disabled={submitting}
                    id="edit-remarks"
                  />
                </div>
              </div>
            ) : (
              /* Replace PDF Form */
              <div>
                <div className="alert alert-warning d-flex align-items-start gap-2 mb-3" role="alert">
                  <i className="bi bi-exclamation-triangle-fill fs-5 mt-1"></i>
                  <div>
                    <strong>Replace Document</strong>
                    <p className="mb-0 small">
                      This will replace the existing PDF file with a new one. The previous file will be permanently removed from cloud storage.
                      The document metadata (title, description, etc.) will remain unchanged.
                    </p>
                  </div>
                </div>

                <label className="form-label small fw-semibold">
                  Select New PDF <span className="text-danger">*</span>
                </label>
                <div
                  className={`border rounded-3 p-4 text-center ${
                    selectedFile ? 'border-success bg-success bg-opacity-10' :
                    errors.file ? 'border-danger' : ''
                  }`}
                  onClick={() => !submitting && fileInputRef.current?.click()}
                  style={{ cursor: submitting ? 'not-allowed' : 'pointer', borderStyle: selectedFile ? 'solid' : 'dashed' }}
                >
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept=".pdf,application/pdf"
                    onChange={handleFileSelect}
                    className="d-none"
                    disabled={submitting}
                    id="replace-file-input"
                  />

                  {selectedFile ? (
                    <div className="d-flex align-items-center justify-content-center gap-3">
                      <div className="bg-danger bg-opacity-10 text-danger rounded p-2">
                        <i className="bi bi-file-earmark-pdf-fill fs-3"></i>
                      </div>
                      <div className="text-start">
                        <div className="fw-semibold small text-dark">{selectedFile.name}</div>
                        <div className="text-muted" style={{ fontSize: '0.75rem' }}>
                          {formatFileSize(selectedFile.size)} • Click to change
                        </div>
                      </div>
                    </div>
                  ) : (
                    <>
                      <i className="bi bi-cloud-arrow-up display-5 text-muted opacity-50"></i>
                      <p className="text-muted mb-1 mt-2 small">
                        Click to select the replacement PDF file
                      </p>
                      <p className="text-muted mb-0" style={{ fontSize: '0.7rem' }}>
                        Only PDF files up to 20 MB are accepted
                      </p>
                    </>
                  )}
                </div>
                {errors.file && <div className="text-danger small mt-1">{errors.file}</div>}

                {/* Upload Progress */}
                {submitting && (
                  <div className="mt-3">
                    <div className="d-flex justify-content-between small text-muted mb-1">
                      <span>Uploading replacement file...</span>
                      <span>{uploadProgress}%</span>
                    </div>
                    <div className="progress" style={{ height: '8px' }}>
                      <div
                        className="progress-bar progress-bar-striped progress-bar-animated bg-warning"
                        style={{ width: `${uploadProgress}%` }}
                      ></div>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="modal-footer border-0 pt-0 px-4 pb-3 flex-shrink-0">
            <button type="button" className="btn btn-light px-4" onClick={onClose} disabled={submitting}>
              Cancel
            </button>
            <button
              className={`btn ${mode === 'replace' ? 'btn-warning' : 'btn-info'} px-4 d-flex align-items-center gap-2`}
              onClick={mode === 'replace' ? handleSubmitReplace : handleSubmitEdit}
              disabled={submitting}
              id="btn-submit-edit"
            >
              {submitting ? (
                <>
                  <span className="spinner-border spinner-border-sm"></span>
                  {mode === 'replace' ? 'Replacing...' : 'Saving...'}
                </>
              ) : (
                <>
                  <i className={`bi ${mode === 'replace' ? 'bi-arrow-repeat' : 'bi-check-lg'}`}></i>
                  {mode === 'replace' ? 'Replace PDF File' : 'Save Changes'}
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default LessonPlanEditModal
