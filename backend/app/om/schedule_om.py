import uuid
import logging

from app.models.schedule import Schedule
from app.om.institution_om import institution_om
from app.dao.schedule_dao import schedule_dao


logger = logging.getLogger(__name__)


class ScheduleOM:
    async def list(self) -> list[Schedule]:
        schedules =  await schedule_dao.list()        
        for schedule in schedules:
            schedule.institution = await institution_om.get(schedule.institution_id)
        return schedules

    async def get(self, id: str) -> Schedule | None:
        schedule =  await schedule_dao.get(id)
        schedule.institution = await institution_om.get(schedule.institution_id)
        return schedule    

    async def create(self, schedule: Schedule) -> int:
        schedule.id = str(uuid.uuid4())
        return await schedule_dao.create(schedule)

    async def update(self, schedule: Schedule) -> int:
        logger.debug("start to updating.")
        num = await schedule_dao.update(schedule)
        logger.debug(f"complete to updating; count {num}")
        return num

    async def delete(self, id: str) -> int:
        return await schedule_dao.delete(id)


schedule_om = ScheduleOM()