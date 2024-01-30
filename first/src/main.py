from contextlib import asynccontextmanager

from fastapi import FastAPI
from orm import AsyncORM
from api import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await AsyncORM.create_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
def health_check():
    return {"status": "OK"}


app.include_router(api_router)


