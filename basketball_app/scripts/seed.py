"""Seed file"""
from basketball_app.models import db
from basketball_app import app

# Create all tables
db.drop_all()
db.create_all()
