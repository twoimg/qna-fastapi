from typing import Annotated

from app.core.config import settings

import jwt
from jwt.exceptions import InvalidTokenError

from pydantic import ValidationError

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app import crud
from sqlalchemy.orm import Session
from app.core.database.db import get_db

from app.models.user import User
from app.schemas.auth import TokenPayload


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]

def get_current_user(token: TokenDep, db: SessionDep) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=["HS256"]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid Token"
        )
    
    user = crud.get_user_by_id(db, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="Invalid Credentials")
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]