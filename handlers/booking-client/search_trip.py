from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
import os
import certifi
import gtfs_to_mongo as utils

app = Flask(__name__)
CORS(app)


# Initialize MongoDB client
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri, tlsCAFile=certifi.where())
db = client["Booking-App-VGI"]
stop_times = db["stop_times"]
stops = db["stops"]

# util functions


def get_bus_number(trip_id):
    trip_id = trip_id.split(":")
    return trip_id[0]


def time_in_seconds(time):
    splitted_time = time.split(":")
    hours = int(splitted_time[0])
    mins = int(splitted_time[1])
    seconds = int(splitted_time[2])

    time_seconds = (hours*3600) + (mins*60) + (seconds)
    return time_seconds


def adjust_time(time_str):
    parts = time_str.split(":")
    hours = int(parts[0])
    if hours >= 24:
        hours -= 24
        parts[0] = f"{hours:02d}"
    return ":".join(parts)

# Define the route to search trips


@app.route("/api/search-trip", methods=["POST"])
def search_trips():
    trip_details = request.json

    departure_stop = trip_details.get('departure_stop')
    arrival_stop = trip_details.get('arrival_stop')

    departure_date = trip_details.get('departure_date')

    required_seats = trip_details.get('required_seats')

    departure_time = trip_details.get('departure_time')
    departure_time_seconds = time_in_seconds(departure_time)

    all_trips = utils.find_trips(departure_stop, arrival_stop)

    valid_routes = []

    if all_trips:
        for trip in all_trips:
            trip_id = trip["trip_id"]
            available_seats = stop_times.find_one(
                {"trip_id": trip_id}).get("max_seats")

            # Get the departure time of the trip from the database
            trip_departure_time = trip['departure_time']
            trip_departure_time_seconds = time_in_seconds(trip_departure_time)

            trip["departure_time"] = adjust_time(trip_departure_time)
            trip["arrival_time"] = adjust_time(trip["arrival_time"])

            # Compare times and seats
            if departure_time_seconds <= trip_departure_time_seconds and available_seats >= int(required_seats):
                valid_routes.append(trip)

    return jsonify({
        "valid_routes": valid_routes,
        "departure_stop": departure_stop,
        "arrival_stop": arrival_stop,
        "departure_time": departure_time,
        "required_seats": required_seats,
        "departure_date": departure_date
    })


if __name__ == "__main__":
    app.run(debug=True)
