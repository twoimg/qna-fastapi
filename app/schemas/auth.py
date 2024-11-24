from datetime import datetime
from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_at: datetime

class TokenPayload(BaseModel):
    exp: datetime
    sub: str

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str