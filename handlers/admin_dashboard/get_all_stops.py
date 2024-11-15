from extensions import get_mongo_db
from flask import jsonify


mongo_db = get_mongo_db()
stops_collection = mongo_db['stops']

def get_all_stops():
    # Query the stops collection and retrieve all stop names
    stop_names = stops_collection.distinct("stop_name")  # Use 'distinct' to get unique stop names
    print(stop_names)
    return jsonify({"message":"success", "stop_names": stop_names})
