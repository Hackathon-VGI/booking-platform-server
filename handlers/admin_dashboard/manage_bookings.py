from flask import Flask, request, jsonify
from extensions import get_mongo_db

app = Flask(__name__)
mongo_db = get_mongo_db()

# MongoDB collections
user_trip_details = mongo_db["user_trip_details"]
trips = mongo_db["trips"]
stop_times = mongo_db["stop_times"]
stops = mongo_db["stops"]


def manage_bookings():
    try:
        all_bookings = []

        for booking in user_trip_details.find({"booking_status": "Pending"}):
            try:
                trip_id = booking.get("trip_id")

                # Get bus details
                trip = trips.find_one({"trip_id": trip_id})
                if not trip:
                    continue  # Skip if trip not found

                bus_name = trip.get("trip_headsign")

                # Get stop details
                departure_time = booking.get("departure_time")
                arrival_time = booking.get("arrival_time")

                departure_stop_time = stop_times.find_one({
                    "departure_time": departure_time,
                    "trip_id": trip_id
                })
                arrival_stop_time = stop_times.find_one({
                    "arrival_time": arrival_time,
                    "trip_id": trip_id
                })

                if not departure_stop_time or not arrival_stop_time:
                    continue  # Skip if stop times not found

                departure_stop_id = str(departure_stop_time.get("stop_id"))
                arrival_stop_id = str(arrival_stop_time.get("stop_id"))

                departure_stop = stops.find_one({"stop_id": departure_stop_id})
                arrival_stop = stops.find_one({"stop_id": arrival_stop_id})

                if not departure_stop or not arrival_stop:
                    continue  # Skip if stops not found

                departure_stop_name = departure_stop.get("stop_name")
                arrival_stop_name = arrival_stop.get("stop_name")
                bus_route = f"{departure_stop_name} - {arrival_stop_name}"

                booking_data = {
                    "booking_id": booking.get("booking_id"),
                    "bus_name": bus_name,
                    "user_name": booking.get("user_name"),
                    "bus_route": bus_route,
                    "departure_time": departure_time,
                    "departure_date": booking.get("departure_date"),
                    "bus_number": booking.get("bus_number"),

                }

                all_bookings.append(booking_data)

            except Exception as e:
                print(
                    f"Error processing booking {booking.get('booking_id')}: {str(e)}")
                continue

        return jsonify({"pending_bookings": all_bookings}), 201

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
