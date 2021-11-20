from typing import Optional,List

from pydantic import BaseModel
from datetime import datetime

class ItemProduk(BaseModel):
    productid: str = "PR00000"
    quantity: int
    price: int
    total: int

class Invoice(BaseModel):
    datetime: datetime
    orderid: str = "OR00000"
    paymentid: str = "PY00000"
    itempesanan: List[ItemProduk] = []
    totalprice: int = 0
    amount: int = 0
    change: int = 0

    class Config:
        orm_mode = True