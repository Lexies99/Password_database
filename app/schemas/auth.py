from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class SsoVerifyRequest(BaseModel):
    email: EmailStr
    password: str
    client_app: Optional[str] = "unknown_client"
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

class SsoVerifyResponse(BaseModel):
    valid: bool
    user_id: Optional[int] = None
    email: str
    full_name: Optional[str] = None
    role: Optional[str] = None
    roles: Optional[List[str]] = []
    is_admin: bool = False
    is_active: bool = True
    token: Optional[str] = None
    message: Optional[str] = None

class SsoSyncPasswordRequest(BaseModel):
    email: EmailStr
    new_password: str = Field(..., min_length=6)
    old_password: Optional[str] = None
    client_app: Optional[str] = "unknown_client"

class SsoSyncPasswordResponse(BaseModel):
    success: bool
    email: str
    message: str
    updated_at: datetime

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: Dict[str, Any]\n