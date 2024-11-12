from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
import certifi

app = Flask(__name__)

# Initialize MongoDB client
# mongo_uri = os.getenv("MONGO_URI")
MONGO_URI="mongodb+srv://zainanwer24:osyP2q9A6L83y4Ku@booking-platform.w3axp.mongodb.net/"
mongo_uri = MONGO_URI

client = MongoClient(mongo_uri, tlsCAFile=certifi.where())
db = client["Booking-App-VGI"]
stop_times = db["stop_times"]
user_trip_details = db["user_trip_details"]
stops = db["stops"]

# util function
def get_bus_number(trip_id):
    trip_id = trip_id.split(":")
    return trip_id[0]

# Define the route to retrieve user data by user email
@app.route("/api/get-trip/<email>", methods=["GET"])
def get_trip(email):
    # Find the trip data by trip_id
    trips = user_trip_details.find({"email": email})
    all_trips_data = []

    # If the trip is found, return the trip details
    for trip in trips:

        # Needed to parse the bus no. and find stop names
        trip_id = trip.get("trip_id")
        departure_time = trip.get("departure_time")
        arrival_time = trip.get("arrival_time")

        departure_stop_id = stop_times.find_one({"departure_time":departure_time, "trip_id":trip_id}).get("stop_id")
        arrival_stop_id = stop_times.find_one({"arrival_time":arrival_time, "trip_id":trip_id}).get("stop_id")
        
        departure_stop_id = str(departure_stop_id)
        arrival_stop_id = str(arrival_stop_id)

        departure_stop_name = stops.find_one({"stop_id":departure_stop_id}).get("stop_name")
        arrival_stop_name = stops.find_one({"stop_id":arrival_stop_id}).get("stop_name")

        # Remove the '_id' field before returning the data (optional)
        trip_data = {
            "bus_number": get_bus_number(trip_id),
            "departure_stop_name": departure_stop_name,
            "arrival_stop_name": arrival_stop_name,
            "organization_name": trip.get("organization_name"),
            "number_of_passengers": trip.get("number_of_passengers"),
            "departure_date": trip.get("departure_date"),
            "departure_time": trip.get("departure_time"),
            "arrival_date": trip.get("arrival_date"),
            "arrival_time": trip.get("arrival_time"),
            "booking_status": trip.get("booking_status")
        }
        
        all_trips_data.append(trip_data)

        print(all_trips_data)

    # If there are trips found, return the details
    if all_trips_data:
        return jsonify({"message": "Trips found", "trips": all_trips_data}), 200
    else:
        return jsonify({"message": "No trips found for this email"}), 404
    

if __name__ == "__main__":
    app.run() 

with app.app_context():
    get_trip("john.doe@example.com")