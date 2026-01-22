from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func
from app.src.db import Base

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String, index=True)
    loan_amount = Column(Float)
    loan_term = Column(Integer)
    status = Column(String, default="ACTIVE")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
