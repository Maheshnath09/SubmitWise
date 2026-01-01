from typing import Dict, Any
from app.services.vector_store_simple import vector_store
from app.services.groq_client import groq_client
from app.core.config import settings


class RAGPipeline:
    """RAG pipeline for project generation"""
    
    async def generate_project(
        self,
        subject: str,
        semester: int,
        difficulty: str,
        additional_requirements: str,
        language: str,
        user_id: str,
        job_id: str
    ) -> Dict[str, Any]:
        """
        Complete RAG pipeline for project generation
        
        Steps:
        1. Construct user query
        2. Retrieve relevant context from vector store
        3. Call Groq API with context
        4. Return structured project JSON
        """
        
        # Step 1: Construct detailed query with Indian university context
        difficulty_expectations = {
            "beginner": "suitable for diploma/polytechnic students with basic programming knowledge",
            "intermediate": "suitable for 3rd-4th year engineering students with moderate complexity",
            "advanced": "suitable for final year students with industry-level complexity and advanced features"
        }
        
        difficulty_desc = difficulty_expectations.get(difficulty.lower(), "suitable for engineering students")
        
        user_query = f"""Generate a comprehensive semester project for an Indian engineering/diploma student.

PROJECT PARAMETERS:
- Subject/Domain: {subject}
- Semester: {semester}
- Difficulty Level: {difficulty} ({difficulty_desc})
- Preferred Language: {language}
- Special Requirements: {additional_requirements if additional_requirements else "None specified"}

UNIVERSITY STANDARDS:
Follow Indian engineering college project formats (GTU/VTU/AICTE/Government Polytechnic standards).
Include all mandatory sections: Abstract, Introduction, Literature Survey, System Design, Implementation, Testing, Conclusion.

EXPECTED DELIVERABLES:
1. Detailed project documentation with 8+ chapters
2. Well-commented, working code samples (3-5 files)
3. Database design with ER diagram description
4. 15-20 viva questions with comprehensive answers
5. Test cases table with at least 10 test scenarios
6. Professional references in IEEE format

Generate a complete, ready-to-submit project that meets all academic requirements."""
        
        # Step 2: Retrieve RAG context
        rag_context = vector_store.search(
            query=f"{subject} {difficulty}",
            top_k=settings.RAG_TOP_K
        )
        
        # Step 3: Generate with Groq
        project_data = await groq_client.generate_project(
            user_prompt=user_query,
            rag_context=rag_context,
            user_id=user_id,
            job_id=job_id
        )
        
        return project_data


# Singleton instance
rag_pipeline = RAGPipeline()
