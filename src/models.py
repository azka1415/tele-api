from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional


class Status(str, Enum):
    DONE = 'DONE'
    ON_PROGRESS = 'ON PROGRESS'
    PENDING = 'PENDING'
    NOTED = 'NOTED'


class Usernames(str, Enum):
    alfa = "urbiscuit"
    arigo = "Arigofhrz"
    iki = "iki_be_ph"
    nasri = "nanassssa"
    nathan = "nathan_aptanta"
    okta = "Oktapiancaw"
    pasca = "pascarmdn"
    rizal = "rizalwidiatmaja"


class Task(BaseModel):
    username: str
    task: str
    task_detail: str
    from_user: str
    status: Status = Status.NOTED
    created_at: str = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    last_updated: str = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    deadline: str = datetime.now().strftime('%d/%m/%Y %H:%M:%S')


class NewTask(BaseModel):
    username: str
    task: str
    task_detail: str
    status: Status = Status.ON_PROGRESS
    deadline: str = datetime.now().strftime('%d/%m/%Y %H:%M:%S')


class ResTask(Task):
    task_id: str


class UpdateTask(BaseModel):
    username: str
    task: str
    task_detail: str
    status: Status = Status.ON_PROGRESS
    deadline: Optional[str] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
