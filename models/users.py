from db.database import Base
from sqlalchemy import String, Column, Integer, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=True, default="user")
    time_created = Column(TIMESTAMP, nullable=False, server_default=func.now())

    #user establishes relationship to the Expense model and back populates to this attribute expense
    expenses = relationship(argument="Expense", back_populates="user")