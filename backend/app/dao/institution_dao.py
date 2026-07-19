from app.dao.base_dao import BaseDAO
from app.models import Institution


class InstitutionDAO(BaseDAO):

    def __init__(self):
        self.sql_select = "select id, name, location, contact_name, contact_mobile, contact_wechat from institution"

    async def list(self) -> list[Institution]:
        rows = await self.fetch_all(self.sql_select)
        return [Institution(**row) for row in rows]

    async def get(self, id: str) -> Institution | None:
        sql = f"{self.sql_select} where id=%s"
        row = await self.fetch_one(sql, (id,))
        if row:
            return Institution(**row)
        return None

    async def create(self, institution: Institution) -> int:
        sql = """
            insert into institution (id, name, location, contact_name, contact_mobile, contact_wechat) 
            values (%s, %s, %s, %s, %s, %s) 
        """
        return await self.execute(
            sql,
            (
                institution.id,
                institution.name,
                institution.location,
                institution.contact_name,
                institution.contact_mobile,
                institution.contact_wechat,
            ),
        )

    async def update(self, institution: Institution) -> int:
        sql = """
            update institution 
            set name = %s, location = %s, contact_name = %s, contact_mobile = %s, contact_wechat = %s             
            where id = %s
        """
        return await self.execute(
            sql,
            (
                institution.name,
                institution.location,
                institution.contact_name,
                institution.contact_mobile,
                institution.contact_wechat,
                institution.id,
            ),
        )

    async def delete(self, id: str) -> int:
        sql = "delete from institution where id = %s"
        return await self.execute(sql, (id,))


institution_dao = InstitutionDAO()
