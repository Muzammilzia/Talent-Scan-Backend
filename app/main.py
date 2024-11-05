from typing import Union
from dotenv import load_dotenv
from fastapi import FastAPI
from app.api.v1.routers import api_router
from .db.base import connect_to_database

load_dotenv()

app = FastAPI()

connect_to_database()

# Include the API router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return "Hello World!"