from datetime import datetime, timedelta
from typing import Optional, List

from fastapi import FastAPI, HTTPException, status, Depends, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, oauth2
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from src import models, schemas
from .auth import UserHandler
from .database import get_db


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
@app.post("/login", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = UserHandler.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=UserHandler.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = UserHandler.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
  
    return schemas.Token(**{"access_token": access_token, "token_type": "bearer"})


##Product
# Add Product
@app.post('/products',response_model=schemas.Produk, tags=['product']) 
async def create_product(new_produk: schemas.ProdukCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(UserHandler.get_current_user)): 
    db_produk = db.query(models.Produk).filter(models.Produk.productname==new_produk.productname).first()
    if db_produk is not None:
        raise HTTPException(status_code=400,detail="Product already exists")
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
async def get_all_products(db: Session = Depends(get_db), current_user: schemas.User = Depends(UserHandler.get_current_user)): 
    all_produk = db.query(models.Produk).all()
    return all_produk

# Read Spesific Product
@app.get('/products/{productId}',response_model=schemas.Produk , tags=['product']) 
async def get_product(productId: str, db: Session = Depends(get_db), current_user: schemas.User = Depends(UserHandler.get_current_user)): 
    spesific_produk = db.query(models.Produk).filter(models.Produk.productid == productId).first()
    if spesific_produk is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return spesific_produk

# Update Specific Product
@app.put('/products/{productId}',response_model=schemas.Produk, tags=['product']) 
async def update_product(productId: str, update_produk: schemas.ProdukUpdate, db: Session = Depends(get_db), current_user: schemas.User = Depends(UserHandler.get_current_user)):
    produk = db.query(models.Produk).filter(models.Produk.productid == productId).first()
    if produk is None:
        raise HTTPException(status_code=404, detail="Product not found")
    produk_exist = db.query(models.Produk).filter(models.Produk.productname==update_produk.productname).first()
    if produk_exist is not None:
        raise HTTPException(status_code=400,detail="Product already exists")

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
async def delete_product(productId: str, db: Session = Depends(get_db), current_user: schemas.User = Depends(UserHandler.get_current_user)):
    produk = db.query(models.Produk).filter(models.Produk.productid == productId).first()
    if produk is None:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(produk)
    db.commit()
    return produk

##Order
# Add New Order
@app.post('/orders', response_model=schemas.Pesanan, tags=['order']) 
async def create_order(new_order: schemas.PesananCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(UserHandler.get_current_user)): 
    try:
        db_pesanan_id = db.query(func.max(models.Pesanan.orderid)).scalar()
    except:
        db_pesanan_id = None
    db_pesanan_id = set_table_id("OR", db_pesanan_id)
    db_new_order = models.Pesanan(
        orderid=db_pesanan_id, 
        datetime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        paymentstatus=new_order.paymentstatus
    )
    for itempesanan in new_order.itempesanan:
        db_new_itempesanan = models.ItemPesanan(
            productid=itempesanan.productid,
            amount=itempesanan.amount,
            orderid=db_pesanan_id
        )
        db_new_order.products.append(db_new_itempesanan)
    db.add(db_new_order)
    try:
        db.commit()
        db.refresh(db_new_order)
    except:
        raise HTTPException(status_code=400, detail="Order invalid")
    spesific_order = db.query(models.Pesanan).filter(models.Pesanan.orderid == db_new_order.orderid).first()
    order = parse_to_Pesanan(spesific_order)
    return order

# Read All Orders
@app.get('/orders', response_model=List[schemas.Pesanan], tags=['order']) 
async def get_all_orders(db: Session = Depends(get_db), current_user: schemas.User = Depends(UserHandler.get_current_user)): 
    all_orders = db.query(models.Pesanan).all()
    orders = []
    for order in all_orders:
        orders.append(parse_to_Pesanan(order))
    return orders

# Read Spesific Order
@app.get('/orders/{orderId}', response_model=schemas.Pesanan, tags=['order']) 
async def get_order(orderId: str, db: Session = Depends(get_db), current_user: schemas.User = Depends(UserHandler.get_current_user)): 
    spesific_order = db.query(models.Pesanan).filter(models.Pesanan.orderid == orderId).first()
    if spesific_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    order = parse_to_Pesanan(spesific_order)
    return order


# Update Specific Order
@app.put('/orders/{orderId}', response_model=schemas.Pesanan, tags=['order']) 
async def update_order(orderId: str, update_order: schemas.PesananUpdate, db: Session = Depends(get_db), current_user: schemas.User = Depends(UserHandler.get_current_user)):
    order = db.query(models.Pesanan).filter(models.Pesanan.orderid == orderId).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    update_order_dict = update_order.dict(exclude_unset=True)
    for field in update_order_dict:
        if field == 'itempesanan':
            order.products.clear()
            for item in update_order_dict[field]:
                order.products.append(models.ItemPesanan(
                    productid=item['productid'],
                    orderid=orderId,
                    amount=item['amount']
                ))
        else:
            setattr(order, field, update_order_dict[field])
    db.add(order)
    try:
        db.commit()
        db.refresh(order)
    except:
        raise HTTPException(status_code=400, detail="Order invalid")
    order = parse_to_Pesanan(order)
    return order


#Delete Spesific Order
@app.delete('/orders/{orderId}', response_model=schemas.PesananInDB, tags=['order']) 
async def delete_order(orderId: str, db: Session = Depends(get_db), current_user: schemas.User = Depends(UserHandler.get_current_user)):
    order = db.query(models.Pesanan).filter(models.Pesanan.orderid == orderId).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    return order

##Payment
# Add New Payment
@app.post('/orders/{orderId}/pay', response_model=schemas.Pembayaran, tags=['payment']) 
async def create_payment(orderId: str, new_payment: schemas.PembayaranCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(UserHandler.get_current_user)):
    order = db.query(models.Pesanan).filter(models.Pesanan.orderid == orderId).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    payment_exist = db.query(models.Pembayaran).filter(models.Pembayaran.orderid == orderId).first()
    if payment_exist is not None:
        raise HTTPException(status_code=400, detail="Payment already exist")

    total_price = get_total_price(order)
    if new_payment.amount<total_price:
        raise HTTPException(status_code=400, detail="Payment invalid")
    try:
        db_payment_id = db.query(func.max(models.Pembayaran.paymentid)).scalar()
    except:
        db_payment_id = None
    db_payment_id = set_table_id("PY", db_payment_id)
    db_new_payment = models.Pembayaran(
        paymentid=db_payment_id,
        orderid=orderId,
        amount=new_payment.amount,
        change=new_payment.amount-total_price
    )
    order.paymentstatus = True
    db_new_payment.order = order
    db.add(db_new_payment)
    db.commit()
    return db_new_payment

# Read Spesific Payment
@app.get('/orders/{orderId}/pay',response_model=schemas.Pembayaran, tags=['payment']) 
async def get_payment(orderId: str, db: Session = Depends(get_db), current_user: schemas.User = Depends(UserHandler.get_current_user)): 
    order = db.query(models.Pesanan).filter(models.Pesanan.orderid == orderId).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    payment = db.query(models.Pembayaran).filter(models.Pembayaran.orderid == orderId).first()
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

# Update Specific Payment
@app.put('/orders/{orderId}/pay', response_model=schemas.Pembayaran, tags=['payment']) 
async def update_payment(orderId: str, update_payment: schemas.PembayaranUpdate, db: Session = Depends(get_db), current_user: schemas.User = Depends(UserHandler.get_current_user)):
    order = db.query(models.Pesanan).filter(models.Pesanan.orderid == orderId).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    payment = db.query(models.Pembayaran).filter(models.Pembayaran.orderid == orderId).first()
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")

    total_price = get_total_price(order)
    if update_payment.amount<total_price:
        raise HTTPException(status_code=400, detail="Payment invalid")

    obj_payment = jsonable_encoder(payment)
    update_payment_dict = update_payment.dict(exclude_unset=True)
    for field in obj_payment:
        if field in update_payment_dict:
            setattr(payment, field, update_payment_dict[field])
            if field == 'amount':
                setattr(payment, 'change', update_payment_dict['amount']-total_price)
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


#Delete Spesific Payment
@app.delete('/orders/{orderId}/pay', response_model=schemas.Pembayaran, tags=['payment']) 
async def delete_payment(orderId: str, db: Session = Depends(get_db), current_user: schemas.User = Depends(UserHandler.get_current_user)):
    order = db.query(models.Pembayaran).filter(models.Pembayaran.orderid == orderId).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
  
    payment = db.query(models.Pembayaran).filter(models.Pembayaran.orderid == orderId).first()
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")

    payment.order.paymentstatus = False
    db.delete(payment)
    db.commit()
    return payment

##Expense
# Add New Expense
@app.post('/expenses', response_model=schemas.Pengeluaran, tags=['expense']) 
async def create_expense(new_expense: schemas.PengeluaranCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(UserHandler.get_current_user)): 
    try:
        db_pengeluaran_id = db.query(func.max(models.Pengeluaran.expenseid)).scalar()
    except:
        db_pengeluaran_id = None
    db_pengeluaran_id = set_table_id("EX", db_pengeluaran_id)
    db_new_expense = models.Pengeluaran(
        expenseid=db_pengeluaran_id, 
        datetime=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
  
    try:
        db_item_id = db.query(func.max(models.ItemPengeluaran.itemid)).scalar()
    except:
        db_item_id = None
    db_item_id = set_table_id("EI", db_item_id)
    for expense_item in new_expense.itempengeluaran:
        db_new_itempengeluaran = models.ItemPengeluaran(
            itemid=db_item_id,
            expenseid=db_pengeluaran_id,
            nama=expense_item.nama,
            harga =expense_item.harga
        )
        db_item_id = set_table_id("EI", db_item_id)
        db_new_expense.items.append(db_new_itempengeluaran)
  
    db.add(db_new_expense)
    try:
        db.commit()
        db.refresh(db_new_expense)
    except:
        raise HTTPException(status_code=400, detail="Expense invalid")
    expense = db.query(models.Pengeluaran).filter(models.Pengeluaran.expenseid == db_new_expense.expenseid).first()
    expense = parse_to_Pengeluaran(expense)
    return expense

# Read All Expenses
@app.get('/expenses', response_model=List[schemas.Pengeluaran], tags=['expense']) 
async def get_all_expenses(db: Session = Depends(get_db), current_user: schemas.User = Depends(UserHandler.get_current_user)): 
    all_expenses = db.query(models.Pengeluaran).all()
    expenses = []
    for expense in all_expenses:
        expenses.append(parse_to_Pengeluaran(expense))
    return expenses

# Read Spesific Expense
@app.get('/expenses/{expenseId}', response_model=schemas.Pengeluaran, tags=['expense']) 
async def get_expense(expenseId: str, db: Session = Depends(get_db), current_user: schemas.User = Depends(UserHandler.get_current_user)): 
    expense = db.query(models.Pengeluaran).filter(models.Pengeluaran.expenseid == expenseId).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    expense = parse_to_Pengeluaran(expense)
    return expense

# Update Specific Expense
@app.put('/expenses/{expenseId}', response_model=schemas.Pengeluaran, tags=['expense']) 
async def update_expense(expenseId: str, update_expense: schemas.PengeluaranUpdate, db: Session = Depends(get_db), current_user: schemas.User = Depends(UserHandler.get_current_user)):
    expense = db.query(models.Pengeluaran).filter(models.Pengeluaran.expenseid == expenseId).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    update_expese_dict = update_expense.dict(exclude_unset=True)
    for field in update_expese_dict:
        if field == 'itempengeluaran':
            expense.items.clear()
            try:
                db_item_id = db.query(func.max(models.ItemPengeluaran.itemid)).scalar()
            except:
                db_item_id = None
            db_item_id = set_table_id("EI", db_item_id)
            for item in update_expese_dict[field]:
                expense.items.append(models.ItemPengeluaran(
                    itemid=db_item_id,
                    expenseid=expenseId,
                    nama=item['nama'],
                    harga=item['harga']
                ))
                db_item_id = set_table_id("EI", db_item_id)
        else:
            setattr(expense, field, update_expese_dict[field])
    db.add(expense)
    try:
        db.commit()
        db.refresh(expense)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Expense invalid")
    expense = parse_to_Pengeluaran(expense)
    return expense

# Update Expense Expense Based on Item
@app.put('/expenses/{expenseId}/{itemId}', response_model=schemas.ItemPengeluaran, tags=['expense']) 
async def update_expense(expenseId: str, itemId: str, update_item: schemas.ItemPengeluaranUpdate, db: Session = Depends(get_db), current_user: schemas.User = Depends(UserHandler.get_current_user)):
    expense = db.query(models.Pengeluaran).filter(models.Pengeluaran.expenseid == expenseId).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    item = (db.query(models.ItemPengeluaran)
        .filter(models.ItemPengeluaran.expenseid == expenseId)
        .filter(models.ItemPengeluaran.itemid == itemId).first())
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    obj_item = jsonable_encoder(item)
    update_item_dict = update_item.dict(exclude_unset=True)
    for field in obj_item:
        if field in update_item_dict:
            setattr(item, field, update_item_dict[field])
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

#Delete Spesific Expense
@app.delete('/expenses/{expenseId}',response_model=schemas.PengeluaranInDB, tags=['expense']) 
async def delete_expense(expenseId: str, db: Session = Depends(get_db), current_user: schemas.User = Depends(UserHandler.get_current_user)):
    expense = db.query(models.Pengeluaran).filter(models.Pengeluaran.expenseid == expenseId).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
    return expense

#Delete An Item in Expense
@app.delete('/expenses/{expenseId}/{itemId}',response_model=schemas.ItemPengeluaran, tags=['expense']) 
async def delete_expense(expenseId: str, itemId: str, db: Session = Depends(get_db), current_user: schemas.User = Depends(UserHandler.get_current_user)):
    expense = db.query(models.Pengeluaran).filter(models.Pengeluaran.expenseid == expenseId).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    item = (db.query(models.ItemPengeluaran)
        .filter(models.ItemPengeluaran.expenseid == expenseId)
        .filter(models.ItemPengeluaran.itemid == itemId).first())
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()
    return item

##Invoice
# Get Invoice
@app.get('/orders/{orderId}/invoice', response_model=schemas.Invoice, tags=['invoice']) 
async def get_invoice(orderId: str, db: Session = Depends(get_db), current_user: schemas.User = Depends(UserHandler.get_current_user)): 
    order = db.query(models.Pesanan).filter(models.Pesanan.orderid == orderId).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.paymentstatus is False:
        raise HTTPException(status_code=400, detail="Payment invalid")
    
    invoice = schemas.Invoice(
        datetime=order.datetime,
        orderid=order.orderid,
        paymentid=order.payment.paymentid,
        amount=order.payment.amount,
        change=order.payment.change
    )
    total_price = 0
    for product_item in order.products:
        invoice.itempesanan.append(
            schemas.ItemProduk(
                productid=product_item.productid,
                quantity=product_item.amount,
                price=product_item.product.price,
                total=product_item.amount*product_item.product.price
            ))
        total_price+=product_item.amount*product_item.product.price
    invoice.totalprice = total_price
    return invoice

##Report
# Get Report
@app.get('/reports?from={startDateTime}&to={endDateTime}', tags=['report']) 
async def create_expense(startDateTime: datetime, endDateTime: datetime): 
    pass

##Function
def set_table_id(prefix: str, prev_id: str):
    if prev_id is None:
        id = 0
    else:
        id = int(prev_id[-5:])
    id+=1
    id = prefix+str(id).zfill(5)
    return id

def parse_to_Pesanan(order_model: models.Pesanan):
    obj_order = jsonable_encoder(order_model)
    order_schema = schemas.Pesanan(**obj_order)
    for item_pesanan in order_model.products:
        order_schema.itempesanan.append(
            schemas.ItemPesanan(
                productid=item_pesanan.productid,
                orderid=item_pesanan.orderid,
                amount=item_pesanan.amount
            ))
        order_schema.totalprice+=item_pesanan.amount*item_pesanan.product.price
    return order_schema

def get_total_price(order_model: models.Pesanan):
    total_price = 0
    for order_item in order_model.products:
        total_price+=order_item.amount*order_item.product.price
    return total_price

def parse_to_Pengeluaran(expense_model: models.Pengeluaran):
    obj_expense = jsonable_encoder(expense_model)
    expense_schema = schemas.Pengeluaran(**obj_expense)
    for expense_item in expense_model.items:
        expense_schema.itempengeluaran.append(
            schemas.ItemPengeluaran(
                itemid=expense_item.itemid,
                expenseid=expense_item.expenseid,
                nama=expense_item.nama,
                harga=expense_item.harga
            ))
    return expense_schema