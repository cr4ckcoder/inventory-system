from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.db.models.inventory import Inventory, Location

router = APIRouter()

@router.get("/stock-summary")
def stock_summary(db: Session = Depends(get_db)):
    total_items = db.query(func.sum(Inventory.quantity_on_hand)).scalar() or 0
    total_locations = db.query(func.count(Location.location_id)).scalar() or 0
    return {"total_items": int(total_items), "total_locations": int(total_locations)}
