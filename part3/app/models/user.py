import re

from app import db, bcrypt
from sqlalchemy.orm import validates

from .base_model import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    places = db.relationship(
        "Place",
        backref="owner",
        lazy=True,
        cascade="all, delete-orphan"
    )

    reviews = db.relationship(
        "Review",
        backref="author",
        lazy=True,
        cascade="all, delete-orphan"
    )
    
    @validates("first_name")
    def validate_first_name(self, key, value):
        if not value or len(value) > 50:
            raise ValueError(
                "first_name is required and must be <= 50 characters"
            )
        return value

    @validates("last_name")
    def validate_last_name(self, key, value):
        if not value or len(value) > 50:
            raise ValueError(
                "last_name is required and must be <= 50 characters"
            )
        return value

    @validates("email")
    def validate_email(self, key, value):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not value or not re.match(pattern, value):
            raise ValueError("Invalid email format")
        return value

    def hash_password(self, password):
        """Hash the password before storing it."""
        if not password:
            raise ValueError("Password is required")
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password):
        """Verify the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    def add_place(self, place):
        """Add a place owned by the user."""
        if place not in self.places:
            self.places.append(place)

    def add_review(self, review):
        """Add a review written by the user."""
        if review not in self.reviews:
            self.reviews.append(review)

    def delete_review(self, review):
        """Remove a review written by the user."""
        if review in self.reviews:
            self.reviews.remove(review)
