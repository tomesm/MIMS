
%% visa application %%
sequenceDiagram
    participant P as Passenger
    participant PS as PassengerService
    participant VAP as VisaApplicationPortal
    participant IO as ImmigrationOfficer
    participant SB as ShuttleBay
    participant CS as ColonyService

    P->>VAP: Click on "Apply" button 
    VAP->>PS: Request status of the passenger
    PS-->>VAP: Return passenger information
    VAP-->>VAP: Evaluate the eligibility
    alt Passenger eligible for visa
        VAP-->>P: Provide guidance to Immigration Counter and Shuttle Bay
        P-->>IO: Officer just checks ID/passport and let the passenger through.
        P-->>SB: Proceed to the shuttlebay based on giuadence
        else Flagged
            VAP-->>P: Provide guidance to the Immigration Counter
            IO-->>IO: Manualy checks eligibility
            alt Eligible
                IO-->CS: Ask for resource assignment
                CS-->>CS: Check resource avalability
                alt Resources granted
                    IO-->>PS: Update passengers status. Assign visa id
                    IO-->>P: Visa approved. Gudance to shuttle bay provided.
                else Resources not granted


                end

            end
    end