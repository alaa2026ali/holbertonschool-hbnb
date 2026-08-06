# HBnB - Auth & DB

## Description

HBnB is an Airbnb-like application developed as part of the Holberton School Software Engineering Program. This project represents the third part of the HBnB evolution, focusing on implementing authentication, authorization, and database integration.

In this phase, the application is upgraded from an in-memory storage system to a persistent database solution using SQLAlchemy. The project also introduces secure user authentication using JWT and password hashing.

## Project Objectives

The main objectives of this project are:

* Implement user authentication and authorization.
* Secure user passwords using hashing techniques.
* Integrate a relational database using SQLAlchemy ORM.
* Replace in-memory storage with database persistence.
* Implement CRUD operations with database models.
* Manage relationships between application entities.
* Apply role-based access control for protected resources.

## Technologies Used

* Python 3
* Flask
* Flask-RESTX
* Flask-JWT-Extended
* Flask-Bcrypt
* SQLAlchemy
* SQLite (development)
* MySQL (production-ready)
* Git & GitHub

## Project Architecture

The project follows a layered architecture:

```
API Layer
    |
    v
Business Logic Layer (Facade)
    |
    v
Repository Layer
    |
    v
Database Layer (SQLAlchemy)
```

### Main Components

* **Models**

  * User
  * Place
  * Review
  * Amenity

* **Repositories**

  * Database repository for persistent data management.

* **Services**

  * Facade pattern to handle communication between API and repositories.

* **API Endpoints**

  * User management
  * Place management
  * Review management
  * Amenity management
  * Authentication

## Authentication

The project uses JWT-based authentication.

Features include:

* User registration.
* User login.
* Token generation.
* Protected API endpoints.
* Access control based on user roles.

Passwords are securely stored using hashing and are never saved as plain text.

## Database Design

The application uses SQLAlchemy ORM to define database models and relationships.

Main entities:

### User

Stores user information:

* ID
* First name
* Last name
* Email
* Hashed password
* Admin status

### Place

Represents properties created by users.

### Review

Stores reviews written by users about places.

### Amenity

Stores available features for places.

## Installation

Clone the repository:

```bash
git clone <repository_url>
```

Navigate to the project directory:

```bash
cd HBnB
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate the environment:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Start the Flask server:

```bash
python3 run.py
```

The application will run on:

```
http://127.0.0.1:5000
```

## API Testing

The API can be tested using:

* Postman
* Curl
* Automated tests

Example:

```bash
curl http://127.0.0.1:5000/api/v1/users
```

## Testing

Run the test suite:

```bash
python3 -m pytest tests/ -v
```

## Future Improvements

Possible future improvements:

* Front-end user interface.
* Advanced search functionality.
* Image upload support.
* Payment integration.
* Deployment using cloud services.

## Authors

* Alaa Aldwasari
* Lama
* Noura Alosimi
