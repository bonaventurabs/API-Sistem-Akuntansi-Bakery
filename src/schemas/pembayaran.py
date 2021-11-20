from typing import Optional

from pydantic import BaseModel


# Shared properties
class PembayaranBase(BaseModel):
    amount: Optional[int] = None


# Properties to receive on pembayaran creation
class PembayaranCreate(PembayaranBase):
    amount: int


# Properties to receive on pembayaran update
class PembayaranUpdate(PembayaranBase):
    amount: int


# Properties shared by models stored in DB
class PembayaranInDBBase(BaseModel):
    paymentid: str = "PY00000"
    orderid: str = "OR00000"
    amount: int
    change: int

    class Config:
        orm_mode = True


# Properties to return to client
class Pembayaran(PembayaranInDBBase):
    pass


# Properties properties stored in DB
class PembayaranInDB(PembayaranInDBBase):
    pass