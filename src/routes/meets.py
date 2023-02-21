from fastapi import APIRouter


router = APIRouter(
    prefix='/meets',
    tags=['Meets']
)


@router.get('')
async def get_all_meets():
    pass
