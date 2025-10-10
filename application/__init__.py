from flask import Flask
from application.extensions import db, ma
from config import Config

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    
    # Register blueprints
    from application.blueprints.customers import customers_bp
    from application.blueprints.mechanics import mechanics_bp
    from application.blueprints.service_tickets import service_tickets_bp
    
    app.register_blueprint(customers_bp)
    app.register_blueprint(mechanics_bp)
    app.register_blueprint(service_tickets_bp)
    
    return app