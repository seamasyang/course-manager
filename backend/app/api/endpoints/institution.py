import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.institution import InstitutionCreate, InstitutionRead, InstitutionUpdate
from app.services import institution as institution_service

router = APIRouter(prefix="/institutions", tags=["institutions"])


@router.get("/", response_model=list[InstitutionRead])
async def list_institutions(db: AsyncSession = Depends(get_db)):
    return await institution_service.list_institutions(db)


@router.get("/{institution_id}", response_model=InstitutionRead)
async def get_institution(institution_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    institution = await institution_service.get_institution(db, institution_id)
    if not institution:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Institution not found")
    return institution


@router.post("/", response_model=InstitutionRead, status_code=status.HTTP_201_CREATED)
async def create_institution(data: InstitutionCreate, db: AsyncSession = Depends(get_db)):
    return await institution_service.create_institution(db, data)


@router.put("/{institution_id}", response_model=InstitutionRead)
async def update_institution(institution_id: uuid.UUID, data: InstitutionUpdate, db: AsyncSession = Depends(get_db)):
    institution = await institution_service.update_institution(db, institution_id, data)
    if not institution:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Institution not found")
    return institution


@router.delete("/{institution_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_institution(institution_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    deleted = await institution_service.delete_institution(db, institution_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Institution not found")