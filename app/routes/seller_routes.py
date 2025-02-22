from flask import Blueprint, request
from controllers.seller_controller import get_all_sellers, get_seller_by_id, create_seller, update_seller, delete_seller

seller_bp = Blueprint("seller_bp", __name__)

# Get all sellers
@seller_bp.route("/", methods=["GET"])
def get_sellers():
    return get_all_sellers()

# Get seller by ID
@seller_bp.route("/<int:seller_id>", methods=["GET"])
def get_seller(seller_id):
    return get_seller_by_id(seller_id)

# Create a new seller
@seller_bp.route("/", methods=["POST"])
def add_seller():
    data = request.get_json()
    return create_seller(data)

# Update an existing seller
@seller_bp.route("/<int:seller_id>", methods=["PUT"])
def edit_seller(seller_id):
    data = request.get_json()
    return update_seller(seller_id, data)

# Delete a seller
@seller_bp.route("/<int:seller_id>", methods=["DELETE"])
def remove_seller(seller_id):
    return delete_seller(seller_id)
