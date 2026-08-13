from app import db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


def test_user_places_relationship(client):
    with client.application.app_context():
        user = User(
            first_name="Test",
            last_name="User",
            email="user@example.com",
            password="password"
        )

        user.hash_password("password")

        db.session.add(user)
        db.session.commit()

        place = Place(
            title="Test Place",
            description="Test description",
            price=100,
            latitude=24.7136,
            longitude=46.6753,
            owner_id=user.id
        )

        db.session.add(place)
        db.session.commit()

        assert len(user.places) == 1
        assert user.places[0].id == place.id


def test_place_reviews_relationship(client):
    with client.application.app_context():
        user = User(
            first_name="Test",
            last_name="User",
            email="reviewer@example.com",
            password="password"
        )

        user.hash_password("password")

        db.session.add(user)
        db.session.commit()

        place = Place(
            title="Test Place",
            description="Test description",
            price=100,
            latitude=24.7136,
            longitude=46.6753,
            owner_id=user.id
        )

        db.session.add(place)
        db.session.commit()

        review = Review(
            text="Great place",
            rating=5,
            user_id=user.id,
            place_id=place.id
        )

        db.session.add(review)
        db.session.commit()

        assert len(place.reviews) == 1
        assert place.reviews[0].id == review.id


def test_user_reviews_relationship(client):
    with client.application.app_context():
        user = User(
            first_name="Test",
            last_name="User",
            email="reviewer2@example.com",
            password="password"
        )

        user.hash_password("password")

        db.session.add(user)
        db.session.commit()

        place = Place(
            title="Test Place",
            description="Test description",
            price=100,
            latitude=24.7136,
            longitude=46.6753,
            owner_id=user.id
        )

        db.session.add(place)
        db.session.commit()

        review = Review(
            text="Excellent",
            rating=5,
            user_id=user.id,
            place_id=place.id
        )

        db.session.add(review)
        db.session.commit()

        assert len(user.reviews) == 1
        assert user.reviews[0].id == review.id


def test_place_amenities_relationship(client):
    with client.application.app_context():
        user = User(
            first_name="Test",
            last_name="User",
            email="amenity@example.com",
            password="password"
        )

        user.hash_password("password")

        db.session.add(user)
        db.session.commit()

        place = Place(
            title="Test Place",
            description="Test description",
            price=100,
            latitude=24.7136,
            longitude=46.6753,
            owner_id=user.id
        )

        amenity = Amenity(name="Wi-Fi")

        db.session.add(place)
        db.session.add(amenity)
        db.session.commit()

        place.amenities.append(amenity)
        db.session.commit()

        assert len(place.amenities) == 1
        assert place.amenities[0].id == amenity.id


def test_amenity_places_relationship(client):
    with client.application.app_context():
        user = User(
            first_name="Test",
            last_name="User",
            email="amenity2@example.com",
            password="password"
        )

        user.hash_password("password")

        db.session.add(user)
        db.session.commit()

        place = Place(
            title="Test Place",
            description="Test description",
            price=100,
            latitude=24.7136,
            longitude=46.6753,
            owner_id=user.id
        )

        amenity = Amenity(name="Parking")

        db.session.add(place)
        db.session.add(amenity)
        db.session.commit()

        place.amenities.append(amenity)
        db.session.commit()

        assert len(amenity.places) == 1
        assert amenity.places[0].id == place.id
