from dotenv import find_dotenv, load_dotenv
from pymongo import MongoClient, ReturnDocument
from pymongo.cursor import Cursor
import os
from src.models import ResTask, Usernames
from datetime import datetime
from typing import Optional
from bson.objectid import ObjectId
load_dotenv(find_dotenv())

mongo = MongoClient(os.getenv('MONGO_URL'))

db = mongo['bot_assistant']

tasks_coll = db['tasks']


async def set_task_id(task: dict, old_dict: Optional[dict] = False):

    if old_dict is not False:
        task['task_id'] = str(old_dict['_id'])
        return
    task['task_id'] = str(task['_id'])
    return


async def db_parser(cursor: Cursor) -> list[ResTask]:
    ''' parse data from database into lists '''
    items = []
    for doc in cursor:
        await set_task_id(doc)
        items.append(
            ResTask(**doc))
    return items


async def get_all(username: Optional[Usernames] = None) -> list[ResTask]:
    name = username.value if username is not None else ''
    if name == '':
        conn = conn = tasks_coll.find()
        result = await db_parser(conn)
        return result
    conn = tasks_coll.find({
        'username': name
    })
    result = await db_parser(conn)
    return result


async def create_task(task: dict):
    task['created_at'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    task['last_updated'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    if 'deadline' in task:
        new = tasks_coll.insert_one(task)
        task_id = tasks_coll.find_one(
            {'_id': new.inserted_id}
        )
        await set_task_id(task, task_id)

        return task

    task['deadline'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    new = tasks_coll.insert_one(task)
    task_id = tasks_coll.find_one(
        {'_id': new.inserted_id}
    )
    await set_task_id(task, task_id)
    return task


async def update_task(task_id: str, updates: dict):

    tasks_coll.find_one_and_update({'_id': ObjectId(task_id)}, {
        '$set': {
            'username': updates['username'],
            'task': updates['task'],
            'task_detail': updates['task_detail'],
            'status': updates['status'],
            'last_updated': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            'deadline': updates['deadline'],
            'task_id': task_id
        }
    })
    find = tasks_coll.find_one({'_id': ObjectId(task_id)})
    return find
