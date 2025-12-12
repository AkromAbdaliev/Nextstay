from sqlalchemy import JSON, Column, Integer, String

from app.core.database import Base


class Hotels(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    city = Column(String, index=True, nullable=False)
    location = Column(String, index=True, nullable=False)
    services = Column(JSON)
    rooms_quantity = Column(Integer, nullable=False)
    image_id = Column(String)
