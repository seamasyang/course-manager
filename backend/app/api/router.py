from fastapi import APIRouter
from app.api.institution import router as institution_router
from app.api.schedule import router as schedule_router
from app.api.course import router as course_router

api_router = APIRouter(prefix="/api")
api_router.include_router(institution_router)
api_router.include_router(schedule_router)
api_router.include_router(course_router)
