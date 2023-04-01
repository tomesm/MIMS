classDiagram
    class PassengerManagementService
    class ImmigrationService
    class DockingBayManagementService
    class ColonyService
    class OrbitalStationManagerService
    class ShuttleBayManagementService
    class UserManagementService
    class SpacelineManagementMicroservice
    class FlightManagementService

    ImmigrationService -- ColonyService
    ImmigrationService -- UserManagementService
    ImmigrationService -- PassengerManagementService
    DockingBayManagementService -- SpacelineManagementMicroservice
    OrbitalStationManagerService -- ImmigrationService
    OrbitalStationManagerService -- DockingBayManagementService
    OrbitalStationManagerService -- FlightManagementService
    ShuttleBayManagementService -- FlightManagementService
    SpacelineManagementMicroservice -- FlightManagementService
    PassengerManagementService -- ColonyService
