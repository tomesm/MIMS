sequenceDiagram
    participant P as Passenger
    participant PS as ProvisioningSystem
    participant PM as PassengerManagementService
    participant IS as ImmigrationService
    participant CS as ColonyService

    PS->>PM: Provision passengers data
    PM->>IS: Notify about new passengers
    IS->>PM: Request new passenger data
    PM-->>IS: Provide new passenger data
    IS-->CS: Request latest colony rules
    CS-->IS: Provide latest colony rules
    IS->>IS: Evaluate for visa eligibility
    alt Passenger is eligible for automatic visa
        IS->>CS: Request resources for passenger
        alt Resources granted
            CS-->>IS: Grant resources
            IS-->>PM: Update passenger (status: eligible_for_visa)
        else Resources not granted
            CS-->>IS: Deny resources
            IS->>PM: Update passenger (status: not_eligible_for_visa)
        end
    else Passenger is flagged
        IS->>PM: Update passenger (flagged)
    end