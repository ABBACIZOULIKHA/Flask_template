from flask import request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from app import db
from models.product import Product

# Allowed image extensions
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def get_all_products():
    """Fetch all products."""
    products = Product.query.all()
    return jsonify([{
         "id": product.id,
         "title": product.title,
         "description": product.description,
         "price": product.price,
         "quantity": product.quantity,
         "category": product.category,  # Fixed incorrect assignment
         "date": product.date,
         "image_filename": product.image_filename
    } for product in products])

def get_product_by_id(product_id):
    """Fetch a single product by ID."""
    product = Product.query.get(product_id)
    if product:
        return jsonify({
            "id": product.id,
            "title": product.title,
            "description": product.description,
            "price": product.price,
            "quantity": product.quantity,
            "category": product.category,  # Fixed incorrect assignment
            "date": product.date,
            "image_filename": product.image_filename
        })

    return jsonify({"error": "Product not found"}), 404

def create_product():
    """Create a new product with optional image upload."""
    try:
        title = request.form.get("title")
        description = request.form.get("description")
        price = request.form.get("price")
        quantity = request.form.get("quantity")
        category = request.form.get("category")
        seller_id = request.form.get("seller_id")
        date = request.form.get("date")

        if not title or not description or not price or not quantity or not category:
            return jsonify({"error": "Missing required fields"}), 400

        try:
            price = float(price)  # Convert price to float
            quantity = int(quantity)  # Ensure quantity is an integer
        except ValueError:
            return jsonify({"error": "Invalid price or quantity format"}), 400

        # Handle image upload
        image_filename = None
        if "image" in request.files:
            file = request.files["image"]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
                file.save(file_path)
                image_filename = filename  # Store filename in DB instead of full path

        new_product = Product(
            title=title,
            description=description,
            price=price,
            quantity=quantity,
            category=category,
            image_filename=image_filename,
            date = date,
            seller_id = seller_id
        )

        db.session.add(new_product)
        db.session.commit()

        return jsonify({"message": "Product created successfully", "product": {
            "id": new_product.id,
            "title": new_product.title,
            "description": new_product.description,
            "price": new_product.price,
            "quantity": new_product.quantity,
            "category": new_product.category,
            "seller_id" : new_product.seller_id,
            "date" : new_product.date,
            "image_filename": new_product.image_filename
        }}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

def update_product(product_id):
    """Update product details and image."""
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    try:
        product.title = request.form.get("title", product.title)
        product.description = request.form.get("description", product.description)
        price = request.form.get("price", product.price)
        quantity = request.form.get("quantity", product.quantity)
        category = request.form.get("category", product.category)
        seller_id = request.form.get("seller_id", product.seller_id)
        date = request.form.get("date", product.date)
        try:
            product.price = float(price)  # Convert to float if provided
            product.quantity = int(quantity)  # Convert to int if provided
        except ValueError:
            return jsonify({"error": "Invalid price or quantity format"}), 400

        # Handle image update
        if "image" in request.files:
            file = request.files["image"]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
                file.save(file_path)

                # Delete the old image if it exists
                if product.image_filename:
                    old_image_path = os.path.join(current_app.config["UPLOAD_FOLDER"], product.image_filename)
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)

                product.image_filename = filename  # Store new image filename

        db.session.commit()
        return jsonify({"message": "Product updated successfully", "product": {
            "id": product.id,
            "title": product.title,
            "description": product.description,
            "price": product.price,
            "quantity": product.quantity,
            "category": product.category,
            "seller_id" : product.seller_id,
            "date": product.date,
            "image_filename": product.image_filename
        }})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

def delete_product(product_id):
    """Delete a product."""
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    # Delete the associated image if it exists
    if product.image_filename:
        image_path = os.path.join(current_app.config["UPLOAD_FOLDER"], product.image_filename)
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"})
