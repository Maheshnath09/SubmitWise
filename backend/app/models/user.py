from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="student")  # student, college_admin, platform_admin
    
    # Student-specific fields
    college_id = Column(String, ForeignKey("colleges.id"), nullable=True)
    semester = Column(Integer, nullable=True)
    subjects = Column(JSON, nullable=True)  # List of subjects
    language = Column(String, default="english")  # english or hindi
    
    # Credits & subscription
    credits = Column(Integer, default=2)  # Free tier: 2 projects/month
    subscription_tier = Column(String, default="free")  # free, pro, enterprise
    
    # OAuth
    google_id = Column(String, nullable=True, unique=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    college = relationship("College", back_populates="users")
    projects = relationship("Project", back_populates="user")
    payments = relationship("Payment", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")
