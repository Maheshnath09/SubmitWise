from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.database import get_db, SessionLocal
from app.core.security import get_current_user_id
from app.core.config import settings
from app.models.user import User
from app.models.project import Project
from app.schemas.project import (
    ProjectGenerateRequest,
    ProjectStatusResponse,
    ProjectPreviewResponse,
    ProjectDownloadResponse,
    ProjectHistoryItem
)
from typing import List
import uuid


router = APIRouter(prefix="/api/projects", tags=["Projects"])


def run_project_generation_sync(
    job_id: str,
    user_id: str,
    subject: str,
    semester: int,
    difficulty: str,
    additional_requirements: str,
    language: str
):
    """Run project generation synchronously (for local development without Celery)"""
    from app.services.rag_pipeline import rag_pipeline
    from app.services.docx_generator import docx_generator
    from app.services.pptx_generator import pptx_generator
    from app.services.zip_bundler import zip_bundler
    from app.services.minio_client import minio_client
    from app.services.plagiarism_checker import plagiarism_checker
    from datetime import datetime
    import asyncio
    import re
    
    db = SessionLocal()
    
    try:
        # Get project
        project = db.query(Project).filter(Project.job_id == job_id).first()
        if not project:
            print(f"Project not found: {job_id}")
            return
        
        # Update status to processing
        project.status = "processing"
        db.commit()
        
        print(f"Starting project generation for job: {job_id}")
        
        # Generate project with AI
        project_data = asyncio.run(
            rag_pipeline.generate_project(
                subject=subject,
                semester=semester,
                difficulty=difficulty,
                additional_requirements=additional_requirements,
                language=language,
                user_id=user_id,
                job_id=job_id
            )
        )
        
        # Validate
        if not project_data.get('title'):
            raise Exception("Invalid project data: missing title")
        
        # Update project with JSON data
        project.json_data = project_data
        project.title = project_data.get('title', 'Untitled Project')
        project.subject = subject
        project.semester = semester
        project.difficulty = difficulty
        db.commit()
        
        print(f"Project data generated: {project.title}")
        
        # Generate DOCX
        docx_bytes = docx_generator.generate_report(project_data)
        
        # Generate PPTX
        pptx_bytes = pptx_generator.generate_slides(project_data)
        
        # Create ZIP bundle
        zip_bytes = zip_bundler.create_bundle(project_data, docx_bytes, pptx_bytes)
        
        # Plagiarism check
        plagiarism_result = asyncio.run(
            plagiarism_checker.check_plagiarism(project_data, db)
        )
        
        project.plagiarism_score = plagiarism_result['plagiarism_score']
        project.plagiarism_warnings = plagiarism_result
        db.commit()
        
        # Upload to MinIO
        zip_filename = f"projects/{user_id}/{job_id}/bundle.zip"
        minio_client.upload_bytes(zip_bytes, zip_filename, "application/zip")
        
        # Generate presigned URL
        safe_title = re.sub(r'[^\w\s-]', '', project.title or 'Project')[:50].strip()
        download_filename = f"{safe_title.replace(' ', '_')}_project.zip"
        zip_url = minio_client.get_presigned_url(zip_filename, expires=604800, filename=download_filename)
        
        # Update database
        project.zip_url = zip_url
        project.status = "completed"
        project.completed_at = datetime.utcnow()
        db.commit()
        
        print(f"Project generation completed: {job_id}")
        
    except Exception as e:
        print(f"Project generation failed: {e}")
        if project:
            project.status = "failed"
            project.error_message = str(e)
            db.commit()
    finally:
        db.close()


