from fastapi import APIRouter
from app.api.endpoints.institution import router as institution_router

api_router = APIRouter(prefix="/api")
api_router.include_router(institution_router)