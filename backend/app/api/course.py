from fastapi import APIRouter

from app.models.course import Course
from app.om.course_om import course_om

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("")
async def list():
    return await course_om.list()


@router.get("/{id}")
async def get(id: str):
    return await course_om.get(id)


@router.post("")
async def create(course: Course):
    return await course_om.create(course)


@router.put("/{id}")
async def update(id: str, course: Course):
    course.id = id
    return await course_om.update(course)


@router.delete("/{id}")
async def delete(id: str):
    return await course_om.delete(id)