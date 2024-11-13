from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
import os
import certifi
from datetime import datetime
import gtfs_to_mongo as utils

app = Flask(__name__)
CORS(app)


# Initialize MongoDB client
# mongo_uri = os.getenv("MONGO_URI")
MONGO_URI="mongodb+srv://zainanwer24:osyP2q9A6L83y4Ku@booking-platform.w3axp.mongodb.net/"
mongo_uri = MONGO_URI

client = MongoClient(mongo_uri, tlsCAFile=certifi.where())
db = client["Booking-App-VGI"]
stop_times = db["stop_times"]
stops = db["stops"]

# util function
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


# Define the route to search trips
@app.route("/api/search-trip", methods=["GET"])
def search_trips():
    trip_details = request.json

    departure_stop = trip_details.get('departure_stop')  
    arrival_stop = trip_details.get('arrival_stop') 

    ### still need to implement seat logic     
    # required_seats = trip_details.get('required_seats') 
    departure_time = trip_details.get('departure_time') 

    departure_time_seconds = time_in_seconds(departure_time)
    
    all_trips = utils.find_trips(departure_stop, arrival_stop)
    
    valid_routes = []

    if all_trips:
        for trip in all_trips:
            # Get the departure time of the trip from the database
            trip_departure_time = trip['departure_time']
            trip_departure_time_seconds = time_in_seconds(trip_departure_time)

            # Compare times
            if departure_time_seconds <= trip_departure_time_seconds:
                valid_routes.append(trip)

    return jsonify(valid_routes)


if __name__ == "__main__":
    app.run(debug=True)