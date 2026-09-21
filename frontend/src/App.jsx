import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { ToastContainer } from 'react-toastify'
import { AuthProvider } from './context/AuthContext'
import { ThemeProvider } from './context/ThemeContext'
import { ProtectedRoute } from './components/ProtectedRoute'
import Layout from './components/Layout'

// Pages import
import Landing from './pages/Landing'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import StudentList from './pages/Students/StudentList'
import StudentDetail from './pages/Students/StudentDetail'
import StudentForm from './pages/Students/StudentForm'
import PersonalOccurrenceReporting from './pages/Students/PersonalOccurrenceReporting'

import DailyParade from './pages/ParadeState/DailyParade'
import AccommodationPanel from './pages/Accommodation/AccommodationPanel'
import CourseList from './pages/Academic/CourseList'
import ReportGenerator from './pages/Reports/ReportGenerator'
import UserManagement from './pages/Admin/UserManagement'
import UserProfile from './pages/Admin/UserProfile'
import AccessDenied from './components/AccessDenied'

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
          <Routes>
            {/* Public routes */}
            <Route path="/" element={<Landing />} />
            <Route path="/login" element={<Login />} />

            {/* Shielded routes inside Layout shell */}
            <Route element={<ProtectedRoute />}>
              <Route element={<Layout />}>
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/profile" element={<UserProfile />} />
                <Route path="/access-denied" element={<AccessDenied />} />
                
                {/* Student Management */}
                <Route element={<ProtectedRoute permissionCode="student:read" moduleName="Student & Trainee Management" />}>
                  <Route path="/students" element={<StudentList />} />
                  <Route path="/students/:id" element={<StudentDetail />} />
                </Route>
                <Route element={<ProtectedRoute permissionCode="personal_occurrence:read" moduleName="Personal Occurrence Reporting" />}>
                  <Route path="/students/occurrences" element={<PersonalOccurrenceReporting />} />
                </Route>
                <Route element={<ProtectedRoute permissionCode="student:write" moduleName="Trainee Registration & Editing" />}>
                  <Route path="/students/new" element={<StudentForm />} />
                  <Route path="/students/:id/edit" element={<StudentForm />} />
                </Route>

                {/* Parade State */}
                <Route element={<ProtectedRoute permissionCode="parade:read" moduleName="Daily Parade State & Muster" />}>
                  <Route path="/parade" element={<DailyParade />} />
                </Route>

                {/* Accommodation */}
                <Route element={<ProtectedRoute permissionCode="room:read" moduleName="Accommodation & Housing Management" />}>
                  <Route path="/accommodation" element={<AccommodationPanel />} />
                  <Route path="/accommodation/:subview" element={<AccommodationPanel />} />
                </Route>

                {/* Academics */}
                <Route element={<ProtectedRoute permissionCode="academic:read" moduleName="Academic Activities & Course Syllabus" />}>
                  <Route path="/academic" element={<CourseList />} />
                </Route>

                {/* Reports */}
                <Route element={<ProtectedRoute permissionCode="reports:read" moduleName="Institutional Reports & Analytics" />}>
                  <Route path="/reports" element={<ReportGenerator />} />
                </Route>

                {/* System Administration */}
                <Route element={<ProtectedRoute permissionCode="system:audit" moduleName="System Administration & RBAC Security" />}>
                  <Route path="/admin" element={<UserManagement />} />
                  <Route path="/admin/:subview" element={<UserManagement />} />
                </Route>
              </Route>
            </Route>

            {/* Default Catch-all */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </BrowserRouter>
        
        <ToastContainer 
          position="bottom-right"
          autoClose={4000}
          hideProgressBar={false}
          newestOnTop={false}
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
          theme="colored"
        />
      </AuthProvider>
    </ThemeProvider>
  )
}
export default App
