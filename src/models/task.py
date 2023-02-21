from pydantic import BaseModel
from datetime import datetime
from fastapi import Query
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


class UsernamesAndId(int, Enum):
    iki_be_ph = 1211950206
    urbiscuit = 1268637225
    Arigofhrz = 1415008365
    nanassssa = 731203660
    nathan_aptanta = 1239587269
    Oktapiancaw = 916823025
    rizalwidiatmaja = 757866026


class FromUser(dict):
    username: str
    user_id: int


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