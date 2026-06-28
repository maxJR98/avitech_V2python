from flask import Blueprint, render_template, request, jsonify
from sqlalchemy import or_
from app.models import Disease
from app.services.diagnostic_service import suggest_correction

aveologia_bp = Blueprint('aveologia', __name__, template_folder='../templates/aveologia')

@aveologia_bp.route('/')
def search():
    return render_template('search.html')

@aveologia_bp.route('/api/search')
def api_search():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'results': [], 'suggestions': []})
    
    termino_busqueda = f'%{query}%'
    resultados = Disease.query.filter(
        or_(
            Disease.name.ilike(termino_busqueda),
            Disease.description.ilike(termino_busqueda),
            Disease.keywords.ilike(termino_busqueda)
        )
    ).all()
    
    diseases_data = [
        {
            'id': d.id, 
            'name': d.name, 
            'description': d.description
        } for d in resultados
    ]
    
    try:
        suggestions = suggest_correction(query)
    except Exception:
        suggestions = []
        
    return jsonify({'results': diseases_data, 'suggestions': suggestions})

@aveologia_bp.route('/disease/<int:disease_id>')
def disease_detail(disease_id):
    disease = Disease.query.get_or_404(disease_id)
    
    return render_template('disease_detail.html', disease=disease)