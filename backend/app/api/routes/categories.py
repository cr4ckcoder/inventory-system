from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.products import Category
from app.api.schemas.products import CategoryIn, CategoryOut

router = APIRouter()

@router.get("/", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

@router.post("/", response_model=CategoryOut)
def create_category(payload: CategoryIn, db: Session = Depends(get_db)):
    existing = db.query(Category).filter_by(category_name=payload.category_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")

    category = Category(category_name=payload.category_name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category
