from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from ..persistence import Base


class ProductPrice(Base):
    """
    ProductPrice model represents scraped product price for a specified product
    """
    __tablename__ = "product_prices"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    price = Column(Float)
    date_created = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="prices")
