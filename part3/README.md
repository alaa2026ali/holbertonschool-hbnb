# Part 3: HBnB - Authentication and Database Integration

## Description

HBnB is an Airbnb-inspired RESTful API built with Flask. This is **Part 3** of the HBnB Evolution project and represents the most complete version of the backend application.

Building on the REST API developed in Part 2, this version adds:

- JWT-based user authentication and login.
- Secure password hashing using Flask-Bcrypt.
- Role-based access control for regular users and administrators.
- Ownership-based permissions for places and reviews.
- Persistent data storage using SQLAlchemy and SQLite.
- SQLAlchemy mapping for users, places, reviews, and amenities.
- One-to-many and many-to-many relationships between entities.
- Raw SQL scripts for schema creation and initial data insertion.
- An Entity-Relationship diagram documenting the database structure.

## Table of Contents

- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [Database Relationships](#database-relationships)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [Authentication](#authentication)
- [API Reference](#api-reference)
- [Example Requests](#example-requests)
- [Testing](#testing)
- [Known Limitations](#known-limitations)
- [Authors](#authors)

## Technologies Used

- Python 3
- Flask
- Flask-RESTX
- Flask-JWT-Extended
- Flask-Bcrypt
- Flask-SQLAlchemy
- SQLAlchemy
- SQLite
- Pytest
- Mermaid.js

## Project Structure

```text
part3/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       └── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── associations.py
│   │   ├── base_model.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── amenity.py
│   ├── persistence/
│   │   ├── __init__.py
│   │   └── repository.py
│   └── services/
│       ├── __init__.py
│       ├── facade.py
│       └── repositories/
│           ├── __init__.py
│           └── user_repository.py
├── sql_scripts/
│   ├── schema.sql
│   ├── initial_data.sql
│   └── test_crud.sql
├── tests/
├── instance/
├── config.py
├── ER_DIAGRAM.md
├── er_diagram.png
├── requirements.txt
├── run.py
├── TESTING_REPORT.md
└── README.md
```

## Architecture

The application follows a layered architecture:

```text
API Layer (Flask-RESTX Resources)
        |
        v
Business Logic Layer (HBnBFacade)
        |
        v
Repository Layer (SQLAlchemyRepository / UserRepository)
        |
        v
Database Layer (SQLAlchemy ORM / SQLite)
```

### API Layer

Defines routes, request and response models, authentication requirements, and API input validation.

### Business Logic Layer

The `HBnBFacade` acts as the main interface between the API and persistence layers. It applies business rules and delegates data operations to the appropriate repository.

### Repository Layer

The repository layer abstracts database access:

- `UserRepository` extends `SQLAlchemyRepository` and provides user-specific queries such as retrieving a user by email.
- `SQLAlchemyRepository` provides generic CRUD operations for `Place`, `Review`, and `Amenity`.

### Database Layer

SQLAlchemy maps the Python entities to SQLite database tables and manages their relationships.

## Database Relationships

The database contains the following relationships:

- One `User` can own many `Place` records.
- Every `Place` belongs to one `User`.
- One `User` can write many `Review` records.
- Every `Review` is written by one `User`.
- One `Place` can receive many `Review` records.
- Every `Review` belongs to one `Place`.
- A `Place` can have many `Amenity` records.
- An `Amenity` can belong to many `Place` records.
- The many-to-many relationship between places and amenities is implemented through the `place_amenity` association table.

The complete Entity-Relationship diagram is available in:

```text
ER_DIAGRAM.md
```

An exported image of the diagram is also available as:

```text
er_diagram.png
```

## Installation

Clone the repository:

```bash
git clone https://github.com/alaa2026ali/holbertonschool-hbnb.git
```

Enter the Part 3 directory:

```bash
cd holbertonschool-hbnb/part3
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

On Windows without WSL:

```bash
venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Database Setup

### Using SQLAlchemy

Start a Flask shell:

```bash
flask --app run.py shell
```

Then create all mapped tables:

```python
from app import db
from app.models import User, Place, Review, Amenity

db.create_all()
exit()
```

This creates the SQLite development database in:

```text
instance/development.db
```

The generated tables are:

- `users`
- `places`
- `reviews`
- `amenities`
- `place_amenity`

### Using the Raw SQL Scripts

The `sql_scripts` directory contains scripts for creating and testing the database independently of SQLAlchemy.

Create a test database schema:

```bash
sqlite3 hbnb_test.db < sql_scripts/schema.sql
```

Insert the administrator and initial amenities:

```bash
sqlite3 hbnb_test.db < sql_scripts/initial_data.sql
```

Run the CRUD test script:

```bash
sqlite3 -header -column hbnb_test.db < sql_scripts/test_crud.sql
```

Display the generated tables:

```bash
sqlite3 hbnb_test.db ".tables"
```

The initial data includes:

### Administrator

- Email: `admin@hbnb.io`
- Password: `admin1234`
- Administrator access: enabled

The password is stored as a bcrypt hash rather than plain text.

### Amenities

- WiFi
- Swimming Pool
- Air Conditioning

## Running the Application

Activate the virtual environment and run:

```bash
python run.py
```

Alternatively:

```bash
flask --app run.py run
```

The API will be available at:

```text
http://127.0.0.1:5000
```

The Flask-RESTX Swagger documentation is available at:

```text
http://127.0.0.1:5000/api/v1/
```

## Authentication

### Login

```text
POST /api/v1/auth/login
```

Request body:

```json
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

A successful login returns a JWT access token:

```json
{
  "access_token": "..."
}
```

The token contains an `is_admin` claim used to determine the user's permission level.

Use the token on protected requests:

```text
Authorization: Bearer <access_token>
```

### Permission Levels

| Level | Description |
| --- | --- |
| Public | No JWT token is required for public read operations. |
| Authenticated | A valid JWT token is required. Regular users can manage resources they own. |
| Administrator | A user with `is_admin = true` can access administrator endpoints and bypass ownership restrictions. |

Passwords are hashed with Flask-Bcrypt before storage and are never returned in API responses.

## API Reference

### Authentication — `/api/v1/auth`

| Method | Endpoint | Authorization | Description |
| --- | --- | --- | --- |
| POST | `/login` | Public | Log in and receive a JWT access token. |

### Users — `/api/v1/users`

| Method | Endpoint | Authorization | Description |
| --- | --- | --- | --- |
| GET | `/` | Public | List all users. |
| POST | `/` | Administrator | Create a new user. |
| GET | `/<user_id>` | Public | Retrieve a user by ID. |
| PUT | `/<user_id>` | Owner or Administrator | Update a user. Regular users cannot change their email or password. Administrators can modify all allowed fields. |

### Places — `/api/v1/places`

| Method | Endpoint | Authorization | Description |
| --- | --- | --- | --- |
| GET | `/` | Public | List all places. |
| POST | `/` | Authenticated | Create a place owned by the logged-in user. |
| GET | `/<place_id>` | Public | Retrieve a place by ID. |
| PUT | `/<place_id>` | Owner or Administrator | Update a place. |
| GET | `/<place_id>/reviews` | Public | Retrieve all reviews associated with a place. |

### Reviews — `/api/v1/reviews`

| Method | Endpoint | Authorization | Description |
| --- | --- | --- | --- |
| GET | `/` | Public | List all reviews. |
| POST | `/` | Authenticated | Create a review for a place. |
| GET | `/<review_id>` | Public | Retrieve a review by ID. |
| PUT | `/<review_id>` | Owner or Administrator | Update a review. |
| DELETE | `/<review_id>` | Owner or Administrator | Delete a review. |

A regular user cannot review their own place or submit more than one review for the same place.

### Amenities — `/api/v1/amenities`

| Method | Endpoint | Authorization | Description |
| --- | --- | --- | --- |
| GET | `/` | Public | List all amenities. |
| POST | `/` | Administrator | Create a new amenity. |
| GET | `/<amenity_id>` | Public | Retrieve an amenity by ID. |
| PUT | `/<amenity_id>` | Administrator | Update an amenity. |

## Example Requests

### Log In as the Initial Administrator

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@hbnb.io",
    "password": "admin1234"
  }'
```

### Create a User as an Administrator

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "password": "password123"
  }'
```

### Create a Place

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/places/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "title": "Cozy Apartment",
    "description": "A comfortable apartment in the city",
    "price": 100,
    "latitude": 24.7,
    "longitude": 46.7,
    "amenities": []
  }'
```

### Create a Review

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/reviews/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "text": "Excellent place",
    "rating": 5,
    "place_id": "<place_id>"
  }'
```

## Testing

Run the automated test suite:

```bash
python3 -m pytest tests/ -v
```

Check the syntax of the SQLAlchemy model and service files:

```bash
python -m py_compile app/models/associations.py
python -m py_compile app/models/user.py
python -m py_compile app/models/place.py
python -m py_compile app/models/review.py
python -m py_compile app/models/amenity.py
python -m py_compile app/services/facade.py
```

See `TESTING_REPORT.md` for the detailed manual and automated testing report.

## Known Limitations

- SQLite is intended for development and testing.
- A production deployment may require configuration for MySQL or another production-grade relational database.
- The Flask development server should not be used in production.
- Database migrations are not currently configured. Structural model changes may require recreating the development database.
- Additional production security configuration may be required for secret keys and JWT expiration settings.

## Authors

- Alaa Aldwasari
- Lama
- Noura Alosimi

