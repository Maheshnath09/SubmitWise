from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class College(Base):
    __tablename__ = "colleges"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    domain = Column(String, nullable=True)  # Email domain for auto-verification
    admin_user_id = Column(String, nullable=True)
    
    # Custom templates
    templates = Column(JSON, nullable=True)  # College-specific project templates
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    users = relationship("User", back_populates="college")
