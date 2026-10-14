from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Activity(Base):
    __tablename__ = "activity"

    id = Column(Integer,primary_key=True, index=True,autoincrement=True)
    amount = Column(Numeric(9,2),nullable=True,index=True)
    succeeded_in = Column(DateTime,nullable=True,index=True)
    transfer_id = Column(Integer, ForeignKey("transfers.id"),nullable=True)
    account_id = Column(Integer, ForeignKey("accounts.id"),nullable=True)
    activity_type_id = Column(String, ForeignKey("activity_types.id"),nullable=True)
    timezone_id = Column(String, ForeignKey("timezones.id"),nullable=True)

    transfer = relationship("Transfer", back_populates="activities")
    account = relationship("Account", back_populates="activities")
    activity_types = relationship("ActivityType", back_populates="activities")
    timezone = relationship("Timezone", back_populates="activities")