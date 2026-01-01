from typing import Dict, Any, List
from app.services.embeddings_simple import embedding_service
from sqlalchemy.orm import Session


class PlagiarismChecker:
    """Basic plagiarism detection using embeddings"""
    
    async def check_plagiarism(
        self,
        project_data: Dict[str, Any],
        db: Session
    ) -> Dict[str, Any]:
        """
        Check for plagiarism against existing projects
        
        Args:
            project_data: Generated project JSON
            db: Database session
            
        Returns:
            Plagiarism report with score and warnings
        """
        from app.models.project import Project
        
        # Extract key content for comparison
        content_to_check = f"{project_data.get('title', '')} {project_data.get('abstract', '')}"
        
        # Generate embedding
        query_embedding = embedding_service.embed_text(content_to_check)
        
        # Get all existing projects
        existing_projects = db.query(Project).filter(
            Project.status == "completed",
            Project.json_data.isnot(None)
        ).all()
        
        max_similarity = 0.0
        similar_projects = []
        
        for existing in existing_projects:
            if not existing.json_data:
                continue
            
            # Handle json_data that might be a string or dict
            json_data = existing.json_data
            if isinstance(json_data, str):
                try:
                    import json
                    json_data = json.loads(json_data)
                except json.JSONDecodeError:
                    continue
            
            if not isinstance(json_data, dict):
                continue
            
            # Extract content from existing project
            existing_content = f"{json_data.get('title', '')} {json_data.get('abstract', '')}"
            
            # Generate embedding
            existing_embedding = embedding_service.embed_text(existing_content)
            
            # Calculate similarity
            similarity = embedding_service.cosine_similarity(query_embedding, existing_embedding)
            
            if similarity > 0.75:  # Threshold for concern (raised from 0.7)
                similar_projects.append({
                    'project_id': existing.id,
                    'title': existing.title,
                    'similarity': similarity
                })
            
            if similarity > max_similarity:
                max_similarity = similarity
        
        # Generate warnings - adjusted thresholds to be less aggressive
        warnings = []
        if max_similarity > 0.90:
            warnings.append("Very high similarity detected with existing projects. Consider adding unique requirements.")
        elif max_similarity > 0.80:
            warnings.append("Moderate similarity detected. Content may need revision.")
        elif max_similarity > 0.70:
            # Just informational, not a warning
            pass
        
        return {
            'plagiarism_score': max_similarity,
            'warnings': warnings,
            'similar_projects': sorted(similar_projects, key=lambda x: x['similarity'], reverse=True)[:5]
        }


# Singleton instance
plagiarism_checker = PlagiarismChecker()
