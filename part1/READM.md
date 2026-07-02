# HBnB Project

## Project Objective: HBnB Evolution - Part 1

HBnB Evolution is a simplified Airbnb-inspired application designed to demonstrate software architecture and object-oriented design. The project prepares the system for future implementation by defining its structure, business logic, and relationships between components.

### Project Objectives

* Design a scalable and maintainable architecture.
* Apply object-oriented programming principles.
* Prepare the project for future REST API and database integration.
* Build a solid foundation for the next development phases.

---

## Project Scope

HBnB Evolution allows users to:

* Register and manage user accounts.
* Create and manage places.
* Associate amenities with places.
* Create and manage reviews.

---

## Business Rules and Requirements

### User Entity

* First name
* Last name
* Email
* Password
* Administrator status

**Operations**

* Create
* Update
* Delete

### Place Entity

* Title
* Description
* Price
* Latitude
* Longitude

**Relationships**

* Belongs to one User (Owner)
* Can have multiple Amenities

**Operations**

* Create
* Update
* Delete
* List

### Review Entity

* Rating
* Comment

**Relationships**

* Belongs to one User
* Belongs to one Place

**Operations**

* Create
* Update
* Delete
* List by Place

### Amenity Entity

* Name
* Description

**Operations**

* Create
* Update
* Delete
* List

### General Rules

* Every entity has a unique UUID.
* All entities include creation and update timestamps.

---

## General Architecture

The project follows a **three-layer architecture** using the **Facade Pattern** to simplify communication between components.

## High-Level Package Diagram

![High-Level Package Diagram](High-Level%20Package%20Diagram.drawio.png)

### 1. Presentation Layer

* Handles user interactions.
* Receives requests and returns responses.

### 2. Business Logic Layer

* Contains the core models:

  * User
  * Place
  * Review
  * Amenity
* Applies business rules.
* Communicates with the Persistence Layer through the Facade.

### 3. Persistence Layer

* Manages data storage.
* Performs CRUD operations.
* Ensures data consistency.

---
# Business Logic Layer (Class Diagram)

<img width="1071" height="689" alt="business_logic_class_diagram drawio (1)" src="https://github.com/user-attachments/assets/3b4e4ac5-4e27-42c2-8542-a88dad261cea" />

This section outlines the core domain models designed for the HBnB Evolution application. All business entities inherit from a shared base to ensure a clean, maintainable, and decoupled codebase.

## Core Components
* **BaseModel:** The parent class providing unique identification (id as UUID4) and audit timestamps (created_at, updated_at) for all entities, along with core lifecycle operations (save, update, delete).

* **User:** Handles profile management (first_name, last_name, email, protected password, and is_admin status) and authentication operations (register, login).

* **Place:** Represents property listings, detailing title, description, price, latitude, and longitude. It links to the owner via owner_id and tracks features through amenity_ids.

* **Review:** Manages user feedback and scores (rating, comment) for specific properties, mapping relationships using place_id and user_id.

* **Amenity:** Represents available property facilities (name, description).

## Entity Relationships
* **User <-> Place (1 to Many):** A user can own multiple places; each place has one owner.

* **User <-> Review (1 to Many):** A user can write multiple reviews.

* **Place <-> Review (1 to Many):** A place can receive multiple reviews.

* **Place <-> Amenity (Many to Many):** Places can include multiple amenities, and amenities can belong to multiple places (managed via ID cross-referencing).


---

# Sequence Diagrams for API Calls

## Overview

This task focuses on creating sequence diagrams for the main API calls in the HBnB application. The diagrams illustrate how requests move between the User, API, Business Logic, and Database to complete different operations within the system.

---

## User Registration

![User Registration](User%20Registration.png)

This diagram shows the process of creating a new user account. The request is received by the API, validated by the Business Logic layer, and then stored in the database if all the required conditions are met.

---

## Place Creation

![Place Creation](Place%20Creation.png)

This diagram illustrates how a user creates a new place listing. The system validates the request, checks the required information, and saves the new place in the database before returning the result.

---

## Review Submission

![Review Submission](Review%20Submission.png)

This diagram shows how a review is submitted for a place. The system validates the review, verifies the selected place, stores the review in the database, and returns the appropriate response.

---

## Fetching a List of Places

![Fetching a List of Places](Fetching%20a%20List%20of%20Places.png)

This diagram illustrates how users retrieve a list of places. The request is processed by the Business Logic layer, which retrieves the matching records from the database and returns them through the API.

---

## Tool Used

- Mermaid

---

## Files

- `User Registration.png`
- `Place Creation.png`
- `Review Submission.png`
- `Fetching a List of Places.png`
