from fastapi import APIRouter
import src.database as database
from src.models import NewTask
from src.models import Task, ResTask

router = APIRouter(
    prefix='/task',
    tags=['Tasks']
)


@router.get('', response_model=list[ResTask])
async def get_all_tasks():
    result = await database.get_all()
    return result


@router.post('', response_model=ResTask)
async def create_task(task: NewTask):
    result = await database.create_task(task.dict())
    return result


@router.put('/{id}')
async def update_task(task_id: str, task: Task):

    print(task_id)
    return task_id


@router.delete('/{id}')
async def delete_task(task_id: str):
    pass