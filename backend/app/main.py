from fastapi import FastAPI
from app.api.routes import products, inventory, users, transfers, webhooks, analytics
from app.db.session import engine, Base
import logging

logger = logging.getLogger("uvicorn.error")

app = FastAPI(title="CIS API - Full")

# include routers
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])
app.include_router(transfers.router, prefix="/transfers", tags=["Transfers"])
app.include_router(webhooks.router, prefix="/webhooks", tags=["Webhooks"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])

@app.on_event("startup")
async def on_startup():
    # For development convenience: create tables if they don't exist.
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables ensured (create_all).")

@app.get('/')
def root():
    return {"message":"CIS API running"}
