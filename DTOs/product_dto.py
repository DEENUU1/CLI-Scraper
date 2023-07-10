from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import relationship


class ProductBase(BaseModel):
    name: str
    website_id: int


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    date_created: Optional[datetime] = None
    date_updated: Optional[datetime] = None
    website: Website = relationship("Website", back_populates="products")
    prices: List["ProductPrice"] = relationship("ProductPrice", back_populates="product")

    class Config:
        orm_mode = True