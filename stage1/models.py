from extensions import db
from datetime import datetime

class Profile(db.Model):
    __tablename__ = 'profiles'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    gender = db.Column(db.String)
    gender_probability = db.Column(db.Float)
    sample_size = db.Column(db.Integer)

    age = db.Column(db.Integer)
    age_group = db.Column(db.String)

    country_id = db.Column(db.String)
    country_probability = db.Column(db.Float)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)