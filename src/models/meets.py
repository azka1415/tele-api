from pydantic import BaseModel
from datetime import datetime


class Meet(BaseModel):
    topic: str
    from_user: str
    topic_detail: str
    time_start: str = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    time_end: str = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    created_at: str = datetime.now().strftime('%d/%m/%Y %H:%M:%S')


class ResMeet(Meet):
    meet_id: str
