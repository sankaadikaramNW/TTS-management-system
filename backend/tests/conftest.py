import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.database import Base, get_db
from app.main import app

# Create a test SQLite database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_database.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Seed default roles and admin
    db = TestingSessionLocal()
    from app.models.user import Role, Permission, User
    if db.query(Role).count() == 0:
        admin_role = Role(id='role-super-admin', name='Super Administrator', description='Full admin control')
        db.add(admin_role)
        db.commit()
        
        # Admin user
        admin_user = User(
            id='user-slaf-admin',
            username='admin',
            email='admin@slaf.lk',
            hashed_password='$2b$12$mtZ8.IsD3Dt60K8x73tpgOC8sWZRzKKx0sU.O5zvzsfAzyOSNc4kG', # Admin@123
            full_name='SLAF Administrator',
            role_id='role-super-admin',
            is_active=True
        )
        db.add(admin_user)
        db.commit()

    from app.models.student import StudentStatusType, Rank, Trade
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

    db.close()
    
    yield
    
    # Tear down tables
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
            
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
