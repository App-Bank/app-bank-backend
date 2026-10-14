from sqlalchemy import CheckConstraint, Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class ActivityType(Base):

    __tablename__ = "activities_types"
    
    id = Column(Integer,primary_key=True, index=True,autoincrement=True)
    name = Column(String,CheckConstraint("name IN ('Debit', 'Credit')"),nullable=False,index=True)

    activity = relationship("Activity", back_populates="activity_type")