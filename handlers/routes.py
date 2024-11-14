from flask import Blueprint
from handlers.booking_client import *

booking_blueprint = Blueprint('booking_client', __name__)

booking_blueprint.route('/search_trips', methods=['POST'])(search_trips)

booking_blueprint.route('/book_trip', methods=['POST'])(book_trip)

booking_blueprint.route('/debounce_search', methods=['POST'])(debounce_search)

booking_blueprint.route('/get_all_booking/<email>', methods=['GET'])(get_trip)