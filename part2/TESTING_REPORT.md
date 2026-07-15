# HBnB Evolution - Part 2 Testing Report

## Overview

This report documents the testing and validation process performed for the **HBnB Evolution - Part 2** REST API. The objective was to verify that all implemented endpoints function correctly, validate user input, return the appropriate HTTP status codes, and conform to the project requirements.

---

# Testing Environment

- **Programming Language:** Python 3
- **Framework:** Flask
- **API Documentation:** Flask-RESTX (Swagger)
- **Manual Testing Tool:** cURL
- **Automated Testing Framework:** unittest

---

# Test Methods

The API was verified using the following methods:

- Manual endpoint testing with **cURL**.
- Interactive endpoint verification using **Swagger UI**.
- Automated testing using the Python **unittest** framework.
- Validation testing for incorrect or missing input data.

---

# Tested Endpoints

## User Endpoints

### POST /api/v1/users/

| Test Case | Expected Result | Status |
|-----------|-----------------|--------|
| Create a valid user | 201 Created | Passed |
| Missing required field | 400 Bad Request | Passed |
| Invalid email format | 400 Bad Request | Passed |

### GET /api/v1/users/

| Test Case | Expected Result | Status |
|-----------|-----------------|--------|
| Retrieve all users | 200 OK | Passed |

### GET /api/v1/users/{id}

| Test Case | Expected Result | Status |
|-----------|-----------------|--------|
| Existing user | 200 OK | Passed |
| Non-existing user | 404 Not Found | Passed |

### PUT /api/v1/users/{id}

| Test Case | Expected Result | Status |
|-----------|-----------------|--------|
| Valid update | 200 OK | Passed |
| Invalid user ID | 404 Not Found | Passed |

---

## Amenity Endpoints

### POST /api/v1/amenities/

| Test Case | Expected Result | Status |
|-----------|-----------------|--------|
| Create a valid amenity | 201 Created | Passed |
| Missing name | 400 Bad Request | Passed |

### GET /api/v1/amenities/

| Test Case | Expected Result | Status |
|-----------|-----------------|--------|
| Retrieve all amenities | 200 OK | Passed |

### GET /api/v1/amenities/{id}

| Test Case | Expected Result | Status |
|-----------|-----------------|--------|
| Existing amenity | 200 OK | Passed |
| Invalid ID | 404 Not Found | Passed |

### PUT /api/v1/amenities/{id}

| Test Case | Expected Result | Status |
|-----------|-----------------|--------|
| Valid update | 200 OK | Passed |

---

## Place Endpoints

### POST /api/v1/places/

| Test Case | Expected Result | Status |
|-----------|-----------------|--------|
| Create a valid place | 201 Created | Passed |
| Invalid price | 400 Bad Request | Passed |
| Missing title | 400 Bad Request | Passed |

### GET /api/v1/places/

| Test Case | Expected Result | Status |
|-----------|-----------------|--------|
| Retrieve all places | 200 OK | Passed |

### GET /api/v1/places/{id}

| Test Case | Expected Result | Status |
|-----------|-----------------|--------|
| Existing place | 200 OK | Passed |
| Invalid ID | 404 Not Found | Passed |

### PUT /api/v1/places/{id}

| Test Case | Expected Result | Status |
|-----------|-----------------|--------|
| Valid update | 200 OK | Passed |

---

## Review Endpoints

### POST /api/v1/reviews/

| Test Case | Expected Result | Status |
|-----------|-----------------|--------|
| Create a valid review | 201 Created | Passed |
| Invalid rating | 400 Bad Request | Passed |

### GET /api/v1/reviews/

| Test Case | Expected Result | Status |
|-----------|-----------------|--------|
| Retrieve all reviews | 200 OK | Passed |

### GET /api/v1/reviews/{id}

| Test Case | Expected Result | Status |
|-----------|-----------------|--------|
| Existing review | 200 OK | Passed |
| Invalid ID | 404 Not Found | Passed |

### PUT /api/v1/reviews/{id}

| Test Case | Expected Result | Status |
|-----------|-----------------|--------|
| Valid update | 200 OK | Passed |

---

# Validation Testing

The following validation rules were tested:

- Required fields must not be empty.
- Email addresses must follow a valid format.
- Numeric fields must contain valid numeric values.
- Rating values must be within the accepted range.
- Invalid resource identifiers must return **404 Not Found**.
- Invalid request data must return **400 Bad Request**.

---

# Swagger Documentation

The API documentation was generated using **Flask-RESTX**.

Swagger UI was used to verify:

- Endpoint availability.
- HTTP methods.
- Request models.
- Response formats.
- Response status codes.

---

# Automated Testing

Automated tests were implemented using the Python **unittest** framework.

The automated test suite covers:

- User endpoints.
- Amenity endpoints.
- Place endpoints.
- Review endpoints.
- Validation scenarios.

---

# Summary

| Component | Result |
|----------|--------|
| User API | Passed |
| Amenity API | Passed |
| Place API | Passed |
| Review API | Passed |
| Validation | Passed |
| Swagger Documentation | Passed |
| Automated Tests | Passed |

---

# Conclusion

The HBnB Evolution - Part 2 REST API was successfully validated through both manual and automated testing. All implemented endpoints behaved as expected, input validation rules were enforced correctly, and the API documentation generated by Flask-RESTX accurately reflects the available resources and operations.
