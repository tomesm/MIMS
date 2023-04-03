# 5. Technology Architecture

In this section, we will define the technology stack and infrastructure components that will be used to build, deploy, and maintain the Mars immigration system.

## 5.1 Technology Stack

The following technology stack will be used to develop the Mars immigration system:

- **Programming Language**: Go/Rust
- **API Framework**: net/http(golang)/Actix(Rust)
- **Frontend**: React.js (web) and  React Native (mobile)
- **Database**: CockroachDB (distributed SQL database)
- **Orchestration & Deployment**: Kubernetes
- **Infrastructure**: Local Mars station Kubernetes cluster. IaC will be used (terraform, ansible).
- **Monitoring**: Grafana, Consul, Prometheus
- **Security**: SUSE Rancher for container security

- **Local 5G Network**: A local 5G network provided within the Mars station to enable seamless communication between passengers, immigration officers, station managers, spaceline dispatchers, and colony officials.


## 5.2 Technology Considerations

- The use of Kubernetes allows for easy scaling and management of the system components, ensuring high availability and fault tolerance.

- The local Kubernetes cluster within the Mars station provides low-latency access to the system, reducing reliance on Earth-based services and ensuring smooth operation even during communication delays or outages.

- CockroachDB provides a distributed SQL database that meets the requirements for data consistency, survivability, and scalability, while also allowing for easy integration with the Python-based backend.

- The local 5G network ensures high-speed communication between all system actors, supporting real-time interactions and data access.
