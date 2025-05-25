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
        required_fields = ['usuario_id', 'cuenta_id', 'tipo']
        
        # Validar campos requeridos
        for field in required_fields:
            if field not in rental_data:
                return jsonify({
                    "mensaje": f"El campo {field} es requerido",
                    "data": None
                }), 400

        # Validar tipo de alquiler
        if rental_data['tipo'] not in ['completa', 'perfil']:
            return jsonify({
                "mensaje": "El tipo de alquiler debe ser 'completa' o 'perfil'",
                "data": None
            }), 400

        # Si es alquiler de perfil, verificar perfil_id
        if rental_data['tipo'] == 'perfil' and 'perfil_id' not in rental_data:
            return jsonify({
                "mensaje": "El campo perfil_id es requerido para alquiler de perfil",
                "data": None
            }), 400

        return self.model.create_rental(rental_data)

    def get_active_rentals(self, user_id):
        return self.model.get_active_rentals(user_id)

    def get_expired_rentals(self, user_id):
        return self.model.get_expired_rentals(user_id) 