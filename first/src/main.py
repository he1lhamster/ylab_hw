import asyncio
from fastapi import FastAPI
from src.orm import AsyncORM
from src.api import router as api_router

app = FastAPI()


@app.on_event('startup')
async def on_startup_app():
    await AsyncORM.create_tables()


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(api_router)

