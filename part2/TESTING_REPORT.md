# TESTING_REPORT.md

# HBnB Evolution - Part 2 Testing Report

## Overview

This report documents the testing process performed on the HBnB Evolution Part 2 REST API. The purpose of the tests is to verify that all implemented endpoints work correctly, validate input data, return the appropriate HTTP status codes, and comply with the project requirements.

---

# Testing Environment

* Language: Python 3
* Framework: Flask
* API Documentation: Flask-RESTX (Swagger)
* Manual Testing Tool: cURL
* Automated Testing Framework: unittest

---

# Tested Endpoints

## User Endpoints

### POST /api/v1/users/

| Test Case              | Expected Result | Status |
| ---------------------- | --------------- | ------ |
| Create a valid user    | 201 Created     | Passed |
| Missing required field | 400 Bad Request | Passed |
| Invalid email format   | 400 Bad Request | Passed |

### GET /api/v1/users/

| Test Case          | Expected Result | Status |
| ------------------ | --------------- | ------ |
| Retrieve all users | 200 OK          | Passed |

### GET /api/v1/users/{id}

| Test Case         | Expected Result | Status |
| ----------------- | --------------- | ------ |
| Existing user     | 200 OK          | Passed |
| Non-existing user | 404 Not Found   | Passed |

### PUT /api/v1/users/{id}

| Test Case       | Expected Result | Status |
| --------------- | --------------- | ------ |
| Valid update    | 200 OK          | Passed |
| Invalid user ID | 404 Not Found   | Passed |

---

## Amenity Endpoints

### POST /api/v1/amenities/

| Test Case              | Expected Result | Status |
| ---------------------- | --------------- | ------ |
| Create a valid amenity | 201 Created     | Passed |
| Missing name           | 400 Bad Request | Passed |

### GET /api/v1/amenities/

| Test Case              | Expected Result | Status |
| ---------------------- | --------------- | ------ |
| Retrieve all amenities | 200 OK          | Passed |

### GET /api/v1/amenities/{id}

| Test Case        | Expected Result | Status |
| ---------------- | --------------- | ------ |
| Existing amenity | 200 OK          | Passed |
| Invalid ID       | 404 Not Found   | Passed |

### PUT /api/v1/amenities/{id}

| Test Case    | Expected Result | Status |
| ------------ | --------------- | ------ |
| Valid update | 200 OK          | Passed |

---

## Place Endpoints

### POST /api/v1/places/

| Test Case            | Expected Result | Status |
| -------------------- | --------------- | ------ |
| Create a valid place | 201 Created     | Passed |
| Invalid price        | 400 Bad Request | Passed |
| Missing title        | 400 Bad Request | Passed |

### GET /api/v1/places/

| Test Case           | Expected Result | Status |
| ------------------- | --------------- | ------ |
| Retrieve all places | 200 OK          | Passed |

### GET /api/v1/places/{id}

| Test Case      | Expected Result | Status |
| -------------- | --------------- | ------ |
| Existing place | 200 OK          | Passed |
| Invalid ID     | 404 Not Found   | Passed |

### PUT /api/v1/places/{id}

| Test Case    | Expected Result | Status |
| ------------ | --------------- | ------ |
| Valid update | 200 OK          | Passed |

---

## Review Endpoints

### POST /api/v1/reviews/

| Test Case             | Expected Result | Status |
| --------------------- | --------------- | ------ |
| Create a valid review | 201 Created     | Passed |
| Invalid rating        | 400 Bad Request | Passed |

### GET /api/v1/reviews/

| Test Case            | Expected Result | Status |
| -------------------- | --------------- | ------ |
| Retrieve all reviews | 200 OK          | Passed |

### GET /api/v1/reviews/{id}

| Test Case       | Expected Result | Status |
| --------------- | --------------- | ------ |
| Existing review | 200 OK          | Passed |
| Invalid ID      | 404 Not Found   | Passed |

### PUT /api/v1/reviews/{id}

| Test Case    | Expected Result | Status |
| ------------ | --------------- | ------ |
| Valid update | 200 OK          | Passed |

---

# Validation Testing

The following validation rules were verified:

* Required fields cannot be empty.
* Invalid email formats are rejected.
* Numeric values are validated.
* Rating values are restricted to the allowed range.
* Invalid resource identifiers return **404 Not Found**.
* Invalid request payloads return **400 Bad Request**.

---

# Swagger Documentation

Swagger documentation was successfully generated using Flask-RESTX.

The documentation correctly lists all implemented endpoints, supported HTTP methods, request models, and response formats.

---

# Automated Testing

Automated tests were created using the Python **unittest** framework.

The test suite covers:

* User endpoints
* Amenity endpoints
* Place endpoints
* Review endpoints
* Validation scenarios

---

# Summary

| Component             | Result |
| --------------------- | ------ |
| User API              | Passed |
| Amenity API           | Passed |
| Place API             | Passed |
| Review API            | Passed |
| Validation            | Passed |
| Swagger Documentation | Passed |
| Automated Tests       | Passed |

---

# Conclusion

The HBnB Evolution Part 2 REST API was successfully tested using both manual and automated testing techniques. All endpoints returned the expected HTTP status codes, input validation worked correctly, and the generated Swagger documentation accurately described the implemented API.
