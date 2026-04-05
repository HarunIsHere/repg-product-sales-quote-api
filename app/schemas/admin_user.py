from pydantic import BaseModel, EmailStr


class AdminUserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    company_name: str
    role: str
