from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from datetime import datetime
from app.database import Base

class ClientApp(Base):
    __tablename__ = "client_apps"

    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String(150), unique=True, nullable=False)  # e.g., "GIMPA Thesis Repository", "SOTSS Library App"
    client_id = Column(String(100), unique=True, index=True, nullable=False)
    api_key_hash = Column(String(255), nullable=False)
    app_url = Column(String(255), nullable=True)
    allowed_redirect_uris = Column(Text, default="[]", nullable=False) # JSON string of allowed URIs
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<ClientApp id={self.id} name={self.client_name}>"
