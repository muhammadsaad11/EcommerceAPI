from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from databaseCon import get_db
from models import Product
from schema import CreateProduct, ReturnProduct


route = APIRouter(prefix="/product", tags=["Product"])

@route.get("/", response_model=list[ReturnProduct])
def list_product(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Product).offset(skip).limit(limit).all()

@route.get("/{product_id}", response_model=ReturnProduct)
def get_product(product_id: int, db: Session = Depends(get_db)):
    item = db.query(Product).filter(Product.id == product_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found in Product")
    return item

@route.post("/", response_model=ReturnProduct)
def create_product(item: CreateProduct, db: Session = Depends(get_db)):
    db_item = Product(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item