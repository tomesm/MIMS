sequenceDiagram
    participant PS as PassengerService
    participant IC as InformationCounter
    participant CS as ColonyService


   
    PS-->>IC: Hey officer!
    IC-->>CS: Give me passengers colony rules
    CS-->>IC: Here you go
    IC-->>IC: Check if passenger is eligible
    alt Eligible
        IC-->>CS: Pre-approve resources
        alt Resoruces granted
            CS-->>IC: We can spare N months
            IC-->>PS: Passenger is pre-approved for N months
        else Not granted
            IC-->>PS: Passenger is updated: visa_not granted
        end

    else Not eligible
        IC-->>PS: Update passanger with status flagged

    end
    