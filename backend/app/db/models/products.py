from sqlalchemy import Column, String, Text, ForeignKey, DECIMAL, Boolean, JSON, TIMESTAMP, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.db.session import Base

class Category(Base):
    __tablename__ = "categories"
    category_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_name = Column(String(100), nullable=False)

class Product(Base):
    __tablename__ = "products"
    product_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    style_name = Column(String(255), nullable=False)
    brand = Column(String(100))
    description = Column(Text)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.category_id"))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

class ProductVariant(Base):
    __tablename__ = "product_variants"
    variant_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.product_id"))
    sku = Column(String(100), unique=True, nullable=False)
    ean = Column(String(50), unique=True)
    upc = Column(String(50), unique=True)
    attributes = Column(JSON)
    cost_price = Column(DECIMAL(10,2))
    selling_price = Column(DECIMAL(10,2))
    is_active = Column(Boolean, default=True)

class ProductBundleComponent(Base):
    __tablename__ = "product_bundle_components"
    bundle_component_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bundle_variant_id = Column(UUID(as_uuid=True), ForeignKey("product_variants.variant_id"))
    component_variant_id = Column(UUID(as_uuid=True), ForeignKey("product_variants.variant_id"))
    quantity = Column(Integer, nullable=False, default=1)
