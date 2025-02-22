from flask import jsonify
from app import db
from models.seller import Seller

def get_all_sellers():
    sellers = Seller.query.all()
    return jsonify([{
        "id": seller.id,
        "first_name": seller.first_name,
        "last_name": seller.last_name,
        "email": seller.email,
        "phone_number": seller.phone_number,
        "username": seller.username,
        "address": seller.address
    } for seller in sellers])

def get_seller_by_id(seller_id):
    seller = Seller.query.get(seller_id)
    if seller:
        return jsonify({
            "id": seller.id,
            "first_name": seller.first_name,
            "last_name": seller.last_name,
            "email": seller.email,
            "phone_number": seller.phone_number,
            "username": seller.username,
            "address": seller.address
        })
    return jsonify({"error": "Seller not found"}), 404

def create_seller(data):
    try:
        new_seller = Seller(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            phone_number=data.get("phone_number"),
            username=data.get("username"),
            password=data.get("password"),  # Hashing should be implemented
            address=data.get("address")
        )
        db.session.add(new_seller)
        db.session.commit()
        return jsonify({"message": "Seller created successfully", "seller": {
            "id": new_seller.id,
            "first_name": new_seller.first_name,
            "last_name": new_seller.last_name,
            "email": new_seller.email,
            "phone_number": new_seller.phone_number,
            "username": new_seller.username,
            "address": new_seller.address
        }}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def update_seller(seller_id, data):
    seller = Seller.query.get(seller_id)
    if not seller:
        return jsonify({"error": "Seller not found"}), 404
    
    try:
        seller.first_name = data.get("first_name", seller.first_name)
        seller.last_name = data.get("last_name", seller.last_name)
        seller.email = data.get("email", seller.email)
        seller.phone_number = data.get("phone_number", seller.phone_number)
        seller.username = data.get("username", seller.username)
        seller.address = data.get("address", seller.address)

        db.session.commit()
        return jsonify({"message": "Seller updated successfully", "seller": {
            "id": seller.id,
            "first_name": seller.first_name,
            "last_name": seller.last_name,
            "email": seller.email,
            "phone_number": seller.phone_number,
            "username": seller.username,
            "address": seller.address
        }})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def delete_seller(seller_id):
    seller = Seller.query.get(seller_id)
    if not seller:
        return jsonify({"error": "Seller not found"}), 404

    db.session.delete(seller)
    db.session.commit()
    return jsonify({"message": "Seller deleted successfully"})
