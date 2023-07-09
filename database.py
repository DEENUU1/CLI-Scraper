from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import create_engine, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Session, sessionmaker, relationship

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
