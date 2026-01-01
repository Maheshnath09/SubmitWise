from app.tasks.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.project import Project
from app.services.rag_pipeline import rag_pipeline
from app.services.docx_generator import docx_generator
from app.services.pptx_generator import pptx_generator
from app.services.zip_bundler import zip_bundler
from app.services.minio_client import minio_client
from app.services.plagiarism_checker import plagiarism_checker
from datetime import datetime
import uuid


@celery_app.task(bind=True, name="generate_project_task")
def generate_project_task(
    self,
    job_id: str,
    user_id: str,
    subject: str,
    semester: int,
    difficulty: str,
    additional_requirements: str,
    language: str
):
    """
    Background task to generate complete project
    
    Steps:
    1. Update status to processing
    2. Run RAG pipeline
    3. Generate JSON from Groq
    4. Validate schema
    5. Generate DOCX
    6. Generate PPTX
    7. Create ZIP bundle
    8. Run plagiarism check
    9. Upload to MinIO
    10. Update database
    """
    db = SessionLocal()
    
    try:
        # Step 1: Update status
        project = db.query(Project).filter(Project.job_id == job_id).first()
        if not project:
            raise Exception(f"Project not found: {job_id}")
        
        project.status = "processing"
        db.commit()
        
        # Step 2-3: Run RAG pipeline and generate with Groq
        self.update_state(state='PROGRESS', meta={'step': 'Generating project with AI'})
        
        import asyncio
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
        
        # Step 4: Validate (basic check)
        if not project_data.get('title'):
            raise Exception("Invalid project data: missing title")
        
        # Update project with JSON data
        project.json_data = project_data
        project.title = project_data.get('title', 'Untitled Project')
        project.subject = subject
        project.semester = semester
        project.difficulty = difficulty
        db.commit()
        
        # Step 5: Generate DOCX
        self.update_state(state='PROGRESS', meta={'step': 'Creating report document'})
        docx_bytes = docx_generator.generate_report(project_data)
        
        # Step 6: Generate PPTX
        self.update_state(state='PROGRESS', meta={'step': 'Creating presentation slides'})
        pptx_bytes = pptx_generator.generate_slides(project_data)
        
        # Step 7: Create ZIP bundle
        self.update_state(state='PROGRESS', meta={'step': 'Bundling files'})
        zip_bytes = zip_bundler.create_bundle(project_data, docx_bytes, pptx_bytes)
        
        # Step 8: Plagiarism check
        self.update_state(state='PROGRESS', meta={'step': 'Running plagiarism check'})
        plagiarism_result = asyncio.run(
            plagiarism_checker.check_plagiarism(project_data, db)
        )
        
        project.plagiarism_score = plagiarism_result['plagiarism_score']
        project.plagiarism_warnings = plagiarism_result
        db.commit()
        
        # Step 9: Upload to MinIO
        self.update_state(state='PROGRESS', meta={'step': 'Uploading files'})
        
        zip_filename = f"projects/{user_id}/{job_id}/bundle.zip"
        minio_client.upload_bytes(zip_bytes, zip_filename, "application/zip")
        
        # Generate presigned URL (valid for 7 days) with proper download filename
        # Create a clean filename from the project title
        import re
        safe_title = re.sub(r'[^\w\s-]', '', project.title or 'Project')[:50].strip()
        download_filename = f"{safe_title.replace(' ', '_')}_project.zip"
        zip_url = minio_client.get_presigned_url(zip_filename, expires=604800, filename=download_filename)
        
        # Step 10: Update database
        project.zip_url = zip_url
        project.status = "completed"
        project.completed_at = datetime.utcnow()
        db.commit()
        
        return {
            'status': 'completed',
            'job_id': job_id,
            'title': project.title,
            'zip_url': zip_url
        }
        
    except Exception as e:
        # Handle errors
        if project:
            project.status = "failed"
            project.error_message = str(e)
            db.commit()
        
        raise e
        
    finally:
        db.close()
