import React, { useState, useEffect } from 'react'
import axios from 'axios'

export const LessonPlanPreviewModal = ({ show, document: doc, onClose }) => {
  const [isFullscreen, setIsFullscreen] = useState(false)
  const [activeTab, setActiveTab] = useState('pdf') // 'pdf', 'embed', 'google'
  const [blobUrl, setBlobUrl] = useState(null)
  const [loadingPdf, setLoadingPdf] = useState(true)
  const [loadError, setLoadError] = useState(null)

  const rawUrl = doc?.cloudinary_url || doc?.file_url || doc?.file_path || ''
  const docId = doc?.id

  // Asynchronously fetch raw PDF stream via backend proxy endpoint into a local Blob URL
  // This bypasses Cloudinary 401 Unauthorized / CORS restrictions by serving via backend JWT authentication.
  useEffect(() => {
    let isMounted = true
    let createdUrl = null

    if (!show || !docId) {
      setBlobUrl(null)
      setLoadingPdf(false)
      return
    }

    const loadPdfBlob = async () => {
      setLoadingPdf(true)
      setLoadError(null)

      try {
        // Primary: fetch via backend authenticated streaming endpoint
        const res = await axios.get(`/api/v1/academic/lesson-plans/${docId}/file`, {
          responseType: 'blob'
        })

        const pdfBlob = new Blob([res.data], { type: 'application/pdf' })
        createdUrl = URL.createObjectURL(pdfBlob)

        if (isMounted) {
          setBlobUrl(createdUrl)
          setLoadingPdf(false)
        }
      } catch (err) {
        console.warn('Backend PDF stream failed, trying direct URL fetch:', err)
        // Secondary fallback: fetch direct URL if backend proxy endpoint is unavailable
        try {
          if (!rawUrl) throw new Error('No raw URL available')
          const directRes = await fetch(rawUrl)
          if (!directRes.ok) throw new Error(`HTTP ${directRes.status}`)
          const buffer = await directRes.arrayBuffer()
          const fallbackBlob = new Blob([buffer], { type: 'application/pdf' })
          createdUrl = URL.createObjectURL(fallbackBlob)

          if (isMounted) {
            setBlobUrl(createdUrl)
            setLoadingPdf(false)
          }
        } catch (fallbackErr) {
          console.error('All PDF stream methods failed:', fallbackErr)
          if (isMounted) {
            setLoadError('Unable to load document stream.')
            setLoadingPdf(false)
          }
        }
      }
    }

    loadPdfBlob()

    return () => {
      isMounted = false
      if (createdUrl) {
        URL.revokeObjectURL(createdUrl)
      }
    }
  }, [show, docId, rawUrl])

  if (!show || !doc) return null

  const formatFileSize = (bytes) => {
    if (!bytes) return 'N/A'
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`
  }

  const displayPdfUrl = blobUrl || `/api/v1/academic/lesson-plans/${doc.id}/file`
  const downloadUrl = `/api/v1/academic/lesson-plans/${doc.id}/file`

  const googleDocsUrl = rawUrl
    ? `https://docs.google.com/gview?url=${encodeURIComponent(rawUrl)}&embedded=true`
    : ''

  return (
    <div className="modal show d-block" tabIndex="-1" style={{ backgroundColor: 'rgba(0,0,0,0.85)', zIndex: 1060 }}>
      <div className={`modal-dialog modal-dialog-centered ${isFullscreen ? 'modal-fullscreen' : 'modal-xl'}`}
        style={!isFullscreen ? { maxWidth: '94vw' } : {}}>
        <div className="modal-content shadow-lg border-0 bg-dark text-white" style={{ height: isFullscreen ? '100vh' : '92vh' }}>

          {/* Header */}
          <div className="modal-header py-2 px-3 bg-dark text-white border-bottom border-secondary flex-shrink-0">
            <div className="d-flex align-items-center gap-2 overflow-hidden me-2">
              <div className="bg-danger bg-opacity-25 text-danger rounded d-flex align-items-center justify-content-center flex-shrink-0"
                style={{ width: '36px', height: '36px' }}>
                <i className="bi bi-file-earmark-pdf-fill fs-5"></i>
              </div>
              <div className="overflow-hidden">
                <h6 className="modal-title fw-bold mb-0 text-truncate text-light" style={{ fontSize: '0.92rem' }}>
                  {doc.title || doc.original_file_name || 'Lesson Plan PDF'}
                </h6>
                <div className="text-white-50" style={{ fontSize: '0.72rem' }}>
                  {doc.original_file_name} • {formatFileSize(doc.file_size)}
                  {doc.version && ` • v${doc.version}`}
                  {doc.course_name && ` • ${doc.course_name}`}
                </div>
              </div>
            </div>

            {/* View Mode Tabs */}
            <div className="d-none d-md-flex align-items-center bg-secondary bg-opacity-25 rounded p-1 mx-auto gap-1">
              <button
                className={`btn btn-sm py-1 px-3 border-0 small ${activeTab === 'pdf' ? 'btn-danger fw-semibold shadow-sm' : 'text-white-50'}`}
                onClick={() => setActiveTab('pdf')}
                title="Direct PDF Viewer (Native Browser Engine)"
              >
                <i className="bi bi-file-earmark-pdf me-1"></i> Direct PDF
              </button>
              <button
                className={`btn btn-sm py-1 px-3 border-0 small ${activeTab === 'embed' ? 'btn-danger fw-semibold shadow-sm' : 'text-white-50'}`}
                onClick={() => setActiveTab('embed')}
                title="Embedded Plugin Object"
              >
                <i className="bi bi-window-sidebar me-1"></i> Embedded PDF
              </button>
              {rawUrl && (
                <button
                  className={`btn btn-sm py-1 px-3 border-0 small ${activeTab === 'google' ? 'btn-danger fw-semibold shadow-sm' : 'text-white-50'}`}
                  onClick={() => setActiveTab('google')}
                  title="Google Docs Viewer Embed"
                >
                  <i className="bi bi-globe me-1"></i> Google Viewer
                </button>
              )}
            </div>

            {/* Actions */}
            <div className="d-flex align-items-center gap-1 flex-shrink-0 ms-2">
              {/* Download */}
              <a
                href={downloadUrl}
                target="_blank"
                rel="noopener noreferrer"
                download={doc.original_file_name}
                className="btn btn-sm btn-outline-light border-0"
                title="Download PDF File"
              >
                <i className="bi bi-download"></i>
              </a>

              {/* Open in New Tab */}
              <a
                href={downloadUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-sm btn-outline-light border-0"
                title="Open in New Window / Full Browser Tab"
              >
                <i className="bi bi-box-arrow-up-right"></i>
              </a>

              {/* Fullscreen Toggle */}
              <button
                className="btn btn-sm btn-outline-light border-0"
                onClick={() => setIsFullscreen(!isFullscreen)}
                title={isFullscreen ? 'Exit Fullscreen' : 'Fullscreen'}
              >
                <i className={`bi ${isFullscreen ? 'bi-fullscreen-exit' : 'bi-arrows-fullscreen'}`}></i>
              </button>

              {/* Close */}
              <button
                className="btn btn-sm btn-outline-light border-0 ms-1"
                onClick={onClose}
                title="Close Preview"
              >
                <i className="bi bi-x-lg"></i>
              </button>
            </div>
          </div>

          {/* Mobile Tab Switcher */}
          <div className="d-md-none bg-dark border-bottom border-secondary py-1.5 px-2 d-flex justify-content-center gap-1 flex-wrap">
            <button
              className={`btn btn-xs ${activeTab === 'pdf' ? 'btn-danger' : 'btn-outline-light'} py-1 px-2`}
              style={{ fontSize: '0.75rem' }}
              onClick={() => setActiveTab('pdf')}
            >
              Direct PDF
            </button>
            <button
              className={`btn btn-xs ${activeTab === 'embed' ? 'btn-danger' : 'btn-outline-light'} py-1 px-2`}
              style={{ fontSize: '0.75rem' }}
              onClick={() => setActiveTab('embed')}
            >
              Embedded PDF
            </button>
            {rawUrl && (
              <button
                className={`btn btn-xs ${activeTab === 'google' ? 'btn-danger' : 'btn-outline-light'} py-1 px-2`}
                style={{ fontSize: '0.75rem' }}
                onClick={() => setActiveTab('google')}
              >
                Google Viewer
              </button>
            )}
          </div>

          {/* PDF Viewer Body */}
          <div className="modal-body p-0 bg-dark position-relative d-flex align-items-center justify-content-center overflow-hidden" style={{ flex: 1 }}>

            {loadingPdf ? (
              <div className="d-flex flex-column align-items-center justify-content-center h-100 text-light p-4">
                <div className="spinner-border text-danger mb-3" style={{ width: '3rem', height: '3rem' }} role="status"></div>
                <h6 className="fw-semibold mb-1">Loading Lesson Plan PDF Stream...</h6>
                <small className="text-white-50">Streaming document from secure repository</small>
              </div>
            ) : loadError && !blobUrl ? (
              <div className="text-center p-4 text-white-50">
                <i className="bi bi-exclamation-triangle text-warning fs-1 mb-2 d-block"></i>
                <p className="mb-2">Document stream failed: {loadError}</p>
                <a href={downloadUrl} target="_blank" rel="noopener noreferrer" className="btn btn-danger btn-sm">
                  <i className="bi bi-download me-1"></i> Direct Download PDF
                </a>
              </div>
            ) : (
              <>
                {/* TAB 1: Direct Native Browser PDF Iframe */}
                {activeTab === 'pdf' && (
                  <iframe
                    src={`${displayPdfUrl}#toolbar=1&navpanes=1&statusbar=1`}
                    title={`PDF Preview: ${doc.title}`}
                    style={{ width: '100%', height: '100%', border: 'none', backgroundColor: '#323639' }}
                  />
                )}

                {/* TAB 2: Native Embedded PDF Plugin */}
                {activeTab === 'embed' && (
                  <embed
                    src={displayPdfUrl}
                    type="application/pdf"
                    title={`Embedded PDF: ${doc.title}`}
                    style={{ width: '100%', height: '100%', border: 'none', backgroundColor: '#323639' }}
                  />
                )}

                {/* TAB 3: Google Docs Embedded Viewer */}
                {activeTab === 'google' && (
                  <div className="w-100 h-100 position-relative">
                    <iframe
                      src={googleDocsUrl}
                      title={`Google Docs Preview: ${doc.title}`}
                      style={{ width: '100%', height: '100%', border: 'none' }}
                    />
                    <div 
                      className="position-absolute bottom-0 start-50 translate-middle-x mb-3 bg-dark bg-opacity-90 border border-secondary rounded px-3 py-1.5 d-flex align-items-center gap-3 shadow-lg"
                      style={{ zIndex: 10 }}
                    >
                      <span className="text-white-50 small">
                        <i className="bi bi-info-circle me-1 text-warning"></i>
                        If Google Viewer shows "No preview available", switch to Direct PDF:
                      </span>
                      <button className="btn btn-danger btn-xs" onClick={() => setActiveTab('pdf')}>
                        Direct PDF
                      </button>
                    </div>
                  </div>
                )}
              </>
            )}
          </div>

          {/* Footer */}
          <div className="modal-footer py-2 px-3 bg-dark border-top border-secondary text-white-50 flex-shrink-0">
            <div className="w-100 d-flex justify-content-between align-items-center small">
              <div className="d-flex align-items-center gap-2">
                <i className="bi bi-file-earmark-check text-success fs-6"></i>
                <span>Active Viewer: <strong className="text-white">{activeTab === 'pdf' ? 'Direct Browser PDF' : activeTab === 'embed' ? 'Embedded Plugin' : 'Google Docs Embed'}</strong></span>
              </div>
              <div className="d-flex gap-2">
                <a
                  href={downloadUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn btn-outline-light btn-sm"
                >
                  <i className="bi bi-box-arrow-up-right me-1"></i> Open in Tab
                </a>
                <a
                  href={downloadUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  download={doc.original_file_name}
                  className="btn btn-primary btn-sm"
                >
                  <i className="bi bi-download me-1"></i> Download PDF
                </a>
                <button className="btn btn-secondary btn-sm" onClick={onClose}>
                  Close
                </button>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  )
}

export default LessonPlanPreviewModal
