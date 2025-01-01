from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
import os
from ..models.product import Product
from .. import db
from flask import current_app

product_bp = Blueprint('products', __name__)

# Fonction pour vérifier les extensions de fichiers autorisées
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@product_bp.route('/', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])

@product_bp.route('/', methods=['POST'])
def add_product():
    # Récupérer les données envoyées en form-data, y compris l'image
    data = request.form.to_dict()  # Convertir ImmutableMultiDict en dictionnaire mutable
    image = request.files.get('image')  # Récupérer l'image du formulaire

    if image and allowed_file(image.filename):
        # Sauvegarder l'image dans le dossier 'uploads'
        filename = secure_filename(image.filename)
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)
        data['image_filename'] = filename  # Ajouter le nom de fichier dans les données
    elif image:
        return jsonify({"error": "Image file is not allowed. Only PNG, JPG, JPEG, and GIF are supported."}), 400

    # Créer un nouveau produit avec les données récupérées
    new_product = Product(**data)
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict()), 201
