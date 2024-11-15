from flask import request, jsonify
from extensions import get_mongo_db

mongo_db = get_mongo_db()

# MongoDB collections
stop_times = mongo_db["stop_times"]
user_trip_details = mongo_db["user_trip_details"]
stops = mongo_db["stops"]

def toggle_stop_status():
  data = request.json
  stop_name = data.get("stop_name")

  current_stop_status = stops.find_one({"stop_name" : stop_name}).get("stop_blocked")

  if not current_stop_status:
    stops.update_one(
    {"stop_name": stop_name},  # Find the document where stop_name matches
    {"$set": {"stop_blocked": True}}  # Set stop_blocked to True
)
  else:
    stops.update_one(
    {"stop_name": stop_name},  # Find the document where stop_name matches
    {"$set": {"stop_blocked": False}}  # Set stop_blocked to True
)
  return jsonify({"message":"status changed successfully"})

