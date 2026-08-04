import React, { useEffect, useState } from 'react'
import { useNavigate, useParams, Link } from 'react-router-dom'
import axios from 'axios'
import { toast } from 'react-toastify'

export const StudentForm = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const isEdit = !!id

  const [courses, setCourses] = useState([])
  const [statuses, setStatuses] = useState([])
  const [ranks, setRanks] = useState([])
  const [trades, setTrades] = useState([])
  const [formData, setFormData] = useState({
    service_number: '',
    initials: '',
    full_name: '',
    nic: '',
    dob: '',
    gender: 'Male',
    rank: 'Aircraftman',
    trade: 'Airframe',
    course_id: '',
    batch: '',
    squadron: 'Training Squadron',
    unit: 'SLAF TTS Ekala',
    posting: '',
    joining_date: '',
    passing_out_date: '',
    status: 'Active',
    phone: '',
    email: '',
    emergency_contact_name: '',
    emergency_contact_phone: '',
    blood_group: 'O+',
    medical_category: 'A4G4',
    religion: 'Buddhist',
    nationality: 'Sri Lankan',
    permanent_address: '',
    temporary_address: ''
  })
  
  const [photoFile, setPhotoFile] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    // Load courses
    const loadCourses = async () => {
      try {
        const res = await axios.get('/api/v1/academic/courses')
        setCourses(res.data)
      } catch (err) {
        console.error(err)
      }
    }
    loadCourses()

    // Load student status types from DB
    const loadStatuses = async () => {
      try {
        const res = await axios.get('/api/v1/students/statuses')
        if (res.data && res.data.length > 0) {
          setStatuses(res.data)
        }
      } catch (err) {
        console.error('Failed to load student status types from DB', err)
      }
    }
    loadStatuses()

    // Load student ranks from DB
    const loadRanks = async () => {
      try {
        const res = await axios.get('/api/v1/students/ranks')
        if (res.data && res.data.length > 0) {
          setRanks(res.data)
        }
      } catch (err) {
        console.error('Failed to load student ranks from DB', err)
      }
    }
    loadRanks()

    // Load student trades from DB
    const loadTrades = async () => {
      try {
        const res = await axios.get('/api/v1/students/trades')
        if (res.data && res.data.length > 0) {
          setTrades(res.data)
        }
      } catch (err) {
        console.error('Failed to load student trades from DB', err)
      }
    }
    loadTrades()

    if (isEdit) {
      const loadStudent = async () => {
        try {
          const res = await axios.get(`/api/v1/students/${id}`)
          const data = res.data
          
          setFormData({
            service_number: data.service_number || '',
            initials: data.initials || '',
            full_name: data.full_name || '',
            nic: data.nic || '',
            dob: data.dob ? data.dob.substring(0, 10) : '',
            gender: data.gender || 'Male',
            rank: data.rank || 'Aircraftman',
            trade: data.trade || 'Airframe',
            course_id: data.course_id || '',
            batch: data.batch || '',
            squadron: data.squadron || 'Training Squadron',
            unit: data.unit || 'SLAF TTS Ekala',
            posting: data.posting || '',
            joining_date: data.joining_date ? data.joining_date.substring(0, 10) : '',
            passing_out_date: data.passing_out_date ? data.passing_out_date.substring(0, 10) : '',
            status: data.status || 'Active',
            phone: data.phone || '',
            email: data.email || '',
            emergency_contact_name: data.emergency_contact_name || '',
            emergency_contact_phone: data.emergency_contact_phone || '',
            blood_group: data.blood_group || 'O+',
            medical_category: data.medical_category || 'A4G4',
            religion: data.religion || 'Buddhist',
            nationality: data.nationality || 'Sri Lankan',
            permanent_address: data.permanent_address || '',
            temporary_address: data.temporary_address || ''
          })
        } catch (err) {
          toast.error('Failed to load student details')
        }
      }
      loadStudent()
    }
  }, [id, isEdit])

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  const handleFileChange = (e) => {
    setPhotoFile(e.target.files[0])
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      let savedStudent = null
      
      // Sanitize payload: convert empty strings back to null so they validate correctly in FastAPI/Pydantic
      const payload = {}
      Object.keys(formData).forEach(key => {
        payload[key] = (formData[key] === '' || formData[key] === null) ? null : formData[key]
      })

      if (isEdit) {
        const res = await axios.put(`/api/v1/students/${id}`, payload)
        savedStudent = res.data
        toast.success('Trainee profile updated successfully')
      } else {
        const res = await axios.post('/api/v1/students', payload)
        savedStudent = res.data
        toast.success('Trainee registered successfully')
      }

      // If photo was chosen, upload photo
      if (photoFile && savedStudent) {
        const fileForm = new FormData()
        fileForm.append('file', photoFile)
        await axios.post(`/api/v1/students/${savedStudent.id}/photo`, fileForm)
        toast.success('Profile photo uploaded')
      }

      navigate(`/students/${savedStudent.id}`)
    } catch (err) {
      toast.error(err.response?.data?.detail || 'An error occurred during submission')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fade-in-slide">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 className="mb-0 text-primary display-font">{isEdit ? 'Modify Profile' : 'Register New Trainee'}</h2>
          <p className="text-muted mb-0">{isEdit ? `Edit details for service number ${formData.service_number}` : 'Add a new student profile to single source of truth'}</p>
        </div>
        <Link to="/students" className="btn btn-outline-secondary">
          Cancel
        </Link>
      </div>

      <div className="card slaf-card p-4">
        <form onSubmit={handleSubmit}>
          {/* Section 1: Military details */}
          <h5 className="mb-3 display-font text-primary border-bottom pb-2">1. Service Particulars</h5>
          <div className="row g-3 mb-4">
            <div className="col-md-3">
              <label className="form-label fw-semibold">Service Number *</label>
              <input 
                type="text" 
                className="form-control" 
                name="service_number"
                value={formData.service_number}
                onChange={handleInputChange}
                required
                disabled={isEdit}
                placeholder="e.g. 51837"
              />
            </div>
            <div className="col-md-2">
              <label className="form-label fw-semibold">Initials *</label>
              <input 
                type="text" 
                className="form-control" 
                name="initials"
                value={formData.initials}
                onChange={handleInputChange}
                required
                placeholder="e.g. W A"
              />
            </div>
            <div className="col-md-4">
              <label className="form-label fw-semibold">Full Name *</label>
              <input 
                type="text" 
                className="form-control" 
                name="full_name"
                value={formData.full_name}
                onChange={handleInputChange}
                required
                placeholder="e.g. Wasala Mudiyanselage Sanka"
              />
            </div>
            <div className="col-md-3">
              <label className="form-label fw-semibold">NIC Number *</label>
              <input 
                type="text" 
                className="form-control" 
                name="nic"
                value={formData.nic}
                onChange={handleInputChange}
                required
                placeholder="e.g. 199612345678"
              />
            </div>

            <div className="col-md-3">
              <label className="form-label fw-semibold">Rank *</label>
              <select className="form-select" name="rank" value={formData.rank} onChange={handleInputChange} required>
                {ranks.length > 0 ? (
                  ranks.map(r => (
                    <option key={r.id} value={r.label}>
                      {r.label} ({r.code})
                    </option>
                  ))
                ) : (
                  <>
                    <option value="Aircraftman">Aircraftman (AC)</option>
                    <option value="Leading Aircraftman">Leading Aircraftman (LAC)</option>
                    <option value="Corporal">Corporal (Cpl)</option>
                    <option value="Sergeant">Sergeant (Sgt)</option>
                  </>
                )}
              </select>
            </div>
            <div className="col-md-3">
              <label className="form-label fw-semibold">Trade *</label>
              <select className="form-select" name="trade" value={formData.trade} onChange={handleInputChange} required>
                {trades.length > 0 ? (
                  trades.map(t => (
                    <option key={t.id} value={t.label}>
                      {t.label}
                    </option>
                  ))
                ) : (
                  <>
                    <option value="Airframe">Airframe Fitters</option>
                    <option value="Avionics">Avionics Fitters</option>
                    <option value="Safety Equipment">Safety Equipment Fitters</option>
                  </>
                )}
              </select>
            </div>
            <div className="col-md-3">
              <label className="form-label fw-semibold">Course Enrollment</label>
              <select className="form-select" name="course_id" value={formData.course_id} onChange={handleInputChange}>
                <option value="">No Course Assignment</option>
                {courses.map(c => (
                  <option key={c.id} value={c.id}>{c.name}</option>
                ))}
              </select>
            </div>
            <div className="col-md-3">
              <label className="form-label fw-semibold">Batch / Intake *</label>
              <input 
                type="text" 
                className="form-control" 
                name="batch"
                value={formData.batch}
                onChange={handleInputChange}
                required
                placeholder="e.g. Intake 171"
              />
            </div>

            <div className="col-md-3">
              <label className="form-label fw-semibold">Squadron</label>
              <input 
                type="text" 
                className="form-control" 
                name="squadron"
                value={formData.squadron}
                onChange={handleInputChange}
                placeholder="Training Squadron"
              />
            </div>
            <div className="col-md-3">
              <label className="form-label fw-semibold">Unit / Base</label>
              <input 
                type="text" 
                className="form-control" 
                name="unit"
                value={formData.unit}
                onChange={handleInputChange}
                placeholder="SLAF TTS Ekala"
              />
            </div>
            <div className="col-md-3">
              <label className="form-label fw-semibold">Unit Posting</label>
              <input 
                type="text" 
                className="form-control" 
                name="posting"
                value={formData.posting}
                onChange={handleInputChange}
                placeholder="e.g. SLAF Katunayake"
              />
            </div>
            <div className="col-md-3">
              <label className="form-label fw-semibold">Enlistment / Joining Date</label>
              <input 
                type="date" 
                className="form-control" 
                name="joining_date"
                value={formData.joining_date}
                onChange={handleInputChange}
              />
            </div>
            <div className="col-md-3">
              <label className="form-label fw-semibold">Passing Out Date</label>
              <input 
                type="date" 
                className="form-control" 
                name="passing_out_date"
                value={formData.passing_out_date}
                onChange={handleInputChange}
              />
            </div>
          </div>

          {/* Section 2: Personal details */}
          <h5 className="mb-3 display-font text-primary border-bottom pb-2">2. Personal & Contact Particulars</h5>
          <div className="row g-3 mb-4">
            <div className="col-md-3">
              <label className="form-label fw-semibold">Date of Birth *</label>
              <input 
                type="date" 
                className="form-control" 
                name="dob"
                value={formData.dob}
                onChange={handleInputChange}
                required
              />
            </div>
            <div className="col-md-2">
              <label className="form-label fw-semibold">Gender *</label>
              <select className="form-select" name="gender" value={formData.gender} onChange={handleInputChange} required>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
              </select>
            </div>
            <div className="col-md-2">
              <label className="form-label fw-semibold">Blood Group *</label>
              <select className="form-select" name="blood_group" value={formData.blood_group} onChange={handleInputChange} required>
                <option value="A+">A+</option>
                <option value="A-">A-</option>
                <option value="B+">B+</option>
                <option value="B-">B-</option>
                <option value="AB+">AB+</option>
                <option value="AB-">AB-</option>
                <option value="O+">O+</option>
                <option value="O-">O-</option>
              </select>
            </div>
            <div className="col-md-2">
              <label className="form-label fw-semibold">Medical Class Code</label>
              <input 
                type="text" 
                className="form-control" 
                name="medical_category"
                value={formData.medical_category}
                onChange={handleInputChange}
                placeholder="A4G4"
              />
            </div>
            <div className="col-md-3">
              <label className="form-label fw-semibold">Religion *</label>
              <input 
                type="text" 
                className="form-control" 
                name="religion"
                value={formData.religion}
                onChange={handleInputChange}
                required
                placeholder="e.g. Buddhist"
              />
            </div>
            <div className="col-md-3">
              <label className="form-label fw-semibold">Nationality</label>
              <input 
                type="text" 
                className="form-control" 
                name="nationality"
                value={formData.nationality}
                onChange={handleInputChange}
                placeholder="Sri Lankan"
              />
            </div>
            <div className="col-md-3">
              <label className="form-label fw-semibold">Personal Phone</label>
              <input 
                type="text" 
                className="form-control" 
                name="phone"
                value={formData.phone}
                onChange={handleInputChange}
                placeholder="0771234567"
              />
            </div>
            <div className="col-md-4">
              <label className="form-label fw-semibold">Email Address</label>
              <input 
                type="email" 
                className="form-control" 
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                placeholder="trainee@slaf.gov.lk"
              />
            </div>
          </div>

          {/* Section 3: Address & Emergency Particulars */}
          <h5 className="mb-3 display-font text-primary border-bottom pb-2">3. Address & Emergency Contacts</h5>
          <div className="row g-3 mb-4">
            <div className="col-md-6">
              <label className="form-label fw-semibold">Permanent Address *</label>
              <textarea 
                className="form-control" 
                name="permanent_address" 
                value={formData.permanent_address}
                onChange={handleInputChange}
                rows="2"
                required
                placeholder="Full permanent residential address"
              ></textarea>
            </div>
            <div className="col-md-6">
              <label className="form-label fw-semibold">Temporary / Boarding Address</label>
              <textarea 
                className="form-control" 
                name="temporary_address" 
                value={formData.temporary_address}
                onChange={handleInputChange}
                rows="2"
                placeholder="Temporary or local contact address"
              ></textarea>
            </div>
            <div className="col-md-4">
              <label className="form-label fw-semibold">Emergency Contact Name *</label>
              <input 
                type="text" 
                className="form-control" 
                name="emergency_contact_name"
                value={formData.emergency_contact_name}
                onChange={handleInputChange}
                required
                placeholder="Next of Kin / Contact Person"
              />
            </div>
            <div className="col-md-4">
              <label className="form-label fw-semibold">Emergency Contact Phone *</label>
              <input 
                type="text" 
                className="form-control" 
                name="emergency_contact_phone"
                value={formData.emergency_contact_phone}
                onChange={handleInputChange}
                required
                placeholder="0711234567"
              />
            </div>

            <div className="col-md-4">
              <label className="form-label fw-semibold">Profile Photo</label>
              <input 
                type="file" 
                className="form-control" 
                onChange={handleFileChange}
                accept="image/*"
              />
              <small className="text-muted">Maximum file size: 2MB. Jpeg, png formats only.</small>
            </div>
            
            {isEdit && (
              <div className="col-md-3">
                <label className="form-label fw-semibold text-danger">Trainee Status</label>
                <select className="form-select border-danger text-danger" name="status" value={formData.status} onChange={handleInputChange}>
                  {statuses.map(st => (
                    <option key={st.id || st.code} value={st.label}>
                      {st.label}
                    </option>
                  ))}
                </select>
              </div>
            )}
          </div>

          <div className="d-flex justify-content-end gap-2 mt-4">
            <button 
              type="submit" 
              className="btn btn-primary px-5 py-2 fw-semibold"
              disabled={loading}
            >
              {loading ? 'Saving Trainee Profile...' : 'Save Trainee Profile'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
export default StudentForm
