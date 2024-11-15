from flask import request, jsonify
from extensions import get_mongo_db
from datetime import datetime

mongo_db = get_mongo_db()

user_trip_details = mongo_db["user_trip_details"]
stops = mongo_db["stops"]


def book_trip():
    # Get data from the request
    user_data = request.json

    # to get unique booking id
    booking_id = str(datetime.now().timestamp() * 1000000)

    # Insert the user data into the collection
    result = user_trip_details.insert_one({
        "user_name": user_data.get("user_name"),
        "email": user_data.get("email"),
        "phone": user_data.get("phone"),
        "organization_name": user_data.get("organization_name"),
        "number_of_passengers": user_data.get("number_of_passengers"),
        "trip_id": user_data.get("trip_id"),
        "departure_date": user_data.get("departure_date"),
        "departure_time": user_data.get("departure_time"),
        "arrival_date": user_data.get("arrival_date"),
        "arrival_time": user_data.get("arrival_time"),
        "booking_id" : booking_id,

        # when initialised, default status is pending
        "booking_status": "Pending"
    })

    # Return a success response
    return jsonify({"message": "Booking created successfully!", "booking_id": booking_id}), 201

