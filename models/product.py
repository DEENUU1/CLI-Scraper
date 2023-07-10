from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from ..persistence import Base


class Product(Base):
    """
    Product model represents scraped product
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    website_id = Column(Integer, ForeignKey("websites.id"))
    date_created = Column(DateTime, default=datetime.utcnow)
    date_updated = Column(DateTime, default=datetime.utcnow)

    website = relationship("Website", back_populates="products")
    prices = relationship("ProductPrice", back_populates="product")
