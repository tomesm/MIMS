
%% visa application %%
sequenceDiagram
    participant P as Passenger
    %% participant PS as PassengerService
    participant IC as ImmigrationCounter
    participant IS as ImmigrationService

    participant IO as ImmigrationOfficer
    participant SB as ShuttleBay
    participant PS as PassengerService

    P->>IC: Check in
    IC-->>PS: Provide passenger data
    PS-->>IC: Passenger
    IC-->>IC: Check for passenger status
    alt Visa granted
        IC-->>P: You may go
        P-->>SB: Proceed to the shuttle bay
    else Passenger flagged
        IC-->>IC: Manual check

        alt Visa Granted
            IC-->>P: You may go
            P-->>SB: Proceed to the shuttle bay

        else Not granted
            IC-->>P: I am sorry
        
        end


    end
