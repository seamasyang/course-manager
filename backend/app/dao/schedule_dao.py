from app.dao.base_dao import BaseDAO
from app.models.schedule import Schedule


class ScheduleDAO(BaseDAO):

    def __init__(self):
        self.sql_select = (
            "select id, institution_id, subject, teacher_name, "
            "start_date, end_date, start_time, end_time, remarks "
            "from schedule"
        )

    async def list(self) -> list[Schedule]:
        sql = f"{self.sql_select} order by start_date "
        rows = await self.fetch_all(sql)
        return [Schedule(**row) for row in rows]

    async def get(self, id: str) -> Schedule | None:
        sql = f"{self.sql_select} where id=%s"
        row = await self.fetch_one(sql, (id,))
        if row:
            return Schedule(**row)
        return None

    async def create(self, schedule: Schedule) -> int:
        sql = """
            insert into schedule (id, institution_id, subject, teacher_name, 
                                  start_date, end_date, start_time, end_time, remarks) 
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s) 
        """
        return await self.execute(
            sql,
            (
                schedule.id,
                schedule.institution_id,
                schedule.subject,
                schedule.teacher_name,
                schedule.start_date,
                schedule.end_date,
                schedule.start_time,
                schedule.end_time,
                schedule.remarks,
            ),
        )

    async def update(self, schedule: Schedule) -> int:
        sql = """
            update schedule 
            set institution_id = %s, subject = %s, teacher_name = %s, 
                start_date = %s, end_date = %s, start_time = %s, end_time = %s, remarks = %s
            where id = %s
        """
        return await self.execute(
            sql,
            (
                schedule.institution_id,
                schedule.subject,
                schedule.teacher_name,
                schedule.start_date,
                schedule.end_date,
                schedule.start_time,
                schedule.end_time,
                schedule.remarks,
                schedule.id,
            ),
        )

    async def delete(self, id: str) -> int:
        sql = "delete from schedule where id = %s"
        return await self.execute(sql, (id,))


schedule_dao = ScheduleDAO()