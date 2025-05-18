from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from databaseCon import get_db
from models import Inventory, InventoryHistory
from schema import ReturnInventory, CreateInventory, InventoryUpdateRequest

route = APIRouter(prefix="/inventory", tags=["Inventory"])

@route.get("/get-low-stock", response_model=list[ReturnInventory])
def get_low_stock(db: Session = Depends(get_db)):
    items = db.query(Inventory).filter(
        Inventory.stock_quantity < Inventory.low_stock_threshold
    ).all()
    return items

@route.post("/", response_model=ReturnInventory)
def create_inventory(item: CreateInventory, db: Session = Depends(get_db)):
    db_item = Inventory(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# @route.put("/{inventory_id}", response_model=ReturnInventory)
# def update_inventory(inventory_id: int, item: CreateInventory, db: Session = Depends(get_db)):
#     db_item = db.query(Inventory).filter(Inventory.id == inventory_id).first()
#     if not db_item:
#         raise HTTPException(status_code=404, detail="Item not found in Inventory")
#     for key, value in item.dict().items():
#         setattr(db_item, key, value)
#     db.commit()
#     db.refresh(db_item)
#     return db_item

@route.get("/", response_model=list[ReturnInventory])
def list_inventory(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Inventory).offset(skip).limit(limit).all()

@route.get("/{inventory_id}", response_model=ReturnInventory)
def get_inventory(inventory_id: int, db: Session = Depends(get_db)):
    item = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found in Inventory")
    return item

@route.put("/update")
def update_inventory(inventory_id: int, item: InventoryUpdateRequest, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory record not found")

    old_qty = inventory.stock_quantity
    inventory.stock_quantity = item.new_quantity
    db.add(inventory)

    history = InventoryHistory(
        product_id=item.product_id,
        old_quantity=old_qty,
        new_quantity=item.new_quantity
    )
    db.add(history)

    db.commit()
    db.refresh(inventory)

    return {
        "message": "Inventory updated successfully",
        "product_id": item.product_id,
        "old_quantity": old_qty,
        "new_quantity": item.new_quantity
    }
