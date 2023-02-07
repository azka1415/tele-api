from fastapi import APIRouter
import src.database as database
from src.models import NewTask
from src.models import ResTask, UpdateTask, Usernames
from typing import Optional
router = APIRouter(
    prefix='/task',
    tags=['Tasks']
)


@router.get('', response_model=list[ResTask])
async def get_all_tasks(username: Optional[Usernames] = None):
    result = await database.get_all(username)
    return result


@router.post('', response_model=ResTask)
async def create_task(task: NewTask):
    result = await database.create_task(task.dict())
    return result


@router.put('/{task_id}', response_model=ResTask)
async def update_task(task_id: str, task: UpdateTask):
    res = await database.update_task(task_id, task.dict())
    return res


@router.delete('/{id}')
async def delete_task(task_id: str):
    pass
