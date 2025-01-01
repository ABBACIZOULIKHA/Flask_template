from flask import Blueprint, jsonify, request
from ..models.seller import Seller
from .. import db

# Create the Blueprint for seller routes
seller_bp = Blueprint('sellers', __name__)

# GET route: Fetch all sellers
@seller_bp.route('/', methods=['GET'])
def get_sellers():
    sellers = Seller.query.all()
    return jsonify([{
        "id": seller.id,
        "first_name": seller.first_name,
        "last_name": seller.last_name,
        "email": seller.email,
        "phone_number": seller.phone_number,
        "username": seller.username,
        "address": seller.address
    } for seller in sellers]), 200

# POST route: Add a new seller
@seller_bp.route('/', methods=['POST'])
def add_seller():
    data = request.get_json()
    
    try:
        new_seller = Seller(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            phone_number=data.get('phone_number'),
            username=data.get('username'),
            password=data.get('password'),  # Note: Hash password in production
            address=data.get('address')
        )
        
        db.session.add(new_seller)
        db.session.commit()
        return jsonify({
            "id": new_seller.id,
            "first_name": new_seller.first_name,
            "last_name": new_seller.last_name,
            "email": new_seller.email,
            "phone_number": new_seller.phone_number,
            "username": new_seller.username,
            "address": new_seller.address
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
