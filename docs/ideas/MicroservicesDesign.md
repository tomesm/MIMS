# Mars Immigration System - Microservices Design

Here's a brief summary of which microservices are responsible for database which entities:

Passenger Management Service - Passenger
Immigration Service - ImmigrationCounter
Docking Bay Management Service - DockingBay
Colony Official Service - Colony, ImmigrationRule,
Orbital Station Manager Service - OrbitalStation, 
Shuttle Bay Management Service - Shuttle, Shuttlebay
User Management Service - User, Role, SystemPermission
Spaceline Management Microservice - Spaceline, Spacecraft
Flight Management Service - Flight

## 1. Functional Boundaries

In order to build a microservices-based architecture for the Mars immigration system that fulfills all functional requirements and user stories, we need to identify the functional boundaries and divide the system into smaller, self-contained services. The following microservices can be proposed:

### 1.1. Passenger Management Service

Responsible for handling passenger-related data and operations, such as registration, updating passenger details, and retrieving passenger information.

### 1.2. Immigration Service

Handles the validation of passengers' documents. 
Automates visa validation and send requests to Colony official service to issue visa. It can be also done manually.
Requests visa rules from Colony Official service. Visa should be granted when a passenger fulfills colonys criteria and is granted resources from colony. Than officer can approve the visa.

Assign and unassign users(immigration officers) to counters
Create, update, and delete Immigration counters.
Process passenger visa applications and status updates
Provides metrics on average visa processing time

### 1.3. Docking Bay Management Service

Manages the assignment and scheduling of docking bays for incoming and outgoing ships, ensuring efficient utilization of resources.
Allows docking bay reservation.

Provides information about docking bay availability.

### 1.4. Colony Service

Provides an interface for colony officials to manage colony-specific rules and regulations. Issues visas for passengers based on approval from Immigration Service.

Create, update, and delete colony information
Manage colony resources and immigration rules
Supports or denies resources for arriving passengers (automatically or manually)
Retrieve planned arrivals data
Create, update, provides, and delete visa.
Create, update, provides, and delete immigration rules.

### 1.5. Orbital Station Management Service

Enables the orbital station managers to oversee the entire immigration process, monitor the status of docking bays, and coordinate with colony officials.

Create, update, and delete orbital station information

Retrieve visa processing time, passenger capacity, and forecasts
Retrieve spacecraft schedules

By aggregating passenger data from related services like PassengerManagementService, FlightManagementService, and DockingBayManagementService, it can calculate the percentage of station passenger capacity used at any given moment.


### 1.6 Shuttle Bay Management Service 

The Shuttle Service is responsible for managing the shuttles and their schedules between the orbital station and the Mars colony. This service provides endpoints for creating, updating, retrieving, and deleting shuttle schedules.
Assign and unassign shuttles to shuttle bays.
Assign and unassign shutlles to flights.

### 1.7 User Management Service
Create, update, and delete user information
Create, update, and delete roles and permissions
Handles user authentication and authorisation.


### 1.8 Flight Management Microservice

Create, update, and delete flight information
Retrieve and update flight schedules
Assign and remove spacecrafts from flights. 
Reserves shuttles and shuttlebays for a flight. 

### 1.9 Spaceline Management Microservice

Requests docking bay assignemnts and time slot for arrival, departure or maintenance.
Provides information about planned arrivals and departures (flights).
Provides information about spacecraft and capacities.

Create, update, and delete spaceline information

Manage spacecrafts and schedules for spacelines
Request and receive docking bay assignments and information
Receive not-allowed passengers list

Create, update, and delete spacecraft information
Manage spacecraft capacities



## 2. API Design

The following API design will be used for each microservice in the Mars immigration system.

### 1.1. Passenger Management Service

#### Endpoints:

- `POST /passengers`: Register a new passenger
- `GET /passengers`: Get a list of passengers
- `GET /passengers/{id}`: Get passenger details
- `PUT /passengers/{id}`: Update passenger details
- `DELETE /passengers/{id}`: Delete a passenger

### 1.2. Immigration Service

#### Endpoints:

- `POST /immigration/counters`: Create a new immigration counter
- `GET /immigration/counters`: Get a list of immigration counters
- `PUT /immigration/counters/{id}`: Update an immigration counter
- `DELETE /immigration/counters/{id}`: Delete an immigration counter
- `POST /immigration/counters/{id}/assign`: Assign a user to an immigration counter
- `POST /immigration/counters/{id}/unassign`: Unassign a user from an immigration counter
- `POST /immigration/visas`: Process a passenger visa application
- `PUT /immigration/visas/{id}`: Update visa status
- `GET /immigration/metrics`: Get average visa processing time

### 1.3. Docking Bay Management Service

#### Endpoints:

