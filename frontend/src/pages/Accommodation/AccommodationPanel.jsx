import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import axios from 'axios'
import { toast } from 'react-toastify'
import { useAuth } from '../../context/AuthContext'
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
  Title
} from 'chart.js'
import { Pie } from 'react-chartjs-2'

// Register Chart.js models
ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title)

export const AccommodationPanel = () => {
  const { hasPermission } = useAuth()
  const { subview } = useParams()
  const navigate = useNavigate()

  // Master states
  const [buildings, setBuildings] = useState([])
  const [activeAllocations, setActiveAllocations] = useState([])
  const [students, setStudents] = useState([])
  const [loading, setLoading] = useState(true)

  // Dashboard states
  const [dashboardStats, setDashboardStats] = useState(null)
  const [recentActivities, setRecentActivities] = useState([])
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResult, setSearchResult] = useState(null)

  // Report states
  const [reportType, setReportType] = useState('active')
  const [reportData, setReportData] = useState([])
  const [reportSearch, setReportSearch] = useState('')

  // Map Interactive States
  const [selectedBed, setSelectedBed] = useState(null)
  const [selectedAllocation, setSelectedAllocation] = useState(null)
  const [showAllocateModal, setShowAllocateModal] = useState(false)
  const [showDetailModal, setShowDetailModal] = useState(false)
  const [showTransferModal, setShowTransferModal] = useState(false)
  const [showVacateModal, setShowVacateModal] = useState(false)
  
  // Forms states
  const [targetStudentId, setTargetStudentId] = useState('')
  const [allocationRemarks, setAllocationRemarks] = useState('')
  const [transferRemarks, setTransferRemarks] = useState('')
  const [transferTargetBedId, setTransferTargetBedId] = useState('')
  const [vacateReason, setVacateReason] = useState('Course Completed')
  const [vacateRemarks, setVacateRemarks] = useState('')

  // Master Data CRUD Form Modals
  const [showBldgFormModal, setShowBldgFormModal] = useState(false)
  const [showBilletFormModal, setShowBilletFormModal] = useState(false)
  const [showBedFormModal, setShowBedFormModal] = useState(false)
  const [editingItem, setEditingItem] = useState(null)

  // CRUD Form states
  const [bldgForm, setBldgForm] = useState({ name: '', type: 'Airmen', capacity: 30 })
  const [billetForm, setBilletForm] = useState({ building_id: '', name: '', capacity: 10 })
  const [bedForm, setBedForm] = useState({ billet_id: '', bed_number: '', status: 'Vacant' })

  // Filters for CRUD dropdowns
  const [selectedBldgFilter, setSelectedBldgFilter] = useState('')
  const [selectedBilletFilter, setSelectedBilletFilter] = useState('')

  // Fetch functions
  const loadData = async () => {
    setLoading(true)
    try {
      const bRes = await axios.get('/api/v1/accommodation/buildings')
      setBuildings(bRes.data)

      const aRes = await axios.get('/api/v1/accommodation/allocations')
      setActiveAllocations(aRes.data)

      const sRes = await axios.get('/api/v1/students', { params: { limit: 200 } })
      setStudents(sRes.data.items)

      const dRes = await axios.get('/api/v1/accommodation/dashboard')
      setDashboardStats(dRes.data)
      
      // Fetch recent accommodation-related logs
      const lRes = await axios.get('/api/v1/dashboard/summary')
      if (lRes.data.recent_activities) {
        const filtered = lRes.data.recent_activities.filter(log => 
          log.action.includes('BED') || log.action.includes('ACCOMMODATION') || log.action.includes('ROOM')
        )
        setRecentActivities(filtered.slice(0, 5))
      }
    } catch (err) {
      toast.error('Failed to load accommodation system data')
    } finally {
      setLoading(false)
    }
  }

  const loadDashboard = async () => {
    try {
      const dRes = await axios.get('/api/v1/accommodation/dashboard')
      setDashboardStats(dRes.data)
      
      const lRes = await axios.get('/api/v1/dashboard/summary')
      if (lRes.data.recent_activities) {
        const filtered = lRes.data.recent_activities.filter(log => 
          log.action.includes('BED') || log.action.includes('ACCOMMODATION') || log.action.includes('ROOM')
        )
        setRecentActivities(filtered.slice(0, 5))
      }
    } catch (err) {
      console.error(err)
    }
  }

  const loadReport = async () => {
    try {
      const rRes = await axios.get('/api/v1/accommodation/reports', { params: { report_type: reportType } })
      setReportData(rRes.data)
    } catch (err) {
      toast.error('Failed to load report data')
    }
  }

  useEffect(() => {
    loadData()
  }, [])

  useEffect(() => {
    if (subview === 'reports') {
      loadReport()
    } else if (!subview || subview === 'dashboard') {
      loadDashboard()
    }
  }, [subview, reportType])

  // Placement handlers
  const handleAllocateSubmit = async (e) => {
    e.preventDefault()
    if (!targetStudentId || !selectedBed) return
    try {
      await axios.post('/api/v1/accommodation/allocate', {
        student_id: targetStudentId,
        bed_id: selectedBed.id,
        remarks: allocationRemarks
      })
      toast.success('Bed successfully allocated')
      setShowAllocateModal(false)
      setSelectedBed(null)
      setTargetStudentId('')
      setAllocationRemarks('')
      setSearchResult(null)
      setSearchQuery('')
      loadData()
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Allocation failed')
    }
  }

  const handleTransferSubmit = async (e) => {
    e.preventDefault()
    if (!selectedAllocation || !transferTargetBedId) return
    try {
      await axios.post('/api/v1/accommodation/transfer', {
        student_id: selectedAllocation.student_id,
        new_bed_id: transferTargetBedId,
        remarks: transferRemarks
      })
      toast.success('Trainee bed transfer completed successfully')
      setShowTransferModal(false)
      setShowDetailModal(false)
      setSelectedAllocation(null)
      setTransferTargetBedId('')
      setTransferRemarks('')
      setSearchResult(null)
      setSearchQuery('')
      loadData()
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Bed transfer failed')
    }
  }

  const handleVacateSubmit = async (e) => {
    e.preventDefault()
    if (!selectedAllocation) return
    try {
      await axios.post(`/api/v1/accommodation/vacate/${selectedAllocation.id}`, {
        vacate_reason: vacateReason,
        remarks: vacateRemarks
      })
      toast.success('Trainee vacated successfully')
      setShowVacateModal(false)
      setShowDetailModal(false)
      setSelectedAllocation(null)
      setVacateReason('Course Completed')
      setVacateRemarks('')
      setSearchResult(null)
      setSearchQuery('')
      loadData()
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to vacate bed')
    }
  }

  // CRUD handlers
  const handleSaveBuilding = async (e) => {
    e.preventDefault()
    try {
      if (editingItem) {
        await axios.put(`/api/v1/accommodation/buildings/${editingItem.id}`, bldgForm)
        toast.success('Building updated successfully')
      } else {
        await axios.post('/api/v1/accommodation/buildings', bldgForm)
        toast.success('Building added successfully')
      }
      setShowBldgFormModal(false)
      setEditingItem(null)
      setBldgForm({ name: '', type: 'Airmen', capacity: 30 })
      loadData()
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to save building')
    }
  }

  const handleSaveBillet = async (e) => {
    e.preventDefault()
    try {
      if (editingItem) {
        await axios.put(`/api/v1/accommodation/billets/${editingItem.id}`, {
          name: billetForm.name,
          capacity: billetForm.capacity
        })
        toast.success('Billet updated successfully')
      } else {
        await axios.post('/api/v1/accommodation/billets', billetForm)
        toast.success('Billet added successfully')
      }
      setShowBilletFormModal(false)
      setEditingItem(null)
      setBilletForm({ building_id: '', name: '', capacity: 10 })
      loadData()
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to save billet')
    }
  }

  const handleSaveBed = async (e) => {
    e.preventDefault()
    try {
      if (editingItem) {
        await axios.put(`/api/v1/accommodation/beds/${editingItem.id}`, {
          bed_number: bedForm.bed_number,
          status: bedForm.status
        })
        toast.success('Bed status updated successfully')
      } else {
        await axios.post('/api/v1/accommodation/beds', bedForm)
        toast.success('Bed created successfully')
      }
      setShowBedFormModal(false)
      setEditingItem(null)
      setBedForm({ billet_id: '', bed_number: '', status: 'Vacant' })
      loadData()
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to save bed')
    }
  }

  const handleDeleteBuilding = async (bldgId) => {
    if (!window.confirm('Are you sure you want to delete this building? It will soft-delete the master record.')) return
    try {
      await axios.delete(`/api/v1/accommodation/buildings/${bldgId}`)
      toast.success('Building deleted')
      loadData()
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Delete building failed')
    }
  }

  // Trainee search inside panel
  const handleStudentSearch = (e) => {
    const query = e.target.value
    setSearchQuery(query)
    if (!query) {
      setSearchResult(null)
      return
    }

    const foundAlloc = activeAllocations.find(a => 
      a.student_service_number.toLowerCase().includes(query.toLowerCase()) ||
      a.student_name.toLowerCase().includes(query.toLowerCase())
    )

    if (foundAlloc) {
      setSearchResult({ ...foundAlloc, allocated: true })
    } else {
      const foundStudent = students.find(s => 
        s.service_number.toLowerCase().includes(query.toLowerCase()) ||
        s.full_name.toLowerCase().includes(query.toLowerCase())
      )
      if (foundStudent) {
        setSearchResult({ ...foundStudent, allocated: false })
      } else {
        setSearchResult('not_found')
      }
    }
  }

  // Helpers
  const getBedStatusBadge = (status) => {
    switch (status) {
      case 'Vacant': return 'bg-success text-white'
      case 'Occupied': return 'bg-danger text-white'
      case 'Maintenance': return 'bg-warning text-dark'
      case 'Reserved': return 'bg-info text-white'
      default: return 'bg-secondary'
    }
  }

  const exportReportToCSV = () => {
    let headers = []
    let rows = []
    
    if (reportType === 'active') {
      headers = ['Service No', 'Rank', 'Initials', 'Full Name', 'Building', 'Billet', 'Bed', 'Allocated At']
      rows = reportData.map(a => [
        a.student_service_number, a.student_rank, a.student_name, a.student_batch, 
        a.building_name, a.billet_name, a.bed_number, new Date(a.allocated_at).toLocaleDateString()
      ])
    } else if (reportType === 'history') {
      headers = ['Service No', 'Rank', 'Initials', 'Building', 'Billet', 'Bed', 'Allocated At', 'Vacated At', 'Reason', 'Remarks']
      rows = reportData.map(a => [
        a.student_service_number, a.student_rank, a.student_name, 
        a.building_name, a.billet_name, a.bed_number, 
        new Date(a.allocated_at).toLocaleDateString(), 
        a.vacated_at ? new Date(a.vacated_at).toLocaleDateString() : 'N/A', 
        a.vacate_reason || 'N/A', a.remarks || 'None'
      ])
    } else {
      headers = ['Building', 'Billet', 'Total Capacity', 'Occupied Beds', 'Vacant Beds', 'Occupancy Rate (%)']
      rows = reportData.map(b => [
        b.building_name, b.billet_name, b.capacity, b.occupied, b.vacant, `${b.occupancy_rate}%`
      ])
    }

    const csvContent = "data:text/csv;charset=utf-8," 
      + [headers.join(','), ...rows.map(e => e.map(val => `"${val}"`).join(","))].join("\n")
    
    const encodedUri = encodeURI(csvContent)
    const link = document.createElement("a")
    link.setAttribute("href", encodedUri)
    link.setAttribute("download", `SLAF_TTS_Accommodation_${reportType}_Report.csv`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  if (loading && !dashboardStats) {
    return (
      <div className="text-center py-5">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading housing portal...</span>
        </div>
      </div>
    )
  }

  // Filter report lists
  const filteredReports = reportData.filter(item => {
    const term = reportSearch.toLowerCase()
    if (!term) return true
    if (reportType === 'billet_occupancy') {
      return item.building_name.toLowerCase().includes(term) || item.billet_name.toLowerCase().includes(term)
    }
    return (
      (item.student_service_number?.toLowerCase().includes(term)) ||
      (item.student_name?.toLowerCase().includes(term)) ||
      (item.billet_name?.toLowerCase().includes(term))
    )
  })

  // Get list of vacant beds for transfer dropdown
  const vacantBedsList = []
  buildings.forEach(bldg => {
    bldg.billets.forEach(billet => {
      billet.beds.forEach(bed => {
        if (bed.status === 'Vacant') {
          vacantBedsList.push({
            id: bed.id,
            label: `${bldg.name} - ${billet.name} - Bed ${bed.bed_number}`
          })
        }
      })
    })
  })

  // ChartJS Pie Data
  const pieData = dashboardStats ? {
    labels: ['Occupied', 'Available', 'Maintenance', 'Reserved'],
    datasets: [
      {
        data: [
          dashboardStats.occupied_beds,
          dashboardStats.vacant_beds,
          dashboardStats.maintenance_beds,
          dashboardStats.reserved_beds
        ],
        backgroundColor: ['#ef4444', '#10b981', '#f59e0b', '#3b82f6'],
        borderWidth: 1,
      }
    ]
  } : null

  return (
    <div className="fade-in-slide d-flex flex-column min-vh-100 justify-content-between">
      <div>
        {/* Breadcrumbs */}
        <nav aria-label="breadcrumb" className="mb-3 d-print-none">
          <ol className="breadcrumb small">
            <li className="breadcrumb-item"><a href="/dashboard">Portal Gateway</a></li>
            <li className="breadcrumb-item active" aria-current="page">Accommodation Module</li>
          </ol>
        </nav>

        {/* ============================================================== */}
        {/* VIEW 1: DEDICATED MODULE HOME PAGE (DASHBOARD)                 */}
        {/* ============================================================== */}
        {(!subview || subview === 'dashboard') && dashboardStats && (
          <div className="fade-in-slide">
            {/* KPI Cards Row */}
            <div className="row g-3 mb-4">
              <div className="col-md-3 col-sm-6">
                <div className="card slaf-card kpi-card p-3 bg-white pointer" onClick={() => navigate('/accommodation/buildings')}>
                  <span className="text-muted small fw-semibold text-uppercase">Total Buildings</span>
                  <h2 className="mb-0 fw-bold text-primary mt-1">{dashboardStats.total_buildings}</h2>
                  <span className="text-muted mt-1" style={{ fontSize: '0.7rem' }}>Configured structures</span>
                </div>
              </div>
              <div className="col-md-3 col-sm-6">
                <div className="card slaf-card kpi-card p-3 bg-white pointer" onClick={() => navigate('/accommodation/billets')}>
                  <span className="text-muted small fw-semibold text-uppercase">Total Billets</span>
                  <h2 className="mb-0 fw-bold text-secondary mt-1">{dashboardStats.total_billets}</h2>
                  <span className="text-muted mt-1" style={{ fontSize: '0.7rem' }}>Dormitory halls</span>
                </div>
              </div>
              <div className="col-md-3 col-sm-6">
                <div className="card slaf-card kpi-card p-3 bg-white pointer" onClick={() => navigate('/accommodation/beds')}>
                  <span className="text-muted small fw-semibold text-uppercase">Total Bed Capacity</span>
                  <h2 className="mb-0 fw-bold text-dark mt-1">{dashboardStats.total_beds}</h2>
                  <span className="text-muted mt-1" style={{ fontSize: '0.7rem' }}>Total spacing resources</span>
                </div>
              </div>
              <div className="col-md-3 col-sm-6">
                <div className="card slaf-card kpi-card success p-3 bg-white pointer" onClick={() => navigate('/accommodation/map')}>
                  <span className="text-muted small fw-semibold text-uppercase">Occupied / Available</span>
                  <h2 className="mb-0 fw-bold mt-1 text-success">
                    {dashboardStats.occupied_beds} / {dashboardStats.vacant_beds}
                  </h2>
                  <span className="text-muted mt-1" style={{ fontSize: '0.7rem' }}>{dashboardStats.occupancy_percentage}% occupancy rate</span>
                </div>
              </div>
            </div>

            {/* Quick Actions Panel */}
            <div className="card slaf-card p-4 bg-white mb-4">
              <h5 className="display-font fw-bold border-bottom pb-2 mb-3"><i className="bi bi-lightning-charge text-warning me-2"></i>Quick Actions Console</h5>
              <div className="d-flex flex-wrap gap-3">
                <button className="btn btn-outline-primary px-4 py-2.5 rounded-3 fw-semibold d-inline-flex align-items-center gap-2" onClick={() => { setSelectedBed(vacantBedsList[0] ? { id: vacantBedsList[0].id, bed_number: vacantBedsList[0].label } : null); setShowAllocateModal(true); }}>
                  <i className="bi bi-person-plus"></i> Allocate Bed
                </button>
                <button className="btn btn-outline-info px-4 py-2.5 rounded-3 fw-semibold text-dark d-inline-flex align-items-center gap-2" onClick={() => { if (activeAllocations[0]) { setSelectedAllocation(activeAllocations[0]); setShowTransferModal(true); } else { toast.info('No active allocations available to transfer'); } }}>
                  <i className="bi bi-arrow-left-right"></i> Transfer Bed
                </button>
                <button className="btn btn-outline-danger px-4 py-2.5 rounded-3 fw-semibold d-inline-flex align-items-center gap-2" onClick={() => { if (activeAllocations[0]) { setSelectedAllocation(activeAllocations[0]); setShowVacateModal(true); } else { toast.info('No active allocations available to vacate'); } }}>
                  <i className="bi bi-x-circle"></i> Vacate Bed
                </button>
                <button className="btn btn-outline-secondary px-4 py-2.5 rounded-3 fw-semibold d-inline-flex align-items-center gap-2" onClick={() => navigate('/accommodation/map')}>
                  <i className="bi bi-map"></i> View Occupancy Map
                </button>
                <button className="btn btn-outline-success px-4 py-2.5 rounded-3 fw-semibold d-inline-flex align-items-center gap-2" onClick={() => navigate('/accommodation/reports')}>
                  <i className="bi bi-file-earmark-spreadsheet"></i> Generate Report
                </button>
              </div>
            </div>

            {/* Graphs & Alerts & Search */}
            <div className="row g-4 mb-4">
              {/* Left Column: Student Search & Alerts */}
              <div className="col-md-7">
                {/* Dynamic Trainee Search Panel */}
                <div className="card slaf-card p-4 bg-white mb-4">
                  <h5 className="display-font fw-bold border-bottom pb-2 mb-3"><i className="bi bi-search text-primary me-2"></i>Trainee Housing Placement Search</h5>
                  <div className="input-group mb-3">
                    <span className="input-group-text"><i className="bi bi-search"></i></span>
                    <input 
                      type="text" 
                      className="form-control" 
                      placeholder="Input Trainee Service Number or Initials (e.g. SLAF/12345)..."
                      value={searchQuery}
                      onChange={handleStudentSearch}
                    />
                  </div>

                  {searchResult && (
                    <div className="p-3 border rounded bg-light">
                      {searchResult === 'not_found' ? (
                        <div className="text-danger small fw-semibold"><i className="bi bi-exclamation-triangle me-1"></i>No student records found in SSOT master directory.</div>
                      ) : searchResult.allocated ? (
                        <div>
                          <strong className="text-success d-block mb-1"><i className="bi bi-check-circle-fill me-1"></i>Active Housing Placement Found:</strong>
                          <span className="fw-bold">{searchResult.student_rank} {searchResult.student_name}</span> ({searchResult.student_service_number})
                          <div className="text-muted mt-2" style={{ fontSize: '0.85rem' }}>
                            <strong>Location: </strong> {searchResult.building_name} | {searchResult.billet_name} | Bed {searchResult.bed_number}
                          </div>
                          <div className="text-muted small mt-1">Allocated at: {new Date(searchResult.allocated_at).toLocaleDateString()}</div>
                          
                          <div className="mt-3">
                            <button className="btn btn-outline-primary btn-sm me-2" onClick={() => { setSelectedAllocation(searchResult); setShowTransferModal(true); }}>Transfer Bed</button>
                            <button className="btn btn-danger btn-sm" onClick={() => { setSelectedAllocation(searchResult); setShowVacateModal(true); }}>Vacate</button>
                          </div>
                        </div>
                      ) : (
                        <div>
                          <strong className="text-warning d-block mb-1"><i className="bi bi-info-circle-fill me-1"></i>Active Record Found, but has NO housing allocation:</strong>
                          <span className="fw-bold">{searchResult.rank} {searchResult.initials} {searchResult.full_name}</span> ({searchResult.service_number})
                          <div className="text-muted small mt-1">Status: {searchResult.status} | Trade: {searchResult.trade} | Batch: {searchResult.batch}</div>
                          
                          <button className="btn btn-primary btn-sm mt-3" onClick={() => { setSelectedBed(vacantBedsList[0] ? { id: vacantBedsList[0].id, bed_number: vacantBedsList[0].label } : null); setTargetStudentId(searchResult.id); setShowAllocateModal(true); }}>
                            Allocate Bed Now
                          </button>
                        </div>
                      )}
                    </div>
                  )}
                </div>

                {/* Alerts & Notifications */}
                <div className="card slaf-card p-4 bg-white">
                  <h5 className="display-font fw-bold border-bottom pb-2 mb-3"><i className="bi bi-bell text-danger me-2"></i>Module Alerts & Flags</h5>
                  <div className="d-flex flex-column gap-2.5">
                    {dashboardStats.occupancy_percentage > 90 && (
                      <div className="alert alert-danger py-2 px-3 small d-flex align-items-center gap-2 mb-0">
                        <i className="bi bi-exclamation-triangle-fill"></i>
                        <span><strong>Critical Capacity Warning: </strong> Total portal housing capacity is above 90%!</span>
                      </div>
                    )}
                    {dashboardStats.maintenance_beds > 0 && (
                      <div className="alert alert-warning py-2 px-3 small d-flex align-items-center gap-2 mb-0">
                        <i className="bi bi-tools"></i>
                        <span><strong>Maintenance Alert: </strong> {dashboardStats.maintenance_beds} beds are marked under maintenance and cannot be allocated.</span>
                      </div>
                    )}
                    {dashboardStats.vacant_beds < 5 && (
                      <div className="alert alert-info py-2 px-3 small d-flex align-items-center gap-2 mb-0">
                        <i className="bi bi-info-circle-fill"></i>
                        <span><strong>Notice: </strong> Low vacant space. Only {dashboardStats.vacant_beds} beds are currently available.</span>
                      </div>
                    )}
                    {dashboardStats.maintenance_beds === 0 && dashboardStats.vacant_beds >= 5 && (
                      <div className="text-center py-4 text-muted small"><i className="bi bi-shield-check text-success me-1"></i>All building resources operating normally. No alerts.</div>
                    )}
                  </div>
                </div>
              </div>

              {/* Right Column: Charts & Recent Activities */}
              <div className="col-md-5">
                {/* Pie Chart breakdown */}
                <div className="card slaf-card p-4 bg-white mb-4">
                  <h5 className="display-font fw-bold border-bottom pb-2 mb-3"><i className="bi bi-pie-chart text-secondary me-2"></i>Status Distribution</h5>
                  <div className="mx-auto" style={{ maxWidth: '240px' }}>
                    {pieData && <Pie data={pieData} />}
                  </div>
                </div>

                {/* Recent Activities */}
                <div className="card slaf-card p-4 bg-white">
                  <h5 className="display-font fw-bold border-bottom pb-2 mb-3"><i className="bi bi-clock-history text-secondary me-2"></i>Recent Module logs</h5>
                  <div className="d-flex flex-column gap-3">
                    {recentActivities.length === 0 ? (
                      <div className="text-center py-4 text-muted small">No housing logs recorded today.</div>
                    ) : (
                      recentActivities.map((log) => (
                        <div key={log.id} className="d-flex align-items-start gap-2 pb-2 border-bottom border-light">
                          <i className="bi bi-journal-text text-primary mt-0.5"></i>
                          <div>
                            <div className="small fw-semibold">{log.action}</div>
                            <div className="text-muted" style={{ fontSize: '0.75rem' }}>Performed by {log.username}</div>
                            <div className="text-muted" style={{ fontSize: '0.7rem' }}>{new Date(log.created_at).toLocaleString()}</div>
                          </div>
                        </div>
                      ))
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ============================================================== */}
        {/* VIEW 2: PLACEMENT GRID MAP                                     */}
        {/* ============================================================== */}
        {subview === 'map' && (
          <div className="row g-4 fade-in-slide">
            <div className="col-lg-8">
              <div className="d-flex flex-column gap-4">
                {buildings.map(building => (
                  <div key={building.id} className="card slaf-card p-4 bg-white shadow-sm">
                    <div className="d-flex justify-content-between align-items-center border-bottom pb-2 mb-3">
                      <div>
                        <h4 className="mb-0 text-primary display-font fw-bold">{building.name}</h4>
                        <small className="text-muted">Type: {building.type} Block</small>
                      </div>
                      <span className="badge bg-primary px-3 py-2" style={{ borderRadius: '6px' }}>
                        {building.billets.reduce((acc, curr) => acc + curr.current_occupancy, 0)} / {building.capacity} Beds
                      </span>
                    </div>

                    {building.billets.map(billet => (
                      <div key={billet.id} className="mb-4 bg-light-subtle p-3 rounded border border-light">
                        <div className="d-flex justify-content-between align-items-center mb-3">
                          <h5 className="display-font fw-semibold text-secondary mb-0">{billet.name}</h5>
                          <span className="small text-muted">Billet Occupancy: {billet.current_occupancy} / {billet.capacity}</span>
                        </div>

                        <div className="d-flex flex-wrap gap-3">
                          {billet.beds.map(bed => {
                            const activeAlloc = activeAllocations.find(a => a.bed_id === bed.id)
                            return (
                              <div 
                                key={bed.id} 
                                className={`bed-grid-item ${bed.status.toLowerCase()} pointer`}
                                onClick={() => {
                                  if (bed.status === 'Vacant') {
                                    if (hasPermission('room:write')) {
                                      setSelectedBed(bed)
                                      setShowAllocateModal(true)
                                    } else {
                                      toast.warning('Unauthorized: Permission room:write is required.')
                                    }
                                  } else if (bed.status === 'Occupied' && activeAlloc) {
                                    setSelectedAllocation(activeAlloc)
                                    setShowDetailModal(true)
                                  } else {
                                    toast.info(`Bed is marked as ${bed.status}`)
                                  }
                                }}
                              >
                                <i className="bi bi-door-closed" style={{ fontSize: '1.25rem' }}></i>
                                <span style={{ fontSize: '0.85rem' }}>Bed {bed.bed_number}</span>
                                {activeAlloc && (
                                  <small className="d-block text-truncate w-100 mt-1" style={{ fontSize: '0.7rem', fontWeight: 'bold' }}>
                                    {activeAlloc.student_service_number}
                                  </small>
                                )}
                              </div>
                            )
                          })}
                        </div>
                      </div>
                    ))}
                  </div>
                ))}
              </div>
            </div>

            <div className="col-lg-4">
              <div className="card slaf-card p-4 bg-white sticky-top" style={{ top: '90px' }}>
                <h5 className="mb-3 display-font fw-bold border-bottom pb-2">Active Housing Registers</h5>
                <div className="d-flex flex-column gap-3" style={{ maxHeight: '620px', overflowY: 'auto' }}>
                  {activeAllocations.length === 0 ? (
                    <div className="text-center py-5 text-muted">No trainees currently allocated to beds.</div>
                  ) : (
                    activeAllocations.map(alloc => (
                      <div 
                        key={alloc.id} 
                        className="border rounded p-3 bg-light hover-shadow pointer transition"
                        onClick={() => {
                          setSelectedAllocation(alloc)
                          setShowDetailModal(true)
                        }}
                      >
                        <div className="d-flex justify-content-between align-items-start">
                          <div>
                            <strong className="text-primary d-block">{alloc.student_service_number}</strong>
                            <span className="fw-semibold text-dark d-block" style={{ fontSize: '0.85rem' }}>
                              {alloc.student_rank} {alloc.student_name}
                            </span>
                            <div className="text-muted mt-1" style={{ fontSize: '0.75rem' }}>
                              {alloc.building_name} | {alloc.billet_name} | Bed: {alloc.bed_number}
                            </div>
                          </div>
                          <span className="badge bg-danger rounded-pill px-2" style={{ fontSize: '0.65rem' }}>Active</span>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ============================================================== */}
        {/* VIEW 3: MASTER CONFIGURATION                                   */}
        {/* ============================================================== */}
        {subview === 'buildings' && (
          <div className="fade-in-slide bg-white card slaf-card p-4">
            <div className="d-flex justify-content-between align-items-center mb-3">
              <h5 className="fw-bold mb-0">Buildings Configuration Master</h5>
              {hasPermission('room:write') && (
                <button className="btn btn-primary btn-sm d-flex align-items-center gap-1" onClick={() => { setEditingItem(null); setBldgForm({ name: '', type: 'Airmen', capacity: 30 }); setShowBldgFormModal(true); }}>
                  <i className="bi bi-plus-lg"></i> Add Building
                </button>
              )}
            </div>
            <div className="table-responsive">
              <table className="table table-hover align-middle border">
                <thead className="table-light">
                  <tr>
                    <th>Building Name</th>
                    <th>Type Block</th>
                    <th>Max Billet Capacity</th>
                    <th>Current Occupancy</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {buildings.map(b => (
                    <tr key={b.id}>
                      <td><strong>{b.name}</strong></td>
                      <td><span className="badge bg-secondary">{b.type}</span></td>
                      <td>{b.capacity} beds</td>
                      <td>{b.billets.reduce((acc, curr) => acc + curr.current_occupancy, 0)} beds occupied</td>
                      <td>
                        <div className="d-flex gap-2">
                          <button className="btn btn-outline-secondary btn-sm" onClick={() => { setEditingItem(b); setBldgForm({ name: b.name, type: b.type, capacity: b.capacity }); setShowBldgFormModal(true); }}>
                            <i className="bi bi-pencil"></i> Edit
                          </button>
                          <button className="btn btn-outline-danger btn-sm" onClick={() => handleDeleteBuilding(b.id)}>
                            <i className="bi bi-trash"></i> Delete
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {subview === 'billets' && (
          <div className="fade-in-slide bg-white card slaf-card p-4">
            <div className="row g-3 mb-3 align-items-center">
              <div className="col-md-6">
                <label className="form-label fw-semibold">Filter by Building</label>
                <select className="form-select" value={selectedBldgFilter} onChange={(e) => setSelectedBldgFilter(e.target.value)}>
                  <option value="">Select Building to view billets</option>
                  {buildings.map(b => (
                    <option key={b.id} value={b.id}>{b.name}</option>
                  ))}
                </select>
              </div>
              <div className="col-md-6 text-end pt-4">
                {hasPermission('room:write') && selectedBldgFilter && (
                  <button className="btn btn-primary btn-sm d-flex align-items-center gap-1 ms-auto" onClick={() => { setEditingItem(null); setBilletForm({ building_id: selectedBldgFilter, name: '', capacity: 10 }); setShowBilletFormModal(true); }}>
                    <i className="bi bi-plus-lg"></i> Add Billet
                  </button>
                )}
              </div>
            </div>

            {!selectedBldgFilter ? (
              <div className="text-center py-5 text-muted border rounded">Please select a building to view its billets configuration.</div>
            ) : (
              <div className="table-responsive">
                <table className="table table-hover align-middle border">
                  <thead className="table-light">
                    <tr>
                      <th>Billet Name</th>
                      <th>Max Capacity</th>
                      <th>Occupied Beds</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {buildings.find(b => b.id === selectedBldgFilter)?.billets.map(b => (
                      <tr key={b.id}>
                        <td><strong>{b.name}</strong></td>
                        <td>{b.capacity} beds</td>
                        <td>{b.current_occupancy} occupied</td>
                        <td>
                          <button className="btn btn-outline-secondary btn-sm" onClick={() => { setEditingItem(b); setBilletForm({ building_id: selectedBldgFilter, name: b.name, capacity: b.capacity }); setShowBilletFormModal(true); }}>
                            <i className="bi bi-pencil"></i> Edit Capacity
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}

        {subview === 'beds' && (
          <div className="fade-in-slide bg-white card slaf-card p-4">
            <div className="row g-3 mb-3 align-items-end">
              <div className="col-md-4">
                <label className="form-label fw-semibold">Building</label>
                <select className="form-select" value={selectedBldgFilter} onChange={(e) => { setSelectedBldgFilter(e.target.value); setSelectedBilletFilter(''); }}>
                  <option value="">Select Building</option>
                  {buildings.map(b => (
                    <option key={b.id} value={b.id}>{b.name}</option>
                  ))}
                </select>
              </div>
              <div className="col-md-4">
                <label className="form-label fw-semibold">Billet</label>
                <select 
                  className="form-select" 
                  value={selectedBilletFilter} 
                  onChange={(e) => setSelectedBilletFilter(e.target.value)}
                  disabled={!selectedBldgFilter}
                >
                  <option value="">Select Billet</option>
                  {selectedBldgFilter && buildings.find(b => b.id === selectedBldgFilter)?.billets.map(b => (
                    <option key={b.id} value={b.id}>{b.name}</option>
                  ))}
                </select>
              </div>
              <div className="col-md-4 text-end">
                {hasPermission('room:write') && selectedBilletFilter && (
                  <button className="btn btn-primary btn-sm d-flex align-items-center gap-1 ms-auto" onClick={() => { setEditingItem(null); setBedForm({ billet_id: selectedBilletFilter, bed_number: '', status: 'Vacant' }); setShowBedFormModal(true); }}>
                    <i className="bi bi-plus-lg"></i> Add Bed
                  </button>
                )}
              </div>
            </div>

            {!selectedBilletFilter ? (
              <div className="text-center py-5 text-muted border rounded">Please select building and billet to view beds.</div>
            ) : (
              <div className="table-responsive">
                <table className="table table-hover align-middle border">
                  <thead className="table-light">
                    <tr>
                      <th>Bed Number</th>
                      <th>Current Status</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {buildings
                      .find(b => b.id === selectedBldgFilter)
                      ?.billets.find(bt => bt.id === selectedBilletFilter)
                      ?.beds.map(bed => (
                        <tr key={bed.id}>
                          <td><strong>Bed {bed.bed_number}</strong></td>
                          <td><span className={`badge ${getBedStatusBadge(bed.status)}`}>{bed.status}</span></td>
                          <td>
                            <button className="btn btn-outline-secondary btn-sm" onClick={() => { setEditingItem(bed); setBedForm({ billet_id: selectedBilletFilter, bed_number: bed.bed_number, status: bed.status }); setShowBedFormModal(true); }}>
                              <i className="bi bi-gear"></i> Update Status
                            </button>
                          </td>
                        </tr>
                      ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}

        {/* ============================================================== */}
        {/* VIEW 4: REPORTS                                                */}
        {/* ============================================================== */}
        {subview === 'reports' && (
          <div className="fade-in-slide bg-white card slaf-card p-4">
            <div className="d-flex flex-wrap justify-content-between align-items-center border-bottom pb-3 mb-3 gap-3">
              <div className="d-flex gap-2">
                <button className={`btn btn-sm ${reportType === 'active' ? 'btn-primary' : 'btn-outline-secondary'}`} onClick={() => setReportType('active')}>
                  Active Placement Register
                </button>
                <button className={`btn btn-sm ${reportType === 'history' ? 'btn-primary' : 'btn-outline-secondary'}`} onClick={() => setReportType('history')}>
                  Allocation & Transfer History
                </button>
                <button className={`btn btn-sm ${reportType === 'billet_occupancy' ? 'btn-primary' : 'btn-outline-secondary'}`} onClick={() => setReportType('billet_occupancy')}>
                  Billet Occupancy Summary
                </button>
              </div>
              
              <div className="d-flex gap-2">
                <button className="btn btn-outline-secondary btn-sm d-flex align-items-center gap-1" onClick={() => window.print()}>
                  <i className="bi bi-printer"></i> Print Report
                </button>
                <button className="btn btn-success btn-sm d-flex align-items-center gap-1" onClick={exportReportToCSV}>
                  <i className="bi bi-file-spreadsheet"></i> Export CSV
                </button>
              </div>
            </div>

            <div className="mb-3">
              <input 
                type="text" 
                className="form-control" 
                placeholder="Search reports by service number, name, billet..." 
                value={reportSearch} 
                onChange={(e) => setReportSearch(e.target.value)} 
              />
            </div>

            <div className="table-responsive">
              <table className="table table-hover table-striped align-middle border">
                <thead className="table-light">
                  {reportType === 'active' && (
                    <tr>
                      <th>Service No</th>
                      <th>Rank & Name</th>
                      <th>Course Batch</th>
                      <th>Building Name</th>
                      <th>Billet Name</th>
                      <th>Bed Number</th>
                      <th>Allocated At</th>
                    </tr>
                  )}
                  {reportType === 'history' && (
                    <tr>
                      <th>Service No</th>
                      <th>Trainee Name</th>
                      <th>Building & Billet</th>
                      <th>Bed</th>
                      <th>Allocated At</th>
                      <th>Vacated At</th>
                      <th>Reason</th>
                      <th>Remarks</th>
                    </tr>
                  )}
                  {reportType === 'billet_occupancy' && (
                    <tr>
                      <th>Building</th>
                      <th>Billet Name</th>
                      <th>Total Capacity</th>
                      <th>Occupied Beds</th>
                      <th>Vacant Beds</th>
                      <th>Occupancy Rate</th>
                    </tr>
                  )}
                </thead>
                <tbody>
                  {filteredReports.length === 0 ? (
                    <tr>
                      <td colSpan="10" className="text-center py-4 text-muted">No records found matching search queries.</td>
                    </tr>
                  ) : (
                    filteredReports.map((row, idx) => (
                      <tr key={row.id || idx}>
                        {reportType === 'active' && (
                          <>
                            <td><strong>{row.student_service_number}</strong></td>
                            <td>{row.student_rank} {row.student_name}</td>
                            <td>{row.student_batch}</td>
                            <td>{row.building_name}</td>
                            <td>{row.billet_name}</td>
                            <td>Bed {row.bed_number}</td>
                            <td>{new Date(row.allocated_at).toLocaleString()}</td>
                          </>
                        )}
                        {reportType === 'history' && (
                          <>
                            <td><strong>{row.student_service_number}</strong></td>
                            <td>{row.student_rank} {row.student_name}</td>
                            <td>{row.building_name} ({row.billet_name})</td>
                            <td>Bed {row.bed_number}</td>
                            <td>{new Date(row.allocated_at).toLocaleDateString()}</td>
                            <td>{row.vacated_at ? new Date(row.vacated_at).toLocaleDateString() : 'N/A'}</td>
                            <td><span className="badge bg-secondary">{row.vacate_reason || 'N/A'}</span></td>
                            <td><span className="small text-muted">{row.remarks || 'None'}</span></td>
                          </>
                        )}
                        {reportType === 'billet_occupancy' && (
                          <>
                            <td><strong>{row.building_name}</strong></td>
                            <td>{row.billet_name}</td>
                            <td>{row.capacity} beds</td>
                            <td><span className="text-danger fw-bold">{row.occupied}</span></td>
                            <td><span className="text-success fw-bold">{row.vacant}</span></td>
                            <td>
                              <div className="d-flex align-items-center gap-2">
                                <span>{row.occupancy_rate}%</span>
                                <div className="progress w-100" style={{ height: '6px', maxWidth: '80px' }}>
                                  <div className="progress-bar" style={{ width: `${row.occupancy_rate}%` }}></div>
                                </div>
                              </div>
                            </td>
                          </>
                        )}
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>

      {/* ============================================================== */}
      {/* MODULE FOOTER                                                  */}
      {/* ============================================================== */}
      <footer className="mt-5 border-top pt-3 text-muted small d-print-none">
        <div className="d-flex flex-wrap justify-content-between align-items-center g-2 text-secondary">
          <div>
            <strong>Module:</strong> Accommodation Management v1.2.0
          </div>
          <div>
            <strong>Database Status:</strong> <span className="text-success"><i className="bi bi-circle-fill me-1" style={{ fontSize: '0.55rem' }}></i>Connected</span>
          </div>
          <div>
            <strong>Last Synchronization:</strong> {new Date().toLocaleTimeString()}
          </div>
          <div>
            <strong>Support:</strong> <a href="mailto:tts.admin@slaf.lk" className="text-decoration-none">tts.admin@slaf.lk</a>
          </div>
        </div>
      </footer>

      {/* ============================================================== */}
      {/* ALL MODAL DIALOGUES                                            */}
      {/* ============================================================== */}

      {/* Modal 1: Allocate Bed */}
      {showAllocateModal && (
        <div className="modal show d-block" tabIndex="-1" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
          <div className="modal-dialog">
            <div className="modal-content glass-card">
              <div className="modal-header">
                <h5 className="modal-title fw-bold">Allocate Bed {selectedBed ? selectedBed.bed_number : 'Available'}</h5>
                <button type="button" className="btn-close" onClick={() => setShowAllocateModal(false)}></button>
              </div>
              <form onSubmit={handleAllocateSubmit}>
                <div className="modal-body">
                  {!selectedBed && (
                    <div className="mb-3">
                      <label className="form-label fw-semibold">Select Target Bed</label>
                      <select 
                        className="form-select" 
                        onChange={(e) => {
                          const bed = vacantBedsList.find(b => b.id === e.target.value)
                          setSelectedBed(bed ? { id: bed.id, bed_number: bed.label } : null)
                        }}
                        required
                      >
                        <option value="">Choose Bed Location</option>
                        {vacantBedsList.map(item => (
                          <option key={item.id} value={item.id}>{item.label}</option>
                        ))}
                      </select>
                    </div>
                  )}
                  <div className="mb-3">
                    <label className="form-label fw-semibold">Select Trainee (Service Number - Rank - Initials - Full Name)</label>
                    <select 
                      className="form-select" 
                      value={targetStudentId} 
                      onChange={(e) => setTargetStudentId(e.target.value)}
                      required
                    >
                      <option value="">Select Trainee from SSOT</option>
                      {students
                        .filter(s => s.status === 'Active' && !activeAllocations.some(a => a.student_id === s.id))
                        .map(s => (
                          <option key={s.id} value={s.id}>
                            {s.service_number} - {s.rank} {s.initials} ({s.full_name})
                          </option>
                        ))
                      }
                    </select>
                    <small className="text-muted d-block mt-1">Only active trainees without existing housing allocations are listed.</small>
                  </div>
                  <div className="mb-3">
                    <label className="form-label fw-semibold">Allocation Remarks</label>
                    <textarea 
                      className="form-control" 
                      placeholder="Input remarks e.g. Course allocation"
                      value={allocationRemarks}
                      onChange={(e) => setAllocationRemarks(e.target.value)}
                    ></textarea>
                  </div>
                </div>
                <div className="modal-footer">
                  <button type="button" className="btn btn-outline-secondary" onClick={() => setShowAllocateModal(false)}>Cancel</button>
                  <button type="submit" className="btn btn-success">Confirm Allocation</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Modal 2: Trainee Allocation Details */}
      {showDetailModal && selectedAllocation && (
        <div className="modal show d-block" tabIndex="-1" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
          <div className="modal-dialog">
            <div className="modal-content glass-card">
              <div className="modal-header">
                <h5 className="modal-title fw-bold">Trainee Placement Record</h5>
                <button type="button" className="btn-close" onClick={() => setShowDetailModal(false)}></button>
              </div>
              <div className="modal-body">
                <div className="p-3 bg-light rounded mb-3">
                  <span className="text-muted small fw-semibold text-uppercase">Trainee Service Number</span>
                  <h4 className="text-primary fw-bold mb-2">{selectedAllocation.student_service_number}</h4>
                  <p className="mb-0 fw-semibold text-dark">
                    {selectedAllocation.student_rank} {selectedAllocation.student_name}
                  </p>
                  <p className="text-muted small mb-0 mt-1">
                    Trade: {selectedAllocation.student_trade} | Batch: {selectedAllocation.student_batch}
                  </p>
                </div>
                
                <div className="mb-3">
                  <span className="text-muted small d-block">Current Accommodation Details:</span>
                  <strong>{selectedAllocation.building_name}</strong>
                  <div className="text-secondary">{selectedAllocation.billet_name} - Bed {selectedAllocation.bed_number}</div>
                  <div className="text-muted small mt-1">Allocated At: {new Date(selectedAllocation.allocated_at).toLocaleString()}</div>
                  {selectedAllocation.remarks && (
                    <div className="alert alert-info mt-2 py-2 px-3 small mb-0">
                      <strong>Remarks: </strong>{selectedAllocation.remarks}
                    </div>
                  )}
                </div>
              </div>
              {hasPermission('room:write') && (
                <div className="modal-footer d-flex justify-content-between">
                  <button type="button" className="btn btn-danger" onClick={() => { setShowVacateModal(true); }}>
                    <i className="bi bi-x-circle me-1"></i> Vacate Bed
                  </button>
                  <div>
                    <button type="button" className="btn btn-outline-primary me-2" onClick={() => { setShowTransferModal(true); setTransferTargetBedId(''); setTransferRemarks(''); }}>
                      <i className="bi bi-arrow-left-right me-1"></i> Transfer Bed
                    </button>
                    <button type="button" className="btn btn-outline-secondary" onClick={() => setShowDetailModal(false)}>Close</button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Modal 3: Transfer Bed */}
      {showTransferModal && selectedAllocation && (
        <div className="modal show d-block" tabIndex="-1" style={{ backgroundColor: 'rgba(0,0,0,0.5)', zIndex: 1060 }}>
          <div className="modal-dialog">
            <div className="modal-content glass-card">
              <div className="modal-header">
                <h5 className="modal-title fw-bold">Transfer Trainee Bed</h5>
                <button type="button" className="btn-close" onClick={() => setShowTransferModal(false)}></button>
              </div>
              <form onSubmit={handleTransferSubmit}>
                <div className="modal-body">
                  <div className="mb-3 bg-light p-2.5 rounded">
                    <strong>Transferring trainee:</strong> {selectedAllocation.student_rank} {selectedAllocation.student_name} ({selectedAllocation.student_service_number})
                  </div>
                  <p className="small text-muted">Select an available bed to transfer the trainee from their current bed.</p>
                  <div className="mb-3">
                    <label className="form-label fw-semibold">Destination Bed</label>
                    <select 
                      className="form-select" 
                      value={transferTargetBedId} 
                      onChange={(e) => setTransferTargetBedId(e.target.value)} 
                      required
                    >
                      <option value="">Select Available Bed</option>
                      {vacantBedsList.map(item => (
                        <option key={item.id} value={item.id}>{item.label}</option>
                      ))}
                    </select>
                  </div>
                  <div className="mb-3">
                    <label className="form-label fw-semibold">Transfer Reasons / Remarks</label>
                    <textarea 
                      className="form-control" 
                      value={transferRemarks} 
                      onChange={(e) => setTransferRemarks(e.target.value)}
                      placeholder="Input reason for transfer"
                    ></textarea>
                  </div>
                </div>
                <div className="modal-footer">
                  <button type="button" className="btn btn-outline-secondary" onClick={() => setShowTransferModal(false)}>Cancel</button>
                  <button type="submit" className="btn btn-primary">Confirm Transfer</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Modal 4: Vacate Bed */}
      {showVacateModal && selectedAllocation && (
        <div className="modal show d-block" tabIndex="-1" style={{ backgroundColor: 'rgba(0,0,0,0.5)', zIndex: 1060 }}>
          <div className="modal-dialog">
            <div className="modal-content glass-card">
              <div className="modal-header bg-danger text-white">
                <h5 className="modal-title fw-bold">Vacate Trainee Accommodation</h5>
                <button type="button" className="btn-close btn-close-white" onClick={() => setShowVacateModal(false)}></button>
              </div>
              <form onSubmit={handleVacateSubmit}>
                <div className="modal-body">
                  <div className="mb-3 bg-light p-2.5 rounded text-dark">
                    <strong>Vacating trainee:</strong> {selectedAllocation.student_rank} {selectedAllocation.student_name} ({selectedAllocation.student_service_number})
                  </div>
                  <p className="small text-muted">Are you sure you want to release the bed allocated to this trainee?</p>
                  <div className="mb-3">
                    <label className="form-label fw-semibold">Vacate Reason</label>
                    <select 
                      className="form-select" 
                      value={vacateReason} 
                      onChange={(e) => setVacateReason(e.target.value)} 
                      required
                    >
                      <option value="Course Completed">Course Completed</option>
                      <option value="Transfer">Transfer</option>
                      <option value="Medical">Medical</option>
                      <option value="Administrative">Administrative</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>
                  <div className="mb-3">
                    <label className="form-label fw-semibold">Remarks</label>
                    <textarea 
                      className="form-control" 
                      value={vacateRemarks} 
                      onChange={(e) => setVacateRemarks(e.target.value)}
                      placeholder="Input vacate notes"
                    ></textarea>
                  </div>
                </div>
                <div className="modal-footer">
                  <button type="button" className="btn btn-outline-secondary" onClick={() => setShowVacateModal(false)}>Cancel</button>
                  <button type="submit" className="btn btn-danger">Confirm Vacate</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Modal 5: Building Form */}
      {showBldgFormModal && (
        <div className="modal show d-block" tabIndex="-1" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
          <div className="modal-dialog">
            <div className="modal-content glass-card">
              <div className="modal-header">
                <h5 className="modal-title fw-bold">{editingItem ? 'Edit Building' : 'Add New Building'}</h5>
                <button type="button" className="btn-close" onClick={() => setShowBldgFormModal(false)}></button>
              </div>
              <form onSubmit={handleSaveBuilding}>
                <div className="modal-body">
                  <div className="mb-3">
                    <label className="form-label fw-semibold">Building Name</label>
                    <input 
                      type="text" 
                      className="form-control" 
                      value={bldgForm.name} 
                      onChange={(e) => setBldgForm({ ...bldgForm, name: e.target.value })} 
                      required 
                      placeholder="e.g. Training Block Alpha (T2)"
                    />
                  </div>
                  <div className="mb-3">
                    <label className="form-label fw-semibold">Building Type</label>
                    <select 
                      className="form-select" 
                      value={bldgForm.type} 
                      onChange={(e) => setBldgForm({ ...bldgForm, type: e.target.value })}
                    >
                      <option value="Airmen">Airmen</option>
                      <option value="Airwomen">Airwomen</option>
                      <option value="Officers">Officers</option>
                    </select>
                  </div>
                  <div className="mb-3">
                    <label className="form-label fw-semibold">Maximum Bed Capacity</label>
                    <input 
                      type="number" 
                      className="form-control" 
                      value={bldgForm.capacity} 
                      onChange={(e) => setBldgForm({ ...bldgForm, capacity: parseInt(e.target.value) || 0 })} 
                      required 
                      min="1"
                    />
                  </div>
                </div>
                <div className="modal-footer">
                  <button type="button" className="btn btn-outline-secondary" onClick={() => setShowBldgFormModal(false)}>Cancel</button>
                  <button type="submit" className="btn btn-primary">Save Building</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Modal 6: Billet Form */}
      {showBilletFormModal && (
        <div className="modal show d-block" tabIndex="-1" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
          <div className="modal-dialog">
            <div className="modal-content glass-card">
              <div className="modal-header">
                <h5 className="modal-title fw-bold">{editingItem ? 'Edit Billet' : 'Add Billet'}</h5>
                <button type="button" className="btn-close" onClick={() => setShowBilletFormModal(false)}></button>
              </div>
              <form onSubmit={handleSaveBillet}>
                <div className="modal-body">
                  <div className="mb-3">
                    <label className="form-label fw-semibold">Billet Name</label>
                    <input 
                      type="text" 
                      className="form-control" 
                      value={billetForm.name} 
                      onChange={(e) => setBilletForm({ ...billetForm, name: e.target.value })} 
                      required 
                      placeholder="e.g. Billet Alpha-2"
                    />
                  </div>
                  <div className="mb-3">
                    <label className="form-label fw-semibold">Maximum Capacity (Beds)</label>
                    <input 
                      type="number" 
                      className="form-control" 
                      value={billetForm.capacity} 
                      onChange={(e) => setBilletForm({ ...billetForm, capacity: parseInt(e.target.value) || 0 })} 
                      required 
                      min="1"
                    />
                  </div>
                </div>
                <div className="modal-footer">
                  <button type="button" className="btn btn-outline-secondary" onClick={() => setShowBilletFormModal(false)}>Cancel</button>
                  <button type="submit" className="btn btn-primary">Save Billet</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Modal 7: Bed Form */}
      {showBedFormModal && (
        <div className="modal show d-block" tabIndex="-1" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
          <div className="modal-dialog">
            <div className="modal-content glass-card">
              <div className="modal-header">
                <h5 className="modal-title fw-bold">{editingItem ? 'Update Bed Status' : 'Add New Bed'}</h5>
                <button type="button" className="btn-close" onClick={() => setShowBedFormModal(false)}></button>
              </div>
              <form onSubmit={handleSaveBed}>
                <div className="modal-body">
                  <div className="mb-3">
                    <label className="form-label fw-semibold">Bed Number</label>
                    <input 
                      type="text" 
                      className="form-control" 
                      value={bedForm.bed_number} 
                      onChange={(e) => setBedForm({ ...bedForm, bed_number: e.target.value })} 
                      required 
                      placeholder="e.g. 05"
                      disabled={!!editingItem}
                    />
                  </div>
                  <div className="mb-3">
                    <label className="form-label fw-semibold">Status</label>
                    <select 
                      className="form-select" 
                      value={bedForm.status} 
                      onChange={(e) => setBedForm({ ...bedForm, status: e.target.value })}
                      disabled={editingItem && editingItem.status === 'Occupied'}
                    >
                      <option value="Vacant">Available</option>
                      <option value="Maintenance">Maintenance</option>
                      <option value="Reserved">Reserved</option>
                      {editingItem && editingItem.status === 'Occupied' && (
                        <option value="Occupied">Occupied</option>
                      )}
                    </select>
                    {editingItem && editingItem.status === 'Occupied' && (
                      <small className="text-danger mt-1 d-block">Occupied beds cannot change status directly. Use the Vacate workflow instead.</small>
                    )}
                  </div>
                </div>
                <div className="modal-footer">
                  <button type="button" className="btn btn-outline-secondary" onClick={() => setShowBedFormModal(false)}>Cancel</button>
                  <button type="submit" className="btn btn-primary">Save Bed</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
export default AccommodationPanel
