from flask import Blueprint
from flask_cors import CORS, cross_origin
from controllers.users_controller import UsersController

users = Blueprint('users', __name__)
users_controller = UsersController()

@users.route('/users', methods=['GET'])
@cross_origin()
def get_all_users():
    return users_controller.get_all_users()

@users.route('/users/<int:user_id>', methods=['GET'])
@cross_origin()
def get_user_by_id(user_id):
    return users_controller.get_user_by_id(user_id)

@users.route('/users', methods=['POST'])
@cross_origin()
def create_user():
    return users_controller.create_user()

@users.route('/users/<int:user_id>', methods=['PATCH'])
@cross_origin()
def update_user(user_id):
    return users_controller.update_user(user_id)

@users.route('/users/<int:user_id>', methods=['DELETE'])
@cross_origin()
def delete_user(user_id):
    return users_controller.delete_user(user_id) 