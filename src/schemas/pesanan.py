from typing import Optional,List

from pydantic import BaseModel
from datetime import date, datetime 

from src.schemas.produk import ProdukBase, ProdukInDBBase
from src.schemas.pembayaran import PembayaranBase, PembayaranInDBBase


class ItemPesananBase(BaseModel):
    productid: Optional[str] = None
    amount: Optional[int] = None

class ItemPesananCreate(ItemPesananBase):
    productid: str = "PR00000"
    amount: int

class ItemPesananUpdate(ItemPesananBase):
    pass

class ItemPesanan(ItemPesananBase):
    productid: str = "PR00000"
    amount: int
    orderid: str = "OR00000"


# Shared properties
class PesananBase(BaseModel):
    paymentstatus: Optional[bool] = False


# Properties to receive on pesanan creation
class PesananCreate(PesananBase):
    itempesanan: List[ItemPesananCreate] 


# Properties to receive on pesanan update
class PesananUpdate(PesananBase):
    itempesanan: Optional[List[ItemPesananUpdate]]


# Properties shared by models stored in DB
class PesananInDBBase(PesananBase):
    orderid: str = "OR00000"
    datetime: datetime
    paymentstatus: bool

    class Config:
        orm_mode = True


# Properties to return to client
class Pesanan(PesananInDBBase):
    itempesanan: List[ItemPesanan] = []
    totalprice: int = 0


# Properties properties stored in DB
class PesananInDB(PesananInDBBase):
    pass