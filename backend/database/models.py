# backend/database/models.py

from sqlalchemy import Column, Integer, String, Float, DateTime, func, Boolean
from database.connection import Base

class ConversionHistory(Base):
    __tablename__ = "conversion_history"

    id               = Column(Integer, primary_key=True, index=True)
    from_currency    = Column(String(3), nullable=False)
    to_currency      = Column(String(3), nullable=False)
    amount           = Column(Float, nullable=False)
    converted_amount = Column(Float, nullable=False)
    rate             = Column(Float, nullable=False)
    created_at       = Column(DateTime, server_default=func.now())


class User(Base):
    __tablename__ = "users"

    id            = Column(Integer, primary_key=True, index=True)
    username      = Column(String, unique=True, index=True, nullable=False)
    email         = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)   # NEVER store plain passwords
    is_active     = Column(Boolean, default=True)
    created_at    = Column(DateTime, server_default=func.now())