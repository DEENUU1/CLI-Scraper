from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from ..persistence import Base


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

