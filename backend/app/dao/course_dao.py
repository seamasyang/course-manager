from app.dao.base_dao import BaseDAO
from app.models.course import Course


class CourseDAO(BaseDAO):

    def __init__(self):
        self.sql_select = (
            "select id, schedule_id, date, content, follow_up "
            "from course"
        )

    async def list(self) -> list[Course]:
        rows = await self.fetch_all(self.sql_select)
        return [Course(**row) for row in rows]

    async def get(self, id: str) -> Course | None:
        sql = f"{self.sql_select} where id=%s"
        row = await self.fetch_one(sql, (id,))
        if row:
            return Course(**row)
        return None

    async def create(self, course: Course) -> int:
        sql = """
            insert into course (id, schedule_id, date, content, follow_up) 
            values (%s, %s, %s, %s, %s) 
        """
        return await self.execute(
            sql,
            (
                course.id,
                course.schedule_id,
                course.date,
                course.content,
                course.follow_up,
            ),
        )

    async def update(self, course: Course) -> int:
        sql = """
            update course 
            set schedule_id = %s, date = %s, content = %s, follow_up = %s
            where id = %s
        """
        return await self.execute(
            sql,
            (
                course.schedule_id,
                course.date,
                course.content,
                course.follow_up,
                course.id,
            ),
        )

    async def delete(self, id: str) -> int:
        sql = "delete from course where id = %s"
        return await self.execute(sql, (id,))


course_dao = CourseDAO()