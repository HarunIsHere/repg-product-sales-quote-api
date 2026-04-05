from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.core.security import hash_password
from app.db.session import get_db
from app.models.user import User
from app.schemas.admin_user import AdminUserCreate
from app.schemas.user import UserResponse

router = APIRouter(prefix="/admin/users", tags=["admin-users"])


@router.post(
    "/",
    response_model=UserResponse,
    dependencies=[Depends(require_roles("admin", "super_admin"))],
)
def create_internal_user(user: AdminUserCreate, db: Session = Depends(get_db)):
    allowed_roles = {
        "admin",
        "sales_manager",
        "operations_staff",
        "product_manager",
        "super_admin",
        "customer",
    }

    if user.role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role",
        )

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    db_user = User(
        full_name=user.full_name,
        email=user.email,
        password_hash=hash_password(user.password),
        company_name=user.company_name,
        role=user.role,
        is_active=True,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
