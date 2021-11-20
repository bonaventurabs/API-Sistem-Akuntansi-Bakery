from typing import TYPE_CHECKING

from typing import ItemsView
from sqlalchemy.sql.expression import null
from sqlalchemy import Table, Column,  DateTime, ForeignKey, Integer, String ,Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from src.database import Base

if TYPE_CHECKING:
    from .produk import Produk
    from .pembayaran import Pembayaran


class Pesanan(Base):
    __tablename__ = "pesanan"

    orderid = Column(String(12), primary_key=True)
    datetime = Column(DateTime, server_default=func.now())
    paymentstatus = Column(Boolean, nullable=False, default=False)

    products = relationship("ItemPesanan", back_populates="order", cascade="all, delete, delete-orphan")
    payment = relationship("Pembayaran", back_populates="order",uselist=False, cascade="all, delete, delete-orphan")
    # items = relationship('Produk', secondary = 'ItemPesanan')
    # orderPayment = relationship("Pembayaran", back_populates="Pesanan")


class ItemPesanan(Base):
    __tablename__ = "itempesanan"

    productid = Column(String(12), ForeignKey('produk.productid'), primary_key=True)
    orderid = Column(String(12), ForeignKey('pesanan.orderid'), primary_key=True)
    amount = Column(Integer, nullable=False)
    order = relationship("Pesanan", back_populates="products")
    product = relationship("Produk", back_populates="orders")