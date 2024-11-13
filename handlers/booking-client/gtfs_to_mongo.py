import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
print(MONGO_URI)

# MongoDB client setup
# client = MongoClient(MONGO_URI)
client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)

db = client['Booking-App-VGI']  # Specify your database name

def import_gtfs_to_mongodb(stops_file, stop_times_file):
    # Read stops.txt and stop_times.txt files into dataframes
    stops_df = pd.read_csv(stops_file)
    stop_times_df = pd.read_csv(stop_times_file)

    # Convert dataframes to dictionaries
    stops_data = stops_df.to_dict(orient="records")
    stop_times_data = stop_times_df.to_dict(orient="records")

    # Insert data into MongoDB
    stops_collection = db['stops']
    stop_times_collection = db['stop_times']

    # Clear previous data to avoid duplicates
    stops_collection.delete_many({})
    stop_times_collection.delete_many({})

    # Insert new data
    stops_collection.insert_many(stops_data)
    stop_times_collection.insert_many(stop_times_data)

    print("Data imported successfully to MongoDB")

# Example usage
# import_gtfs_to_mongodb(r'C:\Users\anand\PycharmProjects\fletter\GTFS\stops.txt', r'C:\Users\anand\PycharmProjects\fletter\GTFS\stop_times.txt')
def get_all_stops():
    # Query the stops collection and retrieve all stop names
    stops_collection = db['stops']
    stop_names = stops_collection.distinct("stop_name")  # Use 'distinct' to get unique stop names
    return stop_names


def find_trips(from_stop, to_stop):
    """
    Find all trips between two stops using MongoDB collections.

    Args:
        from_stop (str): Name of the departure stop
        to_stop (str): Name of the destination stop
    """
    # Get the collections
    stops_collection = db['stops']
    stop_times_collection = db['stop_times']

    # Debug: Print the stop names we're searching for
    print(f"Searching for trips from '{from_stop}' to '{to_stop}'")

    # Get stop IDs for both stops
    # Convert stop_ids to both string and integer forms to handle different formats
    from_stops = list(stops_collection.find({"stop_name": from_stop}))
    to_stops = list(stops_collection.find({"stop_name": to_stop}))

    # Create lists of stop_ids in both string and integer formats
    from_stop_ids = []
    to_stop_ids = []

    for stop in from_stops:
        try:
            from_stop_ids.append(str(stop['stop_id']))  # String version
            from_stop_ids.append(int(stop['stop_id']))  # Integer version
        except ValueError:
            from_stop_ids.append(stop['stop_id'])  # Keep original if can't convert

    for stop in to_stops:
        try:
            to_stop_ids.append(str(stop['stop_id']))  # String version
            to_stop_ids.append(int(stop['stop_id']))  # Integer version
        except ValueError:
            to_stop_ids.append(stop['stop_id'])  # Keep original if can't convert

    # Debug: Print the stop IDs we found
    print(f"From stop IDs: {from_stop_ids}")
    print(f"To stop IDs: {to_stop_ids}")

    if not from_stop_ids:
        print(f"No stop found with name '{from_stop}'")
        return
    if not to_stop_ids:
        print(f"No stop found with name '{to_stop}'")
        return

    # Find all trip_ids that contain the departure stop
    potential_trips = stop_times_collection.distinct("trip_id", {
        "stop_id": {"$in": from_stop_ids}
    })

    # Debug: Print number of potential trips found
    print(f"Found {len(potential_trips)} potential trips")

    valid_trips = []

    # For each potential trip, check if it contains both stops in the correct order
    for trip_id in potential_trips:
        # Get all stops for this trip in sequence order
        trip_stops = list(stop_times_collection.find(
            {"trip_id": trip_id}
        ).sort("stop_sequence", 1))

        # Find the positions of our stops in the sequence
        from_stop_pos = None
        to_stop_pos = None

        for i, stop in enumerate(trip_stops):
            current_stop_id = stop['stop_id']
            # Convert current_stop_id to string for comparison if it's not already
            if isinstance(current_stop_id, (int, float)):
                current_stop_id = str(current_stop_id)

            if str(current_stop_id) in [str(sid) for sid in from_stop_ids]:
                from_stop_pos = i
            elif from_stop_pos is not None and str(current_stop_id) in [str(sid) for sid in to_stop_ids]:
                to_stop_pos = i
                # We found both stops in the correct order
                valid_trips.append({
                    'trip_id': trip_id,
                    'departure_time': trip_stops[from_stop_pos]['departure_time'],
                    'arrival_time': stop['arrival_time'],
                    'from_stop_id': trip_stops[from_stop_pos]['stop_id'],
                    'to_stop_id': stop['stop_id']
                })
                break

    # # Output results
    # if valid_trips:
    #     print(f"\nTrips from '{from_stop}' to '{to_stop}':")
    #     for trip in valid_trips:
    #         print(f"Trip ID: {trip['trip_id']}")
    #         print(f"From Stop ID: {trip['from_stop_id']}")
    #         print(f"To Stop ID: {trip['to_stop_id']}")
    #         print(f"Departure: {trip['departure_time']}")
    #         print(f"Arrival: {trip['arrival_time']}\n")
    # else:
    #     print(f"\nNo trips found from '{from_stop}' to '{to_stop}'.")

    return valid_trips


# Available Functions:
# Import GTFS data to MongoDB : import_gtfs_to_mongodb(stops_file, stop_times_file) # Imports data from GTFS files
# Find trips between two stops : find_trips(from_stop, to_stop) # Returns a list of valid trips
# Get all stop names : get_all_stops() # Returns a list of all stop names


# Example usage

# Find trips between two stops
# find_trips("Am Westpark 1", "Klinikum")

# Fetch and print all stop names
#all_stops = get_all_stops()
