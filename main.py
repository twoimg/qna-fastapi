from fastapi import FastAPI

from app.api.main import api_router

app = FastAPI(title="anonQA", version="1.0.0")

app.include_router(api_router)

@app.get('/')
async def root():
    return {"message": "Hello Worlds"}
