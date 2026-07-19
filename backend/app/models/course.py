from datetime import date
from typing import Optional

from pydantic import BaseModel


class Course(BaseModel):
    id: str = ""
    schedule_id: str = ""
    date: Optional[date] = None
    content: str = ""
    follow_up: str = ""
