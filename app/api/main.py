from fastapi import APIRouter

from app.api.routes import auth, posts, users

api_router = APIRouter()
api_router.include_router(auth.router, tags=['Auth'])
api_router.include_router(posts.router, tags=['Questions'])
api_router.include_router(users.router, tags=['Users'])