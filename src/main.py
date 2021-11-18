from datetime import datetime, timedelta
from os import error, name
from typing import Optional, List

from fastapi import FastAPI, HTTPException, status, Depends, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, oauth2
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from src import models, schemas
from .database import get_db

# from .schemas import CreateJobRequest
# from .models import Job

# from schema import Token, User, Item, TokenData
# from auth import UserHandler

app = FastAPI() 

# Read Base Path
@app.get('/')
async def root(request: Request):
    url_list = [
        {"path": route.path, "name": route.name} for route in request.app.routes
    ]
    return {
        "API": "Sistem Akutansi Bakery API",
        "Path List": url_list
    }

# Request token c
@app.post("/login", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    pass

def set_table_id(prefix: str, prev_id: str):
    if prev_id is None:
        id = 0
    else:
        id = int(prev_id[-5:])
    id+=1
    id = prefix+str(id).zfill(5)
    return id

##Product
# Add Product
@app.post('/products',response_model=schemas.Produk, tags=['product']) 
async def create_product(new_produk: schemas.ProdukCreate, db: Session = Depends(get_db)): 
    db_produk = db.query(models.Produk).filter(models.Produk.productname==new_produk.productname).first()
    if db_produk is not None:
        raise HTTPException(status_code=400,detail="Produk already exists")
    try:
        db_produk_id = db.query(func.max(models.Produk.productid)).scalar()
    except:
        db_produk_id = None
    db_produk_id = set_table_id("PR", db_produk_id)
    db_new_produk = models.Produk(
        productid=db_produk_id, 
        productname=new_produk.productname,
        price=new_produk.price
    )
    db.add(db_new_produk)
    db.commit()
    return db_new_produk

# Read All Products
@app.get('/products',response_model=List[schemas.Produk], tags=['product']) 
async def get_all_products(db: Session = Depends(get_db)): 
    all_produk = db.query(models.Produk).all()
    return all_produk

# Read Spesific Product
@app.get('/products/{productId}',response_model=schemas.Produk , tags=['product']) 
async def get_product(productId: str, db: Session = Depends(get_db)): 
    spesific_produk = db.query(models.Produk).filter(models.Produk.productid == productId).first()
    if spesific_produk is None:
        raise HTTPException(status_code=404, detail="Produk not found")
    return spesific_produk

# Update Specific Product
@app.put('/products/{productId}',response_model=schemas.Produk, tags=['product']) 
async def update_product(productId: str, update_produk: schemas.ProdukUpdate, db: Session = Depends(get_db)):
    produk = db.query(models.Produk).filter(models.Produk.productid == productId).first()
    if produk is None:
        raise HTTPException(status_code=404, detail="Produk not found")
    produk_exist = db.query(models.Produk).filter(models.Produk.productname==update_produk.productname).first()
    if produk_exist is not None:
        raise HTTPException(status_code=400,detail="Produk already exists")

    obj_produk = jsonable_encoder(produk)
    update_produk_dict = update_produk.dict(exclude_unset=True)
    for field in obj_produk:
        if field in update_produk_dict:
            setattr(produk, field, update_produk_dict[field])
    db.add(produk)
    db.commit()
    db.refresh(produk)
    return produk

#Delete Spesific Product
@app.delete('/products/{productId}',response_model=schemas.Produk, tags=['product']) 
async def delete_product(productId: str, db: Session = Depends(get_db)):
    produk = db.query(models.Produk).filter(models.Produk.productid == productId).first()
    if produk is None:
        raise HTTPException(status_code=404, detail="Produk not found")

    db.delete(produk)
    db.commit()
    return produk

##Order
# Add New Order
@app.post('/orders', tags=['order']) 
async def create_order(): 
    pass

# Read All Orders
@app.get('/orders', tags=['order']) 
async def get_all_orders(): 
    pass

# Read Spesific Order
@app.get('/orders/{orderId}', tags=['order']) 
async def get_order(orderId: str): 
    pass

# Update Specific Order
@app.put('/orders/{orderId}', tags=['order']) 
async def update_order(orderId: str):
    pass

#Delete Spesific Order
@app.delete('/orders/{orderId}', tags=['order']) 
async def delete_order(orderId: str):
    pass

##Payment
# Add New Payment
@app.post('/orders/{orderId}/pay', tags=['payment']) 
async def create_payment(): 
    pass

# Read Spesific Payment
@app.get('/orders/{orderId}/pay', tags=['payment']) 
async def get_payment(orderId: str): 
    pass

# Update Specific Payment
@app.put('/orders/{orderId}/pay', tags=['payment']) 
async def update_payment(orderId: str):
    pass

#Delete Spesific Payment
@app.delete('/orders/{orderId}/pay', tags=['payment']) 
async def delete_payment(orderId: str):
    pass

##Expense
# Add New Expense
@app.post('/expenses', tags=['expense']) 
async def create_expense(): 
    pass

# Read All Expenses
@app.get('/expenses', tags=['expense']) 
async def get_all_expenses(): 
    pass

# Read Spesific Expense
@app.get('/expenses/{expenseId}', tags=['expense']) 
async def get_expense(expenseId: str): 
    pass

# Update Specific Expense
@app.put('/expenses/{expenseId}', tags=['expense']) 
async def update_expense(expenseId: str):
    pass

#Delete Spesific Expense
@app.delete('/expenses/{expenseId}', tags=['expense']) 
async def delete_expense(expenseId: str):
    pass

##Invoice
# Get Invoice
@app.get('/orders/{orderId}/invoice', tags=['invoice']) 
async def get_invoice(orderId: str): 
    pass

##Report
# Get Report
@app.get('/reports?from={startDateTime}&to={endDateTime}', tags=['report']) 
async def create_expense(startDateTime: datetime, endDateTime: datetime): 
    pass