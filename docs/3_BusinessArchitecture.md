# 3. Business Architecture

In this section, we will outline the business architecture of the Mars immigration system, focusing on the key business processes, organizational structure, and actors involved in the system.

A role-based access control system (RBAC) can be a good idea for managing permissions and access to resources in a software application. It allows you to define roles with specific permissions, and then assign these roles to users. This makes it easier to manage user access and maintain security.

In your case, the User and Passenger entities can be related as follows:

User: This entity represents the actual person who logs into the system. A User can have different roles (e.g., passenger, immigration officer, station manager, etc.) that determine their access to different parts of the system. Users can have multiple roles, depending on their responsibilities.

Passenger: This entity represents a traveler who is registered in the system and is associated with a specific User. The Passenger entity contains information about the individual, such as their name, age, health status, and other personal details.

To implement a role-based system, you can create a separate entity called Role, which defines the various roles and their associated permissions in your system. Each User can then be associated with one or more Roles, depending on their responsibilities.

The relationship between User and Passenger can be implemented in different ways, depending on your specific requirements. For instance:

You could create a one-to-one relationship between User and Passenger, where each User can only be associated with a single Passenger. This might be suitable if each person using the system can only ever be a passenger themselves.
Alternatively, you could create a one-to-many relationship between User and Passenger, where a single User can be associated with multiple Passengers. This might be appropriate if a User is responsible for managing multiple passengers, such as a travel agent or a family member booking on behalf of their relatives.
By implementing a role-based system, you can ensure that each User has access only to the appropriate resources and functionalities within the system, based on their assigned roles. This helps maintain security and enables you to manage user access more effectively.

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
- **Station dispatcher**: Coordinates with a colony the shuttle traffic from station to colony and vice versa.



