
%% visa application %%
sequenceDiagram
    participant P as Passenger
    %% participant PS as PassengerService
    participant VAP as VisaApplicationPortal
    participant IS as ImmigrationService
    participant CS as ColonyService
    participant PS as PassengerService

    P->>VAP: Click on "Apply" button. Specify type of visa in months
    %% VAP->>PS: Request status of the passenger
    %% PS-->>VAP: Return passenger information
    VAP-->>PS: Get passenger
    PS-->>VAP: Passenger
    VAP-->>VAP: Check if pre-approved
    alt Passenger pre-approved
        VAP-->>VAP: Compare number of requested months with pre-approved months
        alt Grant resources
            VAP-->>P: Green to go. Provide guidance to Immigration Counter and Shuttle bay
        else Not granted
            VAP-->>PS: Flag
            VAP-->>P: You are flagged. Proceed for manual check.
        end
        
    else Flagged
        VAP-->>P: Provide guidance to an immigration counter

    else Visa denied
        VAP-->P: I am sorry
    end
