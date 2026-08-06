from app import db
from sqlalchemy.orm import validates

from .base_model import BaseModel


class Review(BaseModel):
    """Review model mapped to the reviews table."""

    __tablename__ = "reviews"

    text = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    place_id = db.Column(
        db.String(36),
        db.ForeignKey("places.id"),
        nullable=False
    )

    user_id = db.Column(
        db.String(36),
        db.ForeignKey("users.id"),
        nullable=False
    )

    @validates("text")
    def validate_text(self, key, value):
        if not value:
            raise ValueError("text is required")
        return value

    @validates("rating")
    def validate_rating(self, key, value):
        if not isinstance(value, int) or not 1 <= value <= 5:
            raise ValueError(
                "rating must be an integer between 1 and 5"
            )
        return value
