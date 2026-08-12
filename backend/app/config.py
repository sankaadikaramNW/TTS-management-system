import os
from dotenv import load_dotenv

# Try loading .env from parent directories (e.g. root folder)
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env'))
# Also fallback to local .env if any
load_dotenv()

class Settings:
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # DB configuration
    DB_ENGINE: str = os.getenv("DB_ENGINE", "sqlite")
    DB_FILE: str = os.getenv("DB_FILE", "./database.db")
    
    MYSQL_HOST: str = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT: int = int(os.getenv("MYSQL_PORT", "3306"))
    MYSQL_USER: str = os.getenv("MYSQL_USER", "slaf_admin")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "SlafAdminSecretPass123!")
    MYSQL_DATABASE: str = os.getenv("MYSQL_DATABASE", "slaf_tts_db")
    
    # JWT authentication settings
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "45c4779fe379d71c89f5bc3a6c2f0f4a86161474ea595d73bb851d7cf9d2c180")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
    
    # Seed details
    ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "Admin@123")
    ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL", "admin@slaf.lk")
    
    # UPLOAD paths
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")

    # Cloudinary Configuration (Lesson Plan Document Storage)
    CLOUDINARY_CLOUD_NAME: str = os.getenv("CLOUDINARY_CLOUD_NAME", "")
    CLOUDINARY_API_KEY: str = os.getenv("CLOUDINARY_API_KEY", "")
    CLOUDINARY_API_SECRET: str = os.getenv("CLOUDINARY_API_SECRET", "")

    # Lesson Plan Document Settings
    MAX_LESSON_PLAN_FILE_SIZE_MB: int = int(os.getenv("MAX_LESSON_PLAN_FILE_SIZE_MB", "20"))

    @property
    def database_url(self) -> str:
        if self.DB_ENGINE == "mysql":
            return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"
        # SQLite default fallback
        return f"sqlite:///{self.DB_FILE}"

settings = Settings()

# Ensure directories exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(os.path.dirname(settings.DB_FILE) or ".", exist_ok=True)
