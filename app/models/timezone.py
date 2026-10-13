from sqlalchemy import Column, Integer, String
from app.core.database import Base


class Timezone(Base):
    __tablename__ = "timezones"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    offset = Column(String(10), nullable=False)