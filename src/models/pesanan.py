from typing import TYPE_CHECKING

from typing import ItemsView
from sqlalchemy.sql.expression import null
from sqlalchemy import Table, Column,  DateTime, ForeignKey, Integer, String ,Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from src.database import Base

if TYPE_CHECKING:
    from .produk import Produk

class Pesanan(Base):
    __tablename__ = "Pesanan"

    orderId = Column(String(12), primary_key=True)
    dateTime = Column(DateTime(timezone=True), server_default=func.now())
    paymentStatus = Column(Boolean, nullable=False, default=False)

    items = relationship("Produk", secondary = "ItemPesanan", back_populates="orders")
    # items = relationship('Produk', secondary = 'ItemPesanan')
    # orderPayment = relationship("Pembayaran", back_populates="Pesanan")


class ItemPesanan(Base):
    __tablename__ = "ItemPesanan"

    productId = Column(String(12), ForeignKey('Produk.productId'), primary_key=True)
    orderId = Column(String(12), ForeignKey('Pesanan.orderId'), primary_key=True)
    amount = Column(Integer, nullable=False)


# ItemPesanan = Table('ItemPesanan',
#     Column('productid', String(12), ForeignKey('Produk.productid'), primary_key=True),
#     Column('orderid', String(12), ForeignKey('Pesanan.orderid'), primary_key=True),
#     Column('amount', nullable=False))