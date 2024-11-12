from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
import certifi

app = Flask(__name__)

# Initialize MongoDB client
mongo_uri = os.getenv("MONGO_URI")

client = MongoClient(mongo_uri, tlsCAFile=certifi.where())
db = client["Booking-App-VGI"]
user_trip_details = db["user_trip_details"]

# Define the route to accept user data
@app.route("/api/book-trip", methods=["POST"])
def book_trip(number_of_passengers, trip_id, departure_date, departure_time, arrival_date, arrival_time):
    # Get data from the request
    user_data = request.json

    # Insert the user data into the collection
    result = user_trip_details.insert_one({
        "user_name": user_data.get("user_name"),
        "email" : user_data.get("email"),
        "phone": user_data.get("phone"),
        "organization_name": user_data.get("organization_name"),
        "number_of_passengers": number_of_passengers,
        "trip_id": trip_id,
        "departure_date": departure_date,
        "departure_time": departure_time,
        "arrival_date": arrival_date,
        "arrival_time": arrival_time,
        
        # when initialised, default status is pending 
        "booking_status": "Pending"
    })

    # Return a success response
    return jsonify({"message": "Booking created successfully!", "booking_id": str(result.inserted_id)}), 201

# if __name__ == "__main__":
#     app.run(debug=True) 
