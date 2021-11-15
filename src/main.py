import json
from datetime import datetime, timedelta
from typing import Optional

from fastapi import FastAPI, HTTPException, status, Depends, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, oauth2

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

# Request token 
@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    pass

##Product
# Add Product
@app.post('/products', tags=['product']) 
async def create_product(): 
    pass

# Read All Products
@app.get('/products', tags=['product']) 
async def get_all_products(): 
    pass

# Read Spesific Product
@app.get('/products/{productId}', tags=['product']) 
async def get_product(productId: str): 
    pass

# Update Specific Product
@app.put('/products/{productId}', tags=['product']) 
async def update_product(productId: str):
    pass

#Delete Spesific Product
@app.delete('/products/{productId}', tags=['product']) 
async def delete_product(productId: str):
    pass

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