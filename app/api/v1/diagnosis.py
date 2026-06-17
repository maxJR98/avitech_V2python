from flask import jsonify, request
from app.api.v1 import v1_bp
from app.services.diagnostic_service import search_diseases, diagnostic_search, suggest_correction
from app.models import Disease

@v1_bp.route('/diagnosis/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'results': [], 'suggestions': []})
    diseases = search_diseases(query)
    suggestions = suggest_correction(query)
    return jsonify({
        'results': [{'id': d.id, 'name': d.name, 'description': d.description} for d in diseases],
        'suggestions': suggestions
    })

@v1_bp.route('/diagnosis/diagnostic', methods=['POST'])
def diagnostic():
    data = request.get_json()
    symptoms = data.get('symptoms', [])
    if not symptoms:
        return jsonify({'results': []})
    results = diagnostic_search(symptoms)
    return jsonify({'results': results})

@v1_bp.route('/diagnosis/disease/<int:disease_id>', methods=['GET'])
def get_disease(disease_id):
    disease = Disease.query.get_or_404(disease_id)
    return jsonify({
        'id': disease.id,
        'name': disease.name,
        'scientific_name': disease.scientific_name,
        'description': disease.description,
        'treatment': disease.treatment,
        'prevention': disease.prevention,
        'keywords': disease.keywords
    })