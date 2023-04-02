# 3. Business Architecture

In this section, we will outline the business architecture of the Mars immigration system, focusing on the key business processes, organizational structure, and actors involved in the system.

A role-based access control system (RBAC) will be used for this system. It allows to define roles with specific permissions, and then assign these roles to users. This makes it easier to manage user access and maintain security.


## 3.1 Business Processes

The primary business processes of the Mars immigration system include:

1. **Passenger Registration**: Passengers arriving at the Mars station register using the web or mobile application.

2. **Visa Application**: Registered passengers apply for a temporary visa based on the available options (6, 12, 18, or 24 Mars months).

3. **Visa Approval**: Immigration officers review and process visa applications, approving or denying them based on the colony's immigration rules.

4. **Resource Allocation**: Colony officials allocate and distribute resources, such as power, water, and supplies, to new visitors.

5. **Station Operations**: The station manager oversees the smooth functioning of the station's facilities, infrastructure, and systems.

6. **Spacecraft and Shuttle Operations** Dispatchers are responsible for smooth assigning docking bays.

## 3.2 Roles

The Mars immigration system's organizational structure consists of the following roles:

- **Passenger**: Individuals arriving at the Mars station who need to register and apply for a visa. Uses the web or mobile application to register and apply for a visa.
- **Immigration Officer**: Responsible for reviewing and processing visa applications.
- **Station Manager**: Manages and oversees the operations of the Mars station.
- **Colony Official**: Sets immigration rules and regulations for the colony.
- **Spaceline Dispatcher**: Coordinates with the Mars station regarding passenger arrivals and departures.
- **Station Dispatcher**: Coordinates with a colony the shuttle traffic from station to colony and vice versa.
- **SystemAdministrator**: Poweruser/maintainer of the system.



