from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    # Payment details
    amount = Column(Float, nullable=False)
    currency = Column(String, default="INR")
    status = Column(String, default="pending")  # pending, completed, failed, refunded
    
    # Provider
    provider = Column(String, nullable=False)  # razorpay, stripe
    transaction_id = Column(String, nullable=True)
    order_id = Column(String, nullable=True)
    
    # Credits provisioned
    credits_added = Column(Integer, default=0)
    
    # Metadata
    meta_data = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="payments")
