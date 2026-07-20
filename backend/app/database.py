from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

# For SQLite, we need connect_args to allow multithreading
connect_args = {}
if settings.DB_ENGINE == "sqlite":
    connect_args = {"check_same_thread": False}

try:
    engine = create_engine(
        settings.database_url,
        pool_pre_ping=True,
        connect_args=connect_args
    )
except Exception as e:
    # If connection fails (e.g. MySQL is down), fallback to sqlite so the application is still runnable
    print(f"Warning: Failed to connect to MySQL database at {settings.database_url}. Falling back to SQLite local database.")
    sqlite_url = f"sqlite:///./database.db"
    engine = create_engine(
        sqlite_url,
        pool_pre_ping=True,
        connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
