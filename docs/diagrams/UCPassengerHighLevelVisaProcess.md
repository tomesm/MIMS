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
    alt Eligible for visa
        AP->>P: Notify & provide guidance to shuttle bay
        P->>IO: Pass through immigration counter
        IO-->>IO: Just controls passengers passport or IDs
        P->>ShuttleBay: Proceed to shuttle bay
    else Flagged
        AP->>P: Notify about flag
        P-->>IO: Passenger is guided to an Immigration Officer
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
    else Not eligible for visa 
         AP->>P: Notify not eligible for visa
        
    end
