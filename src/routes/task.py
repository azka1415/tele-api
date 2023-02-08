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
async def get_all_tasks(for_username: Optional[Usernames] = None, by_username: Optional[Usernames] = None):
    result = await database.get_all(for_username, by_username)
    return result


@router.post('', response_model=ResTask)
async def create_task(task: NewTask, task_creator: Usernames):
    result = await database.create_task(task.dict(), task_creator.value)
    return result


@router.put('/{task_id}', response_model=ResTask)
async def update_task(task_id: str, task: UpdateTask):
    res = await database.update_task(task_id, task.dict())
    return res


@router.delete('/{task_id}', status_code=204)
async def delete_task(task_id: str):
    await database.delete_task(task_id)
    return {"detail": 'Task Deleted Successfully'}
