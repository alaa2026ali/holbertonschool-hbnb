from app import db, bcrypt
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity


def seed_data():
    # Create demo user
    user = User.query.filter_by(email="alaa@test.com").first()

    if not user:
        user = User(
            first_name="Alaa",
            last_name="Test",
            email="alaa@test.com"
        )
        user.password = bcrypt.generate_password_hash(
            "123456"
        ).decode("utf-8")

        db.session.add(user)
        db.session.commit()

    # Create amenities
    amenities = {}

    for name in [
        "WiFi",
        "Parking",
        "Air Conditioning",
        "Swimming Pool",
        "Beach Access",
        "Mountain View"
    ]:
        amenity = Amenity.query.filter_by(name=name).first()

        if not amenity:
            amenity = Amenity(name=name)
            db.session.add(amenity)
            db.session.commit()

        amenities[name] = amenity

    # Don't create places twice
    if Place.query.first():
        return

    # Riyadh
    riyadh = Place(
        title="Riyadh Luxury Apartment",
        description="Modern apartment in the heart of Riyadh",
        price=450,
        latitude=24.7136,
        longitude=46.6753,
        owner_id=user.id
    )

    riyadh.amenities.extend([
        amenities["WiFi"],
        amenities["Parking"],
        amenities["Air Conditioning"]
    ])

    # Jeddah
    jeddah = Place(
        title="Jeddah Beach House",
        description="Beautiful stay near the Red Sea",
        price=650,
        latitude=21.5433,
        longitude=39.1728,
        owner_id=user.id
    )

    jeddah.amenities.extend([
        amenities["WiFi"],
        amenities["Swimming Pool"],
        amenities["Beach Access"]
    ])

    # AlUla
    alula = Place(
        title="AlUla Desert Villa",
        description="Peaceful villa surrounded by the landscapes of AlUla",
        price=800,
        latitude=26.6084,
        longitude=37.9232,
        owner_id=user.id
    )

    alula.amenities.extend([
        amenities["WiFi"],
        amenities["Parking"],
        amenities["Mountain View"]
    ])

    db.session.add_all([
        riyadh,
        jeddah,
        alula
    ])

    db.session.commit()
