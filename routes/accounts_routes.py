from flask import Blueprint
from flask_cors import CORS, cross_origin
from controllers.accounts_controller import AccountsController

accounts = Blueprint('accounts', __name__)
accounts_controller = AccountsController()

@accounts.route('/accounts', methods=['GET'])
@cross_origin()
def get_all_accounts():
    return accounts_controller.get_all_accounts()

@accounts.route('/accounts/available', methods=['GET'])
@cross_origin()
def get_available_accounts():
    return accounts_controller.get_available_accounts()

@accounts.route('/accounts/<int:account_id>', methods=['GET'])
@cross_origin()
def get_account_by_id(account_id):
    return accounts_controller.get_account_by_id(account_id)

@accounts.route('/accounts', methods=['POST'])
@cross_origin()
def create_account():
    return accounts_controller.create_account()

@accounts.route('/accounts/<int:account_id>', methods=['PATCH'])
@cross_origin()
def update_account(account_id):
    return accounts_controller.update_account(account_id)

@accounts.route('/accounts/<int:account_id>', methods=['DELETE'])
@cross_origin()
def delete_account(account_id):
    return accounts_controller.delete_account(account_id)

@accounts.route('/accounts/<int:account_id>/mark-available', methods=['PATCH'])
@cross_origin()
def mark_account_as_available(account_id):
    return accounts_controller.mark_as_available(account_id)

@accounts.route('/accounts/<int:account_id>/update-profiles-count', methods=['PATCH'])
@cross_origin()
def update_profiles_count(account_id):
    return accounts_controller.update_used_profiles_count(account_id)

@accounts.route('/accounts/check-expired', methods=['POST'])
@cross_origin()
def check_expired_accounts():
    return accounts_controller.check_expired_accounts()