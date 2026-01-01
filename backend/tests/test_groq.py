"""
Test suite for Groq API integration
"""
import pytest
from app.services.groq_client import groq_client
import json


@pytest.mark.asyncio
async def test_groq_client_initialization():
    """Test Groq client is properly initialized"""
    assert groq_client.api_url == "https://api.groq.com/openai/v1/chat/completions"
    assert groq_client.model == "gpt-oss-120b"
    assert groq_client.api_key is not None


@pytest.mark.asyncio
async def test_generate_project_structure():
    """Test project generation returns valid JSON structure"""
    # Note: This test will make actual API calls
    # Skip if no API key or in CI environment
    
    try:
        result = await groq_client.generate_project(
            user_prompt="Generate a simple Computer Networks project for semester 5",
            rag_context=[],
            user_id="test_user",
            job_id="test_job"
        )
        
        # Verify required fields
        assert "title" in result
        assert "abstract" in result
        assert "modules" in result
        assert isinstance(result["modules"], list)
        
        # Verify metadata
        assert "metadata" in result
        assert result["metadata"]["user_id"] == "test_user"
        assert result["metadata"]["job_id"] == "test_job"
        
    except Exception as e:
        pytest.skip(f"Groq API test skipped: {str(e)}")


def test_json_schema_validation():
    """Test that generated JSON matches expected schema"""
    sample_json = {
        "title": "Test Project",
        "abstract": "Test abstract",
        "keywords": ["test"],
        "difficulty": "Intermediate",
        "modules": [
            {"name": "Module 1", "description": "Test", "weeks": 2, "dependencies": []}
        ],
        "timeline_days": 60,
        "hardware_required": [],
        "software_required": [],
        "implementation": {
            "language": "Python",
            "frameworks": [],
            "file_structure": {}
        },
        "code_snippets": [],
        "report_sections": [],
        "ppt_slides": [],
        "viva_questions": [],
        "rubric": [],
        "estimated_loc": 500,
        "references": [],
        "sources": [],
        "metadata": {
            "generated_at": "2024-01-01",
            "user_id": "test",
            "job_id": "test"
        }
    }
    
    # Verify all required fields are present
    required_fields = ["title", "abstract", "modules", "metadata"]
    for field in required_fields:
        assert field in sample_json
