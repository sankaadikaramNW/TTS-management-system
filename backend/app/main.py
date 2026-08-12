import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import engine, Base, SessionLocal
from app.routers import auth, student, parade, accommodation, academic, dashboard, system, public

# Import ALL models before create_all so SQLAlchemy can resolve all cross-model relationships
import app.models  # noqa: F401 — loads __init__.py which imports every model

# Create tables if they do not exist
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Error creating database tables: {e}")

from sqlalchemy import text

# Lightweight schema migration helper for SQLite & MySQL
def run_lightweight_migrations():
    with engine.connect() as conn:
        migrations = [
            ("roles", "is_active", "BOOLEAN DEFAULT 1"),
            ("permissions", "module", "VARCHAR(50) DEFAULT 'General'"),
            ("users", "service_number", "VARCHAR(50) NULL"),
            ("users", "rank", "VARCHAR(50) NULL"),
            ("users", "mobile_number", "VARCHAR(20) NULL"),
            ("users", "department", "VARCHAR(100) NULL"),
            ("users", "designation", "VARCHAR(100) NULL"),
            ("users", "assigned_module", "VARCHAR(100) NULL"),
            ("users", "profile_photo", "VARCHAR(255) NULL"),
            ("users", "must_change_password", "BOOLEAN DEFAULT 0"),
            ("users", "password_changed_at", "DATETIME NULL"),
            ("users", "deleted_at", "DATETIME NULL"),
            ("login_history", "username", "VARCHAR(50) NULL"),
            ("login_history", "logout_time", "DATETIME NULL"),
            ("audit_logs", "username", "VARCHAR(50) NULL"),
            ("audit_logs", "module", "VARCHAR(50) DEFAULT 'User Management'"),
            ("audit_logs", "action", "VARCHAR(100) NULL"),
            ("audit_logs", "previous_value", "TEXT NULL"),
            ("audit_logs", "new_value", "TEXT NULL"),
            ("parade_states", "submission_id", "VARCHAR(36) NULL"),
            ("trades", "description", "TEXT NULL"),
            ("courses", "trade_id", "VARCHAR(36) NULL"),
            ("courses", "course_type", "VARCHAR(50) DEFAULT 'Basic'"),
            ("courses", "intake_capacity", "INT DEFAULT 30"),
            ("courses", "start_date", "DATE NULL"),
            ("courses", "end_date", "DATE NULL"),
            ("courses", "is_active", "BOOLEAN DEFAULT 1"),
        ]
        for table, col, col_def in migrations:
            try:
                conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {col} {col_def}"))
                conn.commit()
            except Exception:
                pass  # Column already exists

        # Create parade_submissions table if not exists
        try:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS parade_submissions (
                    id VARCHAR(36) PRIMARY KEY,
                    date DATE NOT NULL,
                    trade VARCHAR(50) NOT NULL,
                    submitted_by VARCHAR(36) NULL,
                    approving_officer_id VARCHAR(36) NULL,
                    status ENUM('DRAFT','SUBMITTED','APPROVED','REJECTED') NOT NULL DEFAULT 'DRAFT',
                    submitter_remarks TEXT NULL,
                    approver_remarks TEXT NULL,
                    rejection_reason TEXT NULL,
                    submitted_at DATETIME NULL,
                    reviewed_at DATETIME NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX idx_ps_date (date),
                    INDEX idx_ps_trade (trade),
                    INDEX idx_ps_officer (approving_officer_id)
                )
            """))
            conn.commit()
        except Exception:
            pass

        # Create officer_in_charge table if not exists
        try:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS officer_in_charge (
                    id VARCHAR(36) PRIMARY KEY,
                    trade VARCHAR(50) NOT NULL,
                    user_id VARCHAR(36) NOT NULL,
                    appointed_by VARCHAR(36) NULL,
                    is_active BOOLEAN DEFAULT 1,
                    appointed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX idx_oic_trade (trade),
                    INDEX idx_oic_user (user_id)
                )
            """))
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS role_permissions (
                    role_id VARCHAR(36) NOT NULL,
                    permission_id VARCHAR(36) NOT NULL,
                    PRIMARY KEY (role_id, permission_id)
                )
            """))
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS user_permissions (
                    user_id VARCHAR(36) NOT NULL,
                    permission_id VARCHAR(36) NOT NULL,
                    PRIMARY KEY (user_id, permission_id)
                )
            """))
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS lesson_plan_documents (
                    id VARCHAR(36) PRIMARY KEY,
                    course_id VARCHAR(36) NOT NULL,
                    lesson_id VARCHAR(36) NULL,
                    title VARCHAR(255) NOT NULL,
                    description TEXT NULL,
                    subject_name VARCHAR(150) NULL,
                    version VARCHAR(20) NULL,
                    academic_year VARCHAR(20) NULL,
                    remarks TEXT NULL,
                    original_file_name VARCHAR(255) NOT NULL,
                    cloudinary_public_id VARCHAR(255) NOT NULL,
                    cloudinary_url VARCHAR(500) NOT NULL,
                    resource_type VARCHAR(30) DEFAULT 'raw',
                    file_size INT NOT NULL,
                    mime_type VARCHAR(50) DEFAULT 'application/pdf',
                    uploaded_by VARCHAR(36) NULL,
                    status VARCHAR(20) DEFAULT 'Active',
                    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX idx_lpd_course (course_id),
                    INDEX idx_lpd_uploaded_by (uploaded_by),
                    INDEX idx_lpd_status (status),
                    INDEX idx_lpd_uploaded_at (uploaded_at)
                )
            """))
            conn.commit()
        except Exception:
            pass

        # Alter existing columns to allow NULL in MySQL if table already exists
        modify_sqls = [
            "ALTER TABLE students MODIFY COLUMN nic VARCHAR(20) NULL",
            "ALTER TABLE students MODIFY COLUMN dob DATE NULL",
            "ALTER TABLE students MODIFY COLUMN initials VARCHAR(30) NULL",
            "ALTER TABLE students MODIFY COLUMN joining_date DATE NULL",
            "ALTER TABLE students MODIFY COLUMN emergency_contact_name VARCHAR(100) NULL",
            "ALTER TABLE students MODIFY COLUMN emergency_contact_phone VARCHAR(20) NULL",
            "ALTER TABLE students MODIFY COLUMN permanent_address TEXT NULL",
            "ALTER TABLE students MODIFY COLUMN religion VARCHAR(30) NULL",
            "ALTER TABLE students MODIFY COLUMN blood_group VARCHAR(10) NULL"
        ]
        for m_sql in modify_sqls:
            try:
                conn.execute(text(m_sql))
                conn.commit()
            except Exception:
                pass

run_lightweight_migrations()

# Auto seed check
def auto_seed_database():
    db = SessionLocal()
    try:
        from app.models.user import Role, Permission, User
        from app.models.academic import Course, Subject
        from app.models.accommodation import AccommodationBuilding, AccommodationBillet, AccommodationBed
        from app.models.student import ParadeStatusType, StudentStatusType, Rank, Trade, OfficerInCharge, ParadeSubmission
        
        # 1. Seed Roles
        if db.query(Role).count() == 0:
            roles = [
                Role(id='role-super-admin', name='Super Administrator', description='Full control over users, security configurations, backups, and settings.'),
                Role(id='role-sys-admin', name='System Administrator', description='Manages core database entries, logs, and system operations.'),
                Role(id='role-discipline', name='Discipline Section', description='Manages daily parade state, student profiles, statuses, and logs.'),
                Role(id='role-academic', name='Academic Section', description='Manages courses, subject syllabus, lesson plans, exams, and marks entry.'),
                Role(id='role-accommodation', name='Accommodation Officer', description='Manages billets, rooms, beds, and trainee room allocations.'),
                Role(id='role-instructor', name='Instructor', description='Manages class registers, lesson plans, and marks entry.'),
                Role(id='role-co', name='Commanding Officer', description='High-level dashboard visibility, executive reports, and approval rights.'),
                Role(id='role-viewer', name='Viewer', description='Read-only access to dashboard data and reports.')
            ]
            db.bulk_save_objects(roles)
            db.commit()

        # 2. Seed Permissions
        if db.query(Permission).count() == 0:
            permissions = [
                Permission(id='perm-student-read', name='Read Student Profile', code='student:read', description='Ability to view trainee data'),
                Permission(id='perm-student-write', name='Create/Edit Student Profile', code='student:write', description='Ability to add or edit trainee data'),
                Permission(id='perm-parade-read', name='Read Parade State', code='parade:read', description='Ability to view daily parade state strength'),
                Permission(id='perm-parade-write', name='Update Parade State', code='parade:write', description='Ability to record daily status boards'),
                Permission(id='perm-parade-approve', name='Approve Parade State', code='parade:approve', description='Ability to approve or reject submitted parade states as Officer I/C'),
                Permission(id='perm-parade-officers', name='Manage Officer I/C Assignments', code='parade:manage_officers', description='Ability to appoint and remove Officer I/C assignments by trade'),
                Permission(id='perm-room-read', name='Read Accommodation Map', code='room:read', description='Ability to inspect vacancy charts'),
                Permission(id='perm-room-write', name='Allocate Accommodation', code='room:write', description='Ability to edit room registers and transfers'),
                Permission(id='perm-academic-read', name='Read Grades & Timetable', code='academic:read', description='Ability to view schedules and marks'),
                Permission(id='perm-academic-write', name='Manage Academics', code='academic:write', description='Ability to record marks and edit timetables'),
                Permission(id='perm-reports-read', name='Read Reports & Analytics', code='reports:read', description='Ability to generate reports and analytics'),
                Permission(id='perm-audit-read', name='Read Audit Logs', code='system:audit', description='Ability to review security logs')
            ]
            db.bulk_save_objects(permissions)
            db.commit()
            
            # Map Super Admin & System Admin permissions
            all_perms = db.query(Permission).all()
            for r_id in ['role-super-admin', 'role-sys-admin']:
                r = db.query(Role).filter(Role.id == r_id).first()
                if r:
                    r.permissions = list(all_perms)
            
            # Map CO permissions (Executive overview, trainees, parade state, reports)
            co_role = db.query(Role).filter(Role.id == 'role-co').first()
            if co_role:
                co_role.permissions = db.query(Permission).filter(Permission.code.in_([
                    'student:read', 'parade:read', 'parade:approve', 'reports:read'
                ])).all()

            # Map Discipline Section permissions
            discipline_role = db.query(Role).filter(Role.id == 'role-discipline').first()
            if discipline_role:
                discipline_role.permissions = db.query(Permission).filter(Permission.code.in_([
                    'student:read', 'parade:read', 'parade:write', 'parade:approve', 'parade:manage_officers', 'reports:read'
                ])).all()

            # Map Academic Section permissions
            academic_role = db.query(Role).filter(Role.id == 'role-academic').first()
            if academic_role:
                academic_role.permissions = db.query(Permission).filter(Permission.code.in_([
                    'student:read', 'academic:read', 'academic:write', 'reports:read'
                ])).all()

            # Map Accommodation Officer permissions
            accommodation_role = db.query(Role).filter(Role.id == 'role-accommodation').first()
            if accommodation_role:
                accommodation_role.permissions = db.query(Permission).filter(Permission.code.in_([
                    'student:read', 'room:read', 'room:write', 'reports:read'
                ])).all()

            # Map Instructor permissions
            instructor_role = db.query(Role).filter(Role.id == 'role-instructor').first()
            if instructor_role:
                instructor_role.permissions = db.query(Permission).filter(Permission.code.in_([
                    'student:read', 'academic:read', 'academic:write'
                ])).all()

            # Map Viewer permissions
            viewer_role = db.query(Role).filter(Role.id == 'role-viewer').first()
            if viewer_role:
                viewer_role.permissions = db.query(Permission).filter(Permission.code.in_([
                    'student:read', 'parade:read'
                ])).all()

            db.commit()

        # 3. Seed Default Admin User
        if db.query(User).count() == 0:
            # Hash of "Admin@123" = $2b$12$mtZ8.IsD3Dt60K8x73tpgOC8sWZRzKKx0sU.O5zvzsfAzyOSNc4kG
            admin_user = User(
                id='user-slaf-admin',
                username='admin',
                email='admin@slaf.lk',
                hashed_password='$2b$12$mtZ8.IsD3Dt60K8x73tpgOC8sWZRzKKx0sU.O5zvzsfAzyOSNc4kG',
                full_name='SLAF Administrator',
                role_id='role-super-admin',
                is_active=True
            )
            db.add(admin_user)
            db.commit()

        # 4. Seed Default Courses
        if db.query(Course).count() == 0:
            courses = [
                Course(id='course-basic-airframe', code='BA-AER-01', name='Basic Airframe Mechanics Course', description='Introductory training program for SLAF airframe technicians on structural integrity and aircraft maintenance.', duration_weeks=24),
                Course(id='course-basic-avionics', code='BA-AV-01', name='Basic Avionics Maintenance Course', description='Fundamental course in aircraft electrical systems, radar instruments, and communications navigation.', duration_weeks=24),
                Course(id='course-basic-safety', code='BA-SE-01', name='Basic Safety Equipment Fitters Course', description='Instruction in parachute systems, life preservation equipment, and survival tactics.', duration_weeks=16)
            ]
            db.bulk_save_objects(courses)
            db.commit()

        # 5. Seed default accommodation buildings/billets/beds
        if db.query(AccommodationBuilding).count() == 0:
            bldg = AccommodationBuilding(id='bldg-t1', name='Training Block Alpha (T1)', type='Airmen', capacity=48)
            db.add(bldg)
            db.commit()
            
            billet = AccommodationBillet(id='bill-t1-a', building_id='bldg-t1', name='Billet Alpha-1', capacity=24)
            db.add(billet)
            db.commit()
            
            beds = [
                AccommodationBed(id='bed-t1-a-1', billet_id='bill-t1-a', bed_number='Bed 01', status='Vacant'),
                AccommodationBed(id='bed-t1-a-2', billet_id='bill-t1-a', bed_number='Bed 02', status='Vacant'),
                AccommodationBed(id='bed-t1-a-3', billet_id='bill-t1-a', bed_number='Bed 03', status='Vacant'),
                AccommodationBed(id='bed-t1-a-4', billet_id='bill-t1-a', bed_number='Bed 04', status='Vacant')
            ]
            db.bulk_save_objects(beds)
            db.commit()

        # 6. Seed Public Notices (Notifications with user_id = None)
        from app.models.notification import Notification
        if db.query(Notification).filter(Notification.user_id == None).count() == 0:
            notices = [
                Notification(id='notice-1', user_id=None, title='New Batch Registration', message='New batch registration starts next week. Please ensure all student documents are prepared.', type='INFO'),
                Notification(id='notice-2', user_id=None, title='Timetable Release', message='Examination timetable for BA-AER-01 has been released on the portal.', type='INFO'),
                Notification(id='notice-3', user_id=None, title='Accommodation Inspection', message='Billet inspection scheduled for Training Block Alpha this Friday at 0900 hrs.', type='WARNING'),
                Notification(id='notice-4', user_id=None, title='Parade State Submission', message='Reminder: Daily parade state must be submitted before 0800 hrs daily.', type='ALERT')
            ]
            db.bulk_save_objects(notices)
            db.commit()

        # 7. Seed Parade Status Types
        if db.query(ParadeStatusType).count() == 0:
            status_types = [
                ParadeStatusType(code='PRESENT', label='Present'),
                ParadeStatusType(code='SICK_REPORT', label='Sick Report'),
                ParadeStatusType(code='HOSPITAL', label='Hospital'),
                ParadeStatusType(code='LEAVE', label='Leave'),
                ParadeStatusType(code='TEMPORARY_DUTY', label='Temporary Duty'),
                ParadeStatusType(code='COURSE_VISIT', label='Course Visit'),
                ParadeStatusType(code='DETACHED_DUTY', label='Detached Duty'),
                ParadeStatusType(code='AWOL', label='AWOL')
            ]
            db.bulk_save_objects(status_types)
            db.commit()

        # 8. Seed Student Status Types
        if db.query(StudentStatusType).count() == 0:
            student_statuses = [
                StudentStatusType(id='ss-active', code='ACTIVE', label='Active'),
                StudentStatusType(id='ss-sick-report', code='SICK_REPORT', label='Sick Report'),
                StudentStatusType(id='ss-leave', code='LEAVE', label='Leave'),
                StudentStatusType(id='ss-awol', code='AWOL', label='AWOL'),
                StudentStatusType(id='ss-passed-out', code='PASSED_OUT', label='Passed Out'),
                StudentStatusType(id='ss-suspended', code='SUSPENDED', label='Suspended')
            ]
            db.bulk_save_objects(student_statuses)
            db.commit()

        # 9. Seed Ranks
        if db.query(Rank).count() == 0:
            ranks = [
                Rank(id='rank-ac', code='AC', label='Aircraftman'),
                Rank(id='rank-lac', code='LAC', label='Leading Aircraftman'),
                Rank(id='rank-cpl', code='CPL', label='Corporal'),
                Rank(id='rank-sgt', code='SGT', label='Sergeant'),
                Rank(id='rank-fsgt', code='FSGT', label='Flight Sergeant'),
                Rank(id='rank-wo', code='WO', label='Warrant Officer')
            ]
            db.bulk_save_objects(ranks)
            db.commit()

        # 10. Seed Trades
        if db.query(Trade).count() == 0:
            trades = [
                Trade(id='trade-airframe', code='AIRFRAME', label='Airframe'),
                Trade(id='trade-avionics', code='AVIONICS', label='Avionics'),
                Trade(id='trade-safety', code='SAFETY_EQUIPMENT', label='Safety Equipment'),
                Trade(id='trade-engine', code='ENGINE', label='Engine'),
                Trade(id='trade-logistical', code='LOGISTICAL', label='Logistical'),
                Trade(id='trade-admin', code='ADMINISTRATIVE', label='Administrative')
            ]
            db.bulk_save_objects(trades)
            db.commit()

    except Exception as e:
        print(f"Error seeding database: {e}")
    finally:
        db.close()

# Run Auto Seeding
auto_seed_database()

# Initialize FastAPI App
app = FastAPI(
    title="SLAF TTS Management Portal REST API",
    description="Centralized REST backend API for Sri Lanka Air Force Trade Training School",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/api/v1/openapi.json"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure uploads directories are mounted for static access (e.g. photos)
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/static/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="static_uploads")

# Include Routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(student.router, prefix="/api/v1")
app.include_router(parade.router, prefix="/api/v1")
app.include_router(accommodation.router, prefix="/api/v1")
app.include_router(academic.router, prefix="/api/v1")
app.include_router(dashboard.router, prefix="/api/v1")
app.include_router(system.router, prefix="/api/v1")
app.include_router(public.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "SLAF TTS API is running. Check documentation at /docs."}
