from app import app
from model.models import db

with app.app_context():
    db.create_all()
