import uuid
import logging

from app.models.course import Course
from app.dao.course_dao import course_dao
from app.om.schedule_om import schedule_om

logger = logging.getLogger(__name__)


class CourseOM:
    async def list(self) -> list[Course]:
        courses =  await course_dao.list()
        for course in courses:
            course.schedule = await schedule_om.get(course.schedule_id)
        return courses

    async def get(self, id: str) -> Course | None:
        course = await course_dao.get(id)
        course.schedule = await schedule_om.get(course.schedule_id)
        return course

    async def create(self, course: Course) -> int:
        course.id = str(uuid.uuid4())
        return await course_dao.create(course)

    async def update(self, course: Course) -> int:
        logger.debug("start to updating.")
        num = await course_dao.update(course)
        logger.debug(f"complete to updating; count {num}")
        return num

    async def delete(self, id: str) -> int:
        return await course_dao.delete(id)


course_om = CourseOM()