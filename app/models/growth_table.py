from app.extensions import db

class GrowthTable(db.Model):
    __tablename__ = 'growth_tables'

    id = db.Column(db.Integer, primary_key=True)
    genetic_line_id = db.Column(db.Integer, db.ForeignKey('genetic_lines.id'), nullable=False)
    week = db.Column(db.Integer, nullable=False)  # semana de vida (1 a N)
    daily_feed_grams = db.Column(db.Float, nullable=False)  # gramos de alimento por día
    daily_water_ml = db.Column(db.Float, nullable=False)  # mililitros de agua por día
    weight_kg = db.Column(db.Float, nullable=True)  # peso esperado en kg

    __table_args__ = (
        db.UniqueConstraint('genetic_line_id', 'week', name='uq_genetic_line_week'),
    )

    def __repr__(self):
        return f'<GrowthTable line={self.genetic_line_id} week={self.week}>'