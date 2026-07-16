from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user
    
    def get_users(self):
        return self.user_repo.get_all()

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
    
    def update_user(self, user_id, user_data):
        self.user_repo.update(user_id, user_data)
    
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        self.amenity_repo.update(amenity_id, amenity_data)

    def create_place(self, place_data):
        owner_id = place_data.pop('owner_id', None)
        user = self.user_repo.get(owner_id)
        if not user:
            raise KeyError('Invalid input data: Owner not found')
        
        place_data['owner'] = user
        
        amenities_data = place_data.pop('amenities', [])
        valid_amenities = []
        for a in amenities_data:
            amenity = self.get_amenity(a.get('id'))
            if not amenity:
                raise KeyError('Invalid input data: Amenity not found')
            valid_amenities.append(amenity)

        place = Place(**place_data)
        self.place_repo.add(place)
        user.add_place(place)
        
        for amenity in valid_amenities:
            place.add_amenity(amenity)
            
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)

        if not place:
            raise KeyError("Place not found")

        validated_data = {}

        if "title" in place_data:
            validated_data["title"] = Place.validate_title(
                place_data["title"]
            )

        if "description" in place_data:
            validated_data["description"] = place_data["description"]

        if "price" in place_data:
            validated_data["price"] = Place.validate_price(
                place_data["price"]
            )

        if "latitude" in place_data:
            validated_data["latitude"] = Place.validate_latitude(
                place_data["latitude"]
            )

        if "longitude" in place_data:
            validated_data["longitude"] = Place.validate_longitude(
                place_data["longitude"]
            )

        self.place_repo.update(place_id, validated_data)
        return self.place_repo.get(place_id)

    def create_review(self, review_data):
        user_id = review_data.pop('user_id', None)
        user = self.user_repo.get(user_id)
        if not user:
            raise KeyError('Invalid input data: User not found')
        review_data['user'] = user
        
        place_id = review_data.pop('place_id', None)
        place = self.place_repo.get(place_id)
        if not place:
            raise KeyError('Invalid input data: Place not found')
        review_data['place'] = place

        review = Review(**review_data)
        self.review_repo.add(review)
        user.add_review(review)
        place.add_review(review)
        return review
        
    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise KeyError('Place not found')
        return place.reviews

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)

        if not review:
            raise KeyError("Review not found")

        validated_data = {}

        if "text" in review_data:
            validated_data["text"] = Review.validate_text(
                review_data["text"]
            )

        if "rating" in review_data:
            validated_data["rating"] = Review.validate_rating(
                review_data["rating"]
            )

        self.review_repo.update(review_id, validated_data)
        return self.review_repo.get(review_id)

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise KeyError('Review not found')
        
        user = self.user_repo.get(review.user.id)
        place = self.place_repo.get(review.place.id)

        if user:
            user.delete_review(review)
        if place:
            place.delete_review(review)
            
        self.review_repo.delete(review_id)
