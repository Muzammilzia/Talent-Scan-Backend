# app/api/v1/routers.py
from fastapi import APIRouter
from app.api.v1.endpoints import candidate
from app.api.v1.endpoints import company

api_router = APIRouter()

# Include routes
api_router.include_router(candidate.router, prefix="/candidate", tags=["candidate"])
api_router.include_router(company.router, prefix="/company", tags=["company"])