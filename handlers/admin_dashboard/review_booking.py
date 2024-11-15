from flask import Flask, request, jsonify
from extensions import get_mongo_db

app = Flask(__name__)
mongo_db = get_mongo_db()

# MongoDB collections
user_trip_details = mongo_db["user_trip_details"]
trips = mongo_db["trips"]
stop_times = mongo_db["stop_times"]
stops = mongo_db["stops"]

def review_booking():
  booking_data = request.json

  booking_status = booking_data.get("booking_status")
  booking_id = booking_data.get("booking_id")

  if booking_status == "Reject":
    user_trip_details.update_one(
    {"booking_id": booking_id},  
    {"$set": {"booking_status": "Reject"}} 
    ) 
  else:
    user_trip_details.update_one(
    {"booking_id": booking_id},  
    {"$set": {"booking_status": "Approve"}} 
    )

    trip_id = user_trip_details.find_one({"booking_id":booking_id}).get("trip_id")
    number_of_passengers = int(user_trip_details.find_one({"booking_id":booking_id}).get("number_of_passengers"))
    max_seats = int(stop_times.find_one({"trip_id":trip_id}).get("max_seats"))

    stop_times.update_one(
    {"trip_id": trip_id},  
    {"$set": {"max_seats": max_seats-number_of_passengers}} 
    )
  return jsonify({"message":"booking reviewed successfully"})
