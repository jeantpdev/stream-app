from flask import Blueprint
from flask_cors import CORS, cross_origin
from controllers.profiles_controller import ProfilesController

profiles = Blueprint('profiles', __name__)
profiles_controller = ProfilesController()

@profiles.route('/accounts/<int:account_id>/profiles', methods=['GET'])
@cross_origin()
def get_profiles_by_account(account_id):
    return profiles_controller.get_profiles_by_account(account_id)

@profiles.route('/profiles/<int:profile_id>', methods=['GET'])
@cross_origin()
def get_profile_by_id(profile_id):
    return profiles_controller.get_profile_by_id(profile_id)

@profiles.route('/profiles', methods=['POST'])
@cross_origin()
def create_profile():
    return profiles_controller.create_profile()

@profiles.route('/profiles/<int:profile_id>/assign-client', methods=['PATCH'])
@cross_origin()
def assign_to_client(profile_id):
    return profiles_controller.assign_to_client(profile_id)

@profiles.route('/profiles/<int:profile_id>/mark-available', methods=['PATCH'])
@cross_origin()
def mark_profile_as_available(profile_id):
    return profiles_controller.mark_as_available(profile_id) 