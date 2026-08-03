import uuid
from datetime import datetime

from app import db


class BaseModel(db.Model):
    """SQLAlchemy-mapped base for entities already persisted to the DB."""
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        self.updated_at = datetime.utcnow()

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()


class PlainBaseModel:
    """
    Temporary plain-Python base for entities not yet mapped to SQLAlchemy
    (Place, Review, Amenity). Will be replaced once each gets its own
    SQLAlchemy mapping in a future task.
    """
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        self.updated_at = datetime.now()

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
