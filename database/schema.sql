-- Sri Lanka Air Force Trade Training School (SLAF TTS) Database Schema
-- Target: MySQL 8.0+

CREATE DATABASE IF NOT EXISTS slaf_tts_db;
USE slaf_tts_db;

-- Disable foreign key checks to make recreations easier
SET FOREIGN_KEY_CHECKS = 0;

-- 1. ROLES TABLE
DROP TABLE IF EXISTS roles;
CREATE TABLE roles (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 2. PERMISSIONS TABLE
DROP TABLE IF EXISTS permissions;
CREATE TABLE permissions (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    code VARCHAR(100) UNIQUE NOT NULL,
    description VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 3. ROLE PERMISSIONS LINK TABLE
DROP TABLE IF EXISTS role_permissions;
CREATE TABLE role_permissions (
    role_id VARCHAR(36) NOT NULL,
    permission_id VARCHAR(36) NOT NULL,
    PRIMARY KEY (role_id, permission_id),
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 4. USERS TABLE
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role_id VARCHAR(36) NOT NULL,
    is_active TINYINT(1) DEFAULT 1,
    is_locked TINYINT(1) DEFAULT 0,
    failed_login_attempts INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (role_id) REFERENCES roles(id),
    INDEX idx_user_role (role_id),
    INDEX idx_user_active (is_active)
) ENGINE=InnoDB;

-- 5. COURSES TABLE
DROP TABLE IF EXISTS courses;
CREATE TABLE courses (
    id VARCHAR(36) PRIMARY KEY,
    code VARCHAR(30) UNIQUE NOT NULL,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    duration_weeks INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
) ENGINE=InnoDB;

-- 6. STUDENTS MASTER TABLE (Single Source of Truth - SSOT)
DROP TABLE IF EXISTS students;
CREATE TABLE students (
    id VARCHAR(36) PRIMARY KEY,
    service_number VARCHAR(30) UNIQUE NOT NULL,
    initials VARCHAR(30) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    nic VARCHAR(20) UNIQUE NOT NULL,
    dob DATE NOT NULL,
    gender VARCHAR(10) NOT NULL,
    rank VARCHAR(50) NOT NULL,
    trade VARCHAR(50) NOT NULL,
    course_id VARCHAR(36),
    batch VARCHAR(30) NOT NULL,
    squadron VARCHAR(50) DEFAULT 'Training Squadron',
    unit VARCHAR(50) DEFAULT 'SLAF TTS Ekala',
    posting VARCHAR(100),
    joining_date DATE NOT NULL,
    passing_out_date DATE,
    status VARCHAR(30) DEFAULT 'Active', -- Active, Sick, Leave, Detached, AWOL, Passed Out, Suspended
    phone VARCHAR(20),
    email VARCHAR(100),
    emergency_contact_name VARCHAR(100) NOT NULL,
    emergency_contact_phone VARCHAR(20) NOT NULL,
    blood_group VARCHAR(10) NOT NULL,
    medical_category VARCHAR(50) DEFAULT 'A4G4',
    religion VARCHAR(30) NOT NULL,
    nationality VARCHAR(30) DEFAULT 'Sri Lankan',
    permanent_address TEXT NOT NULL,
    temporary_address TEXT,
    profile_photo_path VARCHAR(255),
    qr_code_data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE SET NULL,
    INDEX idx_student_service_no (service_number),
    INDEX idx_student_status (status),
    INDEX idx_student_course (course_id)
) ENGINE=InnoDB;

-- 7. DAILY PARADE STATE TABLE
DROP TABLE IF EXISTS parade_states;
CREATE TABLE parade_states (
    id VARCHAR(36) PRIMARY KEY,
    student_id VARCHAR(36) NOT NULL,
    date DATE NOT NULL,
    status VARCHAR(30) NOT NULL, -- Present, Sick Report, Hospital, Leave, Temporary Duty, Course Visit, Detached Duty, AWOL
    remarks TEXT,
    updated_by VARCHAR(36),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE SET NULL,
    UNIQUE KEY uq_student_date (student_id, date),
    INDEX idx_parade_date (date),
    INDEX idx_parade_status (status)
) ENGINE=InnoDB;

-- 8. ACCOMMODATION BUILDINGS
DROP TABLE IF EXISTS accommodation_buildings;
CREATE TABLE accommodation_buildings (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    type VARCHAR(30) NOT NULL, -- Officers, Airmen, Airwomen
    capacity INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
) ENGINE=InnoDB;

-- 9. ACCOMMODATION BILLETS
DROP TABLE IF EXISTS accommodation_billets;
CREATE TABLE accommodation_billets (
    id VARCHAR(36) PRIMARY KEY,
    building_id VARCHAR(36) NOT NULL,
    name VARCHAR(100) NOT NULL,
    capacity INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (building_id) REFERENCES accommodation_buildings(id) ON DELETE CASCADE,
    UNIQUE KEY uq_building_billet (building_id, name)
) ENGINE=InnoDB;

-- 10. ACCOMMODATION ROOMS
DROP TABLE IF EXISTS accommodation_rooms;
CREATE TABLE accommodation_rooms (
    id VARCHAR(36) PRIMARY KEY,
    billet_id VARCHAR(36) NOT NULL,
    room_number VARCHAR(30) NOT NULL,
    capacity INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (billet_id) REFERENCES accommodation_billets(id) ON DELETE CASCADE,
    UNIQUE KEY uq_billet_room (billet_id, room_number)
) ENGINE=InnoDB;

-- 11. ACCOMMODATION BEDS
DROP TABLE IF EXISTS accommodation_beds;
CREATE TABLE accommodation_beds (
    id VARCHAR(36) PRIMARY KEY,
    room_id VARCHAR(36) NOT NULL,
    bed_number VARCHAR(30) NOT NULL,
    status VARCHAR(30) DEFAULT 'Vacant', -- Vacant, Occupied, Maintenance
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (room_id) REFERENCES accommodation_rooms(id) ON DELETE CASCADE,
    UNIQUE KEY uq_room_bed (room_id, bed_number)
) ENGINE=InnoDB;

-- 12. ACCOMMODATION ALLOCATIONS
DROP TABLE IF EXISTS accommodation_allocations;
CREATE TABLE accommodation_allocations (
    id VARCHAR(36) PRIMARY KEY,
    student_id VARCHAR(36) NOT NULL,
    bed_id VARCHAR(36) NOT NULL,
    allocated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    vacated_at TIMESTAMP NULL,
    status VARCHAR(20) DEFAULT 'Active', -- Active, History
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (bed_id) REFERENCES accommodation_beds(id) ON DELETE CASCADE,
    INDEX idx_alloc_student (student_id),
    INDEX idx_alloc_bed (bed_id),
    INDEX idx_alloc_status (status)
) ENGINE=InnoDB;

-- 13. SUBJECTS TABLE
DROP TABLE IF EXISTS subjects;
CREATE TABLE subjects (
    id VARCHAR(36) PRIMARY KEY,
    course_id VARCHAR(36) NOT NULL,
    code VARCHAR(30) NOT NULL,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    periods INT NOT NULL DEFAULT 40,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    UNIQUE KEY uq_course_subject_code (course_id, code)
) ENGINE=InnoDB;

-- 14. LESSONS TABLE
DROP TABLE IF EXISTS lessons;
CREATE TABLE lessons (
    id VARCHAR(36) PRIMARY KEY,
    subject_id VARCHAR(36) NOT NULL,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 15. LESSON PLANS TABLE
DROP TABLE IF EXISTS lesson_plans;
CREATE TABLE lesson_plans (
    id VARCHAR(36) PRIMARY KEY,
    lesson_id VARCHAR(36) NOT NULL,
    instructor_id VARCHAR(36) NOT NULL,
    duration_minutes INT DEFAULT 45,
    objectives TEXT,
    training_aids TEXT,
    references_used TEXT,
    plan_doc_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (lesson_id) REFERENCES lessons(id) ON DELETE CASCADE,
    FOREIGN KEY (instructor_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 16. TIMETABLE TABLE
DROP TABLE IF EXISTS timetables;
CREATE TABLE timetables (
    id VARCHAR(36) PRIMARY KEY,
    course_id VARCHAR(36) NOT NULL,
    date DATE NOT NULL,
    period_number INT NOT NULL, -- e.g., 1, 2, 3, 4, 5, 6, 7, 8
    subject_id VARCHAR(36) NOT NULL,
    lesson_id VARCHAR(36) NOT NULL,
    instructor_id VARCHAR(36) NOT NULL,
    location VARCHAR(100) DEFAULT 'Main Lecture Hall',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
    FOREIGN KEY (lesson_id) REFERENCES lessons(id) ON DELETE CASCADE,
    FOREIGN KEY (instructor_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY uq_course_date_period (course_id, date, period_number)
) ENGINE=InnoDB;

-- 17. ACADEMIC ATTENDANCE TABLE
DROP TABLE IF EXISTS academic_attendance;
CREATE TABLE academic_attendance (
    id VARCHAR(36) PRIMARY KEY,
    timetable_id VARCHAR(36) NOT NULL,
    student_id VARCHAR(36) NOT NULL,
    status VARCHAR(20) DEFAULT 'Present', -- Present, Absent, Excused
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (timetable_id) REFERENCES timetables(id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    UNIQUE KEY uq_timetable_student (timetable_id, student_id),
    INDEX idx_acad_attendance_student (student_id)
) ENGINE=InnoDB;

-- 18. EXAMS TABLE
DROP TABLE IF EXISTS exams;
CREATE TABLE exams (
    id VARCHAR(36) PRIMARY KEY,
    course_id VARCHAR(36) NOT NULL,
    subject_id VARCHAR(36) NOT NULL,
    type VARCHAR(30) NOT NULL, -- Phase Test, Final Exam
    date DATE NOT NULL,
    max_marks DOUBLE DEFAULT 100.0,
    pass_marks DOUBLE DEFAULT 50.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 19. EXAM MARKS TABLE
DROP TABLE IF EXISTS exam_marks;
CREATE TABLE exam_marks (
    id VARCHAR(36) PRIMARY KEY,
    exam_id VARCHAR(36) NOT NULL,
    student_id VARCHAR(36) NOT NULL,
    marks_obtained DOUBLE NOT NULL,
    status VARCHAR(20) NOT NULL, -- Pass, Fail, Absent
    remarks TEXT,
    entered_by VARCHAR(36),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (exam_id) REFERENCES exams(id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (entered_by) REFERENCES users(id) ON DELETE SET NULL,
    UNIQUE KEY uq_exam_student (exam_id, student_id),
    INDEX idx_exam_marks_student (student_id)
) ENGINE=InnoDB;

-- 20. AUDIT LOGS TABLE
DROP TABLE IF EXISTS audit_logs;
CREATE TABLE audit_logs (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36),
    action VARCHAR(100) NOT NULL, -- e.g. CREATE_STUDENT, UPDATE_PARADE_STATE
    ip_address VARCHAR(45),
    user_agent TEXT,
    details TEXT, -- JSON-formatted or string details of changes
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_audit_created_at (created_at)
) ENGINE=InnoDB;

-- 21. LOGIN HISTORY TABLE
DROP TABLE IF EXISTS login_history;
CREATE TABLE login_history (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36),
    status VARCHAR(20) NOT NULL, -- SUCCESS, FAILED, LOCKED
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_login_created_at (created_at)
) ENGINE=InnoDB;

-- 22. NOTIFICATIONS TABLE
DROP TABLE IF EXISTS notifications;
CREATE TABLE notifications (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36),
    title VARCHAR(150) NOT NULL,
    message TEXT NOT NULL,
    type VARCHAR(20) DEFAULT 'INFO', -- INFO, WARNING, ALERT
    is_read TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_notif_user_unread (user_id, is_read)
) ENGINE=InnoDB;

SET FOREIGN_KEY_CHECKS = 1;

-- SEED DATA SETUP

-- Seed Default Roles
INSERT INTO roles (id, name, description) VALUES
('role-super-admin', 'Super Administrator', 'Full control over users, security configurations, backups, and settings.'),
('role-sys-admin', 'System Administrator', 'Manages core database entries, logs, and system operations.'),
('role-discipline', 'Discipline Section', 'Manages daily parade state, student profiles, statuses, and logs.'),
('role-academic', 'Academic Section', 'Manages courses, subject syllabus, lesson plans, exams, and marks entry.'),
('role-accommodation', 'Accommodation Officer', 'Manages billets, rooms, beds, and trainee room allocations.'),
('role-instructor', 'Instructor', 'Manages class registers, lesson plans, and marks entry.'),
('role-co', 'Commanding Officer', 'High-level dashboard visibility, executive reports, and approval rights.'),
('role-viewer', 'Viewer', 'Read-only access to dashboard data and reports.');

-- Seed Permissions
INSERT INTO permissions (id, name, code, description) VALUES
('perm-student-read', 'Read Student Profile', 'student:read', 'Ability to view trainee data'),
('perm-student-write', 'Create/Edit Student Profile', 'student:write', 'Ability to add or edit trainee data'),
('perm-parade-read', 'Read Parade State', 'parade:read', 'Ability to view daily parade state strength'),
('perm-parade-write', 'Update Parade State', 'parade:write', 'Ability to record daily status boards'),
('perm-room-read', 'Read Accommodation Map', 'room:read', 'Ability to inspect vacancy charts'),
('perm-room-write', 'Allocate Accommodation', 'room:write', 'Ability to edit room registers and transfers'),
('perm-academic-read', 'Read Grades & Timetable', 'academic:read', 'Ability to view schedules and marks'),
('perm-academic-write', 'Manage Academics', 'academic:write', 'Ability to record marks and edit timetables'),
('perm-audit-read', 'Read Audit Logs', 'system:audit', 'Ability to review security logs');

-- Seed Role Permissions Mapping for Admin and Commanding Officer
INSERT INTO role_permissions (role_id, permission_id) VALUES
('role-super-admin', 'perm-student-read'), ('role-super-admin', 'perm-student-write'),
('role-super-admin', 'perm-parade-read'), ('role-super-admin', 'perm-parade-write'),
('role-super-admin', 'perm-room-read'), ('role-super-admin', 'perm-room-write'),
('role-super-admin', 'perm-academic-read'), ('role-super-admin', 'perm-academic-write'),
('role-super-admin', 'perm-audit-read'),
('role-co', 'perm-student-read'), ('role-co', 'perm-parade-read'), 
('role-co', 'perm-room-read'), ('role-co', 'perm-academic-read');

-- Seed Default Admin User (username: admin, password: hashed Admin@123 using bcrypt)
-- bcrypt hash of "Admin@123" = $2b$12$mtZ8.IsD3Dt60K8x73tpgOC8sWZRzKKx0sU.O5zvzsfAzyOSNc4kG
INSERT INTO users (id, username, email, hashed_password, full_name, role_id, is_active) VALUES
('user-slaf-admin', 'admin', 'admin@slaf.lk', '$2b$12$mtZ8.IsD3Dt60K8x73tpgOC8sWZRzKKx0sU.O5zvzsfAzyOSNc4kG', 'SLAF Administrator', 'role-super-admin', 1);

-- Seed Default Courses
INSERT INTO courses (id, code, name, description, duration_weeks) VALUES
('course-basic-airframe', 'BA-AER-01', 'Basic Airframe Mechanics Course', 'Introductory training program for SLAF airframe technicians on structural integrity and aircraft maintenance.', 24),
('course-basic-avionics', 'BA-AV-01', 'Basic Avionics Maintenance Course', 'Fundamental course in aircraft electrical systems, radar instruments, and communications navigation.', 24),
('course-basic-safety', 'BA-SE-01', 'Basic Safety Equipment Fitters Course', 'Instruction in parachute systems, life preservation equipment, and survival tactics.', 16);

-- Seed Default Subjects for Basic Airframe
INSERT INTO subjects (id, course_id, code, name, description, periods) VALUES
('subj-aer-aerodynamics', 'course-basic-airframe', 'AER-101', 'Aerodynamics Principles', 'Fundamentals of flight mechanics, lift, drag, and control surface operations.', 40),
('subj-aer-structures', 'course-basic-airframe', 'AER-102', 'Aircraft Structural Materials', 'Understanding aluminium alloys, composites, and fatigue analysis.', 60),
('subj-aer-maintenance', 'course-basic-airframe', 'AER-103', 'Practical Maintenance Practice', 'Hands-on training in line servicing and routine inspections.', 80);

-- Seed Default Lessons for Aerodynamics
INSERT INTO lessons (id, subject_id, name, description) VALUES
('less-aero-bernoulli', 'subj-aer-aerodynamics', 'Bernoullis Principle & Fluid Flow', 'Study of pressure differentials, Venturi tubes, and stream flows.'),
('less-aero-airfoils', 'subj-aer-aerodynamics', 'Airfoil Geometry and Lift Mechanics', 'Analyzing chord lines, camber, angle of attack, and stall profiles.');

-- Seed Default Accommodation Buildings, Billets, Rooms, Beds
INSERT INTO accommodation_buildings (id, name, type, capacity) VALUES
('bldg-t1', 'Training Block Alpha (T1)', 'Airmen', 48);

INSERT INTO accommodation_billets (id, building_id, name, capacity) VALUES
('bill-t1-a', 'bldg-t1', 'Billet Alpha-1', 24);

INSERT INTO accommodation_rooms (id, billet_id, room_number, capacity) VALUES
('room-t1-a-101', 'bill-t1-a', 'Room 101', 4);

INSERT INTO accommodation_beds (id, room_id, bed_number, status) VALUES
('bed-t1-a-101-1', 'room-t1-a-101', 'Bed 01', 'Vacant'),
('bed-t1-a-101-2', 'room-t1-a-101', 'Bed 02', 'Vacant'),
('bed-t1-a-101-3', 'room-t1-a-101', 'Bed 03', 'Vacant'),
('bed-t1-a-101-4', 'room-t1-a-101', 'Bed 04', 'Vacant');
