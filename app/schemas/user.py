from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    bio: str | None = None

class UserResponse(BaseModel):
    id: int
    username: str
    created_at: datetime
    bio: str | None