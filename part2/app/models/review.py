from .base_model import BaseModel
from .place import Place
from .user import User


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = self.validate_text(text)
        self.rating = self.validate_rating(rating)
        self.place = self.validate_place(place)
        self.user = self.validate_user(user)

    @staticmethod
    def validate_text(text):
        if not text:
            raise ValueError("text is required")
        return text

    @staticmethod
    def validate_rating(rating):
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("rating must be an integer between 1 and 5")
        return rating

    @staticmethod
    def validate_place(place):
        if not isinstance(place, Place):
            raise ValueError("place must be a valid Place instance")
        return place

    @staticmethod
    def validate_user(user):
        if not isinstance(user, User):
            raise ValueError("user must be a valid User instance")
        return user
