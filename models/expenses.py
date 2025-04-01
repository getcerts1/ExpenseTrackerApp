from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db.database import Base

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category = Column(String, index=True)
    description = Column(String, nullable=True)
    amount = Column(Float, nullable=False)
    time_created = Column(TIMESTAMP, nullable=False, server_default=func.now())


    user = relationship("User", back_populates="expenses")
