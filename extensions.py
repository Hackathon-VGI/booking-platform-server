from flask_pymongo import PyMongo
from pymongo import MongoClient
import certifi
import os

# Flask-PyMongo instance
db = PyMongo()

# Standalone MongoDB client for raw PyMongo usage
mongo_client = None
mongo_db = None

def init_mongo():
    global mongo_client, mongo_db
    if mongo_client is None:  # Ensure it's initialized only once
        mongo_uri = os.getenv("MONGO_URI")
        mongo_client = MongoClient(mongo_uri, tlsCAFile=certifi.where())
        mongo_db = mongo_client["Booking-App-VGI"]


def get_mongo_db():
    global mongo_db
    if mongo_db is None:
        init_mongo()
    return mongo_db