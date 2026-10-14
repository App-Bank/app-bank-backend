from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, func
from app.core.database import Base


class Transfer(Base):
    __tablename__ = "transfers"

    id = Column(Integer, primary_key=True, index=True)
    sender_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False, index=True)
    recipient_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False, index=True)
    amount = Column(Numeric(15, 2), nullable=False)
    concept = Column(String(200), nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())