from sqlalchemy.sql.expression import null
from sqlalchemy import Column,  DateTime, ForeignKey, Integer, String ,Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKeyConstraint

from src.database import Base


class Pengeluaran(Base):
    __tablename__ = "pengeluaran"

    expenseid = Column(String(12), primary_key=True)
    datetime = Column(DateTime, server_default=func.now())

    items = relationship("ItemPengeluaran", back_populates="expense", cascade="all, delete, delete-orphan")

class ItemPengeluaran(Base):
    __tablename__ = "itempengeluaran"

    itemid = Column(String(12), primary_key=True)
    expenseid = Column(String(12), ForeignKey("pengeluaran.expenseid"), nullable=False)
    nama = Column(String(100), nullable=False)
    harga = Column(Integer, nullable=False)

    expense = relationship("Pengeluaran", back_populates="items")