# HBnB Evolution - Technical Documentation

## 1. Context and Objective

This document provides the technical foundation for the **HBnB Evolution** application. It describes the system architecture, business logic, core entities, and their interactions. The objective is to establish a clear and maintainable design before the implementation phase begins.

---

## 2. Problem Description

HBnB Evolution is a simplified property rental platform inspired by Airbnb. The application enables users to manage properties, reviews, and amenities through a structured three-layer architecture.

The system supports the following features:

* **User Management:** Register users, update profiles, and manage administrator privileges.
* **Place Management:** Create, update, delete, and list properties with details such as title, description, price, latitude, and longitude.
* **Review Management:** Create, update, delete, and list reviews for places, including ratings and comments.
* **Amenity Management:** Create, update, delete, and manage amenities associated with places.

---

## 3. Business Rules and Requirements

### User Entity

**Attributes**

* First name
* Last name
* Email
* Password
* Administrator status (Boolean)

**Operations**

* Create
* Update
* Delete

### Place Entity

**Attributes**

* Title
* Description
* Price
* Latitude
* Longitude

**Relationships**

* Belongs to one User (Owner)
* Can be associated with multiple Amenities

**Operations**

* Create
* Update
* Delete
* List

### Review Entity

**Attributes**

* Rating
* Comment

**Relationships**

* Belongs to one User
* Belongs to one Place

**Operations**

* Create
* Update
* Delete
* List reviews by place

### Amenity Entity

**Attributes**

* Name
* Description

**Operations**

* Create
* Update
* Delete
* List

### Common Requirements

All entities must include:

* A unique identifier using **UUID4**.
* Creation timestamp.
* Last update timestamp.

---

## 4. System Architecture

The application follows a **three-layer architecture** to ensure modularity, maintainability, and separation of concerns.

### Presentation Layer

Handles the API used by users and clients.

### Business Logic Layer

Contains the main models and rules of the application.

### Persistence Layer

Stores and retrieves data from the database.

### High-Level Package Diagram

![High-Level Package Diagram](High-Level%20Package%20Diagram.drawio.png)



## 5. Detailed Class Diagram – Business Logic Layer

The following diagram illustrates the main entities in the Business Logic Layer and the relationships between them.

### Main Entities and Relationships

#### User

* Owns places.
* Writes reviews.

#### Place

* Belongs to one user.
* Can have amenities.
* Can receive reviews.

#### Review

* Belongs to one user.
* Belongs to one place.

#### Amenity

* Can be linked to many places.
