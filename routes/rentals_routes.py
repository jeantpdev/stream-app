from flask import Blueprint
from flask_cors import CORS, cross_origin
from controllers.rentals_controller import RentalsController

rentals = Blueprint('rentals', __name__)
rentals_controller = RentalsController()

@rentals.route('/rentals', methods=['GET'])
@cross_origin()
def get_all_rentals():
    return rentals_controller.get_all_rentals()

@rentals.route('/rentals/<int:rental_id>', methods=['GET'])
@cross_origin()
def get_rental_by_id(rental_id):
    return rentals_controller.get_rental_by_id(rental_id)

@rentals.route('/rentals', methods=['POST'])
@cross_origin()
def create_rental():
    return rentals_controller.create_rental()

@rentals.route('/users/<int:user_id>/rentals/active', methods=['GET'])
@cross_origin()
def get_active_rentals(user_id):
    return rentals_controller.get_active_rentals(user_id)

@rentals.route('/users/<int:user_id>/rentals/expired', methods=['GET'])
@cross_origin()
def get_expired_rentals(user_id):
    return rentals_controller.get_expired_rentals(user_id) 