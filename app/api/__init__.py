from flask import Blueprint
from flask import Blueprint
from app.api.v1 import v1_bp

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/')
def api_root():
    return {'message': 'API AVITECH v1'}

api_bp.register_blueprint(v1_bp)