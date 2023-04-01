sequenceDiagram
    participant User
    participant RegistrationPortal 
    participant RoleManagement 
    participant UserManagement 
    participant EmailService 

    User->>RegistrationPortal: Enter personal information and desired role
    RegistrationPortal->>RoleManagement: Validate role and permissions
    RoleManagement-->>RegistrationPortal: Role validation results
    RegistrationPortal->>UserManagement: Create user with provided information and role
    UserManagement->>EmailService: Send registration confirmation email
    UserManagement-->>RegistrationPortal: User creation successful
    EmailService-->>UserManagement: Confirmation email sent
    RegistrationPortal-->>User: Registration successful, confirmation email sent
