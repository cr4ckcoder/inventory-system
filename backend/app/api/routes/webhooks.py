from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.products import ProductVariant
from app.db.models.inventory import Inventory, InventoryLog
from app.services.webhook_service import publish_event
import asyncio

router = APIRouter()

class SaleItem(BaseModel):
    variant_id: UUID
    location_id: UUID
    quantity: int

class OnlineSale(BaseModel):
    sale_id: str
    items: List[SaleItem]
    source: str = "online"

@router.post("/online-sale")
async def online_sale(payload: OnlineSale, db: Session = Depends(get_db)):
    # process sale: decrement inventory for each item
    processed = []
    for it in payload.items:
        inv = db.query(Inventory).filter(Inventory.variant_id==it.variant_id, Inventory.location_id==it.location_id).first()
        if not inv:
            # try to find location of type 'Online' or fail
            raise HTTPException(status_code=404, detail=f"Inventory for variant {it.variant_id} at location {it.location_id} not found")
        inv.quantity_on_hand -= it.quantity
        log = InventoryLog(variant_id=it.variant_id, location_id=it.location_id, quantity_change=-it.quantity, transaction_type="OnlineSale", reference_id=None)
        db.add(inv); db.add(log)
        processed.append({"variant_id": str(it.variant_id), "new_on_hand": inv.quantity_on_hand})
    db.commit()
    # publish event to queue (non-blocking)
    try:
        asyncio.create_task(publish_event("inventory.sale", {"sale_id": payload.sale_id, "items":[{"variant_id": str(i.variant_id), "quantity": i.quantity} for i in payload.items]}))
    except Exception:
        pass
    return {"processed": processed}
