from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
import csv, io
from app.db.session import get_db
from app.db.models.inventory import Inventory, InventoryLog
from app.db.models.products import ProductVariant

router = APIRouter()

class InventoryIn(BaseModel):
    variant_id: UUID
    location_id: UUID
    quantity_on_hand: int = 0
    quantity_committed: int = 0

@router.post("/", response_model=dict)
def create_inventory(payload: InventoryIn, db: Session = Depends(get_db)):
    inv = Inventory(variant_id=payload.variant_id, location_id=payload.location_id, quantity_on_hand=payload.quantity_on_hand, quantity_committed=payload.quantity_committed)
    db.add(inv)
    db.commit()
    db.refresh(inv)
    return {"inventory_id": str(inv.inventory_id)}

@router.post("/adjust", response_model=dict)
def adjust_inventory(variant_id: UUID, location_id: UUID, change: int, transaction_type: str, db: Session = Depends(get_db)):
    inv = db.query(Inventory).filter(Inventory.variant_id==variant_id, Inventory.location_id==location_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    inv.quantity_on_hand = inv.quantity_on_hand + change
    db.add(inv)
    log = InventoryLog(variant_id=variant_id, location_id=location_id, quantity_change=change, transaction_type=transaction_type)
    db.add(log)
    db.commit()
    return {"inventory_id": str(inv.inventory_id), "new_on_hand": inv.quantity_on_hand}

# CSV upload endpoint for offline sales
# Expected CSV columns: sku,location_id,quantity
@router.post("/upload-sales")
async def upload_sales(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    s = contents.decode('utf-8')
    reader = csv.DictReader(io.StringIO(s))
    results = {"processed":0, "errors":[]}
    for i,row in enumerate(reader, start=1):
        try:
            sku = row.get('sku') or row.get('SKU')
            loc = row.get('location_id')
            qty = int(row.get('quantity') or 0)
            if not sku or not loc:
                results['errors'].append({"row": i, "error":"missing sku or location_id"})
                continue
            pv = db.query(ProductVariant).filter(ProductVariant.sku==sku).first()
            if not pv:
                results['errors'].append({"row": i, "error":"variant not found: "+sku})
                continue
            inv = db.query(Inventory).filter(Inventory.variant_id==pv.variant_id, Inventory.location_id==loc).first()
            if not inv:
                results['errors'].append({"row": i, "error":"inventory record not found for sku at location"})
                continue
            inv.quantity_on_hand -= qty
            log = InventoryLog(variant_id=pv.variant_id, location_id=loc, quantity_change=-qty, transaction_type="OfflineSaleCSV")
            db.add(inv); db.add(log); db.commit()
            results['processed'] += 1
        except Exception as e:
            results['errors'].append({"row": i, "error": str(e)})
    return results
