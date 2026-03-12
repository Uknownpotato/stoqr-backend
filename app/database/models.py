from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
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

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime)

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    api_key = Column(String, nullable=False, unique=True)
    name = Column(String)
    created_at = Column(DateTime)