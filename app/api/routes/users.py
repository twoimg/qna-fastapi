from fastapi import APIRouter, HTTPException

from app import crud

from app.api.deps import SessionDep

from app.schemas.user import UserResponse

router = APIRouter()

@router.get("/users/{username}", response_model=UserResponse)
async def get_user(username: str, db: SessionDep):
    user = crud.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user
