from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = User(
            full_name=user.full_name,
            email=user.email,
            password_hash=hash_password(user.password),
            company_name=user.company_name,
            role="customer",
            is_active=True,
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already registered")

    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
