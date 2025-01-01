from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Import and register blueprints
    from .routes.product_routes import product_bp
    from .routes.seller_routes import seller_bp
    app.register_blueprint(product_bp, url_prefix='/products')
    app.register_blueprint(seller_bp, url_prefix='/sellers')
    
    return app
