from typing import Optional,List

from pydantic import BaseModel
from datetime import datetime


class ItemPengeluaran(BaseModel):
    nama: str
    harga: int


class ItemPengeluaraninDB(BaseModel):
    itemId: str
    expenseId: str
    nama: str
    harga: int


# Shared properties
class PengeluaranBase(BaseModel):
    datetime: datetime.now()
    itemPengeluaran: List[ItemPengeluaran]


# Properties to receive on Pengeluaran creation
class PengeluaranCreate(PengeluaranBase):
    pass


# Properties to receive on Pengeluaran update
class PengeluaranUpdate(PengeluaranBase):
    pass


# Properties shared by models stored in DB
class PengeluaranInDBBase(PengeluaranBase):
    expenseId: str
    datetime: datetime
    itemPengeluaran: List[ItemPengeluaraninDB]

    class Config:
        orm_mode = True


# Properties to return to client
class Pengeluaran(PengeluaranInDBBase):
    pass


# Properties properties stored in DB
class PengeluaranInDB(PengeluaranInDBBase):
    pass