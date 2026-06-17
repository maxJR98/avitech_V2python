from app.models import Disease, Symptom, DiagnosticMatrix
from app.extensions import db
from sqlalchemy import func, text
import Levenshtein

def search_diseases(query):
    words = query.split()
    conditions = []
    for word in words:
        conditions.append(Disease.name.ilike(f'%{word}%'))
        conditions.append(Disease.keywords.ilike(f'%{word}%'))
    if conditions:
        diseases = Disease.query.filter(db.or_(*conditions)).all()
    else:
        diseases = []
    return diseases

def suggest_correction(query):
    all_keywords = []
    diseases = Disease.query.all()
    for d in diseases:
        if d.keywords:
            all_keywords.extend(d.keywords.split(','))
        all_keywords.append(d.name)
    all_keywords = list(set(all_keywords))
    suggestions = []
    for kw in all_keywords:
        dist = Levenshtein.distance(query.lower(), kw.lower())
        if dist <= 2:
            suggestions.append(kw)
    return suggestions[:5]

def diagnostic_search(symptom_names):
    symptoms = Symptom.query.filter(Symptom.name.in_(symptom_names)).all()
    if not symptoms:
        return []
    symptom_ids = [s.id for s in symptoms]
    matrix = db.session.query(
        DiagnosticMatrix.disease_id,
        func.sum(DiagnosticMatrix.weight).label('total_weight')
    ).filter(DiagnosticMatrix.symptom_id.in_(symptom_ids)).group_by(DiagnosticMatrix.disease_id).order_by(text('total_weight DESC')).limit(10).all()
    results = []
    for m in matrix:
        disease = Disease.query.get(m.disease_id)
        if disease:
            results.append({
                'disease': disease.name,
                'description': disease.description,
                'treatment': disease.treatment,
                'score': m.total_weight
            })
    return results