@router.post("/generate")
async def generate_project(
    request: ProjectGenerateRequest,
    background_tasks: BackgroundTasks,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Generate a new project"""
    
    # Get user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check credits
    if user.credits <= 0:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Insufficient credits. Please purchase more credits."
        )
    
    # Create job
    job_id = str(uuid.uuid4())
    
    # Create project record
    project = Project(
        id=str(uuid.uuid4()),
        user_id=user_id,
        job_id=job_id,
        subject=request.subject,
        semester=request.semester,
        difficulty=request.difficulty,
        status="pending"
    )
    
    db.add(project)
    
    # Deduct credit
    user.credits -= 1
    
    db.commit()
    db.refresh(project)
    
    # Use FastAPI BackgroundTasks instead of Celery for local development
    background_tasks.add_task(
        run_project_generation_sync,
        job_id=job_id,
        user_id=user_id,
        subject=request.subject,
        semester=request.semester,
        difficulty=request.difficulty,
        additional_requirements=request.additional_requirements or "",
        language=user.language or "english"
    )
    
    return {
        "job_id": job_id,
        "status": "pending",
        "message": "Project generation started"
    }



@router.get("/{job_id}/status", response_model=ProjectStatusResponse)
async def get_project_status(
    job_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get project generation status"""
    
    project = db.query(Project).filter(
        Project.job_id == job_id,
        Project.user_id == user_id
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return ProjectStatusResponse(
        job_id=project.job_id,
        status=project.status,
        title=project.title,
        error_message=project.error_message,
        created_at=project.created_at,
        completed_at=project.completed_at,
        plagiarism_score=project.plagiarism_score,
        plagiarism_warnings=project.plagiarism_warnings
    )


@router.get("/{job_id}/preview", response_model=ProjectPreviewResponse)
async def get_project_preview(
    job_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get project preview"""
    
    project = db.query(Project).filter(
        Project.job_id == job_id,
        Project.user_id == user_id
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project.status != "completed":
        raise HTTPException(status_code=400, detail="Project not yet completed")
    
    if not project.json_data:
        raise HTTPException(status_code=500, detail="Project data not available")
    
    return ProjectPreviewResponse(
        job_id=project.job_id,
        title=project.json_data.get('title', ''),
        abstract=project.json_data.get('abstract', ''),
        keywords=project.json_data.get('keywords', []),
        modules=project.json_data.get('modules', []),
        difficulty=project.json_data.get('difficulty', ''),
        timeline_days=project.json_data.get('timeline_days', 0)
    )


@router.get("/{job_id}/download", response_model=ProjectDownloadResponse)
async def download_project(
    job_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get download URL for project ZIP"""
    
    project = db.query(Project).filter(
        Project.job_id == job_id,
        Project.user_id == user_id
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project.status != "completed":
        raise HTTPException(status_code=400, detail="Project not yet completed")
    
    if not project.zip_url:
        raise HTTPException(status_code=500, detail="Download URL not available")
    
    # Return the backend download endpoint with full URL
    backend_url = f"http://localhost:8000/api/projects/{job_id}/download-file"
    return ProjectDownloadResponse(
        job_id=project.job_id,
        zip_url=backend_url
    )


from fastapi.responses import StreamingResponse
from app.services.minio_client import minio_client
from app.core.security import decode_token
from jose import JWTError
import re


@router.get("/{job_id}/download-file")
async def download_project_file(
    job_id: str,
    token: str = None,  # Accept token as query parameter
    db: Session = Depends(get_db)
):
    """Direct file download with proper filename - accepts token as query param for browser downloads"""
    
    # Verify token from query parameter
    if not token:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    except HTTPException:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    project = db.query(Project).filter(
        Project.job_id == job_id,
        Project.user_id == user_id
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project.status != "completed":
        raise HTTPException(status_code=400, detail="Project not yet completed")
    
    # Get file from MinIO
    zip_object_name = f"projects/{project.user_id}/{job_id}/bundle.zip"
    
    try:
        minio_client.initialize()
        response = minio_client.client.get_object(
            minio_client.bucket_name,
            zip_object_name
        )
        
        # Create safe filename from project title
        safe_title = re.sub(r'[^\w\s-]', '', project.title or 'Project')[:50].strip()
        download_filename = f"{safe_title.replace(' ', '_')}_project.zip"
        
        # Stream the file with proper headers
        return StreamingResponse(
            response,
            media_type="application/zip",
            headers={
                "Content-Disposition": f'attachment; filename="{download_filename}"',
                "Content-Type": "application/zip"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download file: {str(e)}")


@router.get("/history", response_model=List[ProjectHistoryItem])
async def get_project_history(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get user's project history"""
    
    projects = db.query(Project).filter(
        Project.user_id == user_id
    ).order_by(Project.created_at.desc()).limit(50).all()
    
    return projects
