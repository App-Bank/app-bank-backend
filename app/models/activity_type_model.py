from sqlalchemy import CheckConstraint, Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class ActivityType(Base):

    __tablename__ = "activity_types"
    
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    name = Column(String, CheckConstraint("name IN ('Debit', 'Credit')"), nullable=False, index=True)

    activities = relationship("Activity", back_populates="activity_types")