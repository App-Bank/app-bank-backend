from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, index=True, nullable=False, unique=True)
    password = Column(String, index=True, nullable=False)

    account = relationship("Account", back_populates="user", uselist=False)