from pymongo import ReturnDocument
from pymongo.cursor import Cursor
from src.models.task import ResTask, DayQuery, MonthQuery
from src.models.utils import Usernames, UsernamesAndId
from src.database.client import mongo
from datetime import datetime
from typing import Optional
from bson.objectid import ObjectId
from fastapi import HTTPException


db = mongo['bot_assistant']

tasks = db['tasks']


async def set_task_id(task: dict, old_dict: Optional[dict] = False):
    ''' set task id of task from _id or somewhere else'''
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


async def query_parser(for_name: str, by_name: str):
    ''' check and parse the given name and for name '''
    if for_name == '' and by_name == '':
        conn = conn = tasks.find()
        return conn
    if by_name == '':
        conn = tasks.find({
            'username': for_name,
        })
        return conn
    if for_name == '':
        conn = tasks.find({
            'from_user.username': by_name,
        })
        return conn

    conn = tasks.find({
        'username': for_name,
        'from_user.username': by_name
    })
    return conn


async def get_all(for_username: Usernames = None, by_username: Usernames = None) -> list[ResTask]:
    ''' get all tasks '''
    for_name = for_username.value if for_username is not None else ''
    by_name = by_username.value if by_username is not None else ''
    conn = await query_parser(for_name, by_name)
    result = await db_parser(conn)
    return result


async def create_task(task: dict, task_creator: str):
    '''create a task'''
    task['created_at'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    task['last_updated'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    try:
        task['from_user'] = {
            'username': task_creator,
            'user_id': UsernamesAndId[task_creator].value
        }
    except Exception as user_error:
        ''' catch errors '''
        user = str(user_error).replace("'", '')
        raise HTTPException(404, f"{user} is not a valid user") from user_error

    if 'deadline' in task:
        new = tasks.insert_one(task)
        task_id = tasks.find_one(
            {'_id': new.inserted_id}
        )
        await set_task_id(task, task_id)

        return task

    task['deadline'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    new = tasks.insert_one(task)
    task_id = tasks.find_one(
        {'_id': new.inserted_id}
    )

    await set_task_id(task, task_id)
    return task


async def update_task(task_id: str, updates: dict):
    ''' Update a task'''
    res = tasks.find_one_and_update({'_id': ObjectId(task_id)}, {
        '$set': {
            'username': updates['username'],
            'task': updates['task'],
            'task_detail': updates['task_detail'],
            'status': updates['status'],
            'last_updated': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            'deadline': updates['deadline'],
            'task_id': task_id
        }
    }, return_document=ReturnDocument.AFTER)
    if res is None:
        raise HTTPException(404, 'Task not found')
    find = tasks.find_one({'_id': ObjectId(task_id)})
    return find


async def delete_task(task_id: str):
    ''' Delete a task'''
    res = tasks.find_one_and_delete({'_id': ObjectId(task_id)})
    if res is None:
        raise HTTPException(404, 'Task not found')


async def get_task_by_month(deadline: MonthQuery):
    ''' Get a task by month'''
    month = deadline.month.split("/")[1]
    if int(month) > 12:
        raise HTTPException(404, 'Invalid Month')
    get_by_month = tasks.find({
        "deadline": {
            "$regex": f".*/{month}/.*"
        },
        "status": {
            "$ne": "DONE"
        }
    }
    )
    res = await db_parser(get_by_month)
    return res


async def get_task_by_day(deadline: DayQuery):
    ''' Get a task by day'''
    day = deadline.day.split("/")[0]
    if int(day) > 31:
        raise HTTPException(404, 'Invalid Day')
    get_by_day = tasks.find({
        "deadline": {
            "$regex": f"{day}/.*/.*"
        },
        "status": {
            "$ne": "DONE"
        }
    }
    )
    res = await db_parser(get_by_day)
    return res
