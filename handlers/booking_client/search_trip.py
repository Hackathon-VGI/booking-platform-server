from flask import request, jsonify
from utils import get_bus_number
from extensions import get_mongo_db
from utils.time_conversion import adjust_time, time_in_seconds
from utils.gtfs_to_mongo import find_trips
# import gtfs_to_mongo as utils

mongo_db = get_mongo_db()
stop_times = mongo_db["stop_times"]
stops = mongo_db["stops"]



def search_trips():
    trip_details = request.json

    departure_stop = trip_details.get('departure_stop')
    arrival_stop = trip_details.get('arrival_stop')

    departure_date = trip_details.get('departure_date')

    required_seats = trip_details.get('required_seats')

    # flag for checking whether a stop is blocked or not
    # stop_status = stops.get("stop_blocked")

    departure_time = trip_details.get('departure_time')
    departure_time_seconds = time_in_seconds(departure_time)

    all_trips = find_trips(departure_stop, arrival_stop)

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
            trip["available_seats"] = available_seats

            # Compare times and seats
            if departure_time_seconds <= trip_departure_time_seconds and available_seats >= int(required_seats):
                valid_routes.append(trip)

    return jsonify({
        "valid_routes": valid_routes,
        "departure_stop": departure_stop,
        "arrival_stop": arrival_stop,
        "departure_time": departure_time,
        "required_seats": required_seats,
        "departure_date": departure_date,
        # "stop_status": stop_status
    })
