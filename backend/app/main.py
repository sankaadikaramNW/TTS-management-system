import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import engine, Base, SessionLocal
from app.routers import auth, student, parade, accommodation, academic, dashboard, system

# Create database tables automatically if they don't exist
Base.metadata.create_all(bind=engine)

# Auto seed check
def auto_seed_database():
    db = SessionLocal()
    try:
        from app.models.user import Role, Permission, User
        from app.models.academic import Course, Subject
        from app.models.accommodation import AccommodationBuilding, AccommodationBillet, AccommodationRoom, AccommodationBed
        
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
                Permission(id='perm-room-read', name='Read Accommodation Map', code='room:read', description='Ability to inspect vacancy charts'),
                Permission(id='perm-room-write', name='Allocate Accommodation', code='room:write', description='Ability to edit room registers and transfers'),
                Permission(id='perm-academic-read', name='Read Grades & Timetable', code='academic:read', description='Ability to view schedules and marks'),
                Permission(id='perm-academic-write', name='Manage Academics', code='academic:write', description='Ability to record marks and edit timetables'),
                Permission(id='perm-audit-read', name='Read Audit Logs', code='system:audit', description='Ability to review security logs')
            ]
            db.bulk_save_objects(permissions)
            db.commit()
            
            # Map Super Admin permissions
            super_admin = db.query(Role).filter(Role.id == 'role-super-admin').first()
            if super_admin:
                all_perms = db.query(Permission).all()
                super_admin.permissions.extend(all_perms)
                db.commit()

            # Map CO permissions
            co_role = db.query(Role).filter(Role.id == 'role-co').first()
            if co_role:
                co_perms = db.query(Permission).filter(Permission.code.in_([
                    'student:read', 'parade:read', 'room:read', 'academic:read'
                ])).all()
                co_role.permissions.extend(co_perms)
                db.commit()

        # 3. Seed Default Admin User
        if db.query(User).count() == 0:
            # Hash of "Admin@123" = $2b$12$R9h/lIPzNgbC.V.aGvQ8X.7w/KpxsX.uR.y6bN50H1DqZf6sZ0eU2
            admin_user = User(
                id='user-slaf-admin',
                username='admin',
                email='admin@slaf.lk',
                hashed_password='$2b$12$R9h/lIPzNgbC.V.aGvQ8X.7w/KpxsX.uR.y6bN50H1DqZf6sZ0eU2',
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
            
            room = AccommodationRoom(id='room-t1-a-101', billet_id='bill-t1-a', room_number='Room 101', capacity=4)
            db.add(room)
            db.commit()
            
            beds = [
                AccommodationBed(id='bed-t1-a-101-1', room_id='room-t1-a-101', bed_number='Bed 01', status='Vacant'),
                AccommodationBed(id='bed-t1-a-101-2', room_id='room-t1-a-101', bed_number='Bed 02', status='Vacant'),
                AccommodationBed(id='bed-t1-a-101-3', room_id='room-t1-a-101', bed_number='Bed 03', status='Vacant'),
                AccommodationBed(id='bed-t1-a-101-4', room_id='room-t1-a-101', bed_number='Bed 04', status='Vacant')
            ]
            db.bulk_save_objects(beds)
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

@app.get("/")
def read_root():
    return {"message": "SLAF TTS API is running. Check documentation at /docs."}
