"""
Test suite for authentication endpoints
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import Base, engine

client = TestClient(app)


@pytest.fixture(scope="module")
def setup_database():
    """Create test database"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_register_user(setup_database):
    """Test user registration"""
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_register_duplicate_email(setup_database):
    """Test registration with duplicate email"""
    # First registration
    client.post(
        "/api/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "testpassword123"
        }
    )
    
    # Second registration with same email
    response = client.post(
        "/api/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "testpassword123"
        }
    )
    
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_login_success(setup_database):
    """Test successful login"""
    # Register user first
    client.post(
        "/api/auth/register",
        json={
            "email": "login@example.com",
            "password": "testpassword123"
        }
    )
    
    # Login
    response = client.post(
        "/api/auth/login",
        json={
            "email": "login@example.com",
            "password": "testpassword123"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_login_invalid_credentials(setup_database):
    """Test login with invalid credentials"""
    response = client.post(
        "/api/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }
    )
    
    assert response.status_code == 401
    assert "invalid credentials" in response.json()["detail"].lower()


def test_onboard_user(setup_database):
    """Test user onboarding"""
    # Register and get token
    register_response = client.post(
        "/api/auth/register",
        json={
            "email": "onboard@example.com",
            "password": "testpassword123"
        }
    )
    token = register_response.json()["access_token"]
    
    # Onboard
    response = client.post(
        "/api/auth/onboard",
        json={
            "college_name": "Test College",
            "semester": 5,
            "subjects": ["Computer Networks", "DBMS"],
            "language": "english"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    assert "success" in response.json()["message"].lower()
