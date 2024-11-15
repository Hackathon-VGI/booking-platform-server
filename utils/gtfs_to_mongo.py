import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# MongoDB client setup
# client = MongoClient(MONGO_URI)
client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)

db = client['Booking-App-VGI']  # Specify your database name

def import_gtfs_to_mongodb(stops_file, stop_times_file, transfers_file, trips_file, agency_file, calendar_file, calendar_dates_file, feed_info_file, routes_file):
    # Read GTFS files into dataframes
    stops_df = pd.read_csv(stops_file)
    stop_times_df = pd.read_csv(stop_times_file)
    transfers_df = pd.read_csv(transfers_file)
    trips_df = pd.read_csv(trips_file)
    agency_df = pd.read_csv(agency_file)
    calendar_df = pd.read_csv(calendar_file)
    calendar_dates_df = pd.read_csv(calendar_dates_file)
    feed_info_df = pd.read_csv(feed_info_file)
    routes_df = pd.read_csv(routes_file)

    # Convert dataframes to dictionaries
    stops_data = stops_df.to_dict(orient="records")
    stop_times_data = stop_times_df.to_dict(orient="records")
    transfers_data = transfers_df.to_dict(orient="records")
    trips_data = trips_df.to_dict(orient="records")
    agency_data = agency_df.to_dict(orient="records")
    calendar_data = calendar_df.to_dict(orient="records")
    calendar_dates_data = calendar_dates_df.to_dict(orient="records")
    feed_info_data = feed_info_df.to_dict(orient="records")
    routes_data = routes_df.to_dict(orient="records")

    # Add max_seats column with default value 35 to stop_times_data
    for stop_time in stop_times_data:
        stop_time['max_seats'] = 35

    # Insert data into MongoDB
    collections = {
        'stops': stops_data,
        'stop_times': stop_times_data,
        'transfers': transfers_data,
        'trips': trips_data,
        'agency': agency_data,
        'calendar': calendar_data,
        'calendar_dates': calendar_dates_data,
        'feed_info': feed_info_data,
        'routes': routes_data
    }

    for collection_name, data in collections.items():
        collection = db[collection_name]
        # Clear previous data to avoid duplicates
        collection.delete_many({})
        # Insert new data
        collection.insert_many(data)

    print("Data imported successfully to MongoDB")
# Example usage
import_gtfs_to_mongodb(r'C:\Users\anand\PycharmProjects\fletter\GTFS\stops.txt', r'C:\Users\anand\PycharmProjects\fletter\GTFS\stop_times.txt', r'C:\Users\anand\PycharmProjects\fletter\GTFS\transfers.txt', r'C:\Users\anand\PycharmProjects\fletter\GTFS\trips.txt', r'C:\Users\anand\PycharmProjects\fletter\GTFS\agency.txt', r'C:\Users\anand\PycharmProjects\fletter\GTFS\calendar.txt', r'C:\Users\anand\PycharmProjects\fletter\GTFS\calendar_dates.txt', r'C:\Users\anand\PycharmProjects\fletter\GTFS\feed_info.txt', r'C:\Users\anand\PycharmProjects\fletter\GTFS\routes.txt')
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

    # Output results
    if valid_trips:
        print(f"\nTrips from '{from_stop}' to '{to_stop}':")
        for trip in valid_trips:
            print(f"Trip ID: {trip['trip_id']}")
            print(f"From Stop ID: {trip['from_stop_id']}")
            print(f"To Stop ID: {trip['to_stop_id']}")
            print(f"Departure: {trip['departure_time']}")
            print(f"Arrival: {trip['arrival_time']}\n")
    else:
        print(f"\nNo trips found from '{from_stop}' to '{to_stop}'.")

    return valid_trips


def get_possible_end_stops(from_stop):
    """
    Get all possible end stops that have a trip from the given stop.

    Args:
        from_stop (str): Name of the departure stop

    Returns:
        list: List of possible end stops
    """
    # Get the collections
    stops_collection = db['stops']
    stop_times_collection = db['stop_times']

    # Get stop IDs for the from_stop
    from_stops = list(stops_collection.find({"stop_name": from_stop}))
    from_stop_ids = []

    for stop in from_stops:
        try:
            from_stop_ids.append(str(stop['stop_id']))  # String version
            from_stop_ids.append(int(stop['stop_id']))  # Integer version
        except ValueError:
            from_stop_ids.append(stop['stop_id'])  # Keep original if can't convert

    if not from_stop_ids:
        print(f"No stop found with name '{from_stop}'")
        return []

    # Find all trip_ids that contain the departure stop
    potential_trips = stop_times_collection.distinct("trip_id", {
        "stop_id": {"$in": from_stop_ids}
    })

    possible_end_stops = set()

    # For each potential trip, get all stops and add to possible end stops
    for trip_id in potential_trips:
        trip_stops = list(stop_times_collection.find(
            {"trip_id": trip_id}
        ).sort("stop_sequence", 1))

        from_stop_found = False

        for stop in trip_stops:
            current_stop_id = stop['stop_id']
            if isinstance(current_stop_id, (int, float)):
                current_stop_id = str(current_stop_id)

            if str(current_stop_id) in [str(sid) for sid in from_stop_ids]:
                from_stop_found = True
            elif from_stop_found:
                # Fetch the stop name from the stops collection using stop_id
                end_stop = stops_collection.find_one({"stop_id": stop['stop_id']})
                if end_stop:
                    possible_end_stops.add(end_stop['stop_name'])

    return list(possible_end_stops)


# Available Functions:
# Import GTFS data to MongoDB : import_gtfs_to_mongodb(stops_file, stop_times_file) # Imports data from GTFS files
# Find trips between two stops : find_trips(from_stop, to_stop) # Returns a list of valid trips
# Get all stop names : get_all_stops() # Returns a list of all stop names


# Example usage

# Find trips between two stops
# find_trips("Am Westpark 1", "Klinikum")

# Fetch and print all stop names
# all_stops = get_all_stops()


# possible_end_stops = get_possible_end_stops("Am Westpark 2")
# print(possible_end_stops)