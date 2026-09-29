from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    
    # Institution / Profile Info
    student_id = Column(String(100), nullable=True)
    staff_id = Column(String(100), nullable=True)
    department = Column(String(150), nullable=True)
    school = Column(String(150), nullable=True)
    
    # Primary & Secondary Roles
    role = Column(String(50), default="student", nullable=False)       # Primary Role (e.g., student, lecturer, hod, dean, admin)
    roles = Column(Text, default="[]", nullable=False)                # JSON string array of all granted roles
    is_admin = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # Security metadata
    failed_login_attempts = Column(Integer, default=0, nullable=False)
    locked_until = Column(DateTime, nullable=True)
    last_login_at = Column(DateTime, nullable=True)
    last_password_change_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<User id={self.id} email={self.email} role={self.role}>"\n