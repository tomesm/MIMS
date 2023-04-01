sequenceDiagram
    participant SM as SpacelineManager
    participant SMM as SpacelineManagementMicroservice
    participant DBMS as DockingBayManagementService
    participant FM as FlightManagementService

    SM->>SMM: Request docking bay assignment (Spacecraft, arrival time)
    SMM->>DBMS: Check docking bay availability (arrival time)
    DBMS->>SMM: Available docking bays
    SMM->>FM: Create flight (Spacecraft, arrival time, docking bay)
    FM->>SMM: Flight created
    SMM->>SM: Docking bay assigned (docking bay, arrival time)

    Note over SM, FM: Spacecraft arrives and docks

    SM->>SMM: Request departure slot (Spacecraft, departure time)
    SMM->>DBMS: Check docking bay availability (departure time)
    DBMS->>SMM: Available departure slots
    SMM->>FM: Create new flight (Spacecraft, departure time, docking bay)
    FM->>SMM: Flight created
    SMM->>SM: Departure slot assigned (departure time)

    Note over SM, FM: Spacecraft departs
