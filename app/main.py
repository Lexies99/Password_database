from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.api.router import api_router

# Create database tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    ## Central Identity Provider & Single Sign-On (SSO) API
    
    This service serves as the single source of truth for user authentication across all GIMPA web applications:
    * **GIMPA Thesis Repository** (`https://thesis.manamatechnologies.com`)
    * **SOTSS Library Application** (`https://libraryapp.manamatechnologies.com`)
    * Any future integrated institutional portals.
    
    ### Key Features:
    - **One Unified Password:** Secure Argon2id & Bcrypt cryptographic password verification.
    - **Instant Cross-App Sync:** Password updates and role changes propagate immediately.
    - **Secondary & Multi-Role Support:** Preserve primary academic titles while granting administrative privileges.
    - **Comprehensive Security Audit Logs:** Track all login attempts, failures, and credential events.
    """,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/")
def root():
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs_url": "/docs",
        "sso_verify_endpoint": "/api/v1/auth/verify-credentials"
    }\n