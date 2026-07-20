import React, { useEffect, useState } from 'react'
import { useNavigate, useParams, Link } from 'react-router-dom'
import axios from 'axios'
import { toast } from 'react-toastify'

export const StudentForm = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const isEdit = !!id

  const [courses, setCourses] = useState([])
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

    if (isEdit) {
      const loadStudent = async () => {
        try {
          const res = await axios.get(`/api/v1/students/${id}`)
          const data = res.data
          // Format dates for input tags
          if (data.dob) data.dob = data.dob.substring(0, 10)
          if (data.joining_date) data.joining_date = data.joining_date.substring(0, 10)
          if (data.passing_out_date) data.passing_out_date = data.passing_out_date.substring(0, 10)
          
          setFormData(data)
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
      
      const payload = {
        ...formData,
        course_id: formData.course_id || null,
        passing_out_date: formData.passing_out_date || null
      }

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
        await axios.post(`/api/v1/students/${savedStudent.id}/photo`, fileForm, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
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
              />
            </div>

            <div className="col-md-3">
              <label className="form-label fw-semibold">Rank *</label>
              <select className="form-select" name="rank" value={formData.rank} onChange={handleInputChange} required>
                <option value="Aircraftman">Aircraftman (AC)</option>
                <option value="Leading Aircraftman">Leading Aircraftman (LAC)</option>
                <option value="Corporal">Corporal (Cpl)</option>
                <option value="Sergeant">Sergeant (Sgt)</option>
              </select>
            </div>
            <div className="col-md-3">
              <label className="form-label fw-semibold">Trade *</label>
              <select className="form-select" name="trade" value={formData.trade} onChange={handleInputChange} required>
                <option value="Airframe">Airframe Fitters</option>
                <option value="Avionics">Avionics Fitters</option>
                <option value="Safety Equipment">Safety Equipment Fitters</option>
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
              />
            </div>
          </div>

          {/* Section 2: Personal details */}
          <h5 className="mb-3 display-font text-primary border-bottom pb-2">2. Personal Particulars</h5>
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
            <div className="col-md-3">
              <label className="form-label fw-semibold">Medical Class Code</label>
              <input 
                type="text" 
                className="form-control" 
                name="medical_category"
                value={formData.medical_category}
                onChange={handleInputChange}
              />
            </div>
            <div className="col-md-2">
              <label className="form-label fw-semibold">Religion *</label>
              <input 
                type="text" 
                className="form-control" 
                name="religion"
                value={formData.religion}
                onChange={handleInputChange}
                required
              />
            </div>

            <div className="col-md-4">
              <label className="form-label fw-semibold">Permanent Address *</label>
              <textarea 
                className="form-control" 
                name="permanent_address" 
                value={formData.permanent_address}
                onChange={handleInputChange}
                rows="2"
                required
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
                  <option value="Active">Active</option>
                  <option value="Sick Report">Sick Report</option>
                  <option value="Leave">Leave</option>
                  <option value="AWOL">AWOL</option>
                  <option value="Passed Out">Passed Out</option>
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
