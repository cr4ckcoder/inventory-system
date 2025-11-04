from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import products, inventory, users, transfers, webhooks, analytics, categories
from app.db.session import engine, Base
import logging

logger = logging.getLogger("uvicorn.error")

app = FastAPI(title="CIS API - Full")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://frontend:3000",  # container name for internal Docker use
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routers
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])
app.include_router(transfers.router, prefix="/transfers", tags=["Transfers"])
app.include_router(webhooks.router, prefix="/webhooks", tags=["Webhooks"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])

@app.on_event("startup")
async def on_startup():
    # For development convenience: create tables if they don't exist.
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables ensured (create_all).")

@app.get('/')
def root():
    return {"message":"CIS API running"}
