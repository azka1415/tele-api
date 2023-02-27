from pydantic import BaseModel
from datetime import datetime
from src.models.utils import Usernames


class Meet(BaseModel):
    topic: str
    from_user: Usernames
    topic_detail: str
    time_start: str = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    time_end: str = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    created_at: str = datetime.now().strftime('%d/%m/%Y %H:%M:%S')


class ResMeet(Meet):
    meet_id: str


class NewMeet(BaseModel):
    topic: str
    topic_detail: str
    time_start: str = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    time_end: str = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
