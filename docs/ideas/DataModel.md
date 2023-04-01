## Passenger
Represents a passenger. It stores information required for immigration procedures, guidance through the orbital station, and boarding information.

Attributes:
- id: Unique identifier for the passenger
- name: Full name of the passenger
- ticketNumber: Unique ticket number for their journey
- healthCheck: Health check results for the passenger
- criminalRecord: Criminal record information for the passenger
- visa: Associated visa information for the passenger
- specialization: Job or skill the passenger posses (eg. IT, surgeon, etc)
- flightNumber: Number of flight.


Functions:
- requestGuidance(): Retrieve guidance for the passenger's journey through the orbital station

## Spaceline
This entity represents a company providing transportation to and from Mars. It stores information about the company, their spacecraft, and schedules. RESERVES a DOCKING bay.

Attributes:
- id: Unique identifier for the spaceline
- name: Name of the spaceline

Functions:
- requestDockingBayAssignment(flight: Flight): Request a docking bay assignment for a specific flight
- receiveDockingBayInfo(dockingBay: DockingBay): Receive information on available docking bays and time slots
- receiveNotAllowedPassengers(passengers: List[Passenger]): Receive information on passengers not allowed to enter Mars colonies and travelling back to Earth
- getSchedules(): Receive information about planned arrivals and departures of spaceline's spacecrafts.

## Spacecraft
Represents the spacecraft belonging to a Spaceline, including its passenger capacity.

Attributes:
- id: Unique identifier for the spacecraft
- name: Name of the spacecraft
- capacity: Number of passengers the spacecraft can carry
- spacelineId: Spaceline id

## Colony
This entity represents a Mars colony, with details about the number of inhabitants, resources, and immigration rules.

Attributes:
- id: Unique identifier for the colony
- name: Name of the colony
- inhabitants: Number of current inhabitants in the colony

Functions:
- confirmResourcesForPassenger(passenger: Passenger): Confirm resources for an arriving passenger
- getPlannedArrivals(): Retrieve the number of planned arrivals for the coming months and years

## ColonyResource
This entity represents resources avaliable for the colony

Attributes:
- id: Unique identifier for the colony
- name: Name of the resource
- colony_id: ID of the colony
- available_air: available air in m3
- available_lodging: available lodging in number of places 
- available_food: availabe food in kilograms


## OrbitalStation
This entity represents an orbital station, either Quaid or Hauser. The station is responsible for 
managing passenger processing, visa controls, and processing times.

Attributes:
- id: Unique identifier for the orbital station
- name: Name of the orbital station
- passengerCapacity: Maximum number of concurrent passengers the station can handle

Functions:
- getAverageVisaProcessingTime(): Calculate the average visa processing time
- getCurrentPassengerCapacityPercentage(): Calculate the percentage of station passenger capacity currently used
- getPassengerCapacityForecast(): Retrieve the forecast of passenger capacity for the next 6 months
- getSpacecraftSchedule(): Retrieve the schedule of spacecraft arrivals and departures

## Flight
This entity represents a flight between Earth and Mars or between Mars colonies. It includes details about the departure and arrival times, the Spaceline, and the spacecraft.

Attributes
- flightId: Unique identifier for the flight.
- spaceLineID: Spaceline id
- departureTime: The scheduled departure time of the flight.
- arrivalTime: The scheduled arrival time of the flight.
- origin: The location where the flight departs from (Earth or a Mars colony).
- destination: The location where the flight arrives (a Mars colony or Earth).
- spacecraft: The spacecraft used for the flight.
- shuttle: Shuttle assigned for this flight
- passengers: List of passengers

Functions
- getFlightDetails(): Retrieves flight details such as departure and arrival times, origin, destination, Spaceline, and spacecraft.
- updateFlightSchedule(newDepartureTime, newArrivalTime): Updates the flight's departure and arrival times.
- assignSpacecraft(spacecraft): Assigns a spacecraft to the flight.
- removeSpacecraft(): Removes the spacecraft assignment from the flight.

## Shuttle
This entity represents a small transport ship used to transport passengers from the orbital station to their destination colony on Mars or vice versa. 

Attributes
- shuttleId: Unique identifier for the shuttle.
- capacity: The maximum number of passengers the shuttle can carry.
- departureTime: The scheduled departure time of the shuttle.
- arrivalTime: The scheduled arrival time of the shuttle.
- associatedFlight: The flight that the shuttle is associated with.
- shuttle_bay_number: Shuttle bay number for docking.  

