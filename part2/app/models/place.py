from .base_model import BaseModel
from .user import User


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = self.validate_title(title)
        self.description = description  # optional
        self.price = self.validate_price(price)
        self.latitude = self.validate_latitude(latitude)
        self.longitude = self.validate_longitude(longitude)
        self.owner = self.validate_owner(owner)
        self.reviews = []    # list of Review instances
        self.amenities = []  # list of Amenity instances

    @staticmethod
    def validate_title(title):
        if not title or len(title) > 100:
            raise ValueError("title is required and must be <= 100 characters")
        return title

    @staticmethod
    def validate_price(price):
        if price is None or price <= 0:
            raise ValueError("price must be a positive value")
        return price

    @staticmethod
    def validate_latitude(latitude):
        if latitude is None or not (-90.0 <= latitude <= 90.0):
            raise ValueError("latitude must be between -90.0 and 90.0")
        return latitude

    @staticmethod
    def validate_longitude(longitude):
        if longitude is None or not (-180.0 <= longitude <= 180.0):
            raise ValueError("longitude must be between -180.0 and 180.0")
        return longitude

    @staticmethod
    def validate_owner(owner):
        if not isinstance(owner, User):
            raise ValueError("owner must be a valid User instance")
        return owner

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)
