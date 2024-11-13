from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
import re
import certifi


# Initialize Flask app
app = Flask(__name__)

# Set up MongoDB connection
MONGO_URI="mongodb+srv://zainanwer24:osyP2q9A6L83y4Ku@booking-platform.w3axp.mongodb.net/"
mongo_uri = MONGO_URI

client = MongoClient(mongo_uri, tlsCAFile=certifi.where())
db = client["Booking-App-VGI"]
stop_times = db["stop_times"]
user_trip_details = db["user_trip_details"]
stops = db["stops"]

@app.route("/debounce_search", methods=["GET"])
def debounce_search():
    trip_details = request.json    
    partial_stop = trip_details.get("partial_stop")

    all_stops = []  # List to hold matched stop names

    if partial_stop:
        # Search for stops that match the partial stop name (case-insensitive)
        matching_stops = stops.find({"stop_name": {"$regex": re.escape(partial_stop), "$options": "i"}})
        
        # Collect all matched stop names into the list
        for stop in matching_stops:
            stop_name = stop.get("stop_name")
            if stop_name not in all_stops:
                all_stops.append(stop_name)

    # Return the found stop names (empty list if no matches)
    return jsonify(all_stops)

if __name__ == "__main__":
    app.run(debug=True)
