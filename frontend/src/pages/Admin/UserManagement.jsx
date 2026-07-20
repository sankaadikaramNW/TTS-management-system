import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { toast } from 'react-toastify'

export const UserManagement = () => {
  const [users, setUsers] = useState([])
  const [auditLogs, setAuditLogs] = useState([])
  const [loading, setLoading] = useState(true)

  // User form states
  const [username, setUsername] = useState('')
  const [fullName, setFullName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [roleId, setRoleId] = useState('role-instructor')

  const loadAdminData = async () => {
    setLoading(true)
    try {
      const uRes = await axios.get('/api/v1/system/users')
      setUsers(uRes.data)
      const aRes = await axios.get('/api/v1/system/audit-logs')
      setAuditLogs(aRes.data)
    } catch (err) {
      toast.error('Failed to load system logs')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadAdminData()
  }, [])

  const handleAddUser = async (e) => {
    e.preventDefault()
    try {
      await axios.post('/api/v1/system/users', {
        username,
        full_name: fullName,
        email,
        password,
        role_id: roleId
      })
      toast.success('System user created successfully')
      setUsername('')
      setFullName('')
      setEmail('')
      setPassword('')
      loadAdminData()
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to create user')
    }
  }

  const handleBackup = async () => {
    try {
      const res = await axios.post('/api/v1/system/backup')
      toast.success('Database backup initiated successfully')
      toast.info(`Backup file saved: ${res.data.file_name}`)
      loadAdminData() // refresh logs
    } catch (err) {
      toast.error('Failed to initiate backup')
    }
  }

  return (
    <div className="fade-in-slide">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 className="mb-0 text-primary display-font">System Administration</h2>
          <p className="text-muted mb-0">Manage portal operators, view audit trails, and dump database backups</p>
        </div>
        <button className="btn btn-warning d-flex align-items-center gap-2 fw-semibold text-dark" onClick={handleBackup}>
          <i className="bi bi-database-fill-up"></i> Trigger Backup
        </button>
      </div>

      <div className="row g-4">
        {/* User creation form */}
        <div className="col-lg-4 col-md-12">
          <div className="card slaf-card p-3 mb-4">
            <h5 className="display-font text-muted mb-3 border-bottom pb-2">Add Portal User</h5>
            <form onSubmit={handleAddUser}>
              <div className="mb-2">
                <label className="form-label mb-1">Username</label>
                <input type="text" className="form-control form-control-sm" value={username} onChange={e => setUsername(e.target.value)} required />
              </div>
              <div className="mb-2">
                <label className="form-label mb-1">Full Name</label>
                <input type="text" className="form-control form-control-sm" value={fullName} onChange={e => setFullName(e.target.value)} required />
              </div>
              <div className="mb-2">
                <label className="form-label mb-1">Email</label>
                <input type="email" className="form-control form-control-sm" value={email} onChange={e => setEmail(e.target.value)} required />
              </div>
              <div className="mb-2">
                <label className="form-label mb-1">Password</label>
                <input type="password" className="form-control form-control-sm" value={password} onChange={e => setPassword(e.target.value)} required />
              </div>
              <div className="mb-3">
                <label className="form-label mb-1">Portal Role</label>
                <select className="form-select form-select-sm" value={roleId} onChange={e => setRoleId(e.target.value)}>
                  <option value="role-super-admin">Super Administrator</option>
                  <option value="role-sys-admin">System Administrator</option>
                  <option value="role-discipline">Discipline Section</option>
                  <option value="role-academic">Academic Section</option>
                  <option value="role-accommodation">Accommodation Officer</option>
                  <option value="role-instructor">Instructor</option>
                  <option value="role-co">Commanding Officer</option>
                </select>
              </div>
              <button type="submit" className="btn btn-primary btn-sm w-100 fw-semibold">Save Portal User</button>
            </form>
          </div>

          <div className="card slaf-card p-3">
            <h5 className="display-font text-muted mb-3 border-bottom pb-2">Active Users Register</h5>
            {loading ? (
              <div className="spinner-border spinner-border-sm text-primary" role="status"></div>
            ) : (
              <div className="list-group list-group-flush" style={{ maxHeight: '300px', overflowY: 'auto' }}>
                {users.map(u => (
                  <div key={u.id} className="py-2 d-flex justify-content-between align-items-center">
                    <div>
                      <strong className="text-secondary" style={{ fontSize: '0.85rem' }}>{u.username}</strong>
                      <span className="d-block text-muted" style={{ fontSize: '0.75rem' }}>{u.full_name}</span>
                    </div>
                    <span className="badge bg-secondary" style={{ fontSize: '0.65rem' }}>{u.role.name}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Audit Trail List */}
        <div className="col-lg-8 col-md-12">
          <div className="card slaf-card p-4">
            <h5 className="mb-3 display-font border-bottom pb-2">Active Portal Audit Trails</h5>
            {loading ? (
              <div className="text-center py-5">
                <div className="spinner-border text-primary" role="status"></div>
              </div>
            ) : (
              <div className="table-responsive" style={{ maxHeight: '600px', overflowY: 'auto' }}>
                <table className="table slaf-table mb-0">
                  <thead>
                    <tr>
                      <th>User</th>
                      <th>Activity / Action</th>
                      <th>Client Info</th>
                      <th>Details</th>
                      <th>Timestamp</th>
                    </tr>
                  </thead>
                  <tbody>
                    {auditLogs.length === 0 ? (
                      <tr><td colSpan="5" className="text-center text-muted">No activities logged.</td></tr>
                    ) : (
                      auditLogs.map(log => (
                        <tr key={log.id}>
                          <td><strong>{log.user_name}</strong></td>
                          <td><span className="badge bg-light text-dark border">{log.action}</span></td>
                          <td><small className="text-muted">{log.ip_address}</small></td>
                          <td><small style={{ fontSize: '0.75rem' }}>{log.details || '-'}</small></td>
                          <td><small className="text-muted">{new Date(log.created_at).toLocaleString()}</small></td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
export default UserManagement
