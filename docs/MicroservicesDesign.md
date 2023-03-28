# Mars Immigration System - Microservices Design

## 1. Functional Boundaries

In order to build a microservices-based architecture for the Mars immigration system that fulfills all functional requirements and user stories, we need to identify the functional boundaries and divide the system into smaller, self-contained services. The following microservices can be proposed:

### 1.1. Passenger Management Service

Responsible for handling passenger-related data and operations, such as registration, updating passenger details, and retrieving passenger information.

### 1.2. Immigration Control Service

Handles the validation of passengers' documents, health status, and criminal records. This service will also prioritize passengers based on various criteria.

### 1.3. Docking Bay Management Service

Manages the assignment and scheduling of docking bays for incoming and outgoing ships, ensuring efficient utilization of resources.

### 1.4. Colony Official Service

Provides an interface for colony officials to manage colony-specific rules and regulations, review passengers' details, and make decisions on their eligibility for settlement.

### 1.5. Orbital Station Manager Service

Enables the orbital station managers to oversee the entire immigration process, monitor the status of docking bays, and coordinate with colony officials.

### 1.6. Notification Service

Responsible for sending notifications to passengers, colony officials, and orbital station managers regarding updates on the immigration process, docking bay assignments, and other important events.

### 1.7. Reporting Service

Generates various reports and analytics for stakeholders to review and make informed decisions based on the data.

### 1.8. Authentication and Authorization Service

Manages user authentication and authorization, ensuring that only authorized users can access the various services and perform actions within their assigned roles.

### 1.9 Shuttle Service 

The Shuttle Service is responsible for managing the shuttles and their schedules between the orbital station and the Mars colony. This service provides endpoints for creating, updating, retrieving, and deleting shuttle schedules.

## 2. API Design

The following API design will be used for each microservice in the Mars immigration system.

### 2.1. Passenger Management Service API
<details>
 <summary><code>POST</code> <code><b>/passengers</b></code> <code>(Register a new passenger)</code></summary>

###### Request:

```json
{
    "name": "John Doe",
    "date_of_birth": "1990-01-01",
    "gender": "male",
    "country": "Earth",
    "health_status": "healthy",
    "criminal_record": false
}
```
###### Response:
```json
{
  "message": "Passenger created successfully"
}

```
</details>

<details>
 <summary><code>PUT</code> <code><b>/passengers/{id}</b></code> <code>(Update passenger details by ID)</code></summary>

###### Request:

```json
{
    "name": "John Doe",
    "date_of_birth": "1990-01-01",
    "gender": "male",
    "country": "Earth",
    "health_status": "healthy",
    "criminal_record": false
}
```
###### Response:
```json
{
  "message": "Passenger updated successfully"
}

```
</details>

<details>
 <summary><code>GET</code> <code><b>/passengers/{id}</b></code> <code>(Get passenger details by ID)</code></summary>

###### Response:
```json
{
    "name": "John Doe",
    "date_of_birth": "1990-01-01",
    "gender": "male",
    "country": "Earth",
    "health_status": "healthy",
    "criminal_record": false
}
```
</details>

<details>
 <summary><code>GET</code> <code><b>/passengers</b></code> <code>(Get a list of all passengers)</code></summary>

###### Response:
```json
[
    {
        "id": 1,
        "name": "John Doe",
        "date_of_birth": "1990-01-01",
        "gender": "male",
        "country": "Earth",
        "health_status": "healthy",
        "criminal_record": false
    },
...
]
```
</details>

<details>
 <summary><code>DELETE</code> <code><b>/passengers</b></code> <code>(Delete a passenger by ID)</code></summary>

###### Response:
```
Passenger record uuid#<uuid> deleted successfully
```
</details>




### 2.2. Immigration Control Service API

#### Endpoints:

- POST `/immigration/validate`: Validate a passenger's documents, health status, and criminal records
- GET `/immigration/prioritize`: Get a list of prioritized passengers

#### Requests:

- POST /immigration/validate


```json
{
    "id": 1
}
```

#### Responses:

- GET /immigration/prioritize

```json
[
    {
        "id": 1,
        "name": "John Doe",
        "date_of_birth": "1990-01-01",
        "gender": "male",
        "country": "Earth",
        "health_status": "healthy",
        "criminal_record": false,
        "priority": 10
    },
...
]
```


### 2.3. Docking Bay Management Service API

#### Endpoints:

- POST `/docking_bays`: Create a new docking bay
- GET `/docking_bays`: Get a list of all docking bays
- GET `/docking_bays/{id}`: Get docking bay details by ID
- PUT `/docking_bays/{id}`: Update docking bay details by ID
- DELETE `/docking_bays/{id}`: Delete a docking bay by ID
- POST `/docking_bays/{id}`/assign: Assign a ship to a docking bay

#### Requests:

- POST /docking_bays

```json
{
    "name": "Docking Bay A",
    "status": "available"
}
```
- PUT /docking_bays/{id}

```json
{
    "name": "Docking Bay A",
    "status": "occupied"
}
```
- POST /docking_bays/{id}/assign:

```json
{
    "ship_id": 1
}
```
#### Responses:

- GET /docking_bays:

```json
[
    {
        "id": 1,
        "name": "Docking Bay A",
        "status": "available"
    },
...
]
```
- GET /docking_bays/{id}:

```json
{
    "id": 1,
    "name": "Docking Bay A",
    "status": "available"
}
```

### 2.4. Colony Official Service API

#### Endpoints:

