import uuid
import logging

from app.models.course import Course
from app.dao.course_dao import course_dao

logger = logging.getLogger(__name__)


class CourseOM:
    async def list(self) -> list[Course]:
        return await course_dao.list()

    async def get(self, id: str) -> Course | None:
        return await course_dao.get(id)

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