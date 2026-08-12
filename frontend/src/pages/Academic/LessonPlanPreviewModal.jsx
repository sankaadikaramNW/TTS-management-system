import React, { useState } from 'react'

export const LessonPlanPreviewModal = ({ show, document: doc, onClose }) => {
  const [isFullscreen, setIsFullscreen] = useState(false)
  const [activeTab, setActiveTab] = useState('pdf') // 'pdf', 'google', 'image'

  if (!show || !doc) return null

  const formatFileSize = (bytes) => {
    if (!bytes) return 'N/A'
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`
  }

  const formatDate = (dateStr) => {
    if (!dateStr) return 'N/A'
    return new Date(dateStr).toLocaleDateString('en-GB', {
      day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit'
    })
  }

  const pdfUrl = doc.cloudinary_url

  // Google Docs embedded viewer URL
  const googleDocsUrl = pdfUrl ? `https://docs.google.com/gview?url=${encodeURIComponent(pdfUrl)}&embedded=true` : ''

  // Cloudinary converted page image URL (JPEG preview of page 1)
  const cloudinaryPageJpg = pdfUrl ? (
    pdfUrl
      .replace('/image/upload/', '/image/upload/pg_1,w_1200,c_limit,q_auto,f_jpg/')
      .replace('/raw/upload/', '/image/upload/pg_1,w_1200,c_limit,q_auto,f_jpg/')
      .replace(/\.pdf$/i, '') + '.jpg'
  ) : ''

  return (
    <div className="modal show d-block" tabIndex="-1" style={{ backgroundColor: 'rgba(0,0,0,0.8)', zIndex: 1060 }}>
      <div className={`modal-dialog modal-dialog-centered ${isFullscreen ? 'modal-fullscreen' : 'modal-xl'}`}
        style={!isFullscreen ? { maxWidth: '92vw' } : {}}>
        <div className="modal-content shadow-lg border-0" style={{ height: isFullscreen ? '100vh' : '90vh' }}>

          {/* Header */}
          <div className="modal-header py-2 px-3 bg-dark text-white border-0 flex-shrink-0">
            <div className="d-flex align-items-center gap-2 overflow-hidden me-2">
              <div className="bg-danger bg-opacity-25 text-danger rounded d-flex align-items-center justify-content-center flex-shrink-0"
                style={{ width: '34px', height: '34px' }}>
                <i className="bi bi-file-earmark-pdf-fill fs-5"></i>
              </div>
              <div className="overflow-hidden">
                <h6 className="modal-title fw-bold mb-0 text-truncate text-light" style={{ fontSize: '0.9rem' }}>
                  {doc.title}
                </h6>
                <div className="text-white-50" style={{ fontSize: '0.7rem' }}>
                  {doc.original_file_name} • {formatFileSize(doc.file_size)}
                  {doc.version && ` • v${doc.version}`}
                </div>
              </div>
            </div>

            {/* View Mode Tabs */}
            <div className="d-none d-sm-flex align-items-center bg-secondary bg-opacity-25 rounded p-1 mx-auto">
              <button
                className={`btn btn-sm py-1 px-3 border-0 small ${activeTab === 'pdf' ? 'btn-danger fw-semibold' : 'text-white-50'}`}
                onClick={() => setActiveTab('pdf')}
                title="Direct PDF Viewer"
              >
                <i className="bi bi-file-pdf me-1"></i> PDF
              </button>
              <button
                className={`btn btn-sm py-1 px-3 border-0 small ${activeTab === 'image' ? 'btn-danger fw-semibold' : 'text-white-50'}`}
                onClick={() => setActiveTab('image')}
                title="Rendered Page Image"
              >
                <i className="bi bi-file-image me-1"></i> Image Page
              </button>
              <button
                className={`btn btn-sm py-1 px-3 border-0 small ${activeTab === 'google' ? 'btn-danger fw-semibold' : 'text-white-50'}`}
                onClick={() => setActiveTab('google')}
                title="Google Docs Viewer Embed"
              >
                <i className="bi bi-globe me-1"></i> Google Viewer
              </button>
            </div>

            {/* Actions */}
            <div className="d-flex align-items-center gap-1 flex-shrink-0 ms-2">
              {/* Metadata Info */}
              <div className="d-none d-lg-flex align-items-center gap-3 me-3">
                {doc.course_name && (
                  <span className="badge bg-primary bg-opacity-75" style={{ fontSize: '0.65rem' }}>
                    <i className="bi bi-book-half me-1"></i>{doc.course_name}
                  </span>
                )}
                {doc.uploader_name && (
                  <span className="text-white-50" style={{ fontSize: '0.7rem' }}>
                    <i className="bi bi-person me-1"></i>{doc.uploader_name}
                  </span>
                )}
              </div>

              {/* Download */}
              <a
                href={pdfUrl}
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
                href={pdfUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-sm btn-outline-light border-0"
                title="Open in New Window"
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
          <div className="d-sm-none bg-dark border-top border-secondary py-1 px-2 d-flex justify-content-center gap-1">
            <button
              className={`btn btn-xs ${activeTab === 'pdf' ? 'btn-danger' : 'btn-outline-light'} py-0 px-2`}
              style={{ fontSize: '0.75rem' }}
              onClick={() => setActiveTab('pdf')}
            >
              PDF Viewer
            </button>
            <button
              className={`btn btn-xs ${activeTab === 'image' ? 'btn-danger' : 'btn-outline-light'} py-0 px-2`}
              style={{ fontSize: '0.75rem' }}
              onClick={() => setActiveTab('image')}
            >
              Image Page
            </button>
            <button
              className={`btn btn-xs ${activeTab === 'google' ? 'btn-danger' : 'btn-outline-light'} py-0 px-2`}
              style={{ fontSize: '0.75rem' }}
              onClick={() => setActiveTab('google')}
            >
              Google Viewer
            </button>
          </div>

          {/* PDF Viewer Body */}
          <div className="modal-body p-0 bg-dark position-relative d-flex align-items-center justify-content-center" style={{ overflow: 'auto', flex: 1 }}>

            {/* TAB 1: Direct PDF Object/Iframe */}
            {activeTab === 'pdf' && (
              <object
                data={pdfUrl}
                type="application/pdf"
                style={{ width: '100%', height: '100%', border: 'none', minHeight: '400px' }}
              >
                <iframe
                  src={pdfUrl}
                  title={`Preview: ${doc.title}`}
                  style={{ width: '100%', height: '100%', border: 'none' }}
                />
              </object>
            )}

            {/* TAB 2: Rendered Page Image (Cloudinary JPEG) */}
            {activeTab === 'image' && (
              <div className="w-100 h-100 p-3 d-flex flex-column align-items-center overflow-auto">
                <img
                  src={cloudinaryPageJpg}
                  alt={`Lesson Plan: ${doc.title}`}
                  className="img-fluid rounded shadow-lg border"
                  style={{ maxWidth: '100%', maxHeight: '100%', objectFit: 'contain' }}
                  onError={(e) => {
                    // Fallback to pdf tab if image fails
                    setActiveTab('google')
                  }}
                />
              </div>
            )}

            {/* TAB 3: Google Docs Embedded Viewer */}
            {activeTab === 'google' && (
              <iframe
                src={googleDocsUrl}
                title={`Google Docs Preview: ${doc.title}`}
                style={{ width: '100%', height: '100%', border: 'none' }}
              />
            )}
          </div>

          {/* Footer */}
          <div className="modal-footer py-2 px-3 bg-dark border-top border-secondary text-white-50 flex-shrink-0">
            <div className="w-100 d-flex justify-content-between align-items-center small">
              <div>
                <span className="me-3"><i className="bi bi-info-circle me-1"></i>If PDF does not display directly, switch to <strong>Image Page</strong> or <strong>Google Viewer</strong> tab.</span>
              </div>
              <div className="d-flex gap-2">
                <a
                  href={pdfUrl}
                  target="_blank"
                  rel="noopener noreferrer"
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
