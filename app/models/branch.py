from datetime import datetime
from app.extensions import db

class Branch(db.Model):
    __tablename__ = 'branches'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    stocks = db.relationship('Stock', backref='branch', lazy=True, cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='branch', lazy=True)

    def __repr__(self):
        return f'<Branch {self.name}>'