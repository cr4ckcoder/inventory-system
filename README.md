# Inventory System - Dockerized Scaffold

This scaffold contains a minimal backend (FastAPI) and frontend (Next.js) setup, plus PostgreSQL and RabbitMQ
configured via docker-compose.

Quick start:
1. Copy or move this folder to your machine.
2. From the project root, run:
   docker-compose up --build

Services:
- backend: http://localhost:8000
- frontend: http://localhost:3000
- postgres: port 5432
- rabbitmq management UI: http://localhost:15672 (guest/guest)

Next steps:
- Replace in-memory lists with SQLAlchemy models and run Alembic migrations.
- Implement authentication (JWT) and RBAC logic.
- Add webhook worker (aio-pika / Celery) for async deliveries.
- Add SSL reverse proxy (nginx) for production.