- `POST /docking-bays`: Create a new docking bay
- `GET /docking-bays`: Get a list of docking bays
- `PUT /docking-bays/{id}`: Update a docking bay
- `DELETE /docking-bays/{id}`: Delete a docking bay
- `GET /docking-bays/availability`: Get docking bay availability

### 1.4. Colony Service

#### Endpoints:

- `POST /colonies`: Create a new colony
- `GET /colonies`: Get a list of colonies
- `PUT /colonies/{id}`: Update a colony
- `DELETE /colonies/{id}`: Delete a colony
- `POST /colonies/{id}/rules`: Create immigration rules
- `GET /colonies/{id}/rules`: Get immigration rules
- `PUT /colonies/{id}/rules/{ruleId}`: Update immigration rules
- `DELETE /colonies/{id}/rules/{ruleId}`: Delete immigration rules
- `POST /colonies/{id}/visas`: Create a visa
- `GET /colonies/{id}/visas`: Get a list of visas
- `PUT /colonies/{id}/visas/{visaId}`: Update a visa
- `DELETE /colonies/{id}/visas/{visaId}`: Delete a visa
- `GET /colonies/{id}/arrivals`: Retrieve planned arrivals data

### 1.5. Orbital Station Management Service

#### Endpoints:

- `POST /orbital-stations`: Create a new orbital station
- `GET /orbital-stations`: Get a list of orbital stations
- `PUT /orbital-stations/{id}`: Update an orbital station
- `DELETE /orbital-stations/{id}`: Delete an orbital station
- `GET /orbital-stations/{id}/processing-time`: Get visa processing time
- `GET /orbital-stations/{id}/capacity`: Get passenger capacity and forecasts
- `GET /orbital-stations/{id}/schedules`: Get spacecraft schedules

### 1.6. Shuttle Bay Management Service

#### Endpoints:

- `POST /shuttle-bays`: Create a new shuttle bay
- `GET /shuttle-bays`: Get a list of shuttle bays
- `PUT /shuttle-bays/{id}`: Update a shuttle bay
- `DELETE /shuttle-bays/{id}`: Delete a shuttle bay
- `POST /shuttles`: Create a new shuttle
- `GET /shuttles`: Get a list of shuttles
- `PUT /shuttles/{id}`: Update a shuttle
- `DELETE /shuttles/{id}`: Delete a shuttle
- `POST /shuttles/{id}/assign-bay`: Assign a shuttle to a shuttle bay
- `POST /shuttles/{id}/unassign-bay`: Unassign a shuttle from a shuttle bay
- `POST /shuttles/{id}/assign-flight`: Assign a shuttle to a flight
- `POST /shuttles/{id}/unassign-flight`: Unassign a shuttle from a flight

### 1.7. User Management Service

#### Endpoints:

- `POST /users`: Create a new user
- `GET /users`: Get a list of users
- `PUT /users/{id}`: Update a user
- `DELETE /users/{id}`: Delete a user
- `POST /roles`: Create a new role
- `GET /roles`: Get a list of roles
- `PUT /roles/{id}`: Update a role
- `DELETE /roles/{id}`: Delete a role
- `POST /permissions`: Create a new permission
- `GET /permissions`: Get a list of permissions
- `PUT /permissions/{id}`: Update a permission
- `DELETE /permissions/{id}`: Delete a permission
- `POST /auth/login`: Authenticate a user
- `POST /auth/logout`: Logout a user

### 1.8. Flight Management Microservice

#### Endpoints:

- `POST /flights`: Create a new flight
- `GET /flights`: Get a list of flights
- `PUT /flights/{id}`: Update a flight
- `DELETE /flights/{id}`: Delete a flight
- `GET /flights/{id}/schedules`: Retrieve and update flight schedules
- `POST /flights/{id}/assign-spacecraft`: Assign a spacecraft to a flight
- `POST /flights/{id}/remove-spacecraft`: Remove a spacecraft from a flight
- `GET /flights/planned-arrivals`: Get a list of planned arrival flights
- `GET /flights/planned-departures`: Get a list of planned departure flights

### 1.9. Spaceline Management Microservice

#### Endpoints:

- `POST /spacelines`: Create a new spaceline
- `GET /spacelines`: Get a list of spacelines
- `PUT /spacelines/{id}`: Update a spaceline
- `DELETE /spacelines/{id}`: Delete a spaceline
- `POST /spacecrafts`: Create a new spacecraft
- `GET /spacecrafts`: Get a list of spacecrafts
- `PUT /spacecrafts/{id}`: Update a spacecraft
- `DELETE /spacecrafts/{id}`: Delete a spacecraft
- `POST /spacecrafts/{id}/assign-flight`: Assign a spacecraft to a flight
- `POST /spacecrafts/{id}/unassign-flight`: Unassign a spacecraft from a flight
- `GET /spacecrafts/{id}/capacity`: Get spacecraft capacities
- `GET /spacecrafts/{id}/not-allowed-passengers`: Get not-allowed passengers list
- `GET /spacecrafts/{id}/docking-bay-assignments`: Get docking bay assignments









