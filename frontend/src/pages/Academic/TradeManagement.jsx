import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { toast } from 'react-toastify'

export const TradeManagement = () => {
  const [trades, setTrades] = useState([])
  const [loading, setLoading] = useState(true)
  const [query, setQuery] = useState('')
  const [showModal, setShowModal] = useState(false)
  const [editingTrade, setEditingTrade] = useState(null)
  
  const [form, setForm] = useState({
    code: '',
    label: '',
    description: '',
    is_active: true
  })

  const fetchTrades = async () => {
    setLoading(true)
    try {
      const res = await axios.get('/api/v1/academic/trades', { params: { include_inactive: true } })
      setTrades(res.data)
    } catch (err) {
      toast.error('Failed to load trades list')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchTrades()
  }, [])

  const handleOpenCreate = () => {
    setEditingTrade(null)
    setForm({ code: '', label: '', description: '', is_active: true })
    setShowModal(true)
  }

  const handleOpenEdit = (t) => {
    setEditingTrade(t)
    setForm({
      code: t.code,
      label: t.label,
      description: t.description || '',
      is_active: t.is_active
    })
    setShowModal(true)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!form.code.trim() || !form.label.trim()) {
      toast.error('Trade Code and Trade Name are required')
      return
    }

    try {
      if (editingTrade) {
        await axios.put(`/api/v1/academic/trades/${editingTrade.id}`, form)
        toast.success(`Trade '${form.label}' updated successfully`)
      } else {
        await axios.post('/api/v1/academic/trades', form)
        toast.success(`Trade '${form.label}' created successfully`)
      }
      setShowModal(false)
      fetchTrades()
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to save trade')
    }
  }

  const filteredTrades = trades.filter(t => 
    t.code.toLowerCase().includes(query.toLowerCase()) ||
    t.label.toLowerCase().includes(query.toLowerCase())
  )

  return (
    <div className="fade-in-slide">
      {/* Header Bar */}
      <div className="d-flex justify-content-between align-items-center mb-3">
        <div>
          <h5 className="fw-bold text-dark mb-0 display-font">Trade Management Master Data</h5>
          <small className="text-muted">Define & maintain SLAF Technical Training Categories</small>
        </div>
        <button className="btn btn-primary btn-sm fw-semibold" onClick={handleOpenCreate}>
          <i className="bi bi-plus-lg me-1"></i> Add New Trade
        </button>
      </div>

      {/* Filter / Search Bar */}
      <div className="card slaf-card p-3 mb-3 shadow-sm">
        <div className="row g-2">
          <div className="col-md-6">
            <div className="input-group input-group-sm">
              <span className="input-group-text bg-light"><i className="bi bi-search text-muted"></i></span>
              <input 
                type="text" 
                className="form-control" 
                placeholder="Search by Trade Code or Name..." 
                value={query}
                onChange={(e) => setQuery(e.target.value)}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Trades Table */}
      <div className="card slaf-card p-0 shadow-sm">
        <div className="table-responsive">
          <table className="table slaf-table align-middle mb-0">
            <thead>
              <tr>
                <th>Trade Code</th>
                <th>Trade Name</th>
                <th>Description</th>
                <th>Courses Offered</th>
                <th>Status</th>
                <th className="text-end">Actions</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr><td colSpan="6" className="text-center py-5"><div className="spinner-border text-primary"></div></td></tr>
              ) : filteredTrades.length === 0 ? (
                <tr><td colSpan="6" className="text-center py-5 text-muted">No trade records found.</td></tr>
              ) : (
                filteredTrades.map(t => (
                  <tr key={t.id}>
                    <td><span className="badge bg-primary-subtle text-primary border fw-bold">{t.code}</span></td>
                    <td><strong className="text-dark">{t.label}</strong></td>
                    <td><small className="text-muted">{t.description || 'N/A'}</small></td>
                    <td><span className="badge bg-secondary-subtle text-dark border">{t.courses_count || 0} Courses</span></td>
                    <td>
                      <span className={`badge bg-${t.is_active ? 'success' : 'danger'}-subtle text-${t.is_active ? 'success' : 'danger'} border px-2 py-0.5`}>
                        {t.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                    <td className="text-end">
                      <button className="btn btn-outline-secondary btn-sm" onClick={() => handleOpenEdit(t)}>
                        <i className="bi bi-pencil me-1"></i> Edit
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Create / Edit Modal */}
      {showModal && (
        <div className="modal fade show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)', zIndex: 1060 }}>
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content slaf-card">
              <div className="modal-header border-bottom">
                <h5 className="modal-title display-font text-primary fw-bold">
                  {editingTrade ? `Edit Trade: ${editingTrade.code}` : 'Create New Technical Trade'}
                </h5>
                <button type="button" className="btn-close" onClick={() => setShowModal(false)}></button>
              </div>
              <form onSubmit={handleSubmit}>
                <div className="modal-body">
                  <div className="mb-3">
                    <label className="form-label fw-semibold small text-muted">Trade Code (Unique)*</label>
                    <input 
                      type="text" 
                      className="form-control" 
                      placeholder="e.g. COMP_TECH, AIRFRAME, AERO_ENGINE" 
                      value={form.code}
                      onChange={(e) => setForm({ ...form, code: e.target.value })}
                      required
                    />
                  </div>
                  <div className="mb-3">
                    <label className="form-label fw-semibold small text-muted">Trade Name (Unique)*</label>
                    <input 
                      type="text" 
                      className="form-control" 
                      placeholder="e.g. Computer Technician, Airframe Fitter" 
                      value={form.label}
                      onChange={(e) => setForm({ ...form, label: e.target.value })}
                      required
                    />
                  </div>
                  <div className="mb-3">
                    <label className="form-label fw-semibold small text-muted">Description</label>
                    <textarea 
                      className="form-control" 
                      rows="3" 
                      placeholder="Brief scope of training trade category..."
                      value={form.description}
                      onChange={(e) => setForm({ ...form, description: e.target.value })}
                    ></textarea>
                  </div>
                  <div className="form-check form-switch">
                    <input 
                      className="form-check-input" 
                      type="checkbox" 
                      id="tradeActive" 
                      checked={form.is_active}
                      onChange={(e) => setForm({ ...form, is_active: e.target.checked })}
                    />
                    <label className="form-check-label fw-semibold small text-dark" htmlFor="tradeActive">Active Status</label>
                  </div>
                </div>
                <div className="modal-footer border-top">
                  <button type="button" className="btn btn-outline-secondary btn-sm" onClick={() => setShowModal(false)}>Cancel</button>
                  <button type="submit" className="btn btn-primary btn-sm fw-semibold">Save Trade</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
