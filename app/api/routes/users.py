from fastapi import APIRouter, HTTPException

from app import crud

from app.api.deps import SessionDep, CurrentUser

from app.schemas.user import UserResponse, UserUpdate

router = APIRouter()

@router.get("/users/{username}", response_model=UserResponse)
async def get_user(username: str, db: SessionDep):
    user = crud.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.patch("/users/{username}")
async def update_user(username: str, update: UserUpdate, db: SessionDep, user: CurrentUser):
    db_user = crud.get_user_by_username(db, username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if db_user.id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")

    db_user.bio = update.bio
    db.commit()
    db.refresh(db_user)

    return {"message": "User updated successfully"}