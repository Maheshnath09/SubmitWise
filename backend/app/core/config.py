from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application configuration settings"""
    
    # App
    APP_NAME: str = "ProjectGen"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database (use 127.0.0.1:5433 for local dev, postgres:5432 for Docker)
    DATABASE_URL: str = "postgresql://projectgen:projectgen@127.0.0.1:5433/projectgen"
    
    # Redis & Celery (use 127.0.0.1 for local dev, redis for Docker)
    REDIS_URL: str = "redis://127.0.0.1:6379/0"
    CELERY_BROKER_URL: str = "redis://127.0.0.1:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://127.0.0.1:6379/0"
    
    # MinIO (use 127.0.0.1 for local dev, minio for Docker)
    MINIO_ENDPOINT: str = "127.0.0.1:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "projectgen-files"
    MINIO_SECURE: bool = False
    
    # Groq API (MANDATORY - Using Llama 3.3 70B Versatile)
    GROQ_API_KEY: str
    GROQ_API_URL: str = "https://api.groq.com/openai/v1/chat/completions"
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    
    # Security
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production-min-32-chars"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # OAuth
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    
    # Payments
    RAZORPAY_KEY_ID: Optional[str] = None
    RAZORPAY_KEY_SECRET: Optional[str] = None
    STRIPE_SECRET_KEY: Optional[str] = None
    STRIPE_WEBHOOK_SECRET: Optional[str] = None
    
    # RAG Configuration
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    RAG_TOP_K: int = 6
    VECTOR_STORE_TYPE: str = "chroma"  # or "pgvector"
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    
    # Free Tier
    FREE_PROJECTS_PER_MONTH: int = 2
    
    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://frontend:3000",
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields instead of raising error


settings = Settings()
