# app/api/v1/routers.py
from fastapi import APIRouter
from app.api.v1.endpoints import todo
from pymongo import MongoClient

client = MongoClient('mongodb+srv://talenscan:6ObVzMjLPDkZQxIo@cluster0.oqzdd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['talent-scan-db']

api_router = APIRouter()

# Include item routes
api_router.include_router(todo.router, prefix="/todo", tags=["todos"])