from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import create_engine, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, Session

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Website(Base):
    """
    Model represents Website from which product got scraped
    """
    __tablename__ = "websites"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    objects_number = Column(Integer, default=0)
    last_update = Column(DateTime, default=datetime.utcnow)

    products = relationship("Product", back_populates="website")


class WebsiteInput(BaseModel):
    name: str
    object_number: int


class WebsiteOutput(WebsiteInput):
    id: int
    last_update: datetime

    class Config:
        orm_mode = True


class Product(Base):
    """
    Product model represents scraped product
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    website_id = Column(Integer, ForeignKey("websites.id"))
    date_created = Column(DateTime, default=datetime.utcnow)
    date_updated = Column(DateTime, default=datetime.utcnow)

    website = relationship("Website", back_populates="products")


class ProductInput(BaseModel):
    name: str
    price: float
    url: str
    website_id: int


class ProductOutput(ProductInput):
    id: int
    date_created: datetime
    date_updated: datetime

    class Config:
        orm_mode = True


def create_website(
        db: Session,
        name: str
) -> WebsiteInput:
    """
    Create website object
    """
    db_website = Website(name=name, last_update=datetime.utcnow())
    db.add(db_website)
    db.commit()
    db.refresh(db_website)
    return db_website


def website_exists(db: Session, website_name: str) -> bool:
    """
    Check if website exists
    """
    return db.query(Website).filter(Website.name == website_name).first() is not None


def get_website_id(db: Session, website_name: str):
    """
    Get website id
    """
    return db.query(Website).filter(Website.name == website_name).first().id


def update_website():
    pass


def delete_website():
    pass


def create_product(
        db: Session,
        name: str,
        price: float,
        url: str,
        website_id: int
) -> ProductInput:
    """
    Create product object
    """
    db_product = Product(
        name=name, price=price, url=url, website_id=website_id,
        date_created=datetime.utcnow(), date_updated=datetime.utcnow()
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product():
    pass


def delete_product():
    pass


def product_exists(db: Session, product_name: str) -> bool:
    """
    Check if product exists
    """
    return db.query(Product).filter(Product.name == product_name).first() is not None
