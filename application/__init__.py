from flask import Flask, send_from_directory
from application.extensions import db, ma, limiter, cache
from config import Config
from flask_swagger_ui import get_swaggerui_blueprint
import os

SWAGGER_URL = '/api/docs'
API_URL = '/swagger.yaml'  # Simplified - no full URL needed

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Mechanic Shop API"
    }
)

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    
    # Serve swagger.yaml as a custom route
    @app.route('/swagger.yaml')
    def swagger_spec():
        static_folder = os.path.join(os.path.dirname(__file__), 'static')
        print(f"Looking for swagger.yaml in: {static_folder}")  # Debug line
        print(f"File exists: {os.path.exists(os.path.join(static_folder, 'swagger.yaml'))}")  # Debug line
        return send_from_directory(static_folder, 'swagger.yaml')
    
    # Register blueprints
    from application.blueprints.customers import customers_bp
    from application.blueprints.mechanics import mechanics_bp
    from application.blueprints.service_tickets import service_tickets_bp
    from application.blueprints.inventory import inventory_bp
    
    app.register_blueprint(customers_bp)
    app.register_blueprint(mechanics_bp)
    app.register_blueprint(service_tickets_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)  # <-- This was missing!
    
    return app