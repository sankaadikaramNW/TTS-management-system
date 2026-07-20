import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { toast } from 'react-toastify'

export const ReportGenerator = () => {
  const [reportType, setReportType] = useState('student')
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(false)
  const [squadron, setSquadron] = useState('')
  const [status, setStatus] = useState('')

  const handleGenerate = async () => {
    setLoading(true)
    try {
      if (reportType === 'student') {
        const res = await axios.get('/api/v1/students', {
          params: { squadron, status, limit: 100 }
        })
        setData(res.data.items)
      } else if (reportType === 'parade') {
        const res = await axios.get('/api/v1/parade/status', {
          params: { parade_date: new Date().toISOString().substring(0, 10) }
        })
        setData(res.data)
      } else if (reportType === 'accommodation') {
        const res = await axios.get('/api/v1/accommodation/allocations')
        setData(res.data)
      }
    } catch (err) {
      toast.error('Failed to generate report details')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    handleGenerate()
  }, [reportType])

  const handlePrint = () => {
    window.print()
  }

  return (
    <div className="fade-in-slide">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 className="mb-0 text-primary display-font">Reports & Analytics</h2>
          <p className="text-muted mb-0">Generate, print, and export official training registers</p>
        </div>
        <button className="btn btn-outline-primary d-flex align-items-center gap-2" onClick={handlePrint}>
          <i className="bi bi-printer"></i> Print Report
        </button>
      </div>

      {/* Filter and Config Selection Card */}
      <div className="card slaf-card p-3 mb-4">
        <div className="row g-2 align-items-end">
          <div className="col-md-3">
            <label className="form-label fw-semibold">Report Category</label>
            <select className="form-select" value={reportType} onChange={e => setReportType(e.target.value)}>
              <option value="student">Trainee Personal Dossiers</option>
              <option value="parade">Parade Strength Records</option>
              <option value="accommodation">Billet Allocations</option>
            </select>
          </div>
          {reportType === 'student' && (
            <>
              <div className="col-md-3">
                <label className="form-label fw-semibold">Squadron Filter</label>
                <select className="form-select" value={squadron} onChange={e => setSquadron(e.target.value)}>
                  <option value="">All Squadrons</option>
                  <option value="Training Squadron">Training Squadron</option>
                  <option value="Administration Squadron">Administration Squadron</option>
                </select>
              </div>
              <div className="col-md-3">
                <label className="form-label fw-semibold">Status Filter</label>
                <select className="form-select" value={status} onChange={e => setStatus(e.target.value)}>
                  <option value="">All Statuses</option>
                  <option value="Active">Active</option>
                  <option value="Sick Report">Sick Report</option>
                  <option value="Leave">Leave</option>
                  <option value="AWOL">AWOL</option>
                </select>
              </div>
            </>
          )}
          <div className="col-md-3 ms-auto">
            <button className="btn btn-primary w-100 py-2" onClick={handleGenerate}>
              <i className="bi bi-check-lg"></i> Compile Report
            </button>
          </div>
        </div>
      </div>

      {/* Generated Report Data Sheet */}
      <div className="card slaf-card p-4 bg-white text-dark">
        <div className="text-center mb-4">
          <h4 className="display-font mb-1 text-uppercase text-decoration-underline">Sri Lanka Air Force</h4>
          <h5 className="display-font mb-1">Trade Training School - SLAF TTS Ekala</h5>
          <span className="text-muted">Report Generated: {new Date().toLocaleString()}</span>
        </div>

        {loading ? (
          <div className="text-center py-5">
            <div className="spinner-border text-primary" role="status"></div>
          </div>
        ) : (
          <div className="table-responsive mt-3">
            {reportType === 'student' && (
              <table className="table table-bordered align-middle">
                <thead className="table-light text-uppercase" style={{ fontSize: '0.8rem' }}>
                  <tr>
                    <th>Service Number</th>
                    <th>Rank & Name</th>
                    <th>NIC</th>
                    <th>Blood Group</th>
                    <th>Trade</th>
                    <th>Squadron</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {data.length === 0 ? (
                    <tr><td colSpan="7" className="text-center text-muted">No records generated.</td></tr>
                  ) : (
                    data.map(s => (
                      <tr key={s.id}>
                        <td className="fw-semibold">{s.service_number}</td>
                        <td>{s.rank} {s.initials} {s.full_name}</td>
                        <td>{s.nic}</td>
                        <td className="text-danger fw-semibold">{s.blood_group}</td>
                        <td>{s.trade}</td>
                        <td>{s.squadron}</td>
                        <td>{s.status}</td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            )}

            {reportType === 'parade' && (
              <table className="table table-bordered align-middle">
                <thead className="table-light text-uppercase" style={{ fontSize: '0.8rem' }}>
                  <tr>
                    <th>Service Number</th>
                    <th>Trainee</th>
                    <th>Parade Status</th>
                    <th>Remarks / Notes</th>
                  </tr>
                </thead>
                <tbody>
                  {data.length === 0 ? (
                    <tr><td colSpan="4" className="text-center text-muted">No records recorded for today.</td></tr>
                  ) : (
                    data.map(p => (
                      <tr key={p.id}>
                        <td className="fw-semibold">{p.student_service_number}</td>
                        <td>{p.student_rank} {p.student_name}</td>
                        <td><span className="fw-semibold">{p.status}</span></td>
                        <td>{p.remarks || '-'}</td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            )}

            {reportType === 'accommodation' && (
              <table className="table table-bordered align-middle">
                <thead className="table-light text-uppercase" style={{ fontSize: '0.8rem' }}>
                  <tr>
                    <th>Trainee</th>
                    <th>Building Block</th>
                    <th>Billet</th>
                    <th>Room</th>
                    <th>Bed Assigned</th>
                    <th>Allocation Date</th>
                  </tr>
                </thead>
                <tbody>
                  {data.length === 0 ? (
                    <tr><td colSpan="6" className="text-center text-muted">No active billet allocations recorded.</td></tr>
                  ) : (
                    data.map(a => (
                      <tr key={a.id}>
                        <td className="fw-semibold">{a.student_service_number} - {a.student_name}</td>
                        <td>{a.building_name}</td>
                        <td>{a.billet_name}</td>
                        <td>{a.room_number}</td>
                        <td>{a.bed_number}</td>
                        <td>{new Date(a.allocated_at).toLocaleDateString()}</td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
export default ReportGenerator
