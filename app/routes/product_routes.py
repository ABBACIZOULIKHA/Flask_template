from flask import Blueprint, request
from controllers.product_controller import get_all_products, get_product_by_id, create_product, update_product, delete_product

product_bp = Blueprint("product_bp", __name__)

@product_bp.route("/", methods=["GET"])
def get_products():
    return get_all_products()

@product_bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):
    return get_product_by_id(product_id)

@product_bp.route("/", methods=["POST"])
def add_product():
    return create_product()

@product_bp.route("/<int:product_id>", methods=["PUT"])
def edit_product(product_id):
    return update_product(product_id)

@product_bp.route("/<int:product_id>", methods=["DELETE"])
def remove_product(product_id):
    return delete_product(product_id)
