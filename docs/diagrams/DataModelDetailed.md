erDiagram

    Passenger{
        int id
        string first_name
        string last_name
        int age
        string criminal_record
        string health_status
        string colony
        string skills
        string specialization
        string status
        int visa_id
        int user_id
        string flight_code
        string ticket_number
    }

    Spaceline {
        int id
        string name
    }

    Spacecraft {
        int id(pk)
        string name
        int capacity
        int spaceline_id
    }

    Colony {
        int id
        string name
        int inhabitants
    }

    Resource {
        int id
        string name
        int colony_id
        int air
        int lodging
        int food
        int water
    }

    OrbitalStation {
        int id
        string name
        int passenger_capacity

    }

    Flight {
        int id
        string flight_code
        int spaceline_id
        time departure_time
        time arrival_time
        str origin
        str destination
        int spacecraft_id
        int shuttle_id
    }

    Shuttle {
        int id
        int capacity
        time departure_time
        time arrival_time
        int shuttle_bay_id
        string colony
        id flight_id
    }

    ImmigrationCounter {
        int id
        int officer_id
        string status
        int station_id
    }

    Visa {
        int id
        int duration
        time issue_date
        int immigration_counter_id
        int colony_id
    }

    Role {
        int id
        int user_id
        string name
        string[] permissions

    }

    Permission {
        int id
        string name
        string description
    }

    User {
        int id
        string name
        string email
        secret password
        string[] roles

    }

    DockingBay {
        int id
        string status
        int spacecraft_id
        int orbital_station_id
    }

    ShuttleBay {
        int id
        string status
        int shuttle_id
        int orbital_station_id
    }

    ImmigrationRule {
        int id
        int colony_id
        string rule_type
        string description
    }

    Resource {
        string name
        int air
        int food
        int lodging
        int water
        int limit_id
    }

    Limit {
        type name
        int air
        int food
        int lodging
        int water
    }

    Passenger }|--|| Flight : has
    Passenger ||--|| Visa : has
    Flight }|--|| Spaceline : operated_by
    Flight ||--|| Spacecraft : uses
    Flight ||--|{ Shuttle : associated_with
    Shuttle ||--|| ShuttleBay : docked_at
    Spacecraft ||--|| DockingBay : docked_at
    Spacecraft }|--|| Spaceline : belongs_to
    Spaceline ||--|{ DockingBay : reserves
    Colony ||--o{ ImmigrationRule : has
    OrbitalStation ||--|{ ShuttleBay : has
    OrbitalStation ||--|{ DockingBay : has
    OrbitalStation ||--|{ ImmigrationCounter : has
    Visa }o--|| Colony : valid_for
    Role ||--|{ Permission : has
    User ||--|{ Role : has
    User }o--|| ImmigrationCounter : can_be_assigned_to
    User ||--|| Passenger: can_be
    Colony ||--|| Resource: has
    Resource ||--|| Limit: has
    