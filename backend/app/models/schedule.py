from datetime import date, time
from typing import Literal

from pydantic import BaseModel

Subject = Literal["数学", "英语", "物理", "体育", "化学", "语文"]


class Schedule(BaseModel):
    id: str = ""
    institution_id: str = ""
    subject: Subject = "数学"
    teacher_name: str = ""
    start_date: date | None = None
    end_date: date | None = None
    start_time: time | None = None
    end_time: time | None = None
    remarks: str = ""