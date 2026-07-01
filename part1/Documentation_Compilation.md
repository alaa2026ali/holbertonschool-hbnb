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


The following diagram illustrates the main entities in the Business Logic Layer, their attributes, methods, inheritance, and relationships.

### Business Logic Class Diagram

<img width="1071" height="689" alt="business_logic_class_diagram drawio" src="https://github.com/user-attachments/assets/ee3a251b-8991-4c8b-8f26-7a00f2ab4c95" />

The class diagram illustrates the Business Logic Layer, including inheritance from BaseModel, entity attributes, operations, and relationships between User, Place, Review, and Amenity.

### BaseModel

The BaseModel class is the parent class for all business entities. It provides common attributes and operations shared by every model in the application.

### Attributes

- UUID4 identifier (id)
- Creation timestamp (created_at)
- Last update timestamp (updated_at)

### Operations

- Save
- Update
- Delete

### User

Represents a registered user of the HBnB platform.

Attributes

- First name
- Last name
- Email
- Password
- Administrator status

Operations

- Register
- Login
- Update profile

### Place

Represents a property listed on the platform.

Attributes

- Title
- Description
- Price
- Latitude
- Longitude

Operations

- Create
- Update
- Delete

### Review

Represents a review written by a user for a place.

Attributes

- Rating
- Comment

Operations

- Create
- Update
- Delete

### Amenity

Represents facilities or services available for a place.

Attributes

- Name
- Description

Operations

- Create
- Update
- Delete

### Relationships

#### User → Place

- One user can own multiple places.
- Each place belongs to one user.

#### User → Review

- One user can write multiple reviews.
- Each review belongs to one user.

#### Place → Review

- One place can receive multiple reviews.
- Each review belongs to one place.

#### Place ↔ Amenity

- A place can include multiple amenities.
- An amenity can be associated with multiple places.

### Inheritance

All entities inherit from the BaseModel class.

- User inherits from BaseModel.
- Place inherits from BaseModel.
- Review inherits from BaseModel.
- Amenity inherits from BaseModel.

This inheritance allows all entities to share the same identifier, timestamps, and common operations while reducing code duplication and improving maintainability.

---

# 6. Sequence Diagrams for API Calls

The following sequence diagrams show how the main API calls work in the HBnB application. Each diagram explains how the request moves between the API, the Business Logic layer, and the Database until the user receives a response.

---

## 6.1 User Registration

![User Registration](User%20Registration.png)

When a new user registers, the API receives the request and sends it to the Business Logic layer. The system first checks if the email is already registered. If the email is available, the user information is saved in the database and a success message is returned. Otherwise, the registration fails and an error message is sent back.

### Main Steps

- The user submits the registration form.
- The API receives the request.
- The Business Logic validates the data.
- The database checks the email and stores the new user.
- The result is returned to the user.

---

## 6.2 Place Creation

![Place Creation](Place%20Creation.png)

This diagram shows how a user creates a new place. The API receives the place information and passes it to the Business Logic layer. After validating the data and checking the owner, the place is saved in the database if everything is correct.

### Main Steps

- The user sends a create place request.
- The API forwards the request.
- The Business Logic validates the place information.
- The database stores the new place.
- The user receives the result.

---

## 6.3 Review Submission

![Review Submission](Review%20Submission.png)

This diagram shows the process of submitting a review. The system validates the review information and checks whether the selected place exists before saving the review in the database.

### Main Steps

- The user submits a review.
- The API sends the request to the Business Logic layer.
- The system validates the review.
- The database saves the review.
- The user receives a success or failure response.

---

## 6.4 Fetching a List of Places

![Fetching a List of Places](Fetching%20a%20List%20of%20Places.png)

This diagram shows how users request a list of places. The API sends the search request to the Business Logic layer, which retrieves the matching places from the database and returns them to the user.

### Main Steps

- The user requests a list of places.
- The API forwards the request.
- The Business Logic retrieves the data.
- The database returns the matching places.
- The results are sent back to the user.
