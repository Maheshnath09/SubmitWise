from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON, Float, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Project(Base):
    __tablename__ = "projects"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    job_id = Column(String, unique=True, index=True, nullable=False)
    
    # Project details
    title = Column(String, nullable=True)
    subject = Column(String, nullable=True)
    semester = Column(Integer, nullable=True)
    difficulty = Column(String, nullable=True)
    
    # Status
    status = Column(String, default="pending")  # pending, processing, completed, failed
    error_message = Column(Text, nullable=True)
    
    # Generated content
    json_data = Column(JSON, nullable=True)  # Full project JSON from LLM
    
    # Files
    zip_url = Column(String, nullable=True)  # MinIO presigned URL
    docx_path = Column(String, nullable=True)
    pptx_path = Column(String, nullable=True)
    
    # Quality metrics
    plagiarism_score = Column(Float, default=0.0)
    plagiarism_warnings = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="projects")
