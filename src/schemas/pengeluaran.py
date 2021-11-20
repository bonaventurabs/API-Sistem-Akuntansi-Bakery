from typing import Optional,List

from pydantic import BaseModel
from datetime import datetime


class ItemPengeluaranBase(BaseModel):
    nama: Optional[str] = None
    harga: Optional[int] = None

class ItemPengeluaranCreate(ItemPengeluaranBase):
    nama: str 
    harga: int

class ItemPengeluaranUpdate(ItemPengeluaranBase):
    pass

class ItemPengeluaran(BaseModel):
    itemid: str = "EI0000"
    expenseid: str = "EX0000"
    nama: str
    harga: int

    class Config:
        orm_mode = True


# Properties to receive on Pengeluaran creation
class PengeluaranCreate(BaseModel):
    itempengeluaran: List[ItemPengeluaranCreate]


# Properties to receive on Pengeluaran update
class PengeluaranUpdate(BaseModel):
    itempengeluaran: List[ItemPengeluaranUpdate]


# Properties shared by models stored in DB
class PengeluaranInDBBase(BaseModel):
    expenseid: str = "EX0000"
    datetime: datetime
    

    class Config:
        orm_mode = True


# Properties to return to client
class Pengeluaran(PengeluaranInDBBase):
    itempengeluaran: List[ItemPengeluaran] = []


# Properties properties stored in DB
class PengeluaranInDB(PengeluaranInDBBase):
    pass