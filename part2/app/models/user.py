import re
from .base_model import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = self.validate_name(first_name, "first_name")
        self.last_name = self.validate_name(last_name, "last_name")
        self.email = self.validate_email(email)
        self.is_admin = is_admin
        self.places = []
        self.reviews = []

    @staticmethod
    def validate_name(name, field_name):
        if not name or len(name) > 50:
            raise ValueError(f"{field_name} is required and must be <= 50 characters")
        return name

    @staticmethod
    def validate_email(email):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not email or not re.match(pattern, email):
            raise ValueError("Invalid email format")
        return email 
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
