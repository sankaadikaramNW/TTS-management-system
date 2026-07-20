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
            hashed_password='$2b$12$R9h/lIPzNgbC.V.aGvQ8X.7w/KpxsX.uR.y6bN50H1DqZf6sZ0eU2', # Admin@123
            full_name='SLAF Administrator',
            role_id='role-super-admin',
            is_active=True
        )
        db.add(admin_user)
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
