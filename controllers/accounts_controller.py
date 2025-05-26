from models.accounts.accounts_model import AccountsModel
from flask import request, jsonify

class AccountsController():
    def __init__(self):
        self.model = AccountsModel()

    def get_all_accounts(self):
        return self.model.get_all_accounts()

    def get_available_accounts(self):
        return self.model.get_available_accounts()

    def get_account_by_id(self, account_id):
        return self.model.get_account_by_id(account_id)

    def create_account(self):
        # account_data = request.get_json()
        # required_fields = ['nombre', 'tipo_servicio', 'cantidad_perfiles', 'precio_completo', 'precio_por_perfil']
        
        # # Validar campos requeridos
        # for field in required_fields:
        #     if field not in account_data:
        #         return jsonify({
        #             "mensaje": f"El campo {field} es requerido",
        #             "data": None
        #         }), 400

        # # Validar valores numéricos
        # if account_data['cantidad_perfiles'] <= 0 or account_data['precio_completo'] <= 0 or account_data['precio_por_perfil'] <= 0:
        #     return jsonify({
        #         "mensaje": "Los valores numéricos deben ser mayores a 0",
        #         "data": None
        #     }), 400

        return self.model.create_account()

    def update_account(self, account_id):
        account_data = request.get_json()
        return self.model.update_account(account_id, account_data)

    def delete_account(self, account_id):
        return self.model.delete_account(account_id)

    def mark_as_available(self, account_id):
        return self.model.mark_as_available(account_id)

    def update_used_profiles_count(self, account_id):
        return self.model.update_used_profiles_count(account_id)

    def check_expired_accounts(self):
        return self.model.check_and_update_expired_accounts()
