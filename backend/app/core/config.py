from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import Optional, List, Union
import os


class Settings(BaseSettings):
    """Application configuration settings"""
    
    # App
    APP_NAME: str = "SubmitWise"
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
    MINIO_ENABLED: bool = True  # Set to False for deployments without MinIO
    
    # Groq API (MANDATORY - Using Llama 3.3 70B Versatile)
    GROQ_API_KEY: str = ""  # Allow empty default for validation, but required in production
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
    
    # CORS - Can be set as comma-separated string in env var
    CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://frontend:3000",
        "https://submitwise.vercel.app",
        "https://project-gen-ai.vercel.app",
    ]
    
    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS origins from comma-separated string or list"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',') if origin.strip()]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields instead of raising error


settings = Settings()
