import certifi
import os 
from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

mongo_uri = os.getenv("MONGO_URI")
mongo_client = MongoClient(mongo_uri, tlsCAFile=certifi.where())
mongo_db = mongo_client["Booking-App-VGI"]
stops = mongo_db["stops"]

# Add the new key 'stop_blocked' with a default Boolean value of False to all documents
def add_field():
  try:
    stops.update_many({}, {"$set": {"stop_blocked": False}})
    print("successfully updated")
  except Exception as e:
    print("update error")

# add_field()

# if __name__ == "__main__":
#   app.run(host="0.0.0.0", debug=True, port=6000)