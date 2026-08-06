import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { toast } from 'react-toastify'

export const AcademicReports = ({ initialReportType = 'trade' }) => {
  const [reportType, setReportType] = useState(initialReportType)
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(false)

  const fetchReportData = async (type) => {
    setLoading(true)
    try {
      const res = await axios.get(`/api/v1/academic/reports/${type}`)
      setData(res.data)
    } catch (err) {
      toast.error('Failed to generate report data')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchReportData(reportType)
  }, [reportType])

  useEffect(() => {
    setReportType(initialReportType)
  }, [initialReportType])

  const handlePrint = () => {
    window.print()
  }

  const handleExportCSV = () => {
    if (data.length === 0) return
    const headers = Object.keys(data[0]).join(',')
    const rows = data.map(obj => Object.values(obj).map(val => `"${val}"`).join(','))
    const csvContent = "data:text/csv;charset=utf-8," + [headers, ...rows].join("\n")
    const encodedUri = encodeURI(csvContent)
    const link = document.createElement("a")
    link.setAttribute("href", encodedUri)
    link.setAttribute("download", `SLAF_Academic_${reportType}_Report.csv`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  return (
    <div className="fade-in-slide">
      <div className="d-flex justify-content-between align-items-center mb-3">
        <div>
          <h5 className="fw-bold text-dark mb-0 display-font">Academic Enterprise Reporting Suite</h5>
          <small className="text-muted">Generate & Export Official SLAF TTS Academic, Classroom & Instructor Audit Reports</small>
        </div>
        <div className="d-flex gap-2">
          <button className="btn btn-outline-secondary btn-sm fw-semibold" onClick={handleExportCSV}>
            <i className="bi bi-file-earmark-excel me-1 text-success"></i> Export CSV/Excel
          </button>
          <button className="btn btn-primary btn-sm fw-semibold" onClick={handlePrint}>
            <i className="bi bi-printer me-1"></i> Print Official Report
          </button>
        </div>
      </div>

      {/* Report Selector Tabs */}
      <ul className="nav nav-pills custom-pills mb-3 border-bottom pb-2">
        <li className="nav-item">
          <button className={`nav-link btn-sm ${reportType === 'trade' ? 'active fw-bold' : ''}`} onClick={() => setReportType('trade')}>
            <i className="bi bi-wrench me-1"></i> Trade Summary Report
          </button>
        </li>
        <li className="nav-item">
          <button className={`nav-link btn-sm ${reportType === 'course' ? 'active fw-bold' : ''}`} onClick={() => setReportType('course')}>
            <i className="bi bi-journal-bookmark me-1"></i> Course Curriculum Report
          </button>
        </li>
        <li className="nav-item">
          <button className={`nav-link btn-sm ${reportType === 'batch' ? 'active fw-bold' : ''}`} onClick={() => setReportType('batch')}>
            <i className="bi bi-layers me-1"></i> Batch Training Report
          </button>
        </li>
        <li className="nav-item">
          <button className={`nav-link btn-sm ${reportType === 'classroom' ? 'active fw-bold' : ''}`} onClick={() => setReportType('classroom')}>
            <i className="bi bi-door-open me-1"></i> Classroom Utilization Report
          </button>
        </li>
        <li className="nav-item">
          <button className={`nav-link btn-sm ${reportType === 'instructor' ? 'active fw-bold' : ''}`} onClick={() => setReportType('instructor')}>
            <i className="bi bi-person-badge me-1"></i> Instructor Assignment Report
          </button>
        </li>
      </ul>

      {/* Report Data Table */}
      <div className="card slaf-card p-0 shadow-sm print-area">
        <div className="p-3 border-bottom bg-light d-flex justify-content-between align-items-center">
          <div>
            <strong className="text-dark display-font text-uppercase">
              SLAF TTS - {reportType.toUpperCase()} OFFICIAL ACADEMIC REPORT
            </strong>
            <div className="text-muted small">Generated on {new Date().toLocaleDateString()} • System SSOT Record</div>
          </div>
          <span className="badge bg-primary text-white">CONFIDENTIAL</span>
        </div>

        <div className="table-responsive">
          <table className="table slaf-table align-middle mb-0">
            <thead>
              {data.length > 0 && (
                <tr>
                  {Object.keys(data[0]).map((col, i) => (
                    <th key={i} className="text-capitalize">{col.replace(/_/g, ' ')}</th>
                  ))}
                </tr>
              )}
            </thead>
            <tbody>
              {loading ? (
                <tr><td colSpan="10" className="text-center py-5"><div className="spinner-border text-primary"></div></td></tr>
              ) : data.length === 0 ? (
                <tr><td colSpan="10" className="text-center py-5 text-muted">No report data generated.</td></tr>
              ) : (
                data.map((row, idx) => (
                  <tr key={idx}>
                    {Object.values(row).map((val, valIdx) => (
                      <td key={valIdx} className="small">{val !== null && val !== undefined ? String(val) : 'N/A'}</td>
                    ))}
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
