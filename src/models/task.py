from pydantic import BaseModel
from datetime import datetime
from fastapi import Query
from typing import Optional
from src.models.utils import Status, FromUser


class Task(BaseModel):
    username: str
    task: str
    task_detail: str
    from_user: FromUser
    status: Status = Status.NOTED
    created_at: str = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    last_updated: str = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    deadline: str = datetime.now().strftime('%d/%m/%Y %H:%M:%S')


class NewTask(BaseModel):
    username: str
    task: str
    task_detail: str
    status: Status = Status.NOTED
    deadline: str = datetime.now().strftime('%d/%m/%Y %H:%M:%S')


class ResTask(Task):
    task_id: str


class UpdateTask(BaseModel):
    username: str
    task: str
    task_detail: str
    status: Status = Status.ON_PROGRESS
    deadline: Optional[str] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')


class MonthQuery:
    def __init__(self, month: str = Query(..., description='example: 11/02/2023')):
        self.month = month


class DayQuery:
    def __init__(self, day: str = Query(..., description='example: 11/02/2023')):
        self.day = day
