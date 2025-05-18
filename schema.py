from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Config:
    orm_mode = True

class User(BaseModel):
    id: int
    username: str
    email: str
    password: str
    is_admin: bool = False
    company_user: bool = False
    created_at: datetime
    updated_at: datetime

class CreateProduct(BaseModel):
    name: str
    description: str
    category_id: int

class ReturnProduct(BaseModel):
    id: int
    name: str
    description: Optional[str] = ""
    category_id: int

    class Config:
        orm_mode = True

class Order(BaseModel):
    user_id: int
    product_id: int
    quantity: int
    order_date: datetime
    status: str

class CreateInventory(BaseModel):
    product_id: int
    stock_quantity: int
    low_stock_threshold: int

class InventoryUpdateRequest(BaseModel):
    product_id: Optional[int] = None
    new_quantity: Optional[int] = None
    low_stock_threshold: Optional[int] = None

class ReturnInventory(BaseModel):
    id: int
    product_id: int
    stock_quantity: int
    low_stock_threshold: int
    updated_at: datetime

class ReturnSales(BaseModel):
    id: int
    product_id: int
    quantity: int
    total_price: float
    sold_at: datetime

    class Config:
        orm_mode = True

class SaleFilterRequest(BaseModel):
    start_date: datetime | None = None
    end_date: datetime | None = None
    product_id: int | None = None
    category_id: int | None = None