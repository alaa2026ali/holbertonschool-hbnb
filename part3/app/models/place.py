from app import db
from sqlalchemy.orm import validates

from .base_model import BaseModel
from .associations import place_amenity


class Place(BaseModel):
    """Place model mapped to the places table."""

    __tablename__ = "places"

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    owner_id = db.Column(
        db.String(36),
        db.ForeignKey("users.id"),
        nullable=False
    )

    reviews = db.relationship(
        "Review",
        backref="place",
        lazy=True,
        cascade="all, delete-orphan"
    )

    amenities = db.relationship(
        "Amenity",
        secondary=place_amenity,
        lazy="subquery",
        backref=db.backref("places", lazy=True)
    )

    @validates("title")
    def validate_title(self, key, value):
        if not value or len(value) > 100:
            raise ValueError(
                "title is required and must be <= 100 characters"
            )
        return value

    @validates("price")
    def validate_price(self, key, value):
        if value is None or value <= 0:
            raise ValueError("price must be a positive value")
        return value

    @validates("latitude")
    def validate_latitude(self, key, value):
        if value is None or not -90.0 <= value <= 90.0:
            raise ValueError(
                "latitude must be between -90.0 and 90.0"
            )
        return value

    @validates("longitude")
    def validate_longitude(self, key, value):
        if value is None or not -180.0 <= value <= 180.0:
            raise ValueError(
                "longitude must be between -180.0 and 180.0"
            )
        return value

    def add_review(self, review):
        if review not in self.reviews:
            self.reviews.append(review)

    def add_amenity(self, amenity):
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def delete_review(self, review):
        if review in self.reviews:
            self.reviews.remove(review)
