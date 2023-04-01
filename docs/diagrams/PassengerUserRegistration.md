sequenceDiagram
    participant P as Passenger
    participant AP as Application Portal
    participant PMS as PassengerManagementService
    participant UMS as UserManagementService
    participant DB as Database

    P->>AP: Register (Passenger information)
    AP->>PMS: Create user
    PMS-->>DB: Get passenger
    DB->>PMS: Passenger (Passenger ID)
    PMS->>UMS: Create User (Passenger ID, credentials)
    UMS->>PMS: User created
    PMS-->>AP: User created
    AP->>P: Registration successful
    