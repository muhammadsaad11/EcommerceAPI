from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from databaseCon import get_db
from models import Sale, Product
from schema import ReturnSales, SaleFilterRequest
from datetime import datetime, timedelta

route = APIRouter(prefix="/sales", tags=["Sales"])
@route.get("/", response_model=list[ReturnSales])
def list_sales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Sale).offset(skip).limit(limit).all()

@route.post("/", response_model=list[ReturnSales])
def get_sales(filters: SaleFilterRequest, db: Session = Depends(get_db)):
    query = db.query(Sale)

    if filters.start_date:
        query = query.filter(Sale.sold_at >= filters.start_date)
    if filters.end_date:
        query = query.filter(Sale.sold_at <= filters.end_date)
    if filters.product_id:
        query = query.filter(Sale.product_id == filters.product_id)
    if filters.category_id:
        query = query.join(Product).filter(Product.category_id == filters.category_id)

    return query.all()

@route.get("/{sales_id}", response_model=ReturnSales)
def get_sales(sales_id: int, db: Session = Depends(get_db)):
    item = db.query(Sale).filter(Sale.id == sales_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found in Sales")
    return item


@route.get("/revenue/{period}")
def revenue_by_period(period: str, db: Session = Depends(get_db)):
    now = datetime.utcnow()

    if period == "daily":
        start = now - timedelta(days=1)
    elif period == "weekly":
        start = now - timedelta(weeks=1)
    elif period == "monthly":
        start = now - timedelta(days=30)
    elif period == "annual":
        start = now - timedelta(days=365)
    else:
        return {"error": "Invalid Period Selected"}

    total = db.query(func.sum(Sale.total_price)).filter(Sale.sold_at >= start).scalar()
    return {"period": period, "revenue": total or 0.0}

@route.post("/compare")
def compare_revenue(data: dict, db: Session = Depends(get_db)):
    start1 = datetime.fromisoformat(data["start1"])
    end1 = datetime.fromisoformat(data["end1"])
    start2 = datetime.fromisoformat(data["start2"])
    end2 = datetime.fromisoformat(data["end2"])

    sumRange1 = db.query(func.sum(Sale.total_price)).filter(Sale.sold_at.between(start1, end1)).scalar()
    sumRange2 = db.query(func.sum(Sale.total_price)).filter(Sale.sold_at.between(start2, end2)).scalar()

    return {
        "SelectedRange1": {"start": start1, "end": end1, "revenue": sumRange1 or 0.0},
        "SelectedRange2": {"start": start2, "end": end2, "revenue": sumRange2 or 0.0},
        "difference": (sumRange2 or 0.0) - (sumRange1 or 0.0)
    }