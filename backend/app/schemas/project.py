from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime


class ProjectGenerateRequest(BaseModel):
    subject: str
    semester: int
    difficulty: str  # Beginner, Intermediate, Advanced
    additional_requirements: Optional[str] = ""


class ProjectStatusResponse(BaseModel):
    job_id: str
    status: str  # pending, processing, completed, failed
    title: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    plagiarism_score: Optional[float] = None
    plagiarism_warnings: Optional[Dict[str, Any]] = None


class ProjectPreviewResponse(BaseModel):
    job_id: str
    title: str
    abstract: str
    keywords: List[str]
    modules: List[Dict[str, Any]]
    difficulty: str
    timeline_days: int


class ProjectDownloadResponse(BaseModel):
    job_id: str
    zip_url: str
    expires_in: int = 604800  # 7 days


class ProjectHistoryItem(BaseModel):
    id: str
    job_id: str
    title: Optional[str]
    subject: Optional[str]
    status: str
    created_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True
