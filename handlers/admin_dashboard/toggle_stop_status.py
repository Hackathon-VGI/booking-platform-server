from flask import request, jsonify
from extensions import get_mongo_db

mongo_db = get_mongo_db()

# MongoDB collections
stop_times = mongo_db["stop_times"]
user_trip_details = mongo_db["user_trip_details"]
stops = mongo_db["stops"]


def toggle_stop_status():
  '''
    Admin would be block stop
    Stop with same names would be updated together
  '''
  data = request.json
  stop_name = data.get("stop_name")
  stop_blocked = data.get("stop_blocked")

  if not stop_name:
    return jsonify({"message": "stop_name is required"}), 400

  try:
    # Find all stops with the same stop_name
      stops.update_many(
        {"stop_name": stop_name},  # Filter by stop_name
          {"$set": {"stop_blocked": stop_blocked}}  # Update stop_blocked to the new status
      )
      return jsonify({"message": "Stop status updated successfully"}), 200
  except Exception as e:
    return jsonify({"message": str(e)}), 500

