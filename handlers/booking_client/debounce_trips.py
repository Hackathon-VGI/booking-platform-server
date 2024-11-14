from flask import request, jsonify
import re
from extensions import get_mongo_db

mongo_db = get_mongo_db()

# MongoDB collections
stop_times = mongo_db["stop_times"]
user_trip_details = mongo_db["user_trip_details"]
stops = mongo_db["stops"]


def debounce_search():
    trip_details = request.json
    partial_stop = trip_details.get("partial_stop")
    all_stops = []  # List to hold matched stop names

    if partial_stop:
        # Search for stops that match the partial stop name (case-insensitive)
        matching_stops = stops.find(
            {"stop_name": {"$regex": re.escape(partial_stop), "$options": "i"}})

        # Collect all matched stop names into the list
        for stop in matching_stops:
            stop_name = stop.get("stop_name")
            if stop_name not in all_stops:
                all_stops.append(stop_name)

    # Return the found stop names (empty list if no matches)
    return jsonify(all_stops)
