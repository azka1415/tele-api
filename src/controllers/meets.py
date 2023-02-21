from pymongo import ReturnDocument
from pymongo.cursor import Cursor
from src.models.task import ResTask, Usernames, UsernamesAndId
from src.database.client import mongo
from datetime import datetime
from typing import Optional
from bson.objectid import ObjectId
from fastapi import HTTPException


db = mongo['bot_assistant']

meets = db['meets']


async def set_meet_id(task: dict, old_dict: Optional[dict] = False):

    if old_dict is not False:
        task['task_id'] = str(old_dict['_id'])
        return
    task['task_id'] = str(task['_id'])
    return


async def db_parser(cursor: Cursor) -> list[ResTask]:
    ''' parse data from database into lists '''
    items = []
    for doc in cursor:
        await set_meet_id(doc)
        items.append(
            ResTask(**doc))
    return items
