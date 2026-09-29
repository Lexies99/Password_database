import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Header, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.audit_log import AuditLog
from app.schemas.auth import (
    SsoVerifyRequest, SsoVerifyResponse,
    SsoSyncPasswordRequest, SsoSyncPasswordResponse,
    TokenResponse
)
from app.core.security import hash_password, verify_password, create_access_token, verify_service_api_key

router = APIRouter(prefix="/auth", tags=["Central Authentication & SSO"])

@router.post("/verify-credentials", response_model=SsoVerifyResponse)
def verify_credentials(
    req: SsoVerifyRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Primary SSO Verification API.
    Client apps (Library, Thesis, etc.) query this endpoint to authenticate users with one unified password.
    """
    email = req.email.strip().lower()
    user = db.query(User).filter(User.email == email).first()

    client_ip = req.ip_address or (request.client.host if request.client else "unknown")
    user_agent = req.user_agent or request.headers.get("user-agent", "unknown")

    if not user:
        # Log failed attempt
        db.add(AuditLog(
            event_type="LOGIN_FAILED",
            user_email=email,
            client_app=req.client_app,
            ip_address=client_ip,
            user_agent=user_agent,
            status="FAILED",
            details="User not found in Password_database"
        ))
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials: User account does not exist."
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated. Please contact administrator."
        )

    # Check password match
    if not verify_password(req.password, user.password_hash):
        user.failed_login_attempts += 1
        db.add(AuditLog(
            event_type="LOGIN_FAILED",
            user_email=email,
            client_app=req.client_app,
            ip_address=client_ip,
            user_agent=user_agent,
            status="FAILED",
            details="Incorrect password supplied"
        ))
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    # Success! Parse secondary roles
    user_roles = []
    try:
        if user.roles:
            user_roles = json.loads(user.roles) if isinstance(user.roles, str) else list(user.roles)
    except Exception:
        user_roles = []

    # Reset failed attempts and update last login
    user.failed_login_attempts = 0
    user.last_login_at = datetime.utcnow()
    db.add(AuditLog(
        event_type="LOGIN_SUCCESS",
        user_email=email,
        client_app=req.client_app,
        ip_address=client_ip,
        user_agent=user_agent,
        status="SUCCESS",
        details=f"User authenticated successfully via client {req.client_app}"
    ))
    db.commit()

    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "name": user.full_name,
        "role": user.role,
        "roles": user_roles,
        "is_admin": user.is_admin,
        "client_app": req.client_app
    }
    jwt_token = create_access_token(token_data)

    return SsoVerifyResponse(
        valid=True,
        user_id=user.id,
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        roles=user_roles,
        is_admin=user.is_admin or ("system_admin" in user_roles or "Admin" in user_roles),
        is_active=user.is_active,
        token=jwt_token,
        message="Credentials verified successfully"
    )

@router.post("/sync-password", response_model=SsoSyncPasswordResponse)
def sync_password(
    req: SsoSyncPasswordRequest,
    x_api_key: str = Header(None, alias="X-API-Key"),
    db: Session = Depends(get_db)
):
    """
    Update or synchronize a user's single password in the central database.
    Instantly propagates across all connected applications.
    """
    email = req.email.strip().lower()
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {email} not found in central database."
        )

    # If an old password is provided and no administrative master key is supplied, verify old password
    is_service_override = verify_service_api_key(x_api_key)
    if not is_service_override and req.old_password:
        if not verify_password(req.old_password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password verification failed."
            )

    user.password_hash = hash_password(req.new_password)
    user.last_password_change_at = datetime.utcnow()
    user.updated_at = datetime.utcnow()

    db.add(AuditLog(
        event_type="PASSWORD_SYNC",
        user_email=email,
        client_app=req.client_app,
        status="SUCCESS",
        details="Password successfully changed and synced centrally"
    ))
    db.commit()

    return SsoSyncPasswordResponse(
        success=True,
        email=user.email,
        message="Central password updated successfully. Changes are active across all apps.",
        updated_at=user.last_password_change_at
    )
