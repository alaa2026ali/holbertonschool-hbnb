from app import db
from sqlalchemy.orm import validates

from .base_model import BaseModel


class Amenity(BaseModel):
    """Amenity model mapped to the amenities table."""

    __tablename__ = "amenities"

    name = db.Column(db.String(50), nullable=False, unique=True)

    @validates("name")
    def validate_name(self, key, value):
        """Validate the amenity name."""
        if not value or len(value) > 50:
            raise ValueError(
                "Amenity name is required and must be <= 50 characters"
            )

        return value
