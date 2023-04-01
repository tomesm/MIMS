sequenceDiagram
    participant P as Passenger
    participant DB as Database
    participant VAP as VisaApplicationPortal
    participant UM as UserManagement
    participant RM as RoleManagement

    P->>VAP: Enter ticket number
    VAP->>DB: Retrieve passenger information using ticket number
    DB-->>VAP: Return passenger information
    VAP->>P: Display passenger information
    P->>VAP: Confirm information and create account
    VAP->>UM: Register user with passenger information
    UM->>DB: Save user information
    DB-->>UM: Confirm user information saved
    UM->>RM: Assign "Passenger" role to user
    RM->>DB: Update user role
    DB-->>RM: Confirm user role updated
    RM-->>UM: Role assigned successfully
    UM->>VAP: User registration successful
    VAP->>P: Display success message and prompt login
