from app.extensions import db

class DiagnosticMatrix(db.Model):
    __tablename__ = 'diagnostic_matrix'

    id = db.Column(db.Integer, primary_key=True)
    disease_id = db.Column(db.Integer, db.ForeignKey('diseases.id'), nullable=False)
    symptom_id = db.Column(db.Integer, db.ForeignKey('symptoms.id'), nullable=False)
    weight = db.Column(db.Float, nullable=False, default=1.0) 
    
    # Índice compuesto
    __table_args__ = (
        db.UniqueConstraint('disease_id', 'symptom_id', name='uq_disease_symptom'),
        db.Index('idx_matrix_disease_symptom', 'disease_id', 'symptom_id'),
    )

    def __repr__(self):
        return f'<DiagnosticMatrix disease={self.disease_id} symptom={self.symptom_id}>'