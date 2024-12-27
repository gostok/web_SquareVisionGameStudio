from pydantic import BaseModel, EmailStr, field_validator
from uuid import UUID
import re

from app.routers.auth_app.models import Role


class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: Role = Role.USER

    @field_validator("username")
    def validate_username(cls, value):
        if len(value) < 4 or len(value) > 20:
            raise ValueError("Username must be between 4 and 20 characters long")
        return value


class UserCreate(UserBase):
    hashed_password: str

    @field_validator("hashed_password")
    def validate_hashed_password(cls, value):
        if len(value) < 6:
            raise ValueError("Hashed password must be at least 6 characters long")
        if not re.search(r"[a-zA-Z]", value):
            raise ValueError("Password must contain at least one letter")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one number")
        return value


class UserUpdate(UserBase):
    is_verified: bool = False


class User(UserBase):
    id: str
    is_verified: bool

    class Config:
        orm_mode = True  # Позволяет Pydantic работать с объектами SQLAlchemy
