from sqlalchemy.orm import Session
import models
import random
from core.database import SessionLocal
from faker import Faker
import datetime

fake = Faker()

dummy_categories = ["home_decor", "kitchenware", "bathroom", "garden", "car"]

start_date = datetime.date(year=2020, month=1, day=1)


def create_categories(db: Session):
    for cat in dummy_categories:
        db_category = models.Category(**{"name": cat})
        db.add(db_category)
        db.commit()
        db.refresh(db_category)


def create_products(db: Session, n=100):
    for i in range(n):
        c = random.choice(dummy_categories)
        cost_price = round(random.uniform(2.0, 100.0), 2)
        profit_perc = random.randrange(10, 20)
        retail_price = cost_price + round((0.01 * profit_perc * cost_price), 2)
        random_date = fake.date_time_between(start_date=start_date, end_date='+3y')
        random_product = {"name": f"{c}{i}", "category": c, "count": random.randrange(5, 100),
                          "cost_price": cost_price, "retail_price": retail_price, "created_at": random_date,
                          "updated_at": random_date}
        db_product = models.Product(**random_product)
        db.add(db_product)
        db.commit()
        db.refresh(db_product)


def create_sales(db: Session, n=80):
    all_products = db.query(models.Product).all()
    for i in range(n):
        random_product = random.choice(all_products)
        sale_date = fake.date_time_between(start_date=random_product.created_at, end_date='+1y')
        sale_price = random_product.retail_price
        profit = sale_price - random_product.cost_price
        random_sale = {"product_id": random_product.id, "sale_price": sale_price, "profit": profit,
                       "created_at": sale_date}
        db_sale = models.Sale(**random_sale)
        db.add(db_sale)
        db.commit()
        db.refresh(db_sale)


if __name__ == "__main__":
    db = SessionLocal()
    create_categories(db)
    create_products(db)
    create_sales(db)
