import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://harun@localhost:5432/repg_db"
)

JWT_PRIVATE_KEY_PATH = os.getenv("JWT_PRIVATE_KEY_PATH", "keys/private.pem")
JWT_PUBLIC_KEY_PATH = os.getenv("JWT_PUBLIC_KEY_PATH", "keys/public.pem")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "RS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
)


FIRST_SUPERADMIN_EMAIL = os.getenv("FIRST_SUPERADMIN_EMAIL")
FIRST_SUPERADMIN_PASSWORD = os.getenv("FIRST_SUPERADMIN_PASSWORD")
FIRST_SUPERADMIN_FULL_NAME = os.getenv("FIRST_SUPERADMIN_FULL_NAME", "Super Admin")
FIRST_SUPERADMIN_COMPANY = os.getenv("FIRST_SUPERADMIN_COMPANY", "RePG")
