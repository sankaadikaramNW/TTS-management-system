import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { toast } from 'react-toastify'
import { useAuth } from '../../context/AuthContext'

export const DailyParade = () => {
  const { hasPermission } = useAuth()
  const [students, setStudents] = useState([])
  const [paradeRecords, setParadeRecords] = useState({})
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().substring(0, 10))

  const loadTraineesAndParadeState = async () => {
    setLoading(true)
    try {
      // 1. Fetch all active trainees
      const studentsRes = await axios.get('/api/v1/students', { params: { limit: 100 } })
      const activeTrainees = studentsRes.data.items
      setStudents(activeTrainees)

      // 2. Fetch recorded parade states for target date
      const paradeRes = await axios.get('/api/v1/parade/status', { params: { parade_date: selectedDate } })
      const recordedStates = paradeRes.data

      // Create mapping student_id -> {status, remarks}
      const initialMap = {}
      activeTrainees.forEach(s => {
        // Default to student's current status or Present if not set
        initialMap[s.id] = {
          status: s.status || 'Present',
          remarks: ''
        }
      })

      recordedStates.forEach(r => {
        initialMap[r.student_id] = {
          status: r.status,
          remarks: r.remarks || ''
        }
      })

      setParadeRecords(initialMap)
    } catch (err) {
      toast.error('Failed to load daily parade states')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadTraineesAndParadeState()
  }, [selectedDate])

  const handleStatusChange = (studentId, status) => {
    setParadeRecords(prev => ({
      ...prev,
      [studentId]: {
        ...prev[studentId],
        status
      }
    }))
  }

  const handleRemarksChange = (studentId, remarks) => {
    setParadeRecords(prev => ({
      ...prev,
      [studentId]: {
        ...prev[studentId],
        remarks
      }
    }))
  }

  const handleSave = async () => {
    setSaving(true)
    try {
      const records = Object.keys(paradeRecords).map(studentId => ({
        student_id: studentId,
        status: paradeRecords[studentId].status,
        remarks: paradeRecords[studentId].remarks
      }))

      await axios.post('/api/v1/parade/update', {
        date: selectedDate,
        records
      })
      toast.success(`Parade State successfully updated for ${selectedDate}`)
      toast.info('Auto-sync triggered: Academic schedules and Executive Dashboards updated successfully.')
      loadTraineesAndParadeState()
    } catch (err) {
      toast.error('Failed to update parade records')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="fade-in-slide">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 className="mb-0 text-primary display-font">Daily Parade Board</h2>
          <p className="text-muted mb-0">Record and verify the daily strength state of SLAF trainees</p>
        </div>
        <div className="d-flex align-items-center gap-3">
          <div>
            <label className="form-label mb-0 me-2 fw-semibold">Target Date:</label>
            <input 
              type="date" 
              className="form-control d-inline-block" 
              style={{ width: '180px' }}
              value={selectedDate}
              onChange={(e) => setSelectedDate(e.target.value)}
            />
          </div>
          {hasPermission('parade:write') && (
            <button 
              className="btn btn-primary d-flex align-items-center gap-2 px-4 py-2 mt-auto" 
              onClick={handleSave}
              disabled={saving || loading}
            >
              <i className="bi bi-save"></i> Save Parade State
            </button>
          )}
        </div>
      </div>

      <div className="alert alert-info d-flex align-items-center gap-3 slaf-card border-0 mb-4" role="alert">
        <i className="bi bi-info-circle-fill text-primary" style={{ fontSize: '1.5rem' }}></i>
        <div>
          <strong>Auto-Synchronization Enabled:</strong> Saving parade updates will automatically sync academic class registers, billet capacities, and flag security warnings (e.g. for AWOL details) instantly.
        </div>
      </div>

      {loading ? (
        <div className="text-center py-5">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading trainees...</span>
          </div>
        </div>
      ) : (
        <div className="card slaf-card p-0">
          <div className="table-responsive">
            <table className="table slaf-table mb-0">
              <thead>
                <tr>
                  <th>Service Number</th>
                  <th>Rank & Full Name</th>
                  <th>Current State</th>
                  <th style={{ width: '220px' }}>Recorded Parade Status</th>
                  <th>State Remarks (Log)</th>
                </tr>
              </thead>
              <tbody>
                {students.length === 0 ? (
                  <tr>
                    <td colSpan="5" className="text-center py-5 text-muted">No active trainees currently registered in master file.</td>
                  </tr>
                ) : (
                  students.map(student => {
                    const record = paradeRecords[student.id] || { status: 'Present', remarks: '' }
                    return (
                      <tr key={student.id}>
                        <td className="fw-semibold text-primary">{student.service_number}</td>
                        <td>
                          <span className="fw-semibold d-block">{student.rank} {student.initials}</span>
                          <small className="text-muted">{student.full_name}</small>
                        </td>
                        <td>
                          <span className={`slaf-badge ${student.status.toLowerCase().replace(' ', '-')}`}>
                            {student.status}
                          </span>
                        </td>
                        <td>
                          <select 
                            className="form-select form-select-sm"
                            value={record.status}
                            onChange={(e) => handleStatusChange(student.id, e.target.value)}
                            disabled={!hasPermission('parade:write')}
                          >
                            <option value="Present">Present</option>
                            <option value="Sick Report">Sick Report</option>
                            <option value="Hospital">Hospital</option>
                            <option value="Leave">Leave</option>
                            <option value="Temporary Duty">Temporary Duty</option>
                            <option value="Course Visit">Course Visit</option>
                            <option value="Detached Duty">Detached Duty</option>
                            <option value="AWOL">AWOL</option>
                          </select>
                        </td>
                        <td>
                          <input 
                            type="text" 
                            className="form-control form-control-sm"
                            placeholder="Add remarks (e.g. sick certificate, duty orders)"
                            value={record.remarks}
                            onChange={(e) => handleRemarksChange(student.id, e.target.value)}
                            disabled={!hasPermission('parade:write')}
                          />
                        </td>
                      </tr>
                    )
                  })
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}
export default DailyParade
