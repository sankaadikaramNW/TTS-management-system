import React, { useEffect, useState, useCallback } from 'react'
import axios from 'axios'
import { toast } from 'react-toastify'
import { useAuth } from '../../context/AuthContext'

// ─── Status badge config ──────────────────────────────────────
const SUBMISSION_STATUS_CONFIG = {
  DRAFT:     { label: 'Draft',     color: '#64748b', bg: '#f1f5f9', icon: 'bi-pencil-square' },
  SUBMITTED: { label: 'Submitted', color: '#d97706', bg: '#fffbeb', icon: 'bi-clock-history' },
  APPROVED:  { label: 'Approved',  color: '#059669', bg: '#ecfdf5', icon: 'bi-check-circle-fill' },
  REJECTED:  { label: 'Rejected',  color: '#dc2626', bg: '#fef2f2', icon: 'bi-x-circle-fill' },
}

const StatusBadge = ({ status }) => {
  const cfg = SUBMISSION_STATUS_CONFIG[status] || SUBMISSION_STATUS_CONFIG.DRAFT
  return (
    <span className="px-2 py-1 rounded fw-semibold" style={{
      background: cfg.bg, color: cfg.color,
      fontSize: '0.78rem', border: `1px solid ${cfg.color}30`
    }}>
      <i className={`bi ${cfg.icon} me-1`} />
      {cfg.label}
    </span>
  )
}

// ─── Utility ─────────────────────────────────────────────────
const groupByTrade = (students) => {
  return students.reduce((acc, s) => {
    const trade = s.trade || 'Unassigned'
    if (!acc[trade]) acc[trade] = []
    acc[trade].push(s)
    return acc
  }, {})
}

