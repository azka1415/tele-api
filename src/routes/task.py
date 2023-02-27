from fastapi import APIRouter, Depends
import src.controllers.task as task
from src.models.task import ResTask, UpdateTask, NewTask, MonthQuery, DayQuery
from src.models.utils import Usernames
from typing import Optional
router = APIRouter(
    prefix='/task',
    tags=['Tasks']
)


@router.get('', response_model=list[ResTask])
async def get_all_tasks(for_username: Optional[Usernames] = None, by_username: Optional[Usernames] = None):
    result = await task.get_all(for_username, by_username)
    return result


@router.post('', response_model=ResTask)
async def create_task(task: NewTask, task_creator: Usernames):
    result = await task.create_task(task.dict(), task_creator.value)
    return result


@router.put('/{task_id}', response_model=ResTask)
async def update_task(task_id: str, task: UpdateTask):
    res = await task.update_task(task_id, task.dict())
    return res


@router.delete('/{task_id}', status_code=204)
async def delete_task(task_id: str):
    await task.delete_task(task_id)
    return {"detail": 'Task Deleted Successfully'}


@router.get('/new', response_model=list[ResTask])
async def get_all_tasks_new():
    result = await task.get_all()
    return result


@router.get('/deadline-month', response_model=list[ResTask])
async def get_tasks_by_month(deadline_month: MonthQuery = Depends()):
    res = await task.get_task_by_month(deadline_month)
    return res


@router.get('/deadline-day')
async def get_tasks_by_day(deadline_day: DayQuery = Depends()):
    res = await task.get_task_by_day(deadline_day)
    return res
