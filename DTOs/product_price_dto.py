from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from sqlalchemy.orm import relationship
from product_dto import Product


class ProductPriceBase(BaseModel):
    price: float
    product_id: int


class ProductPriceCreate(ProductPriceBase):
    pass


class ProductPrice(ProductPriceBase):
    id: int
    date_created: Optional[datetime] = None
    product: Product = relationship("Product", back_populates="prices")

    class Config:
        orm_mode = True