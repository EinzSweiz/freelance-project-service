# 🛠 Project / Job Service — Upwork-style Microservice

This microservice is part of a distributed Upwork-like platform.  
It handles the creation, management, and tracking of freelance job projects (also called "orders").

---

## 🚀 Features

- ✅ **CRUD** for projects (create, read, update, delete)
- 🧾 **PostgreSQL** for persistent storage
- ⚡️ **Redis caching** for active project lists *(optional enhancement)*
- 🛰 **Kafka integration** for event publishing
  - `project_created`
  - `project_updated`
  - `project_deleted`
- 🔌 **gRPC support** for inter-service communication
  - `GetProjectById`
- ✅ **JWT Auth Middleware**
- 📦 Docker & Docker Compose support

---

## 📁 Folder Structure

```
├── app/
│ ├── domain/ # Entities & abstract repositories
│ ├── infrastructure/
│ │ ├── db/ # SQLAlchemy models and repositories
│ │ ├── kafka/ # Kafka producer
│ │ ├── grpc/ # gRPC service handler
│ ├── presentation/
│ │ ├── http/ # FastAPI REST routes
│ │ ├── grpc/ # gRPC server entry
│ ├── services/ # Business logic
│ └── main.py # FastAPI app
├── migrations/ # Alembic migrations
├── docker-compose.yaml
├── Dockerfile
├── README.md

```

## 🧪 Tech Stack

| Component        | Technology          |
|------------------|---------------------|
| Language         | Python 3.11         |
| Web Framework    | FastAPI             |
| DB               | PostgreSQL          |
| Async ORM        | SQLAlchemy + asyncpg|
| Broker           | Kafka               |
| gRPC             | grpcio + protobuf   |
| Auth             | JWT                 |
| DevOps           | Docker, Docker Compose |
| Logging          | Custom logger       |

---

⚙️ Environment Variables

DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/projects_db
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
JWT_SECRET=your_jwt_secret_key

---

🧰 Usage

# Run REST service
make build
make up
make logs

This uses the Makefile for running the project from the parent directory.

# Run gRPC server
python app/presentation/grpc/run_grpc.py

# Apply database migrations
alembic upgrade head

📬 gRPC Interface

Defined in project.proto:

service ProjectService {
  rpc GetProjectById(ProjectIdRequest) returns (ProjectResponse);
}

📊 Kafka Event Example

{
  "project_id": "uuid",
  "client_id": "uuid",
  "title": "Build a Website",
  "timestamp": "2025-01-01T12:00:00Z"
}

🔒 Authorization

All HTTP endpoints require a valid JWT token:

Authorization: Bearer <access_token>

📈 Next Goals

Add Redis caching for listing active projects

Add search & filtering options

Add test coverage and CI/CD pipeline
