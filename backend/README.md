This backend is a development-ready CIS API.

Features:
- SQLAlchemy models for products, variants, bundles, inventory, transfers, users.
- JWT auth (register/login)
- Webhook endpoint for online sales
- CSV upload for offline sales (inventory adjustments)
- publish_event() to RabbitMQ (aio-pika) - best-effort

Development convenience:
- On startup the app will run Base.metadata.create_all(engine) to create tables automatically.
- For production, replace create_all with Alembic migrations.

Run with docker-compose from project root.
