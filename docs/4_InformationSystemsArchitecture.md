# 4. Information System Architecture

In this section, we will define the data entities, relationships, data flows, and applications within the Mars immigration system.

## 4.1 Data Architecture

### Data Entities

- **Passenger**: Represents an individual arriving at the Mars station.
- **Visa**: Represents a temporary visa issued to a passenger, with a specified duration (6, 12, 18, or 24 Mars months).
- **Colony**: Represents a Mars colony with specific immigration rules and regulations.
- **User**: Represents a system user with a specific role (e.g., Passenger, Immigration Officer, Station Manager, Spaceline Dispatcher, Colony Official, etc.)
- **DockingBay**: Represents a docking bay at the Mars station for arriving and departing spacecraft.

### Relationships

- **Passenger** has one or more **Visa** applications.
- **Visa** is issued by a **Colony**.
- **User** is associated with a **Role** (e.g., Passenger, Immigration Officer, Station Manager, etc.)
- **DockingBay** is managed by a **Station Manager** and used by **Spaceline Dispatcher** to assign spacecraft.

### Data Flows

![alt Visa Process Sequence](./pictures/visa_process_sequence.png)

1. Passengers register and submit visa applications, which include their personal information and visa preferences.
2. Immigration officers access the system to review and process visa applications.
3. The system stores the visa status (approved or denied) and relevant details.
4. Station managers and other authorized personnel access the system to view resource allocation, docking bay assignments, and other relevant information.

## 4.2 Application Architecture

### Applications

- **Visa Application Portal**: A web or mobile application that allows passengers to register and apply for a temporary visa.
- **Immigration Database**: A centralized database that stores all data related to passengers, visas, colonies, users, and docking bays.
- **Reporting Tools**: Tools and applications that generate reports and insights based on the system's data for authorized personnel.
- **Docking Bay Dispatch**: An application that manages docking bay assignments for arriving and departing spacecraft, used by Spaceline Dispatchers and Station Managers.

## 4.3 Microservices

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


### 4.3.1 Passenger Management Service

Responsible for handling passenger-related data and operations, such as registration, updating passenger details, and retrieving passenger information.

#### Endpoints:

- `POST /passengers`: Register a new passenger
- `GET /passengers`: Get a list of passengers
- `GET /passengers/{id}`: Get passenger details
- `PUT /passengers/{id}`: Update passenger details
- `DELETE /passengers/{id}`: Delete a passenger

### 4.3.2 Immigration Service

Handles the validation of passengers' documents. 
Automates visa validation and send requests to Colony official service to issue visa. It can be also done manually.
Requests visa rules from Colony Official service. Visa should be granted when a passenger fulfills colonys criteria and is granted resources from colony. Than officer can approve the visa.

Assign and unassign users(immigration officers) to counters
Create, update, and delete Immigration counters.
Process passenger visa applications and status updates
Provides metrics on average visa processing time

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

### 4.3.3 Docking Bay Management Service

Manages the assignment and scheduling of docking bays for incoming and outgoing ships, ensuring efficient utilization of resources.
Allows docking bay reservation.

Provides information about docking bay availability.

#### Endpoints:

- `POST /docking-bays`: Create a new docking bay
- `GET /docking-bays`: Get a list of docking bays
- `PUT /docking-bays/{id}`: Update a docking bay
- `DELETE /docking-bays/{id}`: Delete a docking bay
- `GET /docking-bays/availability`: Get docking bay availability

### 4.3.4 Colony Service

Provides an interface for colony officials to manage colony-specific rules and regulations. Issues visas for passengers based on approval from Immigration Service.

Create, update, and delete colony information
Manage colony resources and immigration rules
Supports or denies resources for arriving passengers (automatically or manually)
Retrieve planned arrivals data
Create, update, provides, and delete visa.
Create, update, provides, and delete immigration rules.

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

### 4.3.5 Orbital Station Management Service

Enables the orbital station managers to oversee the entire immigration process, monitor the status of docking bays, and coordinate with colony officials.

Create, update, and delete orbital station information

Retrieve visa processing time, passenger capacity, and forecasts
Retrieve spacecraft schedules

By aggregating passenger data from related services like PassengerManagementService, FlightManagementService, and DockingBayManagementService, it can calculate the percentage of station passenger capacity used at any given moment.

#### Endpoints:

- `POST /orbital-stations`: Create a new orbital station
- `GET /orbital-stations`: Get a list of orbital stations
- `PUT /orbital-stations/{id}`: Update an orbital station
- `DELETE /orbital-stations/{id}`: Delete an orbital station
- `GET /orbital-stations/{id}/processing-time`: Get visa processing time
- `GET /orbital-stations/{id}/capacity`: Get passenger capacity and forecasts
- `GET /orbital-stations/{id}/schedules`: Get spacecraft schedules



### 4.3.6 Shuttle Bay Management Service 

The Shuttle Service is responsible for managing the shuttles and their schedules between the orbital station and the Mars colony. This service provides endpoints for creating, updating, retrieving, and deleting shuttle schedules.
Assign and unassign shuttles to shuttle bays.
Assign and unassign shutlles to flights.

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

### 4.3.7 User Management Service
Create, update, and delete user information
Create, update, and delete roles and permissions
Handles user authentication and authorisation.

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


### 4.3.8 Flight Management Microservice

Create, update, and delete flight information
Retrieve and update flight schedules
Assign and remove spacecrafts from flights. 
Reserves shuttles and shuttlebays for a flight. 

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

### 4.3.9 Spaceline Management Microservice

Requests docking bay assignemnts and time slot for arrival, departure or maintenance.
Provides information about planned arrivals and departures (flights).
Provides information about spacecraft and capacities.

Create, update, and delete spaceline information

Manage spacecrafts and schedules for spacelines
Request and receive docking bay assignments and information
Receive not-allowed passengers list

Create, update, and delete spacecraft information
Manage spacecraft capacities

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


## 5. Use Cases