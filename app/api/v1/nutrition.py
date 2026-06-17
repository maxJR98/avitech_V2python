from flask import jsonify, request
from app.api.v1 import v1_bp
from app.services.nutrition_service import calculate_feed_and_water, get_feed_phase

@v1_bp.route('/nutrition/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    genetic_line = data.get('genetic_line')
    weeks = data.get('weeks')
    birds = data.get('birds')
    if not genetic_line or weeks is None or birds is None:
        return jsonify({'error': 'Faltan datos: genetic_line, weeks, birds'}), 400
    result = calculate_feed_and_water(genetic_line, weeks, birds)
    if 'error' in result:
        return jsonify(result), 400
    phase = get_feed_phase(weeks)
    result['feed_phase'] = phase
    return jsonify(result)

@v1_bp.route('/nutrition/phases', methods=['GET'])
def list_phases():
    from app.models import FeedPhase
    phases = FeedPhase.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'min_week': p.min_week,
        'max_week': p.max_week,
        'description': p.description
    } for p in phases])

@v1_bp.route('/nutrition/lines', methods=['GET'])
def list_genetic_lines():
    from app.models import GeneticLine
    lines = GeneticLine.query.all()
    return jsonify([{
        'id': l.id,
        'name': l.name,
        'description': l.description
    } for l in lines])