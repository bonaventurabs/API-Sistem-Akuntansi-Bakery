from typing import Optional

from pydantic import BaseModel


# Shared properties
class ProdukBase(BaseModel):
    productname: Optional[str] = None
    price: Optional[int] = None


# Properties to receive on produk creation
class ProdukCreate(ProdukBase):
    productname: str
    price: int


# Properties to receive on produk update
class ProdukUpdate(ProdukBase):
    pass


# Properties shared by models stored in DB
class ProdukInDBBase(BaseModel):
    productid: str
    productname: str
    price: int

    class Config:
        orm_mode = True


# Properties to return to client
class Produk(ProdukInDBBase):
    pass


# Properties properties stored in DB
class ProdukInDB(ProdukInDBBase):
    pass