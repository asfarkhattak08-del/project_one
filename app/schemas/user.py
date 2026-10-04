from enum import Enum
from typing import Literal, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)   
    
class TokenData(BaseModel):
    id: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginResponse(BaseModel):
    user: UserResponse
    token: Token
    
class TokenData(BaseModel):
    id: Optional[int] = None