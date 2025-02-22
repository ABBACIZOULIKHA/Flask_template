from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from models.seller import Seller  # Assuming Seller model exists

def register_seller():
    """Register a new seller."""
    data = request.get_json()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    phone_number = data.get("phone_number")
    username = data.get("username")
    password = data.get("password")
    address = data.get("address")

    if Seller.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    hashed_password = generate_password_hash(password)

    new_seller = Seller(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number,
        username=username,
        password=hashed_password,
        address=address,
    )
    
    db.session.add(new_seller)
    db.session.commit()

    return jsonify({"message": "Seller registered successfully"}), 201

def login_seller():
    """Authenticate a seller and return a JWT token."""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    seller = Seller.query.filter_by(username=username).first()

    if not seller or not check_password_hash(seller.password, password):
        return jsonify({"error": "Invalid username or password"}), 401

    access_token = create_access_token(identity=str(seller.id)) 
    return jsonify({"access_token": access_token, "message": "Login successful"}), 200

def get_seller_profile():
    """Fetch seller profile (protected route)."""
    seller_identity = get_jwt_identity()
    seller = Seller.query.get(seller_identity) 
    if not seller:
        return jsonify({"error": "Seller not found"}), 404

    return jsonify({
        "id": seller.id,
        "first_name": seller.first_name,
        "last_name": seller.last_name,
        "email": seller.email,
        "phone_number": seller.phone_number,
        "username": seller.username,
        "address": seller.address
    }), 200
