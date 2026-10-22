from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric
from sqlalchemy.orm import relationship

from app.core.database import Base


class Activity(Base):
    __tablename__ = "activity"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    amount = Column(Numeric(9,2), nullable=True, index=True)
    succeeded_in = Column(DateTime, nullable=True, index=True)
    transfer_id = Column(Integer, ForeignKey("transfers.id"), nullable=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    activity_type_id = Column(Integer, ForeignKey("activity_types.id"), nullable=True)

    transfers = relationship("Transfer", back_populates="activities")
    accounts = relationship("Account", back_populates="activities")
    activity_types = relationship("ActivityType", back_populates="activities")