import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { toast } from 'react-toastify'
import { useAuth } from '../../context/AuthContext'

export const AcademicReports = ({ initialReportType = 'trade' }) => {
  const { user } = useAuth()
  const [reportType, setReportType] = useState(initialReportType)
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(false)
  const [orientation, setOrientation] = useState('landscape')
  const [exportingExcel, setExportingExcel] = useState(false)
  const [exportingPdf, setExportingPdf] = useState(false)
  const [filterSearch, setFilterSearch] = useState('')

  const fetchReportData = async (type) => {
    setLoading(true)
    setFilterSearch('')
    try {
      const res = await axios.get(`/api/v1/academic/reports/${type}`)
      setData(res.data)
    } catch (err) {
      toast.error('Failed to compile academic report data')
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

  const columns = data.length > 0 
    ? Object.keys(data[0]).map(k => ({
        field: k,
        label: k.replace(/_/g, ' ').toUpperCase(),
        align: ['id', 's_no', 'code', 'intake', 'batch'].includes(k.toLowerCase()) ? 'center' : 'left'
      }))
    : []

  const filteredRows = filterSearch.trim()
    ? data.filter(r => Object.values(r).some(v => v !== null && v !== undefined && String(v).toLowerCase().includes(filterSearch.toLowerCase())))
    : data

  const handleExportExcel = async () => {
    if (data.length === 0) return
    setExportingExcel(true)
    try {
      const payload = {
        report_type: `academic_${reportType}`,
        title: `OFFICIAL ACADEMIC ${reportType.toUpperCase()} REPORT`,
        header_info: {
          organization: 'SRI LANKA AIR FORCE',
          school_name: 'TRADE TRAINING SCHOOL (TTS EKALA)',
          generated_at: new Date().toISOString().replace('T', ' ').substring(0, 19),
          generated_by: user ? `${user.full_name} (${user.username})` : 'Authorized Officer',
          parameters: { Report_Category: reportType.toUpperCase() }
        },
        columns: columns,
        rows: data
      }
      const res = await axios.post('/api/v1/reports/export/excel', payload, { responseType: 'blob' })
      const blob = new Blob([res.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `SLAF_Academic_${reportType.toUpperCase()}_Report.xlsx`)
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
      toast.success('Official Excel spreadsheet downloaded')
    } catch (err) {
      toast.error('Failed to export Excel')
    } finally {
      setExportingExcel(false)
    }
  }

  const handleExportPdf = async () => {
    if (data.length === 0) return
    setExportingPdf(true)
    try {
      const payload = {
        report_type: `academic_${reportType}`,
        title: `OFFICIAL ACADEMIC ${reportType.toUpperCase()} REPORT`,
        header_info: {
          organization: 'SRI LANKA AIR FORCE',
          school_name: 'TRADE TRAINING SCHOOL (TTS EKALA)',
          generated_at: new Date().toISOString().replace('T', ' ').substring(0, 19),
          generated_by: user ? `${user.full_name} (${user.username})` : 'Authorized Officer',
          parameters: { Report_Category: reportType.toUpperCase() }
        },
        columns: columns,
        rows: data
      }
      const res = await axios.post('/api/v1/reports/export/pdf', payload, { responseType: 'blob' })
      const blob = new Blob([res.data], { type: 'application/pdf' })
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `SLAF_Academic_${reportType.toUpperCase()}_Report.pdf`)
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
      toast.success('Classical PDF document downloaded')
    } catch (err) {
      toast.error('Failed to export PDF')
    } finally {
      setExportingPdf(false)
    }
  }

  return (
    <div className="fade-in-slide">
      {/* Top Application Toolbar */}
      <div className="d-flex justify-content-between align-items-center mb-3 no-print">
        <div>
          <h5 className="fw-bold text-dark mb-0 display-font">
            <i className="bi bi-file-earmark-ruled-fill text-primary me-2"></i>Academic Enterprise Reporting Suite
          </h5>
          <small className="text-muted">Formal, Database-Compiled Official SLAF Academic & Curriculum Registers</small>
        </div>
        <div className="d-flex align-items-center gap-2">
          {/* Orientation Switcher */}
          <div className="btn-group btn-group-sm me-2 shadow-xs" role="group">
            <button
              type="button"
              className={`btn ${orientation === 'portrait' ? 'btn-secondary fw-bold' : 'btn-outline-secondary'}`}
              onClick={() => setOrientation('portrait')}
            >
              <i className="bi bi-file-earmark me-1"></i> A4 Portrait
            </button>
            <button
              type="button"
              className={`btn ${orientation === 'landscape' ? 'btn-secondary fw-bold' : 'btn-outline-secondary'}`}
              onClick={() => setOrientation('landscape')}
            >
              <i className="bi bi-file-earmark-landscape me-1"></i> A4 Landscape
            </button>
          </div>

          <button 
            className="btn btn-outline-dark btn-sm fw-semibold shadow-xs" 
            onClick={handleExportExcel}
            disabled={loading || exportingExcel || !data.length}
          >
            {exportingExcel ? <span className="spinner-border spinner-border-sm me-1"></span> : <i className="bi bi-file-earmark-excel me-1 text-success"></i>}
            Export Excel (.xlsx)
          </button>
          <button 
            className="btn btn-outline-dark btn-sm fw-semibold shadow-xs" 
            onClick={handleExportPdf}
            disabled={loading || exportingPdf || !data.length}
          >
            {exportingPdf ? <span className="spinner-border spinner-border-sm me-1"></span> : <i className="bi bi-file-earmark-pdf me-1 text-danger"></i>}
            Download PDF
          </button>
          <button 
            className="btn btn-primary btn-sm fw-semibold shadow-xs" 
            onClick={handlePrint}
            disabled={loading || !data.length}
          >
            <i className="bi bi-printer me-1"></i> Print Formal Report
          </button>
        </div>
      </div>

      {/* Report Selector Tabs */}
      <div className="card slaf-card p-2 mb-3 shadow-xs bg-white no-print">
        <ul className="nav nav-pills custom-pills flex-nowrap overflow-auto">
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
      </div>

      {/* Filter and Record counter */}
      <div className="d-flex justify-content-between align-items-center mb-2 px-1 no-print">
        <div className="small text-muted">
          Showing <strong>{filteredRows.length}</strong> of <strong>{data.length}</strong> compiled database records
        </div>
        <div style={{ width: '280px' }}>
          <input
            type="text"
            className="form-control form-control-sm"
            placeholder="Search within compiled records..."
            value={filterSearch}
            onChange={(e) => setFilterSearch(e.target.value)}
          />
        </div>
      </div>

      {/* Classical Formal Paper Document */}
      <div className={`report-paper-classical ${orientation === 'landscape' ? 'orientation-landscape' : 'orientation-portrait'} p-4 p-md-5 bg-white`}>
        {loading ? (
          <div className="text-center py-5">
            <div className="spinner-border text-dark" role="status"></div>
            <p className="mt-2 text-muted small">Executing SQL query and compiling official academic report...</p>
          </div>
        ) : (
          <>
            {/* Header */}
            <div className="text-center mb-2">
              <div className="d-flex justify-content-between align-items-center mb-1 text-muted" style={{ fontSize: '0.75rem' }}>
                <span>SRI LANKA AIR FORCE • TRADE TRAINING SCHOOL</span>
                <span className="fw-bold text-dark">RESTRICTED / OFFICIAL USE ONLY</span>
              </div>
              <div className="report-double-rule-top"></div>
              <h4 className="fw-bold mb-0 text-uppercase" style={{ letterSpacing: '0.8px', fontSize: '1.25rem' }}>
                SRI LANKA AIR FORCE
              </h4>
              <h5 className="fw-bold mb-1" style={{ fontSize: '1.05rem', color: '#1f2937' }}>
                TRADE TRAINING SCHOOL (TTS EKALA)
              </h5>
              <div className="fs-6 fw-bold text-uppercase mt-2" style={{ letterSpacing: '0.4px', textDecoration: 'underline' }}>
                OFFICIAL ACADEMIC {reportType.toUpperCase()} REPORT
              </div>
              <div className="text-muted small mt-0.5" style={{ fontSize: '0.825rem' }}>
                System-Compiled Academic & Training Record Register
              </div>
              <div className="report-double-rule-bottom"></div>
            </div>

            {/* Section 1: Report Information */}
            <div className="report-section-header">1. REPORT INFORMATION & PARAMETERS</div>
            <table className="report-formal-table mb-3">
              <tbody>
                <tr>
                  <td style={{ width: '18%', fontWeight: 'bold', backgroundColor: '#f8fafc' }}>Organization:</td>
                  <td style={{ width: '32%' }}>Sri Lanka Air Force (TTS Ekala)</td>
                  <td style={{ width: '20%', fontWeight: 'bold', backgroundColor: '#f8fafc' }}>Generated Date/Time:</td>
                  <td style={{ width: '30%' }}>{new Date().toLocaleString()}</td>
                </tr>
                <tr>
                  <td style={{ fontWeight: 'bold', backgroundColor: '#f8fafc' }}>Security Classification:</td>
                  <td>RESTRICTED / OFFICIAL USE ONLY</td>
                  <td style={{ fontWeight: 'bold', backgroundColor: '#f8fafc' }}>Authorized Officer:</td>
                  <td>{user ? `${user.full_name} (${user.username})` : 'Authorized Officer'}</td>
                </tr>
                <tr>
                  <td style={{ fontWeight: 'bold', backgroundColor: '#f8fafc' }}>Report Category:</td>
                  <td>ACADEMIC {reportType.toUpperCase()} REGISTER</td>
                  <td style={{ fontWeight: 'bold', backgroundColor: '#f8fafc' }}>Total Records Compiled:</td>
                  <td><strong>{data.length} Records</strong></td>
                </tr>
              </tbody>
            </table>

            {/* Section 2: Detailed Records */}
            <div className="report-section-header">2. DETAILED SYSTEM RECORDS</div>
            <div className="table-responsive">
              <table className="report-formal-table mb-2">
                <thead>
                  {columns.length > 0 && (
                    <tr>
                      <th style={{ width: '45px' }}>S/NO</th>
                      {columns.map((col, i) => (
                        <th key={i} style={{ textAlign: col.align }}>{col.label}</th>
                      ))}
                    </tr>
                  )}
                </thead>
                <tbody>
                  {filteredRows.length === 0 ? (
                    <tr>
                      <td colSpan={columns.length + 1} className="text-center py-4 text-muted">
                        No records found for this academic report.
                      </td>
                    </tr>
                  ) : (
                    filteredRows.map((row, rIdx) => (
                      <tr key={rIdx}>
                        <td style={{ textAlign: 'center', fontWeight: 'bold' }}>{rIdx + 1}</td>
                        {columns.map((col, cIdx) => (
                          <td key={cIdx} style={{ textAlign: col.align }}>
                            {row[col.field] !== null && row[col.field] !== undefined ? String(row[col.field]) : '—'}
                          </td>
                        ))}
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>

            {/* Section 3: Signatures */}
            <div className="report-signature-block">
              <div className="report-section-header">OFFICIAL AUTHENTICATION & CERTIFICATION</div>
              <div className="d-flex justify-content-between text-center mt-3">
                <div className="report-sig-col text-start">
                  <div className="fw-bold">PREPARED BY:</div>
                  <div className="report-sig-line"></div>
                  <div className="small">Name: ....................................................</div>
                  <div className="small">Service No: ............................................</div>
                  <div className="small">Designation: Academic Branch Officer</div>
                  <div className="small">Date: .....................................................</div>
                </div>

                <div className="report-sig-col text-start">
                  <div className="fw-bold">CHECKED & VERIFIED BY:</div>
                  <div className="report-sig-line"></div>
                  <div className="small">Name: ....................................................</div>
                  <div className="small">Service No: ............................................</div>
                  <div className="small">Designation: Chief Ground Instructor</div>
                  <div className="small">Date: .....................................................</div>
                </div>

                <div className="report-sig-col text-start">
                  <div className="fw-bold">APPROVED & AUTHENTICATED BY:</div>
                  <div className="report-sig-line"></div>
                  <div className="small">Name: ....................................................</div>
                  <div className="small">Service No: ............................................</div>
                  <div className="small">Designation: Commanding Officer / OC Training</div>
                  <div className="small">Date: .....................................................</div>
                </div>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  )
}

export default AcademicReports
