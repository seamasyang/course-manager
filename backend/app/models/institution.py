import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class Institution(Base):
    __tablename__ = "institution"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False)
    location = Column(String(100), nullable=True)
    contact_name = Column(String(30), nullable=True)
    contact_mobile = Column(String(11), nullable=True)
    contact_wechat = Column(String(30), nullable=True)