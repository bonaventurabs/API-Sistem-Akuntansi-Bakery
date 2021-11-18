from sqlalchemy.sql.expression import null
from sqlalchemy import Column,  DateTime, ForeignKey, Integer, String ,Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from src.database import Base


class Pembayaran(Base):
    __tablename__ = "Pembayaran"

    paymentId = Column(String(12), primary_key=True)
    orderId = Column(String(12), ForeignKey("order.orderId"), nullable=False)
    amount = Column(Integer, nullable=False)
    change = Column(Integer, nullable=False)

    order = relationship("Pesanan")
    # order = relationship("Pesanan", back_populates="Pembayaran")


