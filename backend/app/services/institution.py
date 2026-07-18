import uuid
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.institution import Institution
from app.schemas.institution import InstitutionCreate, InstitutionUpdate


async def list_institutions(db: AsyncSession) -> list[Institution]:
    result = await db.execute(select(Institution).order_by(Institution.name))
    return list(result.scalars().all())


async def get_institution(db: AsyncSession, institution_id: uuid.UUID) -> Institution | None:
    result = await db.execute(select(Institution).where(Institution.id == institution_id))
    return result.scalar_one_or_none()


async def create_institution(db: AsyncSession, data: InstitutionCreate) -> Institution:
    institution = Institution(**data.model_dump())
    db.add(institution)
    await db.flush()
    await db.refresh(institution)
    return institution


async def update_institution(db: AsyncSession, institution_id: uuid.UUID, data: InstitutionUpdate) -> Institution | None:
    institution = await get_institution(db, institution_id)
    if not institution:
        return None
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(institution, key, value)
    await db.flush()
    await db.refresh(institution)
    return institution


async def delete_institution(db: AsyncSession, institution_id: uuid.UUID) -> bool:
    result = await db.execute(delete(Institution).where(Institution.id == institution_id))
    return result.rowcount > 0