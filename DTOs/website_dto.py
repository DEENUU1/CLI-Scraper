from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import relationship
from product_dto import Product


class WebsiteBase(BaseModel):
    name: str
    objects_numbers: int
    last_update: Optional[datetime] = None


class WebsiteCreate(WebsiteBase):
    pass


class Website(WebsiteBase):
    id: int
    products: List["Product"] = relationship("Product", back_populates="website")

    class Config:
        orm_mode = True
