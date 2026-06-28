from datetime import datetime
from app.extensions import db

class GeneticLine(db.Model):
    __tablename__ = 'genetic_lines'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) 
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    growth_tables = db.relationship('GrowthTable', backref='genetic_line', lazy=True)

    def __repr__(self):
        return f'<GeneticLine {self.name}>'