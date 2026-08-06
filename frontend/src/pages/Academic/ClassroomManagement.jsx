import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { toast } from 'react-toastify'

export const ClassroomManagement = () => {
  const [classrooms, setClassrooms] = useState([])
  const [loading, setLoading] = useState(true)
  const [query, setQuery] = useState('')
  const [showModal, setShowModal] = useState(false)
  const [editingClassroom, setEditingClassroom] = useState(null)

  const [form, setForm] = useState({
    code: '',
    name: '',
    block: 'Engineering Block',
    building: 'Building A',
    capacity: 30,
    description: '',
    is_active: true
  })

  const fetchClassrooms = async () => {
    setLoading(true)
    try {
      const res = await axios.get('/api/v1/academic/classrooms', { params: { include_inactive: true } })
      setClassrooms(res.data)
    } catch (err) {
      toast.error('Failed to load classrooms')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchClassrooms()
  }, [])

  const handleOpenCreate = () => {
    setEditingClassroom(null)
    setForm({
      code: '',
      name: '',
      block: 'Engineering Block',
      building: 'Main Complex',
      capacity: 30,
      description: '',
      is_active: true
    })
    setShowModal(true)
  }

  const handleOpenEdit = (c) => {
    setEditingClassroom(c)
    setForm({
      code: c.code,
      name: c.name,
      block: c.block || '',
      building: c.building || '',
      capacity: c.capacity || 30,
      description: c.description || '',
      is_active: c.is_active
    })
    setShowModal(true)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!form.code.trim() || !form.name.trim()) {
      toast.error('Classroom Code and Name are required')
      return
    }

    try {
      if (editingClassroom) {
        await axios.put(`/api/v1/academic/classrooms/${editingClassroom.id}`, form)
        toast.success(`Classroom '${form.name}' updated successfully`)
      } else {
        await axios.post('/api/v1/academic/classrooms', form)
        toast.success(`Classroom '${form.name}' added successfully`)
      }
      setShowModal(false)
      fetchClassrooms()
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to save classroom')
    }
  }

  const filteredClassrooms = classrooms.filter(c => 
    c.code.toLowerCase().includes(query.toLowerCase()) ||
    c.name.toLowerCase().includes(query.toLowerCase()) ||
    (c.block && c.block.toLowerCase().includes(query.toLowerCase()))
  )

  return (
    <div className="fade-in-slide">
      <div className="d-flex justify-content-between align-items-center mb-3">
        <div>
          <h5 className="fw-bold text-dark mb-0 display-font">Classroom Master Management</h5>
          <small className="text-muted">Maintain SLAF TTS lecture halls, technical laboratories, and exam halls</small>
        </div>
        <button className="btn btn-primary btn-sm fw-semibold" onClick={handleOpenCreate}>
          <i className="bi bi-plus-lg me-1"></i> Add Classroom
        </button>
      </div>

      <div className="card slaf-card p-3 mb-3 shadow-sm">
        <div className="row g-2">
          <div className="col-md-6">
            <div className="input-group input-group-sm">
              <span className="input-group-text bg-light"><i className="bi bi-search text-muted"></i></span>
              <input 
                type="text" 
                className="form-control" 
                placeholder="Search Classroom ID, Name or Block..." 
                value={query}
                onChange={(e) => setQuery(e.target.value)}
              />
            </div>
          </div>
        </div>
      </div>

      <div className="card slaf-card p-0 shadow-sm">
        <div className="table-responsive">
          <table className="table slaf-table align-middle mb-0">
            <thead>
              <tr>
                <th>Classroom ID</th>
                <th>Classroom Name</th>
                <th>Block / Building</th>
                <th>Capacity</th>
                <th>Occupancy Status</th>
                <th>Active Status</th>
                <th className="text-end">Actions</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr><td colSpan="7" className="text-center py-5"><div className="spinner-border text-primary"></div></td></tr>
              ) : filteredClassrooms.length === 0 ? (
                <tr><td colSpan="7" className="text-center py-5 text-muted">No classrooms registered.</td></tr>
              ) : (
                filteredClassrooms.map(c => (
                  <tr key={c.id}>
                    <td><span className="badge bg-primary-subtle text-primary border fw-bold">{c.code}</span></td>
                    <td><strong className="text-dark">{c.name}</strong></td>
                    <td>
                      <span className="fw-semibold text-dark d-block" style={{ fontSize: '0.85rem' }}>{c.block || 'Main Block'}</span>
                      <small className="text-muted">{c.building || 'Building A'}</small>
                    </td>
                    <td><span className="badge bg-secondary-subtle text-dark border">{c.capacity} Trainees</span></td>
                    <td>
                      {c.is_occupied ? (
                        <span className="badge bg-warning-subtle text-warning border"><i className="bi bi-person-workspace me-1"></i>Occupied ({c.assigned_batch_name})</span>
                      ) : (
                        <span className="badge bg-success-subtle text-success border"><i className="bi bi-check-circle me-1"></i>Available</span>
                      )}
                    </td>
                    <td>
                      <span className={`badge bg-${c.is_active ? 'success' : 'danger'}-subtle text-${c.is_active ? 'success' : 'danger'} border px-2 py-0.5`}>
                        {c.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                    <td className="text-end">
                      <button className="btn btn-outline-secondary btn-sm" onClick={() => handleOpenEdit(c)}>
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

      {showModal && (
        <div className="modal fade show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)', zIndex: 1060 }}>
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content slaf-card">
              <div className="modal-header border-bottom">
                <h5 className="modal-title display-font text-primary fw-bold">
                  {editingClassroom ? `Edit Classroom: ${editingClassroom.code}` : 'Add New Classroom / Lab'}
                </h5>
                <button type="button" className="btn-close" onClick={() => setShowModal(false)}></button>
              </div>
              <form onSubmit={handleSubmit}>
                <div className="modal-body">
                  <div className="row g-3">
                    <div className="col-md-6">
                      <label className="form-label fw-semibold small text-muted">Classroom ID (Code)*</label>
                      <input 
                        type="text" 
                        className="form-control" 
                        placeholder="e.g. E-01, H-05" 
                        value={form.code}
                        onChange={(e) => setForm({ ...form, code: e.target.value })}
                        required
                      />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label fw-semibold small text-muted">Seating Capacity*</label>
                      <input 
                        type="number" 
                        className="form-control" 
                        value={form.capacity}
                        onChange={(e) => setForm({ ...form, capacity: parseInt(e.target.value) || 0 })}
                        min="1"
                        required
                      />
                    </div>
                    <div className="col-md-12">
                      <label className="form-label fw-semibold small text-muted">Classroom / Lab Name*</label>
                      <input 
                        type="text" 
                        className="form-control" 
                        placeholder="e.g. Electronics Laboratory 01, Lecture Hall E-01" 
                        value={form.name}
                        onChange={(e) => setForm({ ...form, name: e.target.value })}
                        required
                      />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label fw-semibold small text-muted">Block / Wing</label>
                      <input 
                        type="text" 
                        className="form-control" 
                        placeholder="e.g. Engineering Block" 
                        value={form.block}
                        onChange={(e) => setForm({ ...form, block: e.target.value })}
                      />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label fw-semibold small text-muted">Building Name</label>
                      <input 
                        type="text" 
                        className="form-control" 
                        placeholder="e.g. Academic Complex B" 
                        value={form.building}
                        onChange={(e) => setForm({ ...form, building: e.target.value })}
                      />
                    </div>
                    <div className="col-md-12">
                      <div className="form-check form-switch">
                        <input 
                          className="form-check-input" 
                          type="checkbox" 
                          id="clsActive"
                          checked={form.is_active}
                          onChange={(e) => setForm({ ...form, is_active: e.target.checked })}
                        />
                        <label className="form-check-label fw-semibold small text-dark" htmlFor="clsActive">Active Classroom</label>
                      </div>
                    </div>
                  </div>
                </div>
                <div className="modal-footer border-top">
                  <button type="button" className="btn btn-outline-secondary btn-sm" onClick={() => setShowModal(false)}>Cancel</button>
                  <button type="submit" className="btn btn-primary btn-sm fw-semibold">Save Classroom</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
