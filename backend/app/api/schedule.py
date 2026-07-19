from fastapi import APIRouter

from app.models.schedule import Schedule
from app.om.schedule_om import schedule_om

router = APIRouter(prefix="/schedules", tags=["schedules"])


@router.get("")
async def list():
    return await schedule_om.list()


@router.get("/{id}")
async def get(id: str):
    return await schedule_om.get(id)


@router.post("")
async def create(schedule: Schedule):
    return await schedule_om.create(schedule)


@router.put("/{id}")
async def update(id: str, schedule: Schedule):
    schedule.id = id
    return await schedule_om.update(schedule)


@router.delete("/{id}")
async def delete(id: str):
    return await schedule_om.delete(id)