from pymongo import ReturnDocument
from pymongo.cursor import Cursor
from src.models.meets import ResMeet
from src.database.client import mongo
from datetime import datetime
from typing import Optional
from bson.objectid import ObjectId
from fastapi import HTTPException


db = mongo['bot_assistant']

meets = db['meets']


async def set_meet_id(meet: dict, old_dict: Optional[dict] = False):

    if old_dict is not False:
        meet['meet_id'] = str(old_dict['_id'])
        return
    meet['meet_id'] = str(meet['_id'])
    return


async def db_parser(cursor: Cursor) -> list[ResMeet]:
    ''' parse data from database into lists '''
    items = []
    for doc in cursor:
        await set_meet_id(doc)
        items.append(
            ResMeet(**doc))
    return items


async def get_meets():
    conn = meets.find()
    res = await db_parser(conn)
    return res


async def create_meet(meet: dict, meet_creator: str):
    meet['created_at'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    try:
        meet['from_user'] = meet_creator
    except Exception as user_error:
        user = str(user_error).replace("'", '')
        raise HTTPException(404, f'{user} is not a valid user') from user_error

    new = meets.insert_one(meet)
    meet_id = meets.find_one(
        {'_id': new.inserted_id}
    )

    await set_meet_id(meet, meet_id)
    return meet


async def update_meet(meet_id: str, updates: dict):
    res = meets.find_one_and_update({'_id': ObjectId(meet_id)}, {
        '$set': {
            'topic': updates['topic'],
            'topic_detail': updates['topic_detail'],
            'from_user': updates['from_user'],
            'time_start': updates['time_start'],
            'time_end': updates['time_end'],
        }
    }, return_document=ReturnDocument.AFTER)
    if res is None:
        raise HTTPException(404, 'Meet not found')
    find = meets.find_one({'_id': ObjectId(meet_id)})
    return find


async def delete_meet(meet_id: str):
    res = meets.find_one_and_delete({'_id': ObjectId(meet_id)})
    if res is None:
        raise HTTPException(404, 'Meeting not found')
    return {'detail': 'Meeting deleted successfully'}
