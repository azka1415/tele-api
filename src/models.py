from pydantic import BaseModel
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


class UsernamesAndId(dict, Enum):
    iki = {'user_id': 1211950206, 'username': "iki_be_ph"}
    alfa = {'user_id': 1268637225, 'username': "urbiscuit"}
    arigo = {'user_id': 1415008365, 'username': "Arigofhrz"}
    nasri = {'user_id': 731203660, 'username': "nanassssa"}
    nathan = {'user_id': 1239587269, 'username': "nathan_aptanta"}
    okta = {'user_id': 916823025, 'username': "Oktapiancaw"}
    rizal = {'user_id': 757866026, 'username': "rizalwidiatmaja"}


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
