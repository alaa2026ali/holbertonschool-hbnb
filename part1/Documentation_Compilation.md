Task 0: High-Level Package Diagram
Objective

The objective of this task is to design a High-Level Package Diagram that represents the overall architecture of the HBnB application. The diagram provides a clear view of the system's layered structure and the communication between its main components.

Description

The architecture follows a layered design to separate responsibilities and improve scalability, maintainability, and modularity.

Presentation Layer

The Presentation Layer is responsible for handling user interactions. It receives requests from the client and returns responses after processing.

Components:

FrontendServices
API
Business Logic Layer

The Business Logic Layer contains the core application logic and business rules. It processes requests, manages the main entities, and acts as a Facade between the Presentation Layer and the Persistence Layer.

Components:

BaseModel
UserModel
PlaceModel
ReviewModel
AmenityModel
Persistence Layer

The Persistence Layer is responsible for data persistence. It performs CRUD operations and communicates with the database through the database access component.

Components:

DatabaseAccess
Database

The Database stores all application data required by the system.

Layer Communication

The communication flow follows this order:

Presentation Layer → Business Logic Layer → Persistence Layer → Database

Conclusion

This package diagram provides a high-level view of the HBnB architecture and serves as the foundation for the detailed UML diagrams that will be created in the following tasks.
