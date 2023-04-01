erDiagram
    Passenger }|--|| Flight : has
    Passenger ||--|| Visa : has
    Flight }|--|| Spaceline : operated_by
    Flight ||--|| Spacecraft : uses
    Flight ||--|{ Shuttle : associated_with
    Shuttle ||--|| Shuttlebay : docked_at
    Spacecraft ||--|| DockingBay : docked_at
    Spacecraft }|--|| Spaceline : belongs_to
    Spaceline ||--|{ DockingBay : reserves
    Colony ||--o{ ImmigrationRules : has
    OrbitalStation ||--|{ Shuttlebay : has
    OrbitalStation ||--|{ DockingBay : has
    OrbitalStation ||--|{ ImmigrationCounter : has
    Visa }o--|| Colony : valid_for
    Role ||--|{ Permission : has
    User ||--|{ Role : has
    User }o--|| ImmigrationCounter : assigned_to

