from datetime import date
from typing import Optional

from pydantic import BaseModel
from app.models import Schedule

class Course(BaseModel):
    id: str = ""
    schedule_id: str = ""
    date: Optional[date]
    content: str = ""
    follow_up: str = ""

    #
    schedule: Optional[Schedule] = None