- POST `/colony_rules`: Create a new colony rule
- GET `/colony_rules`: Get a list of all colony rules
- GET `/colony_rules/{id}`: Get colony rule details by ID
- PUT `/colony_rules/{id}`: Update colony rule details by ID
- DELETE `/colony_rules/{id}`: Delete a colony rule by ID

#### Requests:

- POST /colony_rules:

```json
{
    "name": "Health requirements",
    "description": "All passengers must be in good health to enter the colony."
}
```
- PUT /colony_rules/{id}

```json
{
    "name": "Health requirements",
    "description": "All passengers must be in good health to enter the colony."
}
```

#### Responses:

- GET /colony_rules


```json
[
    {
        "id": 1,
        "name": "Health requirements",
        "description": "All passengers must be in good health to enter the colony."
    },
...
]
```
- GET /colony_rules/{id}

```json
 {
    "id": 1,
    "name": "Health requirements",
    "description": "All passengers must be in good health to enter the colony."
}
```

### 2.5. Orbital Station Manager Service API

#### Endpoints:

- GET `/station_status`: Get the current status of the orbital station
- POST `/station_actions`: Perform an action on the orbital station (e.g., maintenance, emergency)

#### Requests:

- POST /station_rules

```json
{
    "name": "Luggage restrictions",
    "description": "Passengers are allowed a maximum of 30 kg of luggage."
}
```
- PUT /station_rules/{id}

```json
{
    "name": "Luggage restrictions",
    "description": "Passengers are allowed a maximum of 30 kg of luggage."
}
```

#### Responses:

- GET /station_rules

```json
[
    {
        "id": 1,
        "name": "Luggage restrictions",
        "description": "Passengers are allowed a maximum of 30 kg of luggage."
    },
...
]
```
- GET /station_rules/{id}:

```json
{
    "id": 1,
    "name": "Luggage restrictions",
    "description": "Passengers are allowed a maximum of 30 kg of luggage."
}
```

### 2.6. Notification Service API

- POST `/notifications`: Send a notification to passengers, colony officials, or orbital station managers

##### Request:

```json
{
    "recipient_ids": [1, 2, 3],
    "message": "Shuttle delay notification: The shuttle departure time has been changed to 15:00.",
    "recipient_type": "passenger"
}
```

##### Response

```json
{
    "message": "Notification sent successfully"
}
```


### 2.7. Reporting Service API

#### Endpoints:

- GET `/reports/{type}`: Generate a report of the specified type (e.g., passenger, docking bay, immigration)

##### Response:

```json
{
  "report_type": "passenger",
  "data": [
    {
      "id": 1,
      "name": "John Doe",
      "age": 30,
      "health_status": "fit",
      "criminal_record": false
    },
    ...
  ]
}
```

### 2.8. Authentication and Authorization Service API


> **POST** `/auth/login`: Authenticate a user and return a token

###### Request
```json
{
    "username": "johndoe",
    "password": "password123"
}
```

###### Response
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
}

```

> **POST** `/auth/register`: Register a new user

###### Request
```json
{
    "username": "johndoe",
    "password": "password123",
    "email": "johndoe@example.com",
    "role": "passenger"
}

```

###### Response
```json
{
    "message": "User registered successfully"
}

```


> **GET** `/auth/me`: Get the authenticated user's details

###### Response
```json
{
    "id": 1,
    "username": "johndoe",
    "email": "johndoe@example.com",
    "role": "passenger"
}

```
> **POST** `/auth/roles`: Create a new role
###### Request
```json
{
    "name": "colony_official"
}

```

###### Response
```json
{
  "message": "Role created successfully"
}

```
> **GET** `/auth/roles`: Get a list of all roles

###### Response
```json
[
  {
    "id": 1,
    "name": "passenger"
  },
  {
    "id": 2,
    "name": "colony_official"
  },
  ...
]

```


### 2.9 Shuttle Service API
- POST `shuttle_schedule`: Adds a new shuttle schedule to the system
- PUT `/shuttle_schedule/{id}`: Updates an existing shuttle schedule
- GET `/shuttle_schedule`: Retrieves a list of all shuttle schedules
- GET `/shuttle_schedule{id}`: Retrieves a specific shuttle schedule by its ID
- DELETE `/shuttle_schedule/{id}`: Deletes a specific shuttle schedule by its ID

#### Requests:

- POST /shuttle_schedule
```json
{
    "shuttle_id": 1,
    "departure_time": "2023-04-01T14:30:00Z",
    "arrival_time": "2023-04-01T16:00:00Z",
    "origin": "Quaid",
    "destination": "Lincoln Colony"
}

```
- PUT /shuttle_schedule/{id}
```json
{
    "shuttle_id": 1,
    "departure_time": "2023-04-01T14:30:00Z",
    "arrival_time": "2023-04-01T16:00:00Z",
    "origin": "Hauser",
    "destination": "Bharatha Colony"
}
```
#### Responses:

- GET /shuttle_schedule

```json
[  {    "id": 1,    
        "shuttle_id": 1,    
        "departure_time": "2023-04-01T14:30:00Z",    
        "arrival_time": "2023-04-01T16:00:00Z",    
        "origin": "Hauser",    
        "destination": "Dostoyevsky Colony"  
    },  
...
]

```
- GET /shuttle_schedule/{id}

```json
{
    "id": 1,
    "shuttle_id": 1,
    "departure_time": "2023-04-01T14:30:00Z",
    "arrival_time": "2023-04-01T16:00:00Z",
    "origin": "Orbital Station",
    "destination": "Mars Colony"
}






```

```json

```

```json

```
```json

```
```json

```
```json

```
```json

```
```json

```
```json

```
```json

```
```json

```
```json

```
