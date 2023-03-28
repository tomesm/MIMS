# Data Entities

## 1. Passenger
This entity represents a person traveling to or from Mars. It stores information required for immigration procedures, guidance through the orbital station, and boarding information.


##### Attributes:
```yaml
- passenger_id (UUID): Unique identifier for the passenger
- name (String): Full name of the passenger
- birth_date (Date): Date of birth
- citizenship (String): Country of citizenship
- visa_type (String): Type of visa issued (6, 12, 18, or 24 months)
- visa_expiry_date (Date): Expiration date of the visa
- destination_colony (String): Colony where the passenger is traveling
- arrival_time (DateTime): Time of arrival at the orbital station
- departure_time (DateTime): Time of departure from the orbital station
- gate_number (Integer): Gate number for boarding the spacecraft
- health_status (String): Diagnosis of the passenger (if any)
```

## 2. ImmigrationOfficer
This entity represents an immigration officer working at the orbital station. It stores information required for processing passengers and handling special cases.

Attributes:
- officer_id (UUID): Unique identifier for the immigration officer
- name (String): Full name of the immigration officer
- station_id (UUID): The ID of the station where the officer works

## 3. Spaceline
This entity represents a company providing transportation to and from Mars. It stores information about the company, their spacecraft, and schedules.

Attributes:
- spaceline_id (UUID): Unique identifier for the spaceline
- name (String): Name of the spaceline company
- spacecraft_capacity (Integer): Passenger capacity of the spacecraft (300, 500, or 800)
- spacecraft_count (Integer): Number of spacecraft owned by the company

## 4. Colony
This entity represents a Mars colony. It stores information about the colony, such as location, population, and resources.

Attributes:
- colony_id (UUID): Unique identifier for the colony
- name (String): Name of the colony
- location (String): Location of the colony on Mars
- current_population (Integer): Current number of inhabitants
- max_population (Integer): Maximum number of inhabitants the colony can support

## 5. OrbitalStation
This entity represents an orbital station, either Quaid or Hauser. It stores information about the station, such as capacity, docking bays, and immigration counters.

Attributes:
- station_id (UUID): Unique identifier for the orbital station
- name (String): Name of the orbital station (Quaid or Hauser)
- max_capacity (Integer): Maximum number of concurrent passengers (1500)
- docking_bays (Integer): Number of docking bays for transport ships (6)
- immigration_counters (Integer): Number of immigration counters (100)

## 6. Flight
This entity represents a flight between Earth and Mars or between Mars colonies. It stores information about the flight, such as departure and arrival times, and docking bay assignments.

Attributes:
- flight_id (UUID): Unique identifier for the flight
- spaceline_id (UUID): The ID of the spaceline operating the flight
- origin (String): Departure location (Earth or colony name)
- destination (String): Arrival location (colony name or Earth)
- departure_time (DateTime): Time of departure
- arrival_time (DateTime): Time of arrival
- docking_bay (Integer): Docking bay number assigned to the spacecraft


## ERD

```css
[Passenger] 1----* [ImmigrationRecord] 1----* [Visa] *----1 [Colony]
                     |                          |
                     +----1 [ImmigrationOfficer] |
                                                 |
[SpacelineDispatcher] 1----* [Spacecraft] *----1 [DockingBay]
                             |
                             +----* [PassengerSpacecraft]

```
In this diagram, rectangles represent entities, while lines represent relationships between entities. The numbers "1" and "" indicate the cardinality of the relationships. For example, "1----" means one-to-many, and "*"----1 means many-to-one.

Here's a brief explanation of the relationships:

Each Passenger has one ImmigrationRecord. An ImmigrationRecord can belong to only one Passenger (1:1).
Each ImmigrationRecord has one Visa. A Visa can belong to only one ImmigrationRecord (1:1).
Each Visa is associated with one Colony. A Colony can have multiple Visas (1:*).
Each ImmigrationRecord is processed by one ImmigrationOfficer. An ImmigrationOfficer can process multiple ImmigrationRecords (1:*).
Each SpacelineDispatcher manages multiple Spacecraft. A Spacecraft can belong to only one SpacelineDispatcher (1:*).
Each Spacecraft has one DockingBay. A DockingBay can have multiple Spacecraft (1:*).
Each Spacecraft has multiple PassengerSpacecraft records, representing the passengers on the spacecraft. A PassengerSpacecraft record belongs to only one Spacecraft (*:1).