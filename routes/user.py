from flask import Blueprint, request

from models import ErrorResponse
from services.user_service import UserService

service = UserService()

user_bp = Blueprint('user', __name__)


@user_bp.route('/user', methods=['GET'])
def get_users():
    try:
        return service.get_users()

    except Exception as ex:
        return ErrorResponse(
            error_type=type(ex).__name__,
            message=str(ex)).to_dict()


@user_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id: int):
    try:
        return service.get_user(
            user_id=user_id)

    except Exception as ex:
        return ErrorResponse(
            error_type=type(ex).__name__,
            message=str(ex)).to_dict()


@user_bp.route('/user', methods=['POST'])
def create_user():
    try:
        data = request.get_json()

        return service.create_user(
            data=data)

    except Exception as ex:
        return ErrorResponse(
            error_type=type(ex).__name__,
            message=str(ex)).to_dict()


@user_bp.route('/user', methods=['PUT'])
def update_user():
    try:
        body = request.get_json()

        return service.update_user(
            data=body)

    except Exception as ex:
        return ErrorResponse(
            error_type=type(ex).__name__,
            message=str(ex)).to_dict()


@user_bp.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id: int):
    try:
        return service.delete_user(
            user_id=id)

    except Exception as ex:
        return ErrorResponse(
            error_type=type(ex).__name__,
            message=str(ex)).to_dict()


@user_bp.route('/distance/<int:user_one>/<int:user_two>', methods=['GET'])
def get_degrees_separation(user_one: int, user_two: int):
    try:
        return service.get_degrees_separated(
            user_one=user_one,
            user_two=user_two)

    except Exception as ex:
        return ErrorResponse(
            error_type=type(ex).__name__,
            message=str(ex)).to_dict()
