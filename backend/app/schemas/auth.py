from pydantic import BaseModel, EmailStr
from typing import Optional, List


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    role: str = "student"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserOnboard(BaseModel):
    college_name: Optional[str] = None
    semester: Optional[int] = None
    subjects: Optional[List[str]] = None
    language: str = "english"


class GoogleAuthRequest(BaseModel):
    token: str
