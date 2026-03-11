from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "products"

    barcode = Column(String, primary_key=True)
    product_name = Column(String)
    brand = Column(String)
    cached_at = Column(DateTime)

class ScanEvent(Base):
    __tablename__ = "scan_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String)
    barcode = Column(String, nullable=False)
    action = Column(String, nullable=False)
    timestamp = Column(DateTime)
    source = Column(String)