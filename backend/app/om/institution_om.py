import uuid
import logging

from app.models import Institution
from app.dao.institution_dao import institution_dao

logger = logging.getLogger(__name__)

class InstitutionOM:
    async def list(self) -> list[Institution]:
        return await institution_dao.list()
    
    async def get(self, id:str) -> Institution|None:
        return await institution_dao.get(id)
    
    async def create(self, institution:Institution) -> int:
        institution.id = str(uuid.uuid4())
        return await institution_dao.create(institution)
    
    async def update(self, institution:Institution) -> int:
        logger.debug("start to updating.")
        num = await institution_dao.update(institution)
        logger.debug("complete to updating; count {num}")
        return num
    
    async def delete(self, id:str) -> Institution|None:
        return await institution_dao.delete(id)


institution_om = InstitutionOM()