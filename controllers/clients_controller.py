from models.clients.clients_model import ClientsModel
from flask import request, jsonify

class ClientsController():
    def __init__(self):
        self.model = ClientsModel()

    def get_all_clients(self, revendedor_id):
        return self.model.get_all_clients(revendedor_id)

    def get_client_by_id(self, client_id):
        return self.model.get_client_by_id(client_id)

    def create_client(self):
        client_data = request.get_json()
        required_fields = ['nombre', 'contacto', 'revendedor_id']
        
        # Validar campos requeridos
        for field in required_fields:
            if field not in client_data:
                return jsonify({
                    "mensaje": f"El campo {field} es requerido",
                    "data": None
                }), 400

        return self.model.create_client(client_data)

    def update_client(self, client_id):
        client_data = request.get_json()
        return self.model.update_client(client_id, client_data)

    def delete_client(self, client_id):
        return self.model.delete_client(client_id)

    def get_client_profiles(self, client_id):
        return self.model.get_client_profiles(client_id) 