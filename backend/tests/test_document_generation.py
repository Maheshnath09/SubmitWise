"""
Test suite for document generators
"""
import pytest
from app.services.docx_generator import docx_generator
from app.services.pptx_generator import pptx_generator
from app.services.zip_bundler import zip_bundler
import zipfile
from io import BytesIO


@pytest.fixture
def sample_project_data():
    """Sample project data for testing"""
    return {
        "title": "Test Project",
        "abstract": "This is a test project abstract for testing document generation.",
        "keywords": ["test", "project", "generation"],
        "difficulty": "Intermediate",
        "modules": [
            {
                "name": "Module 1",
                "description": "First module description",
                "weeks": 2,
                "dependencies": []
            },
            {
                "name": "Module 2",
                "description": "Second module description",
                "weeks": 3,
                "dependencies": ["Module 1"]
            }
        ],
        "timeline_days": 60,
        "hardware_required": ["Computer", "Network cables"],
        "software_required": ["Python 3.8+", "VS Code"],
        "implementation": {
            "language": "Python",
            "frameworks": ["Flask"],
            "file_structure": {"src": ["main.py", "utils.py"]}
        },
        "code_snippets": [
            {
                "filename": "main.py",
                "language": "python",
                "content": "```python\nprint('Hello World')\n```"
            }
        ],
        "report_sections": [
            {"title": "Introduction", "content": "Test introduction"}
        ],
        "ppt_slides": [
            {"title": "Overview", "bullets": ["Point 1", "Point 2"]}
        ],
        "viva_questions": [
            {
                "q": "What is this project about?",
                "expected_answer": "Test answer",
                "difficulty": "Easy",
                "hint": "Test hint"
            }
        ],
        "rubric": [
            {"criteria": "Implementation", "weight": 40}
        ],
        "estimated_loc": 500,
        "references": [
            {"id": "1", "title": "Test Reference", "url": "https://example.com"}
        ],
        "sources": [],
        "metadata": {
            "generated_at": "2024-01-01",
            "user_id": "test",
            "job_id": "test"
        }
    }


def test_docx_generation(sample_project_data):
    """Test DOCX report generation"""
    docx_bytes = docx_generator.generate_report(sample_project_data)
    
    assert isinstance(docx_bytes, bytes)
    assert len(docx_bytes) > 0
    
    # Verify it's a valid DOCX file (starts with PK signature)
    assert docx_bytes[:2] == b'PK'


def test_pptx_generation(sample_project_data):
    """Test PPTX slides generation"""
    pptx_bytes = pptx_generator.generate_slides(sample_project_data)
    
    assert isinstance(pptx_bytes, bytes)
    assert len(pptx_bytes) > 0
    
    # Verify it's a valid PPTX file (starts with PK signature)
    assert pptx_bytes[:2] == b'PK'


def test_zip_bundle_creation(sample_project_data):
    """Test ZIP bundle creation"""
    docx_bytes = docx_generator.generate_report(sample_project_data)
    pptx_bytes = pptx_generator.generate_slides(sample_project_data)
    
    zip_bytes = zip_bundler.create_bundle(
        sample_project_data,
        docx_bytes,
        pptx_bytes
    )
    
    assert isinstance(zip_bytes, bytes)
    assert len(zip_bytes) > 0
    
    # Verify ZIP contents
    zip_file = zipfile.ZipFile(BytesIO(zip_bytes))
    filenames = zip_file.namelist()
    
    assert 'README.md' in filenames
    assert 'metadata.json' in filenames
    assert 'report.docx' in filenames
    assert 'slides.pptx' in filenames
    assert 'viva_questions.md' in filenames
    assert 'rubric.md' in filenames


def test_readme_generation(sample_project_data):
    """Test README content in ZIP"""
    docx_bytes = docx_generator.generate_report(sample_project_data)
    pptx_bytes = pptx_generator.generate_slides(sample_project_data)
    zip_bytes = zip_bundler.create_bundle(sample_project_data, docx_bytes, pptx_bytes)
    
    zip_file = zipfile.ZipFile(BytesIO(zip_bytes))
    readme_content = zip_file.read('README.md').decode('utf-8')
    
    assert "Test Project" in readme_content
    assert "Abstract" in readme_content
    assert "Modules" in readme_content
