from datetime import datetime
from app.extensions import db

class Stock(db.Model):
    __tablename__ = 'stocks'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=False)
    quantity = db.Column(db.Integer, default=0)
    min_stock = db.Column(db.Integer, default=5) 
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

   
    __table_args__ = (
        db.UniqueConstraint('product_id', 'branch_id', name='uq_product_branch'),
        db.Index('idx_stock_product_branch', 'product_id', 'branch_id'),
    )

    def __repr__(self):
        return f'<Stock product={self.product_id} branch={self.branch_id} qty={self.quantity}>'