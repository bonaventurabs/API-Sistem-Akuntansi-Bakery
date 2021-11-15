from typing import Optional,List

from pydantic import BaseModel
from datetime import datetime

from src.schemas.produk import ProdukBase, ProdukInDBBase


class ItemPesanan(BaseModel):
    produk: ProdukBase
    amount: int


class ItemPesananinDB(BaseModel):
    produk: ProdukInDBBase
    orderId: str
    amount: int


# Shared properties
class PesananBase(BaseModel):
    datetime: datetime.now()
    paymentStatus: Optional[bool] = False
    itemPesanan: List[ItemPesanan]


# Properties to receive on pesanan creation
class PesananCreate(PesananBase):
    pass


# Properties to receive on pesanan update
class PesananUpdate(PesananBase):
    pass


# Properties shared by models stored in DB
class PesananInDBBase(PesananBase):
    orderId: str
    datetime: datetime
    paymentStatus: bool
    itemPesanan: List[ItemPesananinDB]

    class Config:
        orm_mode = True


# Properties to return to client
class Pesanan(PesananInDBBase):
    pass


# Properties properties stored in DB
class PesananInDB(PesananInDBBase):
    pass