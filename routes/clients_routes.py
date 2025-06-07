from flask import Blueprint
from flask_cors import CORS, cross_origin
from controllers.clients_controller import ClientsController

clients = Blueprint('clients', __name__)
clients_controller = ClientsController()

@clients.route('/revendedores/<uuid:revendedor_id>/clients', methods=['GET'])
@cross_origin()
def get_all_clients(revendedor_id):
    print("HOLA")
    return clients_controller.get_all_clients(revendedor_id)

@clients.route('/clients/<int:client_id>', methods=['GET'])
@cross_origin()
def get_client_by_id(client_id):
    return clients_controller.get_client_by_id(client_id)

@clients.route('/clients', methods=['POST'])
@cross_origin()
def create_client():
    return clients_controller.create_client()

@clients.route('/clients/<int:client_id>', methods=['PATCH'])
@cross_origin()
def update_client(client_id):
    return clients_controller.update_client(client_id)

@clients.route('/clients/<int:client_id>', methods=['DELETE'])
@cross_origin()
def delete_client(client_id):
    return clients_controller.delete_client(client_id)

@clients.route('/clients/<int:client_id>/profiles', methods=['GET'])
@cross_origin()
def get_client_profiles(client_id):
    return clients_controller.get_client_profiles(client_id) 