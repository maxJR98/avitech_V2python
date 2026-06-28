from app.extensions import db

class FeedPhase(db.Model):
    __tablename__ = 'feed_phases'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) 
    min_week = db.Column(db.Integer, nullable=False)
    max_week = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return f'<FeedPhase {self.name}>'