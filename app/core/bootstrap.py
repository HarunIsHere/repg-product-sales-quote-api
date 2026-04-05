from sqlalchemy.orm import Session

from app.core.config import (
    FIRST_SUPERADMIN_COMPANY,
    FIRST_SUPERADMIN_EMAIL,
    FIRST_SUPERADMIN_FULL_NAME,
    FIRST_SUPERADMIN_PASSWORD,
)
from app.core.security import hash_password
from app.models.user import User


def seed_first_superadmin(db: Session) -> None:
    if not FIRST_SUPERADMIN_EMAIL or not FIRST_SUPERADMIN_PASSWORD:
        return

    existing_user = db.query(User).filter(
        User.email == FIRST_SUPERADMIN_EMAIL
    ).first()

    if existing_user:
        return

    super_admin = User(
        full_name=FIRST_SUPERADMIN_FULL_NAME,
        email=FIRST_SUPERADMIN_EMAIL,
        password_hash=hash_password(FIRST_SUPERADMIN_PASSWORD),
        company_name=FIRST_SUPERADMIN_COMPANY,
        role="super_admin",
        is_active=True,
    )

    db.add(super_admin)
    db.commit()
