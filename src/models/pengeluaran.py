from sqlalchemy.sql.expression import null
from sqlalchemy import Column,  DateTime, ForeignKey, Integer, String ,Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKeyConstraint

from src.database import Base


class Pengeluaran(Base):
    __tablename__ = "Pengeluaran"

    expenseId = Column(String(12), primary_key=True)
    dateTime = Column(DateTime(timezone=True), server_default=func.now())

    items = relationship("ItemPengeluaran", backref="Pengeluaran")

class ItemPengeluaran(Base):
    __tablename__ = "ItemPengeluaran"

    itemId = Column(String(12), primary_key=True)
    expenseId = Column(String(12), ForeignKey("expense.expenseId"), nullable=False)
    nama = Column(String(100), nullable=False)
    harga = Column(Integer, nullable=False)

    expense = relationship("Pengeluaran")
    
    # owner_id = Column(Integer, ForeignKey("user.id"))
    # owner = relationship("User", back_populates="items")

    # time_created = Column(DateTime(timezone=True), server_default=func.now())
    # time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    # author_id = Column(Integer, ForeignKey("author.id"))

    # author = relationship("Author")
