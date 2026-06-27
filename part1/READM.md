HBnB Evolution – Part 1
Task 0: High-Level Package Diagram
Project Overview

HBnB Evolution is a simplified Airbnb-inspired application developed as part of the Holberton School curriculum. The project is divided into multiple phases, each focusing on a different aspect of software engineering. Part 1 focuses on designing the system architecture using UML diagrams before moving on to implementation.

The application enables users to register, manage properties, associate amenities with places, and submit reviews while following a modular and scalable software architecture.

Objective

The objective of Task 0 is to design a High-Level Package Diagram that represents the overall architecture of the HBnB application. The diagram provides a clear view of the system's organization by separating responsibilities into three independent layers.

This design improves maintainability, scalability, and readability while establishing a solid foundation for future development.

Three-Layer Architecture

The application follows a Three-Layer Architecture, where each layer has a specific responsibility.

1. Presentation Layer

The Presentation Layer is responsible for handling user interactions. It receives requests from users, validates input, and returns responses. This layer communicates only with the Business Logic Layer.

Responsibilities

Handle user requests.
Validate input data.
Return application responses.
Forward requests to the Business Logic Layer.
2. Business Logic Layer

The Business Logic Layer contains the application's core functionality and business rules. It coordinates communication between the Presentation and Persistence layers using the Facade pattern.

Core Models

User
Place
Review
Amenity

Responsibilities

Process application requests.
Apply business rules.
Manage relationships between entities.
Coordinate data operations.
3. Persistence Layer

The Persistence Layer manages data storage and retrieval. It is responsible for maintaining data integrity and performing CRUD operations.

Responsibilities

Store and retrieve data.
Perform CRUD operations.
Ensure data consistency.
Provide data access to the Business Logic Layer.
Layer Communication

The application follows a unidirectional communication flow:

Presentation Layer
        ↓
Business Logic Layer
        ↓
Persistence Layer

The Presentation Layer never communicates directly with the Persistence Layer. All interactions pass through the Business Logic Layer, which acts as the central coordinator of the application.

Benefits of the Architecture
Separation of concerns.
Improved maintainability.
Better scalability.
Easier testing and debugging.
Modular and reusable components.
Clear communication between system layers.
Deliverables
High-Level Package Diagram (UML)
UML source file (.drawio)
Exported diagram (.png)
Project documentation (README.md)
Conclusion

The High-Level Package Diagram establishes the architectural foundation of the HBnB application. By organizing the system into Presentation, Business Logic, and Persistence layers, the design promotes modularity, simplifies future development, and supports the implementation of a scalable and maintainable application.
