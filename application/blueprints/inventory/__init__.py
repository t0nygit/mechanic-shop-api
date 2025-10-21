from flask import Blueprint

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')

from application.blueprints.inventory import routes