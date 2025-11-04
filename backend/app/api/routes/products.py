from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.products import Product, ProductVariant, ProductBundleComponent

router = APIRouter()

class VariantIn(BaseModel):
    sku: str
    attributes: Optional[dict] = None
    cost_price: Optional[float] = None
    selling_price: Optional[float] = None
    is_active: Optional[bool] = True

class ProductIn(BaseModel):
    style_name: str
    brand: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[UUID] = None
    variants: Optional[List[VariantIn]] = []

@router.post("/", response_model=dict)
def create_product(payload: ProductIn, db: Session = Depends(get_db)):
    p = Product(style_name=payload.style_name, brand=payload.brand, description=payload.description, category_id=payload.category_id)
    db.add(p)
    db.commit()
    db.refresh(p)
    created_variants = []
    for v in payload.variants or []:
        pv = ProductVariant(product_id=p.product_id, sku=v.sku, attributes=v.attributes, cost_price=v.cost_price, selling_price=v.selling_price, is_active=v.is_active)
        db.add(pv)
        db.commit()
        db.refresh(pv)
        created_variants.append({'variant_id': str(pv.variant_id), 'sku': pv.sku})
    return {"product_id": str(p.product_id), "variants": created_variants}

@router.get("/", response_model=List[dict])
def list_products(db: Session = Depends(get_db)):
    prods = db.query(Product).all()
    out = []
    for p in prods:
        variants = db.query(ProductVariant).filter(ProductVariant.product_id==p.product_id).all()
        out.append({"product_id": str(p.product_id), "style_name": p.style_name, "variants":[{"variant_id": str(v.variant_id), "sku": v.sku} for v in variants]})
    return out

# Bundle creation: create a bundle variant and components
class BundleComponent(BaseModel):
    component_variant_id: UUID
    quantity: int

class BundleIn(BaseModel):
    product_id: UUID
    sku: str
    components: List[BundleComponent]

@router.post("/bundles", response_model=dict)
def create_bundle(payload: BundleIn, db: Session = Depends(get_db)):
    # create bundle variant
    bv = ProductVariant(product_id=payload.product_id, sku=payload.sku, is_active=True)
    db.add(bv)
    db.commit()
    db.refresh(bv)
    for c in payload.components:
        comp = ProductBundleComponent(bundle_variant_id=bv.variant_id, component_variant_id=c.component_variant_id, quantity=c.quantity)
        db.add(comp)
    db.commit()
    return {"bundle_variant_id": str(bv.variant_id), "sku": bv.sku}
