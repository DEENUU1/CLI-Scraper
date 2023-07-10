from sqlalchemy.orm import Session
from datetime import datetime
from ..models import ProductPrice
from ..schemas import ProductPriceCreate


def get_product_price(db: Session, product_price_id: int):
    return db.query(ProductPrice).filter(ProductPrice.id == product_price_id).first()


def get_product_prices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ProductPrice).offset(skip).limit(limit).all()


def create_product_price(db: Session, product_price: ProductPriceCreate, product_id: int):
    db_product_price = ProductPrice(price=product_price.price, product_id=product_id, date_created=datetime.now())
    db.add(db_product_price)
    db.commit()
    db.refresh(db_product_price)
    return db_product_price


def update_product_price(db: Session, product_price_id: int, product_price: ProductPriceCreate):
    db_product_price = db.query(ProductPrice).filter(ProductPrice.id == product_price_id).first()
    db_product_price.price = product_price.price
    db.commit()
    db.refresh(db_product_price)
    return db_product_price


def delete_product_price(db: Session, product_price_id: int):
    db_product_price = db.query(ProductPrice).filter(ProductPrice.id == product_price_id).first()
    db.delete(db_product_price)
    db.commit()
    return db_product_price
