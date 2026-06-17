from flask import Blueprint, render_template, request, jsonify
from app.services.diagnostic_service import search_diseases, diagnostic_search, suggest_correction
from app.models import Disease

aveologia_bp = Blueprint('aveologia', __name__, template_folder='../templates/aveologia')

@aveologia_bp.route('/')
def search():
    return render_template('search.html')

@aveologia_bp.route('/api/search')
def api_search():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'results': []})
    diseases = search_diseases(query)
    suggestions = suggest_correction(query)
    return jsonify({'results': [{'id': d.id, 'name': d.name, 'description': d.description} for d in diseases], 'suggestions': suggestions})

@aveologia_bp.route('/diagnostic')
def diagnostic():
    return render_template('diagnostic.html')

@aveologia_bp.route('/api/diagnostic', methods=['POST'])
def api_diagnostic():
    data = request.get_json()
    symptoms = data.get('symptoms', [])
    if not symptoms:
        return jsonify({'results': []})
    results = diagnostic_search(symptoms)
    return jsonify({'results': results})

@aveologia_bp.route('/disease/<int:disease_id>')
def disease_detail(disease_id):
    disease = Disease.query.get_or_404(disease_id)
    return render_template('disease_detail.html', disease=disease)