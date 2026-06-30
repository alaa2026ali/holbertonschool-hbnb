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
