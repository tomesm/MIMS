sequenceDiagram
    participant P as Passenger
    participant PS as PassengerService
    participant VAP as VisaApplicationPortal
    participant UM as UserManagement
    participant DB as Database

    P->>VAP: Enter ticket number
    VAP->>PS: Retrieve passenger information using ticket number
    PS-->>VAP: Return passenger information
    VAP->>UM: Create new user with passenger information
    UM->>UM: Assign "Passenger" role to user
    UM-->DB: Create new user with (role, passenger_id)
    DB-->UM: Confirm save
    UM-->>VAP: Confimrm user creation

