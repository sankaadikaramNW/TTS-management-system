from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

# For SQLite, we need connect_args to allow multithreading
connect_args = {}
if settings.DB_ENGINE == "sqlite":
    connect_args = {"check_same_thread": False}

if settings.DB_ENGINE == "mysql":
    try:
        mysql_connect_args = dict(connect_args)
        mysql_connect_args["connect_timeout"] = 3
        engine = create_engine(
            settings.database_url,
            pool_pre_ping=True,
            pool_recycle=3600,
            pool_size=20,
            max_overflow=30,
            connect_args=mysql_connect_args
        )
        # Test connection immediately so fallback to SQLite triggers if MySQL is unreachable
        with engine.connect() as conn:
            pass
    except Exception as e:
        print(f"\n[WARNING] Could not connect to MySQL server ({e}). Falling back to SQLite local database.\n")
        sqlite_url = f"sqlite:///{settings.DB_FILE}"
        engine = create_engine(
            sqlite_url,
            pool_pre_ping=True,
            pool_recycle=3600,
            connect_args={"check_same_thread": False}
        )
else:
    engine = create_engine(
        settings.database_url,
        pool_pre_ping=True,
        pool_recycle=3600,
        connect_args=connect_args
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
