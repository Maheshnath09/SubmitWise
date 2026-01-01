from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.core.security import require_role
from app.models.user import User
from app.models.project import Project
from app.models.audit_log import AuditLog
from typing import List, Dict, Any
from datetime import datetime, timedelta


router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/usage")
async def get_usage_stats(
    user_data: tuple = Depends(require_role(["college_admin", "platform_admin"])),
    db: Session = Depends(get_db)
):
    """Get usage analytics"""
    
    user_id, role = user_data
    
    # Total users
    total_users = db.query(func.count(User.id)).scalar()
    
    # Total projects
    total_projects = db.query(func.count(Project.id)).scalar()
    
    # Completed projects
    completed_projects = db.query(func.count(Project.id)).filter(
        Project.status == "completed"
    ).scalar()
    
    # Projects by status
    projects_by_status = db.query(
        Project.status,
        func.count(Project.id)
    ).group_by(Project.status).all()
    
    # Projects in last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_projects = db.query(func.count(Project.id)).filter(
        Project.created_at >= thirty_days_ago
    ).scalar()
    
    # Projects by difficulty
    projects_by_difficulty = db.query(
        Project.difficulty,
        func.count(Project.id)
    ).filter(
        Project.difficulty.isnot(None)
    ).group_by(Project.difficulty).all()
    
    return {
        "total_users": total_users,
        "total_projects": total_projects,
        "completed_projects": completed_projects,
        "projects_by_status": dict(projects_by_status),
        "recent_projects_30d": recent_projects,
        "projects_by_difficulty": dict(projects_by_difficulty)
    }


@router.post("/colleges/bulk-upload")
async def bulk_upload_students(
    user_data: tuple = Depends(require_role(["college_admin", "platform_admin"])),
    db: Session = Depends(get_db)
):
    """Bulk upload students from CSV (placeholder)"""
    # TODO: Implement CSV parsing and bulk user creation
    raise HTTPException(status_code=501, detail="Bulk upload not yet implemented")


@router.get("/audit-logs")
async def get_audit_logs(
    limit: int = 100,
    user_data: tuple = Depends(require_role(["college_admin", "platform_admin"])),
    db: Session = Depends(get_db)
):
    """Get audit logs"""
    
    logs = db.query(AuditLog).order_by(
        AuditLog.timestamp.desc()
    ).limit(limit).all()
    
    return [
        {
            "id": log.id,
            "user_id": log.user_id,
            "action": log.action,
            "resource_type": log.resource_type,
            "resource_id": log.resource_id,
            "timestamp": log.timestamp,
            "metadata": log.meta_data
        }
        for log in logs
    ]


@router.post("/templates")
async def manage_templates(
    user_data: tuple = Depends(require_role(["college_admin", "platform_admin"])),
    db: Session = Depends(get_db)
):
    """Manage college-specific templates (placeholder)"""
    # TODO: Implement template management
    raise HTTPException(status_code=501, detail="Template management not yet implemented")
