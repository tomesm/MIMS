sequenceDiagram

    participant PS as ProvisioningSystem
    participant PM as PassengerManagementService
    participant IS as ImmigrationService
    participant CS as ColonyService

    PS->>PM: Provision passengers data
    PM->>IS: Notify about new passengers
    IS->>PM: Request new passenger data
    PM-->>IS: Provide new passenger data
    IS-->>CS: Request latest colony rules
    CS-->>IS: Provide latest colony rules
    IS->>IS: Evaluate for visa eligibility
    alt Passenger is eligible for automatic visa pre-approval
        IS-->>CS: Ask for resources
        alt Resources granted
            CS-->>IS: Granted given number of months.
            IS-->>PM: Update passenger. Status: pre-approved: num_of_months

        end
    else Passenger is flagged
        IS->>PM: Update passenger (flagged)
    end