export const DailyParade = () => {
  const { hasPermission, user: currentUser } = useAuth()

  // ── Shared state ─────────────────────────────────────────
  const [activeTab, setActiveTab] = useState('record')
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().substring(0, 10))
  const [statuses, setStatuses] = useState([])
  const [trades, setTrades] = useState([])  // Loaded from DB trades table

  // ── Tab 1: Record & Submit ───────────────────────────────
  const [students, setStudents] = useState([])
  const [paradeRecords, setParadeRecords] = useState({})
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [selectedTrade, setSelectedTrade] = useState('All')
  const [officerOptions, setOfficerOptions] = useState([])
  const [selectedOfficerId, setSelectedOfficerId] = useState('')
  const [submitterRemarks, setSubmitterRemarks] = useState('')
  const [tradeSubmissions, setTradeSubmissions] = useState({})  // trade -> submission info

  // ── Tab 2: Pending Approvals ─────────────────────────────
  const [pendingApprovals, setPendingApprovals] = useState([])
  const [pendingLoading, setPendingLoading] = useState(false)
  const [approvalDetail, setApprovalDetail] = useState(null)
  const [showApprovalModal, setShowApprovalModal] = useState(false)
  const [approverRemarks, setApproverRemarks] = useState('')
  const [rejectionReason, setRejectionReason] = useState('')
  const [actionLoading, setActionLoading] = useState(false)

  // ── Tab 3: Submission History ────────────────────────────
  const [historyList, setHistoryList] = useState([])
  const [historyLoading, setHistoryLoading] = useState(false)
  const [historyDateFilter, setHistoryDateFilter] = useState('')
  const [historyStatusFilter, setHistoryStatusFilter] = useState('')
  const [expandedHistory, setExpandedHistory] = useState(null)

  // ── Tab 4: Officer I/C Management ────────────────────────
  const [officers, setOfficers] = useState([])
  const [officersLoading, setOfficersLoading] = useState(false)
  const [showOICModal, setShowOICModal] = useState(false)
  const [oicTrade, setOicTrade] = useState('')
  const [oicUserId, setOicUserId] = useState('')
  const [allUsers, setAllUsers] = useState([])
  const [savingOIC, setSavingOIC] = useState(false)


  // ── Boot ─────────────────────────────────────────────────
  useEffect(() => {
    const fetchBootData = async () => {
      try {
        const [statusRes, tradeRes] = await Promise.all([
          axios.get('/api/v1/parade/statuses'),
          axios.get('/api/v1/students/trades', { params: { active_only: true } })
        ])
        setStatuses(statusRes.data)
        setTrades(tradeRes.data)
      } catch { /* non-critical */ }
    }
    fetchBootData()
  }, [])

  // ── Tab 1: Load students + parade state ─────────────────
  const loadParadeData = useCallback(async () => {
    setLoading(true)
    try {
      const [studentsRes, paradeRes, officersRes] = await Promise.all([
        axios.get('/api/v1/students', { params: { limit: 500 } }),
        axios.get('/api/v1/parade/status', { params: { parade_date: selectedDate } }),
        axios.get('/api/v1/parade/officers'),
      ])

      const activeTrainees = studentsRes.data.items || []
      setStudents(activeTrainees)

      const officerList = officersRes.data || []
      setOfficerOptions(officerList)

      const initialMap = {}
      activeTrainees.forEach(s => {
        initialMap[s.id] = { status: 'Present', remarks: '' }
      })
      paradeRes.data.forEach(r => {
        initialMap[r.student_id] = { status: r.status, remarks: r.remarks || '' }
      })
      setParadeRecords(initialMap)

      // Load submission status for each trade on this date
      const subRes = await axios.get('/api/v1/parade/submissions', {
        params: { parade_date: selectedDate }
      })
      const submissionMap = {}
      subRes.data.forEach(s => { submissionMap[s.trade] = s })
      setTradeSubmissions(submissionMap)

    } catch {
      toast.error('Failed to load parade data')
    } finally {
      setLoading(false)
    }
  }, [selectedDate])

  useEffect(() => {
    if (activeTab === 'record') loadParadeData()
  }, [selectedDate, activeTab, loadParadeData])

  // ── Tab 2: Load pending approvals ───────────────────────
  const loadPendingApprovals = useCallback(async () => {
    if (!hasPermission('parade:approve')) return
    setPendingLoading(true)
    try {
      const res = await axios.get('/api/v1/parade/submissions/pending')
      setPendingApprovals(res.data)
    } catch {
      toast.error('Failed to load pending approvals')
    } finally {
      setPendingLoading(false)
    }
  }, [hasPermission])

  useEffect(() => {
    if (activeTab === 'approvals') loadPendingApprovals()
  }, [activeTab, loadPendingApprovals])

  // ── Tab 3: Load history ──────────────────────────────────
  const loadHistory = useCallback(async () => {
    setHistoryLoading(true)
    try {
      const params = { limit: 100 }
      if (historyDateFilter) params.parade_date = historyDateFilter
      if (historyStatusFilter) params.status = historyStatusFilter
      const res = await axios.get('/api/v1/parade/submissions', { params })
      setHistoryList(res.data)
    } catch {
      toast.error('Failed to load history')
    } finally {
      setHistoryLoading(false)
    }
  }, [historyDateFilter, historyStatusFilter])

  useEffect(() => {
    if (activeTab === 'history') loadHistory()
  }, [activeTab, loadHistory])

  // ── Tab 4: Load officers ─────────────────────────────────
  const loadOfficers = useCallback(async () => {
    setOfficersLoading(true)
    try {
      const [officersRes, usersRes] = await Promise.all([
        axios.get('/api/v1/parade/officers'),
        axios.get('/api/v1/system/users', { params: { limit: 200 } }).catch(() => ({ data: { items: [] } }))
      ])
      setOfficers(officersRes.data)
      setAllUsers(usersRes.data.items || usersRes.data || [])
    } catch {
      toast.error('Failed to load officer assignments')
    } finally {
      setOfficersLoading(false)
    }
  }, [])

  useEffect(() => {
    if (activeTab === 'officers') loadOfficers()
  }, [activeTab, loadOfficers])

  // ── Handlers: Record & Submit tab ────────────────────────
  const handleStatusChange = (studentId, status) => {
    setParadeRecords(prev => ({ ...prev, [studentId]: { ...prev[studentId], status } }))
  }

  const handleRemarksChange = (studentId, remarks) => {
    setParadeRecords(prev => ({ ...prev, [studentId]: { ...prev[studentId], remarks } }))
  }

  const getRecordsForTrade = (trade) => {
    const tradeStudents = trade === 'All' ? students : students.filter(s => s.trade === trade)
    return tradeStudents.map(s => ({
      student_id: s.id,
      status: paradeRecords[s.id]?.status || 'Present',
      remarks: paradeRecords[s.id]?.remarks || ''
    }))
  }

  const handleSaveDraft = async () => {
    if (selectedTrade === 'All') {
      toast.warning('Please select a specific trade to save a draft')
      return
    }
    setSaving(true)
    try {
      await axios.post('/api/v1/parade/draft', {
        date: selectedDate,
        trade: selectedTrade,
        records: getRecordsForTrade(selectedTrade)
      })
      toast.success(`Draft saved for ${selectedTrade} — ${selectedDate}`)
      await loadParadeData()
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to save draft')
    } finally {
      setSaving(false)
    }
  }

  const handleSubmitForApproval = async () => {
    if (selectedTrade === 'All') {
      toast.warning('Please select a specific trade to submit')
      return
    }
    if (!selectedOfficerId) {
      toast.warning('Please select an Approving Officer I/C before submitting')
      return
    }
    setSubmitting(true)
    try {
      await axios.post('/api/v1/parade/submit', {
        date: selectedDate,
        trade: selectedTrade,
        approving_officer_id: selectedOfficerId,
        submitter_remarks: submitterRemarks,
        records: getRecordsForTrade(selectedTrade)
      })
      toast.success(`Parade state submitted for approval — ${selectedTrade}`)
      toast.info('The assigned Officer I/C has been notified for review.')
      setSubmitterRemarks('')
      await loadParadeData()
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to submit parade state')
    } finally {
      setSubmitting(false)
    }
  }

  // ── Handlers: Approvals tab ──────────────────────────────
  const openApprovalDetail = async (submission) => {
    try {
      const res = await axios.get(`/api/v1/parade/submissions/${submission.id}`)
      setApprovalDetail(res.data)
      setApproverRemarks('')
      setRejectionReason('')
      setShowApprovalModal(true)
    } catch {
      toast.error('Failed to load submission details')
    }
  }

  const handleApprove = async () => {
    if (!approvalDetail) return
    setActionLoading(true)
    try {
      await axios.post(`/api/v1/parade/submissions/${approvalDetail.id}/approve`, {
        remarks: approverRemarks
      })
      toast.success(`Parade State APPROVED — ${approvalDetail.trade} (${approvalDetail.date})`)
      setShowApprovalModal(false)
      await loadPendingApprovals()
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Approval failed')
    } finally {
      setActionLoading(false)
    }
  }

  const handleReject = async () => {
    if (!approvalDetail) return
    if (!rejectionReason.trim()) {
      toast.warning('Rejection reason is mandatory')
      return
    }
    setActionLoading(true)
    try {
      await axios.post(`/api/v1/parade/submissions/${approvalDetail.id}/reject`, {
        rejection_reason: rejectionReason
      })
      toast.warning(`Parade State REJECTED — ${approvalDetail.trade} (${approvalDetail.date})`)
      setShowApprovalModal(false)
      await loadPendingApprovals()
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Rejection failed')
    } finally {
      setActionLoading(false)
    }
  }

  // ── Handlers: Officer I/C tab ────────────────────────────
  const handleAssignOIC = async () => {
    if (!oicTrade || !oicUserId) {
      toast.warning('Please select both a trade and a user')
      return
    }
    setSavingOIC(true)
    try {
      await axios.post('/api/v1/parade/officers', { trade: oicTrade, user_id: oicUserId })
      toast.success(`Officer I/C assigned for ${oicTrade}`)
      setShowOICModal(false)
      setOicTrade(''); setOicUserId('')
      await loadOfficers()
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to assign Officer I/C')
    } finally {
      setSavingOIC(false)
    }
  }

  const handleRemoveOIC = async (oicId, trade) => {
    if (!window.confirm(`Remove Officer I/C assignment for ${trade}?`)) return
    try {
      await axios.delete(`/api/v1/parade/officers/${oicId}`)
      toast.success('Officer I/C assignment removed')
      await loadOfficers()
    } catch {
      toast.error('Failed to remove assignment')
    }
  }

  // ── Derived ───────────────────────────────────────────────
  const groupedStudents = groupByTrade(students)
  const displayStudents = selectedTrade === 'All'
    ? students
    : students.filter(s => s.trade === selectedTrade)

  const currentTradeSubmission = selectedTrade !== 'All' ? tradeSubmissions[selectedTrade] : null
  const canSubmit = currentTradeSubmission?.status !== 'SUBMITTED' && currentTradeSubmission?.status !== 'APPROVED'

  // Officers available for the selected trade filter
  const officersForTrade = selectedTrade !== 'All'
    ? officerOptions.filter(o => o.trade === selectedTrade)
    : officerOptions

  const getStatusColor = (status) => {
    const map = {
      'Present': '#059669', 'AWOL': '#dc2626', 'Hospital': '#7c3aed',
      'Leave': '#2563eb', 'Sick Report': '#d97706', 'Temporary Duty': '#0891b2',
      'Course Visit': '#0891b2', 'Detached Duty': '#6d28d9'
    }
    return map[status] || '#64748b'
  }

  // ── Render ────────────────────────────────────────────────
  return (
    <div className="fade-in-slide">
      {/* ─── Page Header ─── */}
      <div className="d-flex justify-content-between align-items-start mb-4 flex-wrap gap-3">
        <div>
          <h2 className="mb-0 text-primary display-font">Daily Parade State</h2>
          <p className="text-muted mb-0">Record, submit, and approve the official daily strength of SLAF trainees</p>
        </div>
        <div className="d-flex align-items-center gap-2">
          <label className="form-label mb-0 fw-semibold text-nowrap">Target Date:</label>
          <input
            type="date"
            className="form-control"
            style={{ width: '180px' }}
            value={selectedDate}
            onChange={e => setSelectedDate(e.target.value)}
          />
        </div>
      </div>

      {/* ─── Navigation Tabs ─── */}
      <ul className="nav nav-tabs mb-4" style={{ borderBottom: '2px solid #e2e8f0' }}>
        {[
          { key: 'record',   icon: 'bi-clipboard2-check', label: 'Record & Submit', show: true },
          { key: 'approvals',icon: 'bi-shield-check',      label: `Pending Approvals${pendingApprovals.length ? ` (${pendingApprovals.length})` : ''}`, show: hasPermission('parade:approve') },
          { key: 'history',  icon: 'bi-clock-history',    label: 'Submission History', show: true },
          { key: 'officers', icon: 'bi-person-badge',     label: 'Officer I/C Management', show: hasPermission('parade:manage_officers') || hasPermission('parade:read') },
        ].filter(t => t.show).map(tab => (
          <li key={tab.key} className="nav-item">
            <button
              className={`nav-link fw-semibold ${activeTab === tab.key ? 'active text-primary' : 'text-muted'}`}
              style={{
                border: 'none', borderBottom: activeTab === tab.key ? '3px solid var(--bs-primary)' : '3px solid transparent',
                background: 'none', padding: '10px 20px', fontSize: '0.9rem'
              }}
              onClick={() => setActiveTab(tab.key)}
            >
              <i className={`bi ${tab.icon} me-2`} />{tab.label}
            </button>
          </li>
        ))}
      </ul>

      {/* ═══════════════════════════════════════════════════════
          TAB 1: RECORD & SUBMIT
      ═══════════════════════════════════════════════════════ */}
      {activeTab === 'record' && (
        <div>
          {/* Trade filter + submission status */}
          <div className="d-flex justify-content-between align-items-center mb-3 flex-wrap gap-3">
            <div className="d-flex align-items-center gap-3 flex-wrap">
              <div>
                <label className="form-label mb-1 fw-semibold" style={{ fontSize: '0.82rem' }}>
                  <i className="bi bi-funnel me-1" />Filter by Trade
                </label>
                <select
                  className="form-select form-select-sm"
                  style={{ width: '200px' }}
                  value={selectedTrade}
                  onChange={e => { setSelectedTrade(e.target.value); setSelectedOfficerId('') }}
                >
                  <option value="All">All Trades</option>
                  {trades.map(t => <option key={t.id} value={t.label}>{t.label}</option>)}
                </select>
              </div>

              {selectedTrade !== 'All' && currentTradeSubmission && (
                <div className="mt-auto">
                  <label className="form-label mb-1 fw-semibold" style={{ fontSize: '0.82rem' }}>
                    Submission Status
                  </label>
                  <div><StatusBadge status={currentTradeSubmission.status} /></div>
                </div>
              )}
            </div>

            {/* Summary pill cards */}
            {!loading && (
              <div className="d-flex gap-2 flex-wrap">
                {[
                  { label: 'Total', count: displayStudents.length, color: '#3b82f6' },
                  { label: 'Present', count: displayStudents.filter(s => (paradeRecords[s.id]?.status || 'Present') === 'Present').length, color: '#059669' },
                  { label: 'Absent', count: displayStudents.filter(s => (paradeRecords[s.id]?.status || 'Present') !== 'Present').length, color: '#dc2626' },
                ].map(pill => (
                  <div key={pill.label} className="rounded px-3 py-1 text-center" style={{ background: `${pill.color}15`, border: `1px solid ${pill.color}30` }}>
                    <div className="fw-bold" style={{ color: pill.color, fontSize: '1.1rem' }}>{pill.count}</div>
                    <div style={{ fontSize: '0.72rem', color: pill.color }}>{pill.label}</div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Rejection alert */}
          {currentTradeSubmission?.status === 'REJECTED' && (
            <div className="alert alert-danger d-flex align-items-start gap-3 mb-3">
              <i className="bi bi-x-circle-fill mt-1" style={{ fontSize: '1.3rem' }} />
              <div>
                <strong>Parade State Rejected</strong>
                <div className="mt-1" style={{ fontSize: '0.88rem' }}>
                  Reason: <em>{currentTradeSubmission.rejection_reason || 'No reason provided'}</em>
                  <br />Revise the records below and resubmit.
                </div>
              </div>
            </div>
          )}

          {/* Approved banner */}
          {currentTradeSubmission?.status === 'APPROVED' && (
            <div className="alert alert-success d-flex align-items-center gap-3 mb-3">
              <i className="bi bi-patch-check-fill" style={{ fontSize: '1.5rem' }} />
              <div>
                <strong>Official Daily Strength Confirmed</strong>
                <div style={{ fontSize: '0.85rem' }}>
                  Approved by {currentTradeSubmission.officer_name} on{' '}
                  {currentTradeSubmission.reviewed_at
                    ? new Date(currentTradeSubmission.reviewed_at).toLocaleString()
                    : '—'}
                  {currentTradeSubmission.approver_remarks && ` — "${currentTradeSubmission.approver_remarks}"`}
                </div>
              </div>
            </div>
          )}

          {/* Submitted info */}
          {currentTradeSubmission?.status === 'SUBMITTED' && (
            <div className="alert alert-warning d-flex align-items-center gap-3 mb-3">
              <i className="bi bi-hourglass-split" style={{ fontSize: '1.4rem' }} />
              <div>
                <strong>Awaiting Approval</strong>
                <div style={{ fontSize: '0.85rem' }}>
                  Submitted to <strong>{currentTradeSubmission.officer_name}</strong> at{' '}
                  {currentTradeSubmission.submitted_at
                    ? new Date(currentTradeSubmission.submitted_at).toLocaleString()
                    : '—'}
                </div>
              </div>
            </div>
          )}

          {loading ? (
            <div className="text-center py-5">
              <div className="spinner-border text-primary" role="status" />
            </div>
          ) : (
            <>
              {/* ── Per-student Table ── */}
              <div className="card slaf-card p-0 mb-4">
                <div className="table-responsive">
                  <table className="table slaf-table mb-0">
                    <thead>
                      <tr>
                        <th style={{ width: '130px' }}>Service No.</th>
                        <th>Rank & Name</th>
                        <th style={{ width: '100px' }}>Trade</th>
                        <th style={{ width: '200px' }}>Parade Status</th>
                        <th>Remarks (Log)</th>
                      </tr>
                    </thead>
                    <tbody>
                      {displayStudents.length === 0 ? (
                        <tr>
                          <td colSpan="5" className="text-center py-5 text-muted">
                            No active trainees found{selectedTrade !== 'All' ? ` for trade: ${selectedTrade}` : ''}.
                          </td>
                        </tr>
                      ) : (
                        displayStudents.map(student => {
                          const record = paradeRecords[student.id] || { status: 'Present', remarks: '' }
                          const statusColor = getStatusColor(record.status)
                          const isLocked = currentTradeSubmission?.status === 'SUBMITTED' || currentTradeSubmission?.status === 'APPROVED'
                          return (
                            <tr key={student.id} style={isLocked ? { opacity: 0.75 } : {}}>
                              <td className="fw-semibold text-primary">{student.service_number}</td>
                              <td>
                                <div className="fw-bold text-dark" style={{ fontSize: '0.88rem' }}>
                                  {student.full_name}
                                </div>
                                <div className="d-flex align-items-center gap-1 mt-1">
                                  <span className="badge bg-secondary-subtle text-dark border" style={{ fontSize: '0.7rem' }}>
                                    {student.rank}
                                  </span>
                                  {student.initials && (
                                    <span className="text-muted" style={{ fontSize: '0.73rem' }}>• {student.initials}</span>
                                  )}
                                </div>
                              </td>
                              <td>
                                <span className="badge" style={{ background: '#eff6ff', color: '#2563eb', fontSize: '0.73rem' }}>
                                  {student.trade || '—'}
                                </span>
                              </td>
                              <td>
                                <select
                                  className="form-select form-select-sm"
                                  value={record.status}
                                  onChange={e => handleStatusChange(student.id, e.target.value)}
                                  disabled={!hasPermission('parade:write') || isLocked}
                                  style={{ borderColor: `${statusColor}60`, color: statusColor, fontWeight: 600 }}
                                >
                                  {statuses.map(st => (
                                    <option key={st.id || st.code} value={st.label}>{st.label}</option>
                                  ))}
                                </select>
                              </td>
                              <td>
                                <input
                                  type="text"
                                  className="form-control form-control-sm"
                                  placeholder="Sick cert, duty orders..."
                                  value={record.remarks}
                                  onChange={e => handleRemarksChange(student.id, e.target.value)}
                                  disabled={!hasPermission('parade:write') || isLocked}
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

              {/* ── Submission Panel ── */}
              {hasPermission('parade:write') && selectedTrade !== 'All' && canSubmit && (
                <div className="card slaf-card p-4" style={{ border: '2px solid #3b82f620', background: 'linear-gradient(135deg,#f0f9ff,#eff6ff)' }}>
                  <h6 className="fw-bold text-primary mb-3">
                    <i className="bi bi-send-check me-2" />
                    Submit Parade State for Approval — {selectedTrade}
                  </h6>
                  <div className="row g-3">
                    <div className="col-md-5">
                      <label className="form-label fw-semibold" style={{ fontSize: '0.82rem' }}>
                        <i className="bi bi-person-badge me-1" />Approving Officer I/C *
                      </label>
                      <select
                        className="form-select"
                        value={selectedOfficerId}
                        onChange={e => setSelectedOfficerId(e.target.value)}
                      >
                        <option value="">— Select Approving Officer —</option>
                        {officersForTrade.length > 0
                          ? officersForTrade.map(o => (
                            <option key={o.id} value={o.user_id}>
                              {o.officer_name} ({o.trade})
                            </option>
                          ))
                          : officerOptions.map(o => (
                            <option key={o.id} value={o.user_id}>
                              {o.officer_name} (OIC: {o.trade})
                            </option>
                          ))
                        }
                      </select>
                      {officerOptions.length === 0 && (
                        <div className="form-text text-danger mt-1">
                          <i className="bi bi-exclamation-triangle me-1" />
                          No Officer I/C assigned. Contact administrator.
                        </div>
                      )}
                    </div>
                    <div className="col-md-5">
                      <label className="form-label fw-semibold" style={{ fontSize: '0.82rem' }}>
                        <i className="bi bi-chat-left-text me-1" />Submission Remarks (Optional)
                      </label>
                      <input
                        type="text"
                        className="form-control"
                        placeholder="Any relevant notes for the approving officer..."
                        value={submitterRemarks}
                        onChange={e => setSubmitterRemarks(e.target.value)}
                      />
                    </div>
                    <div className="col-md-2 d-flex flex-column justify-content-end gap-2">
                      <button
                        className="btn btn-outline-secondary btn-sm"
                        onClick={handleSaveDraft}
                        disabled={saving}
                      >
                        {saving ? <span className="spinner-border spinner-border-sm me-1" /> : <i className="bi bi-floppy me-1" />}
                        Save Draft
                      </button>
                      <button
                        className="btn btn-primary btn-sm"
                        onClick={handleSubmitForApproval}
                        disabled={submitting || !selectedOfficerId}
                      >
                        {submitting ? <span className="spinner-border spinner-border-sm me-1" /> : <i className="bi bi-send me-1" />}
                        Submit
                      </button>
                    </div>
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      )}

      {/* ═══════════════════════════════════════════════════════
          TAB 2: PENDING APPROVALS
      ═══════════════════════════════════════════════════════ */}
      {activeTab === 'approvals' && hasPermission('parade:approve') && (
        <div>
          <div className="d-flex justify-content-between align-items-center mb-4">
            <div>
              <h5 className="fw-bold mb-1">Pending Approval Queue</h5>
              <p className="text-muted mb-0" style={{ fontSize: '0.88rem' }}>
                Parade states submitted for your review as Officer I/C
              </p>
            </div>
            <button className="btn btn-outline-primary btn-sm" onClick={loadPendingApprovals}>
              <i className="bi bi-arrow-clockwise me-1" />Refresh
            </button>
          </div>

          {pendingLoading ? (
            <div className="text-center py-5"><div className="spinner-border text-primary" /></div>
          ) : pendingApprovals.length === 0 ? (
            <div className="text-center py-5">
              <i className="bi bi-inbox" style={{ fontSize: '3rem', color: '#94a3b8' }} />
              <div className="text-muted mt-2 fw-semibold">No pending approvals</div>
              <div className="text-muted" style={{ fontSize: '0.85rem' }}>All parade states are up to date.</div>
            </div>
          ) : (
            <div className="row g-3">
              {pendingApprovals.map(sub => (
                <div key={sub.id} className="col-12">
                  <div className="card slaf-card p-0" style={{ border: '2px solid #f59e0b40' }}>
                    <div className="card-body p-4">
                      <div className="d-flex justify-content-between align-items-start flex-wrap gap-3">
                        <div className="d-flex gap-4 flex-wrap">
                          <div>
                            <div className="text-muted" style={{ fontSize: '0.75rem' }}>DATE</div>
                            <div className="fw-bold">{sub.date}</div>
                          </div>
                          <div>
                            <div className="text-muted" style={{ fontSize: '0.75rem' }}>TRADE</div>
                            <div className="fw-bold text-primary">{sub.trade}</div>
                          </div>
                          <div>
                            <div className="text-muted" style={{ fontSize: '0.75rem' }}>SUBMITTED BY</div>
                            <div className="fw-bold">{sub.submitter_name || '—'}</div>
                          </div>
                          <div>
                            <div className="text-muted" style={{ fontSize: '0.75rem' }}>SUBMITTED AT</div>
                            <div className="fw-bold">{sub.submitted_at ? new Date(sub.submitted_at).toLocaleString() : '—'}</div>
                          </div>
                          <div>
                            <div className="text-muted" style={{ fontSize: '0.75rem' }}>STRENGTH</div>
                            <div>
                              <span className="fw-bold text-success">{sub.present_count}</span>
                              <span className="text-muted">/{sub.total_strength} Present</span>
                            </div>
                          </div>
                        </div>
                        <div className="d-flex gap-2 flex-wrap">
                          <button
                            className="btn btn-sm btn-outline-primary"
                            onClick={() => openApprovalDetail(sub)}
                          >
                            <i className="bi bi-eye me-1" />Review Details
                          </button>
                        </div>
                      </div>
                      {sub.submitter_remarks && (
                        <div className="mt-3 p-2 rounded" style={{ background: '#fffbeb', borderLeft: '3px solid #f59e0b', fontSize: '0.85rem' }}>
                          <i className="bi bi-chat-left-quote me-1 text-warning" />
                          <strong>Submitter Remarks:</strong> {sub.submitter_remarks}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* ── Approval Review Modal ── */}
          {showApprovalModal && approvalDetail && (
            <div className="modal show d-block" style={{ background: 'rgba(0,0,0,0.55)', zIndex: 1055 }}>
              <div className="modal-dialog modal-xl modal-dialog-scrollable">
                <div className="modal-content">
                  <div className="modal-header border-0 pb-0">
                    <div>
                      <h5 className="modal-title fw-bold">
                        <i className="bi bi-shield-check text-primary me-2" />
                        Review Parade State — {approvalDetail.trade} ({approvalDetail.date})
                      </h5>
                      <div className="d-flex gap-3 mt-1 flex-wrap" style={{ fontSize: '0.82rem', color: '#64748b' }}>
                        <span><i className="bi bi-person me-1" />Submitted by: {approvalDetail.submitter_name}</span>
                        <span><i className="bi bi-clock me-1" />At: {approvalDetail.submitted_at ? new Date(approvalDetail.submitted_at).toLocaleString() : '—'}</span>
                        <span className="text-success fw-semibold"><i className="bi bi-people me-1" />{approvalDetail.present_count}/{approvalDetail.total_strength} Present</span>
                      </div>
                    </div>
                    <button className="btn-close" onClick={() => setShowApprovalModal(false)} />
                  </div>
                  <div className="modal-body">
                    {approvalDetail.submitter_remarks && (
                      <div className="alert alert-warning py-2 mb-3" style={{ fontSize: '0.85rem' }}>
                        <i className="bi bi-chat-left-quote me-1" />
                        <strong>Submitter Remarks:</strong> {approvalDetail.submitter_remarks}
                      </div>
                    )}

                    {/* Per-student records table */}
                    <div className="table-responsive mb-4" style={{ maxHeight: '40vh', overflowY: 'auto' }}>
                      <table className="table table-sm table-hover">
                        <thead className="table-light sticky-top">
                          <tr>
                            <th>Service No.</th>
                            <th>Name / Rank</th>
                            <th>Status</th>
                            <th>Remarks</th>
                          </tr>
                        </thead>
                        <tbody>
                          {(approvalDetail.records || []).map(rec => (
                            <tr key={rec.id}>
                              <td className="fw-semibold text-primary">{rec.student_service_number}</td>
                              <td>
                                <div className="fw-semibold" style={{ fontSize: '0.85rem' }}>{rec.student_name}</div>
                                <span className="badge bg-secondary-subtle text-dark" style={{ fontSize: '0.7rem' }}>{rec.student_rank}</span>
                              </td>
                              <td>
                                <span className="fw-semibold" style={{ color: getStatusColor(rec.status), fontSize: '0.85rem' }}>
                                  {rec.status}
                                </span>
                              </td>
                              <td style={{ fontSize: '0.82rem', color: '#64748b' }}>{rec.remarks || '—'}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>

                    {/* Approval decision area */}
                    <div className="row g-3">
                      <div className="col-12">
                        <label className="form-label fw-semibold">
                          <i className="bi bi-chat-left-text me-1" />Approval Remarks (Optional)
                        </label>
                        <textarea
                          className="form-control"
                          rows={2}
                          placeholder="Remarks to be noted in the official record..."
                          value={approverRemarks}
                          onChange={e => setApproverRemarks(e.target.value)}
                        />
                      </div>
                      <div className="col-12">
                        <label className="form-label fw-semibold text-danger">
                          <i className="bi bi-x-circle me-1" />Rejection Reason (Required if rejecting)
                        </label>
                        <textarea
                          className="form-control border-danger"
                          rows={2}
                          placeholder="State clearly why this parade state is being returned for revision..."
                          value={rejectionReason}
                          onChange={e => setRejectionReason(e.target.value)}
                        />
                      </div>
                    </div>
                  </div>
                  <div className="modal-footer border-0 pt-0">
                    <button className="btn btn-outline-secondary" onClick={() => setShowApprovalModal(false)}>
                      Cancel
                    </button>
                    <button
                      className="btn btn-danger"
                      onClick={handleReject}
                      disabled={actionLoading || !rejectionReason.trim()}
                    >
                      {actionLoading ? <span className="spinner-border spinner-border-sm me-1" /> : <i className="bi bi-x-lg me-1" />}
                      Reject
                    </button>
                    <button
                      className="btn btn-success px-4"
                      onClick={handleApprove}
                      disabled={actionLoading}
                    >
                      {actionLoading ? <span className="spinner-border spinner-border-sm me-1" /> : <i className="bi bi-check-lg me-1" />}
                      Approve as Official Strength
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* ═══════════════════════════════════════════════════════
          TAB 3: SUBMISSION HISTORY
      ═══════════════════════════════════════════════════════ */}
      {activeTab === 'history' && (
        <div>
          <div className="d-flex justify-content-between align-items-end mb-4 flex-wrap gap-3">
            <div>
              <h5 className="fw-bold mb-1">Submission History</h5>
              <p className="text-muted mb-0" style={{ fontSize: '0.88rem' }}>Complete audit trail of all parade state submissions</p>
            </div>
            <div className="d-flex gap-2 flex-wrap align-items-end">
              <div>
                <label className="form-label mb-1" style={{ fontSize: '0.78rem' }}>Filter by Date</label>
                <input type="date" className="form-control form-control-sm" value={historyDateFilter}
                  onChange={e => setHistoryDateFilter(e.target.value)} />
              </div>
              <div>
                <label className="form-label mb-1" style={{ fontSize: '0.78rem' }}>Filter by Status</label>
                <select className="form-select form-select-sm" style={{ width: '140px' }}
                  value={historyStatusFilter} onChange={e => setHistoryStatusFilter(e.target.value)}>
                  <option value="">All Statuses</option>
                  {['DRAFT','SUBMITTED','APPROVED','REJECTED'].map(s => <option key={s}>{s}</option>)}
                </select>
              </div>
              <button className="btn btn-outline-primary btn-sm" onClick={loadHistory}>
                <i className="bi bi-search me-1" />Search
              </button>
            </div>
          </div>

          {historyLoading ? (
            <div className="text-center py-5"><div className="spinner-border text-primary" /></div>
          ) : historyList.length === 0 ? (
            <div className="text-center py-5 text-muted">
              <i className="bi bi-journal-x" style={{ fontSize: '2.5rem', opacity: 0.4 }} />
              <div className="mt-2">No submissions found for the selected filters.</div>
            </div>
          ) : (
            <div className="card slaf-card p-0">
              <div className="table-responsive">
                <table className="table slaf-table mb-0">
                  <thead>
                    <tr>
                      <th>Date</th>
                      <th>Trade</th>
                      <th>Status</th>
                      <th>Submitted By</th>
                      <th>Approving Officer</th>
                      <th>Strength</th>
                      <th>Reviewed At</th>
                      <th></th>
                    </tr>
                  </thead>
                  <tbody>
                    {historyList.map(sub => (
                      <React.Fragment key={sub.id}>
                        <tr>
                          <td className="fw-semibold">{sub.date}</td>
                          <td>
                            <span className="badge" style={{ background: '#eff6ff', color: '#2563eb', fontSize: '0.78rem' }}>
                              {sub.trade}
                            </span>
                          </td>
                          <td><StatusBadge status={sub.status} /></td>
                          <td style={{ fontSize: '0.85rem' }}>{sub.submitter_name || '—'}</td>
                          <td style={{ fontSize: '0.85rem' }}>{sub.officer_name || '—'}</td>
                          <td style={{ fontSize: '0.85rem' }}>
                            <span className="text-success fw-semibold">{sub.present_count ?? '—'}</span>
                            <span className="text-muted">/{sub.total_strength ?? '—'}</span>
                          </td>
                          <td style={{ fontSize: '0.82rem', color: '#64748b' }}>
                            {sub.reviewed_at ? new Date(sub.reviewed_at).toLocaleDateString() : '—'}
                          </td>
                          <td>
                            <button
                              className="btn btn-outline-secondary btn-sm"
                              style={{ fontSize: '0.75rem', padding: '2px 8px' }}
                              onClick={() => setExpandedHistory(expandedHistory === sub.id ? null : sub.id)}
                            >
                              <i className={`bi ${expandedHistory === sub.id ? 'bi-chevron-up' : 'bi-chevron-down'}`} />
                            </button>
                          </td>
                        </tr>
                        {expandedHistory === sub.id && (
                          <tr>
                            <td colSpan="8" style={{ background: '#f8fafc' }}>
                              <div className="p-3">
                                <div className="row g-3">
                                  {sub.submitter_remarks && (
                                    <div className="col-md-6">
                                      <div className="text-muted mb-1" style={{ fontSize: '0.75rem' }}>SUBMITTER REMARKS</div>
                                      <div style={{ fontSize: '0.85rem' }}>{sub.submitter_remarks}</div>
                                    </div>
                                  )}
                                  {sub.approver_remarks && (
                                    <div className="col-md-6">
                                      <div className="text-muted mb-1" style={{ fontSize: '0.75rem' }}>APPROVER REMARKS</div>
                                      <div className="text-success fw-semibold" style={{ fontSize: '0.85rem' }}>{sub.approver_remarks}</div>
                                    </div>
                                  )}
                                  {sub.rejection_reason && (
                                    <div className="col-12">
                                      <div className="text-muted mb-1" style={{ fontSize: '0.75rem' }}>REJECTION REASON</div>
                                      <div className="text-danger fw-semibold" style={{ fontSize: '0.85rem' }}>{sub.rejection_reason}</div>
                                    </div>
                                  )}
                                </div>
                              </div>
                            </td>
                          </tr>
                        )}
                      </React.Fragment>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}

      {/* ═══════════════════════════════════════════════════════
          TAB 4: OFFICER I/C MANAGEMENT
      ═══════════════════════════════════════════════════════ */}
      {activeTab === 'officers' && (
        <div>
          <div className="d-flex justify-content-between align-items-center mb-4">
            <div>
              <h5 className="fw-bold mb-1">Officer I/C Appointments</h5>
              <p className="text-muted mb-0" style={{ fontSize: '0.88rem' }}>
                Assign Officers I/C to trades for parade state approval routing
              </p>
            </div>
            {hasPermission('parade:manage_officers') && (
              <button className="btn btn-primary btn-sm" onClick={() => setShowOICModal(true)}>
                <i className="bi bi-person-plus me-1" />Assign New Officer I/C
              </button>
            )}
          </div>

          {officersLoading ? (
            <div className="text-center py-5"><div className="spinner-border text-primary" /></div>
          ) : officers.length === 0 ? (
            <div className="text-center py-5">
              <i className="bi bi-person-badge" style={{ fontSize: '3rem', color: '#94a3b8' }} />
              <div className="text-muted mt-2 fw-semibold">No Officer I/C assignments found</div>
              {hasPermission('parade:manage_officers') && (
                <button className="btn btn-primary btn-sm mt-3" onClick={() => setShowOICModal(true)}>
                  <i className="bi bi-person-plus me-1" />Assign First Officer I/C
                </button>
              )}
            </div>
          ) : (
            <div className="row g-3">
              {officers.map(oic => (
                <div key={oic.id} className="col-md-6 col-lg-4">
                  <div className="card slaf-card h-100" style={{ border: '1px solid #e2e8f0' }}>
                    <div className="card-body p-4">
                      <div className="d-flex justify-content-between align-items-start mb-3">
                        <div
                          className="rounded-circle d-flex align-items-center justify-content-center fw-bold"
                          style={{ width: 48, height: 48, background: '#eff6ff', color: '#2563eb', fontSize: '1.2rem' }}
                        >
                          {(oic.officer_name || 'O').charAt(0).toUpperCase()}
                        </div>
                        <span className="badge" style={{ background: '#f0fdf4', color: '#059669', fontSize: '0.75rem' }}>
                          <i className="bi bi-check-circle me-1" />Active
                        </span>
                      </div>
                      <div className="fw-bold mb-1">{oic.officer_name || '—'}</div>
                      <div className="text-muted mb-1" style={{ fontSize: '0.82rem' }}>
                        {oic.officer_service_number && <><i className="bi bi-tag me-1" />{oic.officer_service_number} · </>}
                        {oic.officer_rank}
                      </div>
                      <div className="mb-3">
                        <span className="badge" style={{ background: '#eff6ff', color: '#2563eb', fontWeight: 700, fontSize: '0.82rem' }}>
                          <i className="bi bi-airplane me-1" />OIC: {oic.trade}
                        </span>
                      </div>
                      <div className="text-muted" style={{ fontSize: '0.75rem' }}>
                        <i className="bi bi-calendar3 me-1" />
                        Appointed: {new Date(oic.appointed_at).toLocaleDateString()}
                        {oic.appointed_by_name && <> by {oic.appointed_by_name}</>}
                      </div>
                      {hasPermission('parade:manage_officers') && (
                        <button
                          className="btn btn-outline-danger btn-sm mt-3 w-100"
                          onClick={() => handleRemoveOIC(oic.id, oic.trade)}
                        >
                          <i className="bi bi-person-dash me-1" />Remove Assignment
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* ── Assign Officer I/C Modal ── */}
          {showOICModal && (
            <div className="modal show d-block" style={{ background: 'rgba(0,0,0,0.5)' }}>
              <div className="modal-dialog">
                <div className="modal-content">
                  <div className="modal-header border-0">
                    <h5 className="modal-title fw-bold">
                      <i className="bi bi-person-plus text-primary me-2" />Assign Officer I/C
                    </h5>
                    <button className="btn-close" onClick={() => setShowOICModal(false)} />
                  </div>
                  <div className="modal-body">
                    <div className="mb-3">
                      <label className="form-label fw-semibold">Trade *</label>
                      <select className="form-select" value={oicTrade} onChange={e => setOicTrade(e.target.value)}>
                        <option value="">— Select Trade —</option>
                        {trades.map(t => <option key={t.id} value={t.label}>{t.label}</option>)}
                      </select>
                    </div>
                    <div className="mb-3">
                      <label className="form-label fw-semibold">Officer / User *</label>
                      <select className="form-select" value={oicUserId} onChange={e => setOicUserId(e.target.value)}>
                        <option value="">— Select User —</option>
                        {allUsers.map(u => (
                          <option key={u.id} value={u.id}>
                            {u.rank ? `${u.rank} ` : ''}{u.full_name} ({u.username})
                          </option>
                        ))}
                      </select>
                    </div>
                    <div className="alert alert-info py-2" style={{ fontSize: '0.82rem' }}>
                      <i className="bi bi-info-circle me-1" />
                      The selected user will receive parade state submissions for this trade and will be responsible for approving or rejecting them.
                    </div>
                  </div>
                  <div className="modal-footer border-0">
                    <button className="btn btn-outline-secondary" onClick={() => setShowOICModal(false)}>Cancel</button>
                    <button
                      className="btn btn-primary"
                      onClick={handleAssignOIC}
                      disabled={savingOIC || !oicTrade || !oicUserId}
                    >
                      {savingOIC ? <span className="spinner-border spinner-border-sm me-1" /> : <i className="bi bi-check-lg me-1" />}
                      Assign Officer I/C
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default DailyParade
