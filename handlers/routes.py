from flask import Blueprint
from handlers.booking_client import *
from handlers.admin_dashboard import *

booking_blueprint = Blueprint('booking_client', __name__)
admin_blueprint = Blueprint("admin", __name__)

# booking client api urls
booking_blueprint.route('/search_trips', methods=['POST'])(search_trips)

booking_blueprint.route('/book_trip', methods=['POST'])(book_trip)

booking_blueprint.route('/debounce_search', methods=['POST'])(debounce_search)

booking_blueprint.route('/get_all_booking/<email>', methods=['GET'])(get_trip)

booking_blueprint.route('/cancel_booking/', methods=['POST'])(cancel_booking)

# admin dashboard api urls
admin_blueprint.route('/get_all_stops', methods=['GET'])(get_all_stops)

admin_blueprint.route('/toggle_stop_status/', methods=['POST'])(toggle_stop_status)

admin_blueprint.route('/manage_bookings/', methods=['GET'])(manage_bookings)

admin_blueprint.route('/review_booking/', methods=['POST'])(review_booking)
