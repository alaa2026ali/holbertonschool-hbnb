from app.persistence.repository import (
    PlaceRepository,
    ReviewRepository,
    AmenityRepository
)
from app.services.repositories.user_repository import UserRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()

        self.amenity_repo = AmenityRepository(Amenity)
        self.place_repo = PlaceRepository(Place)
        self.review_repo = ReviewRepository(Review)

    def create_user(self, user_data):
        user = User(**user_data)
        user.hash_password(user_data["password"])
        self.user_repo.add(user)
        return user

    def get_users(self):
        return self.user_repo.get_all()

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)

        if not user:
            raise KeyError("User not found")

        updated_data = user_data.copy()

        if "password" in updated_data:
            password = updated_data.pop("password")
            user.hash_password(password)

        self.user_repo.update(user_id, updated_data)
        return self.user_repo.get(user_id)

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)

        if not amenity:
            raise KeyError("Amenity not found")

        self.amenity_repo.update(amenity_id, amenity_data)
        return self.amenity_repo.get(amenity_id)

    def create_place(self, place_data):
        data = place_data.copy()

        owner_id = data.pop("owner_id", None)
        amenity_ids = data.pop("amenities", [])

        owner = self.user_repo.get(owner_id)

        if not owner:
            raise KeyError("Owner not found")

        place = Place(
            owner_id=owner_id,
            **data
        )

        for amenity_id in amenity_ids:
            amenity = self.amenity_repo.get(amenity_id)

            if not amenity:
                raise KeyError(
                    f"Amenity not found: {amenity_id}"
                )

            place.amenities.append(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)

        if not place:
            raise KeyError("Place not found")

        data = place_data.copy()
        data.pop("owner_id", None)

        amenity_ids = data.pop("amenities", None)

        if amenity_ids is not None:
            amenities = []

            for amenity_id in amenity_ids:
                amenity = self.amenity_repo.get(amenity_id)

                if not amenity:
                    raise KeyError(
                        f"Amenity not found: {amenity_id}"
                    )

                amenities.append(amenity)

            place.amenities = amenities

        self.place_repo.update(place_id, data)
        return self.place_repo.get(place_id)

    def create_review(self, review_data):
        data = review_data.copy()

        user_id = data.get("user_id")
        place_id = data.get("place_id")

        user = self.user_repo.get(user_id)

        if not user:
            raise KeyError("User not found")

        place = self.place_repo.get(place_id)

        if not place:
            raise KeyError("Place not found")

        review = Review(**data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)

        if not review:
            raise KeyError("Review not found")

        data = review_data.copy()
        data.pop("user_id", None)
        data.pop("place_id", None)

        self.review_repo.update(review_id, data)
        return self.review_repo.get(review_id)

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)

        if not review:
            raise KeyError("Review not found")

        self.review_repo.delete(review_id)

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)

        if not place:
            raise KeyError("Place not found")

        return place.reviews