# 3. Service-to-Service Communication

To establish effective and scalable communication between microservices, we will use a combination of synchronous and asynchronous communication methods. The microservices will be deployed on AWS, and we will leverage AWS services for implementing the communication infrastructure.

## 3.1. Synchronous Communication

For synchronous communication, we will use RESTful APIs over HTTP/HTTPS. REST is a simple, widely-adopted standard that allows for easy integration and interoperability between services. AWS provides API Gateway to create, publish, and manage RESTful APIs for our microservices. The API Gateway will serve as the entry point for external clients and will route the incoming requests to the appropriate microservices.

## 3.2. Asynchronous Communication

For asynchronous communication, we will use AWS services like Simple Notification Service (SNS) and Simple Queue Service (SQS). These services enable event-driven architecture and help decouple microservices by allowing them to communicate through messages and events.

### 3.2.1. Simple Notification Service (SNS)

AWS SNS is a fully managed publish-subscribe messaging service that enables microservices to send and receive messages in a decoupled manner. SNS supports fan-out architecture, which means that a single message can be delivered to multiple subscribers.

We will use SNS to send notifications and important events between microservices. For example, when a new passenger is added, the Passenger Service can publish a message to an SNS topic, and other interested services (e.g., Notification Service, Reporting Service) can subscribe to the topic to receive updates.

### 3.2.2. Simple Queue Service (SQS)

AWS SQS is a fully managed message queuing service that allows microservices to communicate by exchanging messages through queues. SQS enables decoupling by acting as a buffer between the sender and receiver, allowing them to operate independently and at different rates.

We will use SQS to handle requests that require processing by multiple services or for cases where we need to manage the load on services. For example, we can use SQS to manage the flow of docking bay assignments. The Docking Bay Service can publish docking bay assignments to an SQS queue, and the Shuttle Service can consume the messages from the queue to update the shuttle schedules accordingly.

By using a combination of synchronous (REST) and asynchronous (SNS, SQS) communication methods, we can create a flexible, scalable, and robust architecture for our microservices running on AWS.

# 4. Data Storage and Management

In a microservices architecture, each service should own its data storage and manage its data independently. This promotes decoupling and allows each service to evolve at its own pace. For our system running on AWS, we will use different storage solutions depending on the requirements of each service.

## 4.1. Relational Database

For services that require transactional and relational data storage, we will use Amazon RDS (Relational Database Service). Amazon RDS supports several popular relational databases, such as PostgreSQL, MySQL, and MariaDB.

Some services that might use a relational database include:

- Passenger Service
- Immigration Service
- Docking Bay Service

## 4.2. NoSQL Database

For services that need to store unstructured, semi-structured, or hierarchical data, we will use Amazon DynamoDB, a fully managed, fast, and flexible NoSQL database service.

Services that might use a NoSQL database include:

- Shuttle Service
- Notification Service

## 4.3. Object Storage

For storing large files, such as images or documents, we will use Amazon S3 (Simple Storage Service), a highly-scalable and durable object storage service.

Services that might use object storage include:

- Reporting Service

# 5. Deployment and Scaling

To deploy and manage our microservices on AWS, we will use a combination of services to ensure that our system is scalable, resilient, and easy to maintain.

## 5.1. Containerization

We will containerize our microservices using Docker, which allows for easy packaging, distribution, and deployment of our services. Each service will have its Dockerfile, defining its dependencies and runtime configuration.

## 5.2. Container Orchestration

For container orchestration, we will use Amazon ECS (Elastic Container Service), a fully managed container orchestration service that supports Docker containers. ECS allows us to easily deploy, manage, and scale our services without having to manage the underlying infrastructure.

## 5.3. Load Balancing

To distribute incoming traffic across multiple instances of our services, we will use Amazon ALB (Application Load Balancer), a fully managed, Layer 7 load balancer. ALB can route requests to different microservices based on the request content, allowing for flexible routing and improved availability.

## 5.4. Auto Scaling

To ensure that our services can handle varying loads, we will use AWS Auto Scaling. Auto Scaling can automatically adjust the number of running instances of our services based on demand, ensuring that we have the right amount of resources to handle the incoming traffic.

# 6. Monitoring and Logging

To monitor the performance and health of our microservices, we will use Amazon CloudWatch, a fully managed monitoring service that provides real-time insights into the operational health of our system. CloudWatch can collect metrics, logs, and events from our services and allow us to set alarms and create dashboards to visualize the data.

For centralized logging, we can use Amazon Elasticsearch Service, which allows us to easily store, search, and analyze log data from our services. We can use AWS
