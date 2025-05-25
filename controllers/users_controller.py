from models.users.users_model import UsersModel
from flask import request

class UsersController():
    def __init__(self):
        self.model = UsersModel()

    def get_all_users(self):
        return self.model.get_all_users()

    def get_user_by_id(self, user_id):
        return self.model.get_user_by_id(user_id)

    def create_user(self):
        user_data = request.get_json()
        required_fields = ['nombre', 'email', 'password', 'rol']
        
        # Validar campos requeridos
        for field in required_fields:
            if field not in user_data:
                return {
                    "mensaje": f"El campo {field} es requerido",
                    "data": None
                }, 400

        # Validar rol
        if user_data['rol'] not in ['admin', 'revendedor']:
            return {
                "mensaje": "El rol debe ser 'admin' o 'revendedor'",
                "data": None
            }, 400

        return self.model.create_user(user_data)

    def update_user(self, user_id):
        user_data = request.get_json()
        return self.model.update_user(user_id, user_data)

    def delete_user(self, user_id):
        return self.model.delete_user(user_id) 