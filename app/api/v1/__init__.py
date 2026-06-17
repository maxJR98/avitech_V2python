from flask import Blueprint

v1_bp = Blueprint('api_v1', __name__, url_prefix='/v1')

# Importar rutas para que se registren
from app.api.v1 import products, cart, orders, diagnosis, nutrition