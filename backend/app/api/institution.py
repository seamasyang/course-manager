from fastapi import APIRouter

from app.models import Institution
from app.om.institution_om import institution_om

router = APIRouter(prefix="/institutions", tags=["institutions"])


@router.get("")
async def list():
    return await institution_om.list()

@router.get("/{id}")
async def get(id: str):
    return await institution_om.get(id)

@router.post("")
async def create(institution: Institution):
    return await institution_om.create(institution)

@router.put("/{id}")
async def update(id:str, institution: Institution):
    institution.id = id
    return await institution_om.update(institution)

@router.delete("/{id}")
async def delete(id: str):
    return await institution_om.delete(id)