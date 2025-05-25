from models.profiles.profiles_model import ProfilesModel
from flask import request, jsonify

class ProfilesController():
    def __init__(self):
        self.model = ProfilesModel()

    def get_profiles_by_account(self, account_id):
        return self.model.get_profiles_by_account(account_id)

    def get_profile_by_id(self, profile_id):
        return self.model.get_profile_by_id(profile_id)

    def create_profile(self):
        profile_data = request.get_json()
        required_fields = ['nombre', 'cuenta_id']
        
        # Validar campos requeridos
        for field in required_fields:
            if field not in profile_data:
                return jsonify({
                    "mensaje": f"El campo {field} es requerido",
                    "data": None
                }), 400

        return self.model.create_profile(profile_data)

    def assign_to_client(self, profile_id):
        data = request.get_json()
        if 'cliente_id' not in data:
            return jsonify({
                "mensaje": "El campo cliente_id es requerido",
                "data": None
            }), 400

        return self.model.assign_to_client(profile_id, data['cliente_id'])

    def mark_as_available(self, profile_id):
        return self.model.mark_as_available(profile_id) 