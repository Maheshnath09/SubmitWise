from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, get_current_user_id
from app.models.user import User
from app.schemas.auth import UserRegister, UserLogin, TokenResponse, UserOnboard
import uuid


router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user"""
    
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    user = User(
        id=str(uuid.uuid4()),
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        role=user_data.role
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Generate tokens
    access_token = create_access_token({"sub": user.id, "role": user.role})
    refresh_token = create_refresh_token({"sub": user.id, "role": user.role})
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user"""
    
    # Find user
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Verify password
    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Generate tokens
    access_token = create_access_token({"sub": user.id, "role": user.role})
    refresh_token = create_refresh_token({"sub": user.id, "role": user.role})
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post("/onboard")
async def onboard(
    onboard_data: UserOnboard,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Complete student onboarding"""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update user profile
    if onboard_data.college_name:
        # TODO: Link to college or create new one
        pass
    
    user.semester = onboard_data.semester
    user.subjects = onboard_data.subjects
    user.language = onboard_data.language
    
    db.commit()
    
    return {"message": "Onboarding completed successfully"}


from pydantic import BaseModel


class GoogleAuthRequest(BaseModel):
    """Request model for Google OAuth authentication"""
    credential: str  # Google ID token from frontend


@router.post("/google", response_model=TokenResponse)
async def google_auth(auth_data: GoogleAuthRequest, db: Session = Depends(get_db)):
    """Authenticate with Google OAuth"""
    import httpx
    from app.core.config import settings
    
    # Verify the Google ID token
    try:
        # Verify token with Google's tokeninfo endpoint
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://oauth2.googleapis.com/tokeninfo?id_token={auth_data.credential}"
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid Google token"
                )
            
            google_data = response.json()
            
            # Verify the token is for our app
            if google_data.get("aud") != settings.GOOGLE_CLIENT_ID:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token not issued for this application"
                )
            
            email = google_data.get("email")
            if not email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email not provided by Google"
                )
            
            # Check if user exists
            user = db.query(User).filter(User.email == email).first()
            
            if not user:
                # Create new user with Google OAuth
                google_id = google_data.get("sub")  # Google user ID
                user = User(
                    id=str(uuid.uuid4()),
                    email=email,
                    hashed_password=hash_password(str(uuid.uuid4())),  # Random password for OAuth users
                    role="student",
                    google_id=google_id
                )
                db.add(user)
                db.commit()
                db.refresh(user)
            
            # Generate tokens
            access_token = create_access_token({"sub": user.id, "role": user.role})
            refresh_token = create_refresh_token({"sub": user.id, "role": user.role})
            
            return TokenResponse(
                access_token=access_token,
                refresh_token=refresh_token
            )
            
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Could not verify Google token: {str(e)}"
        )

