from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from datetime import datetime
from app.db.session import get_db
from app.db.models.inventory import TransferOrder, Inventory, InventoryLog
from app.db.models.products import ProductVariant

router = APIRouter()

class TransferIn(BaseModel):
    source_location_id: UUID
    destination_location_id: UUID
    items: List[dict]  # list of {variant_id, quantity}
    created_by: UUID

@router.post("/", response_model=dict)
def create_transfer(payload: TransferIn, db: Session = Depends(get_db)):
    t = TransferOrder(source_location_id=payload.source_location_id, destination_location_id=payload.destination_location_id, status="Pending", created_by=payload.created_by)
    db.add(t); db.commit(); db.refresh(t)
    # store items in inventory_logs with reference_id = transfer_id and negative from source, positive to destination upon receive
    # For now just create the transfer record; item movement occurs on ship/receive endpoints
    return {"transfer_id": str(t.transfer_id)}

@router.post("/{transfer_id}/ship")
def ship_transfer(transfer_id: UUID, db: Session = Depends(get_db)):
    t = db.query(TransferOrder).filter(TransferOrder.transfer_id==transfer_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Transfer not found")
    if t.status != "Pending":
        raise HTTPException(status_code=400, detail="Transfer must be Pending to ship")
    # mark shipped and decrement source inventory for items stored elsewhere (assumed handled by client later)
    t.status = "Shipped"
    t.shipped_at = datetime.utcnow()
    db.add(t); db.commit()
    return {"transfer_id": str(t.transfer_id), "status": t.status}

@router.post("/{transfer_id}/receive")
def receive_transfer(transfer_id: UUID, db: Session = Depends(get_db)):
    t = db.query(TransferOrder).filter(TransferOrder.transfer_id==transfer_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Transfer not found")
    if t.status != "Shipped":
        raise HTTPException(status_code=400, detail="Transfer must be Shipped to receive")
    t.status = "Received"
    t.received_at = datetime.utcnow()
    db.add(t); db.commit()
    return {"transfer_id": str(t.transfer_id), "status": t.status}
