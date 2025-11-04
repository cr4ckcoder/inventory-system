from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.db.session import Base

class Location(Base):
    __tablename__ = "locations"
    location_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    location_name = Column(String(100), nullable=False)
    location_type = Column(String(50))
    address = Column(String)

class Inventory(Base):
    __tablename__ = "inventory"
    inventory_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    variant_id = Column(UUID(as_uuid=True), ForeignKey("product_variants.variant_id"))
    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.location_id"))
    quantity_on_hand = Column(Integer, default=0, nullable=False)
    quantity_committed = Column(Integer, default=0, nullable=False)
    reorder_point = Column(Integer)
    safety_stock = Column(Integer)

class InventoryLog(Base):
    __tablename__ = "inventory_logs"
    log_id = Column(Integer, primary_key=True, autoincrement=True)
    variant_id = Column(UUID(as_uuid=True), ForeignKey("product_variants.variant_id"))
    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.location_id"))
    quantity_change = Column(Integer, nullable=False)
    transaction_type = Column(String(50))
    reference_id = Column(UUID(as_uuid=True))
    user_id = Column(UUID(as_uuid=True))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

class TransferOrder(Base):
    __tablename__ = "transfer_orders"
    transfer_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_location_id = Column(UUID(as_uuid=True), ForeignKey("locations.location_id"))
    destination_location_id = Column(UUID(as_uuid=True), ForeignKey("locations.location_id"))
    status = Column(String(50), default="Pending")
    created_by = Column(UUID(as_uuid=True))
    shipped_at = Column(TIMESTAMP)
    received_at = Column(TIMESTAMP)
