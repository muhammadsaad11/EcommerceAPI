from sqlalchemy.orm import Session
from databaseCon import SessionLocal, con_factory
from models import Product, Inventory, Category, Sale, InventoryHistory
from models import Base
from datetime import datetime, timedelta
import random

Base.metadata.create_all(bind=con_factory)
db: Session = SessionLocal()


db.query(InventoryHistory).delete()
db.query(Sale).delete()
db.query(Inventory).delete()
db.query(Product).delete()
db.query(Category).delete()


cat1 = Category(name="Electronics", description="Electronic gadgets and devices")
cat2 = Category(name="Sports", description="Sports equipment and gear")

db.add_all([cat1, cat2])
db.commit()


p1 = Product(name="Power Brick", category_id=cat1.id)
p2 = Product(name="FootBall", category_id=cat2.id)
p3 = Product(name="Tennis Ball", category_id=cat2.id)

db.add_all([p1, p2, p3])
db.commit()

inv1 = Inventory(product_id=p1.id, stock_quantity=5, low_stock_threshold=10)
inv2 = Inventory(product_id=p2.id, stock_quantity=15, low_stock_threshold=20)
inv3 = Inventory(product_id=p3.id, stock_quantity=17, low_stock_threshold=5)

db.add_all([inv1, inv2, inv3])
db.commit()
db.close()


products = db.query(Product).all()

for i in range(40): 
    product = random.choice(products)
    quantity = random.randint(1, 5)
    unit_price = random.uniform(10.0, 1000.0)
    total_price = round(quantity * unit_price, 2)
    sold_at = datetime.utcnow() - timedelta(days=random.randint(0, 30))

    sale = Sale(
        product_id=product.id,
        quantity=quantity,
        total_price=total_price,
        sold_at=sold_at
    )

    db.add(sale)
db.commit()
db.close()    

print("Created tablez and inserted demo data.")
