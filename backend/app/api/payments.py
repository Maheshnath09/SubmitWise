from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user_id
from app.core.config import settings
from app.models.user import User
from app.models.payment import Payment
from pydantic import BaseModel
import uuid
from datetime import datetime
from typing import Optional


router = APIRouter(prefix="/api/payments", tags=["Payments"])


# Subscription Plans
SUBSCRIPTION_PLANS = {
    "free": {
        "name": "Free",
        "price": 0,
        "credits": 2,
        "features": ["2 projects per month", "Basic plagiarism check", "Email support"]
    },
    "pro": {
        "name": "Pro",
        "price": 299,  # INR
        "credits": 20,
        "features": ["20 projects per month", "Advanced plagiarism detection", "Priority support", "Hindi language support"]
    },
    "enterprise": {
        "name": "Enterprise",
        "price": None,  # Custom pricing
        "credits": -1,  # Unlimited
        "features": ["Unlimited projects", "API access", "Dedicated support", "Usage analytics"]
    }
}


class CreateOrderRequest(BaseModel):
    plan: str = "pro"  # Plan to upgrade to


class VerifyPaymentRequest(BaseModel):
    razorpay_payment_id: str
    razorpay_order_id: Optional[str] = None
    plan: str = "pro"


@router.get("/plans")
async def get_subscription_plans():
    """Get all available subscription plans"""
    return SUBSCRIPTION_PLANS


@router.get("/subscription")
async def get_subscription_status(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get current user's subscription status"""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    current_plan = SUBSCRIPTION_PLANS.get(user.subscription_tier, SUBSCRIPTION_PLANS["free"])
    
    return {
        "user_id": user.id,
        "email": user.email,
        "subscription_tier": user.subscription_tier,
        "credits": user.credits,
        "plan_name": current_plan["name"],
        "plan_features": current_plan["features"]
    }


@router.post("/create-order")
async def create_payment_order(
    request: CreateOrderRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Create payment order for Razorpay"""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    plan = request.plan.lower()
    if plan not in SUBSCRIPTION_PLANS:
        raise HTTPException(status_code=400, detail="Invalid plan")
    
    if plan == "free":
        raise HTTPException(status_code=400, detail="Cannot create order for free plan")
    
    if plan == "enterprise":
        raise HTTPException(status_code=400, detail="Contact sales for enterprise plan")
    
    plan_details = SUBSCRIPTION_PLANS[plan]
    amount = plan_details["price"]
    
    # Create payment record
    payment = Payment(
        id=str(uuid.uuid4()),
        user_id=user_id,
        amount=amount,
        currency="INR",
        status="pending",
        provider="razorpay",
        credits_added=plan_details["credits"],
        meta_data={"plan": plan}
    )
    
    db.add(payment)
    db.commit()
    db.refresh(payment)
    
    # For client-side Razorpay checkout (no server-side order creation needed in test mode)
    return {
        "payment_id": payment.id,
        "order_id": f"order_{payment.id[:8]}",  # Simple order ID for tracking
        "amount": amount * 100,  # Razorpay expects amount in paise
        "currency": "INR",
        "plan": plan,
        "plan_name": plan_details["name"],
        "credits": plan_details["credits"],
        "key_id": settings.RAZORPAY_KEY_ID,
        "prefill": {
            "email": user.email
        }
    }


@router.post("/verify")
async def verify_payment(
    request: VerifyPaymentRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Verify payment completion and upgrade subscription"""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Find pending payment for this user
    payment = db.query(Payment).filter(
        Payment.user_id == user_id,
        Payment.status == "pending"
    ).order_by(Payment.created_at.desc()).first()
    
    if not payment:
        raise HTTPException(status_code=404, detail="No pending payment found")
    
    plan = request.plan.lower()
    if plan not in SUBSCRIPTION_PLANS:
        raise HTTPException(status_code=400, detail="Invalid plan")
    
    plan_details = SUBSCRIPTION_PLANS[plan]
    
    # Update payment record
    payment.status = "completed"
    payment.transaction_id = request.razorpay_payment_id
    payment.order_id = request.razorpay_order_id
    payment.completed_at = datetime.utcnow()
    
    # Upgrade user subscription
    user.subscription_tier = plan
    user.credits = plan_details["credits"]
    
    db.commit()
    
    return {
        "success": True,
        "message": f"Successfully upgraded to {plan_details['name']} plan!",
        "subscription_tier": user.subscription_tier,
        "credits": user.credits,
        "payment_id": request.razorpay_payment_id
    }


@router.get("/history")
async def get_payment_history(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get user's payment history"""
    
    payments = db.query(Payment).filter(
        Payment.user_id == user_id
    ).order_by(Payment.created_at.desc()).all()
    
    return [
        {
            "id": p.id,
            "amount": p.amount,
            "currency": p.currency,
            "status": p.status,
            "provider": p.provider,
            "credits_added": p.credits_added,
            "plan": p.meta_data.get("plan") if p.meta_data else None,
            "created_at": p.created_at,
            "completed_at": p.completed_at
        }
        for p in payments
    ]

