from sqlalchemy import Column, Integer, Numeric, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    iban = Column(String(34), index=True, nullable=False, unique=True)
    balance = Column(Numeric(9, 2), nullable=False)

    user = relationship(
        "User",
        back_populates="account"
    )
    transfers_sent = relationship(
        "Transfer",
        foreign_keys="Transfer.sender_account_id",
        back_populates="sender_accounts"
    )
    transfers_received = relationship(
        "Transfer",
        foreign_keys="Transfer.recipient_account_id",
        back_populates="recipient_accounts"
    )
    activities = relationship(
        "Activity",
        back_populates="accounts"
    )