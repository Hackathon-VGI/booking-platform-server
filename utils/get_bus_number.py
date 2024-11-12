def get_bus_number(trip_id):
    trip_id = trip_id.split(":")
    return trip_id[0]