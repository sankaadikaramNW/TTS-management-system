import React, { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import { toast } from 'react-toastify'

export const LessonPlanUploadModal = ({ show, onClose, onSuccess, trades }) => {
  const fileInputRef = useRef(null)

  // Form state
  const [selectedTradeId, setSelectedTradeId] = useState('')
  const [courses, setCourses] = useState([])
  const [loadingCourses, setLoadingCourses] = useState(false)

  const [formData, setFormData] = useState({
    course_id: '',
    title: '',
    subject_name: '',
    version: '',
    description: '',
    academic_year: '',
    remarks: ''
  })

  const [selectedFile, setSelectedFile] = useState(null)
  const [dragActive, setDragActive] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [errors, setErrors] = useState({})

  // Load courses based on selected trade
  useEffect(() => {
    if (!selectedTradeId) {
      setCourses([])
      setFormData(prev => ({ ...prev, course_id: '' }))
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
    setFormData(prev => ({ ...prev, course_id: '' }))
  }, [selectedTradeId])

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }))
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: null }))
    }
  }

  const validatePdfFile = (file) => {
    // Extension check
    const ext = file.name.toLowerCase().split('.').pop()
    if (ext !== 'pdf') {
      return 'Only PDF lesson plan documents are allowed.'
    }
    // MIME type check
    if (file.type && file.type !== 'application/pdf') {
      return 'Only PDF lesson plan documents are allowed.'
    }
    // Size check (20 MB default)
    const maxSize = 20 * 1024 * 1024
    if (file.size > maxSize) {
      return 'File size exceeds the maximum allowed size of 20 MB.'
    }
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

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    const file = e.dataTransfer.files?.[0]
    if (!file) return
    const error = validatePdfFile(file)
    if (error) {
      toast.error(error)
      return
    }
    setSelectedFile(file)
    if (errors.file) setErrors(prev => ({ ...prev, file: null }))
  }

  const validate = () => {
    const newErrors = {}
    if (!selectedTradeId) newErrors.trade = 'Trade is required'
    if (!formData.course_id) newErrors.course_id = 'Course is required'
    if (!formData.title.trim()) newErrors.title = 'Lesson plan title is required'
    if (!selectedFile) newErrors.file = 'A PDF document is required'
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!validate()) return

    setUploading(true)
    setUploadProgress(0)

    try {
      const uploadData = new FormData()
      uploadData.append('file', selectedFile)
      uploadData.append('course_id', formData.course_id)
      uploadData.append('title', formData.title.trim())
      if (formData.subject_name.trim()) uploadData.append('subject_name', formData.subject_name.trim())
      if (formData.version.trim()) uploadData.append('version', formData.version.trim())
      if (formData.description.trim()) uploadData.append('description', formData.description.trim())
      if (formData.academic_year.trim()) uploadData.append('academic_year', formData.academic_year.trim())
      if (formData.remarks.trim()) uploadData.append('remarks', formData.remarks.trim())

      await axios.post('/api/v1/academic/lesson-plans', uploadData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: (progressEvent) => {
          const percent = Math.round((progressEvent.loaded * 100) / progressEvent.total)
          setUploadProgress(percent)
        }
      })

      toast.success(`Lesson plan "${formData.title}" uploaded successfully!`)
      onSuccess()
    } catch (err) {
      const detail = err.response?.data?.detail || 'Failed to upload lesson plan.'
      toast.error(detail)
    } finally {
      setUploading(false)
      setUploadProgress(0)
    }
  }

  const formatFileSize = (bytes) => {
    if (!bytes) return ''
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`
  }

  if (!show) return null

  return (
    <div className="modal show d-block" tabIndex="-1" style={{ backgroundColor: 'rgba(0,0,0,0.6)', zIndex: 1055 }}>
      <div className="modal-dialog modal-lg modal-dialog-centered">
        <form onSubmit={handleSubmit} className="modal-content shadow-lg border-0" style={{ maxHeight: '85vh', display: 'flex', flexDirection: 'column' }}>
          {/* Header */}
          <div className="modal-header bg-primary bg-opacity-10 border-0 flex-shrink-0">
            <h5 className="modal-title fw-bold text-primary">
              <i className="bi bi-cloud-upload-fill me-2"></i>
              Upload Lesson Plan Document
            </h5>
            <button type="button" className="btn-close" onClick={onClose} disabled={uploading}></button>
          </div>

          {/* Scrollable Body */}
          <div className="modal-body px-4 py-3" style={{ overflowY: 'auto', flex: '1 1 auto' }}>
            <div className="row g-3">
              {/* Trade Selection */}
              <div className="col-md-6">
                <label className="form-label small fw-semibold">
                  Trade <span className="text-danger">*</span>
                </label>
                <select
                  className={`form-select ${errors.trade ? 'is-invalid' : ''}`}
                  value={selectedTradeId}
                  onChange={(e) => setSelectedTradeId(e.target.value)}
                  disabled={uploading}
                  id="upload-trade"
                >
                  <option value="">Select Trade...</option>
                  {trades.map(t => (
                    <option key={t.id} value={t.id}>{t.label}</option>
                  ))}
                </select>
                {errors.trade && <div className="invalid-feedback">{errors.trade}</div>}
              </div>

              {/* Course Selection */}
              <div className="col-md-6">
                <label className="form-label small fw-semibold">
                  Course <span className="text-danger">*</span>
                </label>
                <select
                  className={`form-select ${errors.course_id ? 'is-invalid' : ''}`}
                  value={formData.course_id}
                  onChange={(e) => handleChange('course_id', e.target.value)}
                  disabled={!selectedTradeId || loadingCourses || uploading}
                  id="upload-course"
                >
                  <option value="">
                    {!selectedTradeId 
                      ? 'Select a Trade first' 
                      : loadingCourses 
                      ? 'Loading courses...' 
                      : courses.length === 0 
                      ? 'No courses available for this Trade' 
                      : 'Select Course...'}
                  </option>
                  {courses.map(c => (
                    <option key={c.id} value={c.id}>{c.name}</option>
                  ))}
                </select>
                {errors.course_id && <div className="invalid-feedback">{errors.course_id}</div>}
              </div>

              {/* Title */}
              <div className="col-12">
                <label className="form-label small fw-semibold">
                  Lesson Plan Title <span className="text-danger">*</span>
                </label>
                <input
                  type="text"
                  className={`form-control ${errors.title ? 'is-invalid' : ''}`}
                  placeholder="e.g. Computer Hardware Lesson Plan"
                  value={formData.title}
                  onChange={(e) => handleChange('title', e.target.value)}
                  disabled={uploading}
                  id="upload-title"
                />
                {errors.title && <div className="invalid-feedback">{errors.title}</div>}
              </div>

              {/* PDF File Upload Zone (Prominent Required Section) */}
              <div className="col-12">
                <label className="form-label small fw-semibold">
                  PDF Document <span className="text-danger">*</span>
                </label>
                <div
                  className={`border rounded-3 p-3 text-center cursor-pointer transition-all ${
                    dragActive ? 'border-primary bg-primary bg-opacity-10' :
                    errors.file ? 'border-danger bg-danger bg-opacity-10' :
                    selectedFile ? 'border-success bg-success bg-opacity-10' :
                    'border-primary bg-light'
                  }`}
                  onDragEnter={handleDrag}
                  onDragLeave={handleDrag}
                  onDragOver={handleDrag}
                  onDrop={handleDrop}
                  onClick={() => !uploading && fileInputRef.current?.click()}
                  style={{ cursor: uploading ? 'not-allowed' : 'pointer', borderStyle: selectedFile ? 'solid' : 'dashed', borderWidth: '2px' }}
                >
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept=".pdf,application/pdf"
                    onChange={handleFileSelect}
                    className="d-none"
                    disabled={uploading}
                    id="upload-file-input"
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
                      <button
                        type="button"
                        className="btn btn-sm btn-outline-danger ms-2"
                        onClick={(e) => {
                          e.stopPropagation()
                          setSelectedFile(null)
                          if (fileInputRef.current) fileInputRef.current.value = ''
                        }}
                        disabled={uploading}
                      >
                        <i className="bi bi-x-lg"></i>
                      </button>
                    </div>
                  ) : (
                    <>
                      <i className="bi bi-file-earmark-pdf-fill display-6 text-danger me-2"></i>
                      <span className="fw-semibold small text-dark">Select or drop PDF document here</span>
                      <p className="text-muted mb-0 mt-1" style={{ fontSize: '0.75rem' }}>
                        Only PDF format is accepted (Max size: 20 MB)
                      </p>
                    </>
                  )}
                </div>
                {errors.file && <div className="text-danger small mt-1">{errors.file}</div>}
              </div>

              {/* Subject / Lesson */}
              <div className="col-md-6">
                <label className="form-label small fw-semibold text-muted">Subject / Lesson</label>
                <input
                  type="text"
                  className="form-control"
                  placeholder="e.g. Computer Hardware"
                  value={formData.subject_name}
                  onChange={(e) => handleChange('subject_name', e.target.value)}
                  disabled={uploading}
                  id="upload-subject"
                />
              </div>

              {/* Version */}
              <div className="col-md-3">
                <label className="form-label small fw-semibold text-muted">Version</label>
                <input
                  type="text"
                  className="form-control"
                  placeholder="e.g. 1.0"
                  value={formData.version}
                  onChange={(e) => handleChange('version', e.target.value)}
                  disabled={uploading}
                  id="upload-version"
                />
              </div>

              {/* Academic Year */}
              <div className="col-md-3">
                <label className="form-label small fw-semibold text-muted">Academic Year</label>
                <input
                  type="text"
                  className="form-control"
                  placeholder="e.g. 2026"
                  value={formData.academic_year}
                  onChange={(e) => handleChange('academic_year', e.target.value)}
                  disabled={uploading}
                  id="upload-academic-year"
                />
              </div>

              {/* Description */}
              <div className="col-12">
                <label className="form-label small fw-semibold text-muted">Description</label>
                <textarea
                  className="form-control"
                  rows="2"
                  placeholder="Brief description of the lesson plan..."
                  value={formData.description}
                  onChange={(e) => handleChange('description', e.target.value)}
                  disabled={uploading}
                  id="upload-description"
                ></textarea>
              </div>

              {/* Remarks */}
              <div className="col-12">
                <label className="form-label small fw-semibold text-muted">Remarks</label>
                <input
                  type="text"
                  className="form-control"
                  placeholder="Any additional notes..."
                  value={formData.remarks}
                  onChange={(e) => handleChange('remarks', e.target.value)}
                  disabled={uploading}
                  id="upload-remarks"
                />
              </div>
            </div>

            {/* Upload Progress */}
            {uploading && (
              <div className="mt-3">
                <div className="d-flex justify-content-between small text-muted mb-1">
                  <span>Uploading to cloud storage...</span>
                  <span>{uploadProgress}%</span>
                </div>
                <div className="progress" style={{ height: '8px' }}>
                  <div
                    className="progress-bar progress-bar-striped progress-bar-animated bg-primary"
                    style={{ width: `${uploadProgress}%` }}
                  ></div>
                </div>
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="modal-footer border-0 pt-2 px-4 pb-3 flex-shrink-0">
            <button type="button" className="btn btn-light px-4" onClick={onClose} disabled={uploading}>
              Cancel
            </button>
            <button
              type="submit"
              className="btn btn-primary px-4 d-flex align-items-center gap-2"
              disabled={uploading}
              id="btn-submit-upload"
            >
              {uploading ? (
                <>
                  <span className="spinner-border spinner-border-sm"></span>
                  Uploading...
                </>
              ) : (
                <>
                  <i className="bi bi-cloud-upload-fill"></i>
                  Upload Lesson Plan
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default LessonPlanUploadModal
