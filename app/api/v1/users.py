import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.audit_log import AuditLog
from app.schemas.user import UserCreate, UserUpdate, UserResponse, RoleAssignmentRequest
from app.core.security import hash_password, verify_service_api_key

router = APIRouter(prefix="/users", tags=["Central User Management"])

def _format_user_roles(roles_field) -> List[str]:
    if not roles_field:
        return []
    if isinstance(roles_field, list):
        return roles_field
    try:
        return json.loads(roles_field)
    except Exception:
        return [r.strip() for r in str(roles_field).split(",") if r.strip()]

@router.get("", response_model=List[UserResponse])
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    role: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    if search:
        s = f"%{search}%"
        query = query.filter((User.email.ilike(s)) | (User.full_name.ilike(s)))
    
    users = query.offset(skip).limit(limit).all()
    results = []
    for u in users:
        results.append(UserResponse(
            id=u.id,
            email=u.email,
            full_name=u.full_name,
            student_id=u.student_id,
            staff_id=u.staff_id,
            department=u.department,
            school=u.school,
            role=u.role,
            roles=_format_user_roles(u.roles),
            is_admin=u.is_admin,
            is_active=u.is_active,
            is_verified=u.is_verified,
            created_at=u.created_at,
            updated_at=u.updated_at
        ))
    return results

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    req: UserCreate,
    db: Session = Depends(get_db)
):
    email = req.email.strip().lower()
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email {email} already exists."
        )

    roles_json = json.dumps(req.roles or [])
    new_user = User(
        email=email,
        password_hash=hash_password(req.password),
        full_name=req.full_name,
        student_id=req.student_id,
        staff_id=req.staff_id,
        department=req.department,
        school=req.school,
        role=req.role or "student",
        roles=roles_json,
        is_admin=req.is_admin or False,
        is_active=req.is_active if req.is_active is not None else True,
        is_verified=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        full_name=new_user.full_name,
        student_id=new_user.student_id,
        staff_id=new_user.staff_id,
        department=new_user.department,
        school=new_user.school,
        role=new_user.role,
        roles=_format_user_roles(new_user.roles),
        is_admin=new_user.is_admin,
        is_active=new_user.is_active,
        is_verified=new_user.is_verified,
        created_at=new_user.created_at,
        updated_at=new_user.updated_at
    )

@router.get("/{email}", response_model=UserResponse)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    clean_email = email.strip().lower()
    user = db.query(User).filter(User.email == clean_email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return UserResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        student_id=user.student_id,
        staff_id=user.staff_id,
        department=user.department,
        school=user.school,
        role=user.role,
        roles=_format_user_roles(user.roles),
        is_admin=user.is_admin,
        is_active=user.is_active,
        is_verified=user.is_verified,
        created_at=user.created_at,
        updated_at=user.updated_at
    )

@router.post("/assign-role")
def assign_role(
    req: RoleAssignmentRequest,
    x_api_key: str = Header(None, alias="X-API-Key"),
    db: Session = Depends(get_db)
):
    """Assign primary or secondary roles to a user centrally."""
    email = req.email.strip().lower()
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    current_roles = _format_user_roles(user.roles)
    clean_role = req.role_title.strip()

    if req.is_secondary:
        if clean_role not in current_roles:
            current_roles.append(clean_role)
    else:
        user.role = clean_role
        if clean_role not in current_roles:
            current_roles.append(clean_role)

    if clean_role.lower() in ["admin", "system_admin", "administrator"]:
        user.is_admin = True

    user.roles = json.dumps(current_roles)
    db.commit()

    return {
        "success": True,
        "email": user.email,
        "primary_role": user.role,
        "roles": current_roles,
        "is_admin": user.is_admin
    }
