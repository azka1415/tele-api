from dotenv import find_dotenv, load_dotenv
from pymongo import MongoClient
from pymongo.cursor import Cursor
import os
from src.models import Task, ResTask
from datetime import datetime

load_dotenv(find_dotenv())

mongo = MongoClient(os.getenv('MONGO_URL'))

db = mongo['bot_assistant']

tasks_coll = db['tasks']


async def set_task_id(task: dict):
    task['task_id'] = str(task['_id'])


async def db_parser(cursor: Cursor) -> list[ResTask]:
    ''' parse data from database into lists '''
    items = []
    for doc in cursor:
        await set_task_id(doc)
        items.append(
            ResTask(**doc))
    return items


async def get_all() -> list[ResTask]:
    conn = tasks_coll.find()
    result = await db_parser(conn)
    return result


async def create_task(task: dict):
    task['created_at'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    task['last_updated'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    await set_task_id(task)
    if 'deadline' in task:
        new = tasks_coll.insert_one(task)
        task_id = tasks_coll.find_one(
            {'_id': new.inserted_id}
        )
        return task

    task['deadline'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    new = tasks_coll.insert_one(task)
    task_id = tasks_coll.find_one(
        {'_id': new.inserted_id}
    )
    return task


async def update_task():
    pass
