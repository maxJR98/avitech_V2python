from flask import Blueprint, render_template, request, jsonify
from app.services.nutrition_service import calculate_feed_and_water, get_feed_phase

calculadora_bp = Blueprint('calculadora', __name__, template_folder='../templates/calculadora')

@calculadora_bp.route('/')
def calculator():
    return render_template('calculator.html')

@calculadora_bp.route('/api/calculate', methods=['POST'])
def api_calculate():
    data = request.get_json()
    genetic_line = data.get('genetic_line')
    weeks = data.get('weeks')
    birds = data.get('birds')
    if not genetic_line or weeks is None or birds is None:
        return jsonify({'error': 'Faltan datos'}), 400
    result = calculate_feed_and_water(genetic_line, weeks, birds)
    phase = get_feed_phase(weeks)
    result['feed_phase'] = phase
    return jsonify(result)