import jwt
import bcrypt

from datetime import timedelta, datetime, timezone

from app.core.config import settings

JWT_ALGORITHM = "HS256"

def create_access_token(sub: str, expires_delta: timedelta) -> tuple[str, datetime]:
    expiration = datetime.now(timezone.utc) + expires_delta

    payload = {"exp": expiration, "sub": str(sub)}
    
    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=JWT_ALGORITHM)

    return encoded_jwt, expiration

def check_password_hash(plain_pw: str, hashed_pw: str) -> bool:
    return bcrypt.checkpw(plain_pw.encode('utf-8'), hashed_pw.encode('utf-8'))

def make_password_hash(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')