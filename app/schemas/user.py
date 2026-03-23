from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    company_name: str | None = None


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    company_name: str | None = None
    role: str
    is_active: bool

    class Config:
        from_attributes = True
