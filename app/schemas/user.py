from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    student_id: Optional[str] = None
    staff_id: Optional[str] = None
    department: Optional[str] = None
    school: Optional[str] = None
    role: Optional[str] = "student"
    roles: Optional[List[str]] = []
    is_admin: Optional[bool] = False
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    student_id: Optional[str] = None
    staff_id: Optional[str] = None
    department: Optional[str] = None
    school: Optional[str] = None
    role: Optional[str] = None
    roles: Optional[List[str]] = None
    is_admin: Optional[bool] = None
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=6)

class UserResponse(UserBase):
    id: int
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class RoleAssignmentRequest(BaseModel):
    email: EmailStr
    role_title: str
    is_secondary: bool = True\n