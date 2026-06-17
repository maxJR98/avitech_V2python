from datetime import datetime
from app.extensions import db

class Disease(db.Model):
    __tablename__ = 'diseases'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    scientific_name = db.Column(db.String(200))
    description = db.Column(db.Text)
    treatment = db.Column(db.Text)
    prevention = db.Column(db.Text)
    keywords = db.Column(db.String(500))  # palabras clave para búsqueda full-text
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    symptoms = db.relationship('Symptom', secondary='diagnostic_matrix', backref='diseases')

    def __repr__(self):
        return f'<Disease {self.name}>'