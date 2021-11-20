from typing import TYPE_CHECKING

from sqlalchemy.sql.expression import null
from sqlalchemy import Column,  DateTime, ForeignKey, Integer, String ,Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .pesanan import Pesanan
from src.database import Base

if TYPE_CHECKING:
    from .pesanan import Pesanan

class Pembayaran(Base):
    __tablename__ = "pembayaran"

    paymentid = Column(String(12), primary_key=True)
    orderid = Column(String(12), ForeignKey("pesanan.orderid"), nullable=False)
    amount = Column(Integer, nullable=False)
    change = Column(Integer, nullable=False)

    order = relationship("Pesanan", back_populates="payment")
    # order = relationship("Pesanan", back_populates="Pembayaran")


