from sqlalchemy.sql.expression import null
from sqlalchemy import Column,  DateTime, ForeignKey, Integer, String ,Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from src.database import Base


class Produk(Base):
    __tablename__ = "Produk"

    productId = Column(String(12), primary_key=True)
    productName = Column(String(50), nullable=False)
    price = Column(Integer, nullable=False)

    orders = relationship('Pesanan', secondary = 'ItemPesanan')