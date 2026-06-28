from flask import Blueprint, render_template, jsonify
from flask_login import login_required

main_bp = Blueprint('main', __name__, template_folder='../templates/main')

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@main_bp.route('/perfil')
@login_required
def profile():
    return render_template('profile.html')

@main_bp.route('/api/cart/count')
def cart_count():
    return jsonify({"count": 0})