Functions
- getShuttleDetails(): Retrieves shuttle details such as capacity, departure and arrival times.
- updateShuttleSchedule(newDepartureTime, newArrivalTime): Updates the shuttle's departure and arrival times.
- addFlightAssociation(flight): Associates a flight with the shuttle.
- removeFlightAssociation(): Removes the flight association from the shuttle.



## ImmigrationCounter
This entity represents an immigration counter at the orbital station, responsible for visa control and processing of passengers.

Attributes:
- id: Unique identifier for the immigration counter
- officerId: The ID of the immigration officer assigned to the counter
- status: The current status of the counter (e.g., open, closed, occupied)
- orbital_station_id

Functions:
- processPassenger(passenger: Passenger): Processes a passenger's visa application and updates their status
- assignOfficer(officer: ImmigrationOfficer): Assigns an immigration officer to the counter
- unassignOfficer(): Removes the assigned immigration officer from the counter


## Visa
This entity represents a temporary visa issued for passengers traveling to Mars colonies, with details about 
the duration and the colony for which it is valid.

Attributes:
- id: Unique identifier for the visa
- duration: Duration of the visa in Mars months
- colony: The Mars colony for which the visa is valid
- issued_by: ImmigrationCounter id
- time_of_issue: Timestamp

## Role
This entity represents the different roles or actors within the system. 
It defines the specific permissions and access levels granted to each user based on their role. 
Roles can include Passenger, Immigration Officer, Spaceline Dispatcher, Colony Official, and Station Manager. 
Each role has a distinct set of responsibilities and allowed actions within the system.

Attributes:
- id: Unique identifier for the role
- user_id: Identifier of the user with this permission
- name: Name of the role
- permissions: List of system permissions associated with the role


Functions:
- addUserToRole(user: User): Add a user to the role
- removeUserFromRole(user: User): Remove a user from the role

## SystemPermission
This entity represents the specific actions or operations that a user with a certain role is allowed to perform within the system. 
Permissions are associated with roles, and users with a specific role inherit the permissions assigned to that role. 
Examples of permissions can include creating, updating, or deleting records, accessing certain features 
or functionalities, and managing specific parts of the system.

Attributes:

id: Unique identifier for the permission
name: Name of the permission
description: Description of the permission

## User
This entity represents a user of the system, with associated personal information and a role. Each user can have one or more roles, which determine their permissions and allowed actions within the system.

Attributes:
- id: Unique identifier for the user
- name: Full name of the user
- email: Email address of the user
- password: Hashed password for the user
- roles: List of roles assigned to the user

Functions:
- authenticate(email, password): Authenticate the user based on the provided email and password
- getRoles(): Retrieve the roles assigned to the user
- addRole(role: Role): Assign a role to the user
- removeRole(role: Role): Remove a role from the user
- hasPermission(permission: Permission): Check if the user has the specified permission based on their assigned roles

## DockingBay
This entity represents a docking bay at the orbital station where spacecraft can dock and undock. It includes details about its current status and associated spacecraft.

Attributes:

- id: Unique identifier for the docking bay
- status: The current status of the docking bay (e.g., available, occupied, under maintenance)
- spacecraft: The spacecraft currently docked at the docking bay (if any)
- orbital_station_id


Functions:
- updateStatus(newStatus): Update the status of the docking bay
- assignSpacecraft(spacecraft: Spacecraft): Assign a spacecraft to the docking bay
- unassignSpacecraft(): Remove the spacecraft assignment from the docking bay

## Shuttlebay
This entity represents a shuttle bay at the orbital station or a Mars colony where shuttles can dock and undock. It includes details about its current status and associated shuttle.

Attributes:

- id: Unique identifier for the shuttle bay
- status: The current status of the shuttle bay (e.g., available, occupied, under maintenance)
- shuttle: The shuttle currently docked at the shuttle bay (if any)
- orbital_station_id

Functions:
- updateStatus(newStatus): Update the status of the shuttle bay
- assignShuttle(shuttle: Shuttle): Assign a shuttle to the shuttle bay
- unassignShuttle(): Remove the shuttle assignment from the shuttle bay

## ImmigrationRule
Represents a rule or requirement for immigration to a Mars colony. These rules are used to determine if a passenger is eligible for automatic visa granting or if they need to go through manual visa processing at an immigration counter.

Attributes:
- id: Unique identifier for the immigration rule
- colonyId: The ID of the Mars colony the rule is associated with
- ruleType: The type of the rule (e.g., health, criminal record, specialization)
- ruleDescription: A description of the rule

Functions:
- checkPassengerEligibility(passenger: Passenger): Check if a passenger fulfills the rule
- addRuleToColony(colony: Colony): Add the rule to a Mars colony
- removeRuleFromColony(colony: Colony): Remove the rule from a Mars colony
