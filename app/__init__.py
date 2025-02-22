from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config
from flask_jwt_extended import JWTManager

import os
from werkzeug.utils import secure_filename
import sys

# Ajouter le chemin actuel au sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Initialisation de la base de données et des migrations
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialiser db et migrate avec l'application
    db.init_app(app)
    migrate.init_app(app, db)

    # Configurer le dossier de stockage des images et les extensions autorisées
    app.config['UPLOAD_FOLDER'] = 'uploads/'
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
    app.config["JWT_SECRET_KEY"] = "SECRET_KEY"  

    jwt = JWTManager(app)  

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

    # Créer le dossier 'uploads' s'il n'existe pas
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Importer et enregistrer les blueprints
    from .routes.product_routes import product_bp
    from .routes.seller_routes import seller_bp
    from .routes.auth_routes import auth_bp  

    app.register_blueprint(product_bp, url_prefix="/products")   
    app.register_blueprint(seller_bp, url_prefix='/sellers')
    app.register_blueprint(auth_bp, url_prefix="/auth")  
    
    return app
