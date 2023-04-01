sequenceDiagram
    participant P as Passenger

    participant PM as PassengerManagementService
    participant IS as ImmigrationService
    participant CS as ColonyService
    participant AP as ApplicationPortal
    participant IO as ImmigrationOfficer


    P->>AP: Register 
    AP-->>P: Register succesfull
    P->>AP: Apply for visa
    AP-->>PM: Get passenger
    PM-->>AP: Send  passenger
    AP-->>AP: Checks passenger status
    alt Visa not granted
        
        AP->>P: Notify visa denial
    else Flagged
        AP->>P: Notify about flag
        P-->>IO: Passenger proceeds towards Immigration Officer
        IO->>IO: Manually check passenger status
        alt Visa granted by officer
            IO->>IS: Approve visa
            IS->>CS: Notify visa approval
            CS->>PM: Issue visa & update passenger
            PM->>P: Notify & provide guidance to shuttle bay
        else Visa denied by officer
            IO->>IS: Deny visa
            IS->>PM: Update passenger (visa denied)
            PM->>P: Notify visa denial
        end
    else Visa granted
        AP->>P: Notify & provide guidance to shuttle bay
        P->>IO: Pass through immigration counter
        P->>ShuttleBay: Proceed to shuttle bay
    end
