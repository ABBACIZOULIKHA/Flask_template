from flask import Blueprint
from flask_jwt_extended import jwt_required
from controllers.auth_controller import register_seller, login_seller, get_seller_profile

auth_bp = Blueprint("auth", __name__)

auth_bp.route("/register", methods=["POST"])(register_seller)
auth_bp.route("/login", methods=["POST"])(login_seller)
auth_bp.route("/profile", methods=["GET"])(jwt_required()(get_seller_profile))

