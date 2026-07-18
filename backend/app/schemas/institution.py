import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class InstitutionCreate(BaseModel):
    name: str = Field(..., max_length=50)
    location: str | None = Field(None, max_length=100)
    contact_name: str | None = Field(None, max_length=30)
    contact_mobile: str | None = Field(None, max_length=11)
    contact_wechat: str | None = Field(None, max_length=30)


class InstitutionUpdate(BaseModel):
    name: str | None = Field(None, max_length=50)
    location: str | None = Field(None, max_length=100)
    contact_name: str | None = Field(None, max_length=30)
    contact_mobile: str | None = Field(None, max_length=11)
    contact_wechat: str | None = Field(None, max_length=30)


class InstitutionRead(BaseModel):
    id: uuid.UUID
    name: str
    location: str | None
    contact_name: str | None
    contact_mobile: str | None
    contact_wechat: str | None

    model_config = {"from_attributes": True}