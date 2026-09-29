from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from datetime import datetime
from app.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(100), nullable=False) # LOGIN_SUCCESS, LOGIN_FAILED, PASSWORD_SYNC, ROLE_CHANGE
    user_email = Column(String(255), nullable=True, index=True)
    client_app = Column(String(150), nullable=True)
    ip_address = Column(String(100), nullable=True)
    user_agent = Column(String(255), nullable=True)
    status = Column(String(50), default="SUCCESS", nullable=False)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<AuditLog id={self.id} event={self.event_type} user={self.user_email}>"\n