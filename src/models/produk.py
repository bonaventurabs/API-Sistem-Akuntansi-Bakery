from typing import TYPE_CHECKING

from sqlalchemy.sql.expression import null
from sqlalchemy import Column,  DateTime, ForeignKey, Integer, String ,Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from src.database import Base

# if TYPE_CHECKING:
    # from .pesanan import Pesanan, ItemPesanan

class Produk(Base):
    __tablename__ = "produk"

    productid = Column(String, primary_key=True)
    productname = Column(String, nullable=False)
    price = Column(Integer, nullable=False)

    # orders = relationship("Pesanan", secondary = "ItemPesanan", back_populates="items")
    # orders = relationship('Pesanan', secondary = 'ItemPesanan')

