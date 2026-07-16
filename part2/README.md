# HBnB Evolution - Part 2

## Overview

HBnB Evolution - Part 2 is a RESTful API developed using **Python**, **Flask**, and **Flask-RESTX**. The project follows a layered architecture to separate the Presentation, Business Logic, and Persistence layers, making the application modular, maintainable, and scalable.

---

## Features

* User Management
* Amenity Management
* Place Management
* Review Management
* RESTful API Endpoints
* Input Validation
* Swagger Documentation
* Unit Testing

---

## Project Structure

```text
.
├── app/
│   ├── api/
│   ├── models/
│   ├── persistence/
│   ├── services/
│   └── __init__.py
├── tests/
├── run.py
├── requirements.txt
├── README.md
└── TESTING_REPORT.md
```

---

## Requirements

* Python 3
* Flask
* Flask-RESTX

Install the dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the Flask server:

```bash
python3 run.py
```

The API will be available at:

```
http://127.0.0.1:5000/api/v1/
```

Swagger documentation:

```
http://127.0.0.1:5000/api/v1/
```

---

## API Endpoints

### Users

* POST `/api/v1/users/`
* GET `/api/v1/users/`
* GET `/api/v1/users/<id>`
* PUT `/api/v1/users/<id>`

### Amenities

* POST `/api/v1/amenities/`
* GET `/api/v1/amenities/`
* GET `/api/v1/amenities/<id>`
* PUT `/api/v1/amenities/<id>`

### Places

* POST `/api/v1/places/`
* GET `/api/v1/places/`
* GET `/api/v1/places/<id>`
* PUT `/api/v1/places/<id>`
* GET `/api/v1/places/<place_id>/reviews`

### Reviews

* POST `/api/v1/reviews/`
* GET `/api/v1/reviews/`
* GET `/api/v1/reviews/<id>`
* PUT `/api/v1/reviews/<id>`
* DELETE `/api/v1/reviews/<id>`

---

## Testing

The project was tested using:

* cURL
* Swagger UI
* Python unittest

A detailed testing report is available in **TESTING_REPORT.md**.

---

## Technologies Used

* Python
* Flask
* Flask-RESTX
* REST API
* unittest

---

## Authors

* Alaa Aldwasari
* Lama
* Noura Alosimi 
