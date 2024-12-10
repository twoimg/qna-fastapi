from fastapi import FastAPI

from app.api.main import api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="anonQA", version="1.0.0")

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get('/')
async def root():
    return {"message": "Hello Worlds"}
