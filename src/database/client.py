from pymongo import MongoClient
from dotenv import find_dotenv, load_dotenv
import os

load_dotenv(find_dotenv())
mongo = MongoClient(os.getenv('MONGO_URL'))
