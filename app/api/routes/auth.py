from fastapi import APIRouter, Depends, status, HTTPException, Response
from app.schemas.auth import Token, UserCreate

from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm
from app.core.database.db import get_db
from sqlalchemy.orm import Session

from app import crud
from app.core.security import create_access_token

from app.core.config import settings
from app.api.deps import SessionDep

router = APIRouter()

@router.post("/login")
async def login(
    response: Response, db: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()
):
    user = crud.authenticate_user(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password"
        )

    token_expiration = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token, exp = create_access_token(user.id, token_expiration)

    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=True,
        max_age=exp,
    )

    return {
        "access_token": access_token,  # Must be "access_token", not "token"
        "token_type": "bearer"
    }

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
     user_create: UserCreate, db: Session = Depends(get_db)
):
    unique, message = crud.verify_unique_user(
        db, user_create.username, user_create.email
    )
    if not unique:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
    
    user = crud.create_user(db, user_create)
    return {"message": f"User {user.username} Created Successfully"}


@router.post("/forgot-password")
async def reset_password():
    return {"message": "Forgot Password"}