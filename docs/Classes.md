# Interfaces

Below are the abstract classes representing the interfaces for different system actors.

## 1. PassengerInterface

```python
from abc import ABC, abstractmethod

class PassengerInterface(ABC):
    @abstractmethod
    def get_immigration_guidance(self):
        """
        Get guidance on the immigration procedures, such as required documents and where to find an available immigration officer.
        
        :return: A string with guidance information.
        """

    @abstractmethod
    def get_flight_gate_information(self):
        """
        Get information about the flight gate for the destination colony.
        
        :return: An integer representing the gate number.
        """

    @abstractmethod
    def get_boarding_status(self):
        """
        Get information about the boarding status of the spacecraft.
        
        :return: A string with the boarding status.
        """
```
## 2. ImmigrationOfficerInterface

```python
from abc import ABC, abstractmethod

class ImmigrationOfficerInterface(ABC):
    @abstractmethod
    def process_passenger(self, passenger):
        """
        Process a passenger, including checking their identification, health, and criminal record.
        
        :param passenger: Passenger instance.
        :return: A boolean indicating whether the passenger has been processed successfully.
        """

    @abstractmethod
    def handle_special_cases(self, passenger):
        """
        Handle passengers that require special attention from the immigration officer.
        
        :param passenger: Passenger instance.
        :return: A boolean indicating whether the special case has been resolved.
        """
```

## 3. SpacelineDispatcherInterface

```python
from abc import ABC, abstractmethod

class SpacelineDispatcherInterface(ABC):
    @abstractmethod
    def request_docking_bay_assignment(self, flight):
        """
        Request a docking bay assignment for a specific flight.
        
        :param flight: Flight instance.
        :return: An integer representing the assigned docking bay.
        """

    @abstractmethod
    def get_available_docking_bays(self):
        """
        Get information about the available docking bays and time slots for arrival, departure, and maintenance.
        
        :return: A list of dictionaries containing docking bay information.
        """

    @abstractmethod
    def handle_denied_passengers(self, flight):
        """
        Handle passengers who are not allowed to enter Mars colonies and are returning to Earth.
        
        :param flight: Flight instance.
        :return: A list of Passenger instances that are denied entry.
        """
```

## 4. ColonyOfficialInterface

```python
from abc import ABC, abstractmethod

class ColonyOfficialInterface(ABC):
    @abstractmethod
    def confirm_resources(self, passenger):
        """
        Confirm that resources are available for the arriving passenger to avoid overcrowding.
        
        :param passenger: Passenger instance.
        :return: A boolean indicating whether resources are available.
        """

    @abstractmethod
    def get_population_forecast(self):
        """
        Get the forecast of planned arrivals in the coming months and years to plan colony population growth.

        :return: A dictionary containing the forecast of planned arrivals.
        """
```

## 4. ColonyOfficialInterface

```python
from abc import ABC, abstractmethod

class ColonyOfficialInterface(ABC):
    @abstractmethod
    def confirm_resources(self, passenger):
        """
        Confirm that resources are available for the arriving passenger to avoid overcrowding.
        
        :param passenger: Passenger instance.
        :return: A boolean indicating whether resources are available.
        """

    @abstractmethod
    def get_population_forecast(self):
        """
        Get the forecast of planned arrivals in the coming months and years to plan colony
```


## 5. StationManagerInterface

```python
from abc import ABC, abstractmethod

class StationManagerInterface(ABC):
    @abstractmethod
    def get_operational_metrics(self):
        """
        Get crucial metrics of the station operations, such as average visa processing time, percentage of station passenger capacity used, and forecast of passenger capacity for 6 months.

        :return: A dictionary containing the operational metrics.
        """

    @abstractmethod
    def get_spacecraft_schedule(self):
        """
        Get the schedule of spacecraft arrivals and departures to plan dock bay maintenance.

        :return: A list of dictionaries containing spacecraft arrival and departure information.
        """
