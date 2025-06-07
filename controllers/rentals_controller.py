from models.rentals.rentals_model import RentalsModel
from flask import request, jsonify

class RentalsController():
    def __init__(self):
        self.model = RentalsModel()

    def get_all_rentals(self, user_id=None):
        return self.model.get_all_rentals(user_id)

    def get_rental_by_id(self, rental_id):
        return self.model.get_rental_by_id(rental_id)

    def create_rental(self):
        rental_data = request.get_json()
        return self.model.create_rental(rental_data)

    def get_active_rentals(self, user_id):
        return self.model.get_active_rentals(user_id)

    def get_expired_rentals(self, user_id):
        return self.model.get_expired_rentals(user_id) 