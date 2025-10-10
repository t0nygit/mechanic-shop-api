from flask import Blueprint

mechanics_bp = Blueprint('mechanics', __name__, url_prefix='/mechanics')

from application.blueprints.mechanics import routes