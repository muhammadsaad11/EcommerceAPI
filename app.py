from fastapi import FastAPI
from databaseCon import con_factory
from models import Base
from api import inventory, product, sales

app = FastAPI(title="E-commerce API")

# Create tables
Base.metadata.create_all(bind=con_factory)

# Include routers
app.include_router(inventory.route)
app.include_router(product.route)
app.include_router(sales.route)
# app.include_router(sales.route)