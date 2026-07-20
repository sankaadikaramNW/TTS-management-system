import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { toast } from 'react-toastify'
import { useAuth } from '../../context/AuthContext'

export const AllocationMap = () => {
  const { hasPermission } = useAuth()
  const [buildings, setBuildings] = useState([])
  const [activeAllocations, setActiveAllocations] = useState([])
  const [students, setStudents] = useState([])
  const [loading, setLoading] = useState(true)

  // Selection state for allocating
  const [selectedBed, setSelectedBed] = useState(null)
  const [targetStudentId, setTargetStudentId] = useState('')

  const loadAccommodationData = async () => {
    setLoading(true)
    try {
      const bRes = await axios.get('/api/v1/accommodation/buildings')
      setBuildings(bRes.data)

      const aRes = await axios.get('/api/v1/accommodation/allocations')
      setActiveAllocations(aRes.data)

      const sRes = await axios.get('/api/v1/students', { params: { limit: 100 } })
      setStudents(sRes.data.items)
    } catch (err) {
      toast.error('Failed to load accommodation register')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadAccommodationData()
  }, [])

  const handleAllocate = async (e) => {
    e.preventDefault()
    if (!targetStudentId || !selectedBed) return
    try {
      await axios.post('/api/v1/accommodation/allocate', {
        student_id: targetStudentId,
        bed_id: selectedBed.id
      })
      toast.success('Bed successfully allocated')
      setSelectedBed(null)
      setTargetStudentId('')
      loadAccommodationData()
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Allocation failed')
    }
  }

  const handleVacate = async (allocId) => {
    if (!window.confirm('Are you sure you want to vacate this trainee allocation?')) return
    try {
      await axios.post(`/api/v1/accommodation/vacate/${allocId}`)
      toast.success('Bed successfully vacated')
      loadAccommodationData()
    } catch (err) {
      toast.error('Failed to vacate bed')
    }
  }

  if (loading) {
    return (
      <div className="text-center py-5">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading housing layout...</span>
        </div>
      </div>
    )
  }

  return (
    <div className="fade-in-slide">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 className="mb-0 text-primary display-font">Accommodation Map</h2>
          <p className="text-muted mb-0">Monitor billets occupancy rates and assign beds to incoming trainees</p>
        </div>
      </div>

      {/* Allocation Drawer/Modal (displayed conditionally) */}
      {selectedBed && (
        <div className="card slaf-card p-4 border-primary mb-4 border-2">
          <div className="d-flex justify-content-between align-items-center mb-3">
            <h5 className="mb-0 fw-bold">Allocate Bed: {selectedBed.bed_number}</h5>
            <button className="btn-close" onClick={() => setSelectedBed(null)}></button>
          </div>
          <form onSubmit={handleAllocate} className="row g-3 align-items-end">
            <div className="col-md-8">
              <label className="form-label fw-semibold">Search Trainee for Placement</label>
              <select 
                className="form-select" 
                value={targetStudentId} 
                onChange={(e) => setTargetStudentId(e.target.value)}
                required
              >
                <option value="">Select Trainee (Service Number - Rank - Name)</option>
                {students
                  .filter(s => s.status === 'Active' && !activeAllocations.some(a => a.student_id === s.id))
                  .map(s => (
                    <option key={s.id} value={s.id}>
                      {s.service_number} - {s.rank} {s.initials} ({s.full_name})
                    </option>
                  ))
                }
              </select>
              <small className="text-muted">Only active trainees without existing housing allocations are listed.</small>
            </div>
            <div className="col-md-4">
              <button type="submit" className="btn btn-primary w-100 py-2 fw-semibold">
                Confirm Placement
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Buildings Visual Layout */}
      <div className="row g-4">
        <div className="col-lg-8 col-md-12">
          <div className="d-flex flex-column gap-4">
            {buildings.map(building => (
              <div key={building.id} className="card slaf-card p-4">
                <div className="d-flex justify-content-between align-items-center border-bottom pb-2 mb-3">
                  <h4 className="mb-0 text-primary display-font">{building.name}</h4>
                  <span className="badge bg-secondary">{building.type} Block</span>
                </div>
                
                {building.billets.map(billet => (
                  <div key={billet.id} className="mb-4 bg-light-subtle p-3 rounded border border-light">
                    <h5 className="display-font text-muted mb-3">{billet.name}</h5>
                    
                    {billet.rooms.map(room => (
                      <div key={room.id} className="mb-3 border p-3 rounded bg-card bg-white">
                        <h6 className="fw-semibold text-secondary mb-3">{room.room_number} (Capacity: {room.capacity})</h6>
                        
                        <div className="d-flex flex-wrap gap-3">
                          {room.beds.map(bed => {
                            const activeAlloc = activeAllocations.find(a => a.bed_id === bed.id)
                            return (
                              <div 
                                key={bed.id} 
                                className={`bed-grid-item ${bed.status.toLowerCase()}`}
                                onClick={() => {
                                  if (bed.status === 'Vacant' && hasPermission('room:write')) {
                                    setSelectedBed(bed)
                                  }
                                }}
                              >
                                <i className="bi bi-door-closed" style={{ fontSize: '1.2rem' }}></i>
                                <span>{bed.bed_number}</span>
                              </div>
                            )
                          })}
                        </div>
                      </div>
                    ))}
                  </div>
                ))}
              </div>
            ))}
          </div>
        </div>

        {/* Allocations sidebar table */}
        <div className="col-lg-4 col-md-12">
          <div className="card slaf-card p-4">
            <h5 className="mb-3 display-font border-bottom pb-2">Active Housing Registers</h5>
            <div className="d-flex flex-column gap-3" style={{ maxHeight: '600px', overflowY: 'auto' }}>
              {activeAllocations.length === 0 ? (
                <div className="text-center py-4 text-muted">No trainees currently allocated to beds.</div>
              ) : (
                activeAllocations.map(alloc => (
                  <div key={alloc.id} className="border rounded p-3 bg-light fade-in-slide">
                    <div className="d-flex justify-content-between align-items-start">
                      <div>
                        <strong className="text-primary d-block">{alloc.student_service_number}</strong>
                        <span className="fw-semibold" style={{ fontSize: '0.85rem' }}>{alloc.student_name}</span>
                        <div className="text-muted mt-1" style={{ fontSize: '0.75rem' }}>
                          Bldg: {alloc.building_name} | {alloc.billet_name} | {alloc.room_number} | Bed: {alloc.bed_number}
                        </div>
                      </div>
                      {hasPermission('room:write') && (
                        <button className="btn btn-outline-danger btn-sm px-2" onClick={() => handleVacate(alloc.id)} title="Vacate Bed">
                          <i className="bi bi-x-square"></i>
                        </button>
                      )}
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
export default AllocationMap
