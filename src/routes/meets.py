from fastapi import APIRouter
from src.controllers import meets
from src.models.meets import ResMeet, NewMeet
from src.models.utils import Usernames
router = APIRouter(
    prefix='/meets',
    tags=['Meets']
)


@router.get('', response_model=list[ResMeet])
async def get_all_meets():
    res = await meets.get_meets()
    return res


@router.post('', response_model=ResMeet)
async def create_meeting(meet: NewMeet, task_creator: Usernames):
    result = await meets.create_meet(meet.dict(), task_creator.value)
    return result


@router.put('/{meet_id}')
async def update_task(meet_id: str, meet: NewMeet):
    res = await meets.update_meet(meet_id, meet.dict())
    return res


@router.delete('/{meet_id}')
async def delete_meet(meet_id: str):
    res = await meets.delete_meet(meet_id)
    return res
