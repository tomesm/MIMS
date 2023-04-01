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
    IS->>IS: Evaluate for automatic visa granting
    alt Passenger is eligible for automatic visa
        IS->>CS: Request resources for passenger
        alt Resources granted
            CS-->>IS: Grant resources
            IS->>IS: Approve visa
            IS->>CS: Sent visa request
            CS-->>IS: Visa issued confirmation (visa_id)
            IS-->>PM: Update passenger (visa_id, status: visa_granted)
            
        else Resources not granted
            CS-->>IS: Deny resources
            IS->>PM: Update passenger (visa denied)
            
        end
    else Passenger is flagged
        IS->>PM: Update passenger (flagged)
    end