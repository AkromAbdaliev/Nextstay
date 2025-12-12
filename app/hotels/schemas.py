from pydantic import BaseModel, ConfigDict
from sqlalchemy import Any


class SHotels(BaseModel):
    id: int
    name: str
    city: str
    location: str
    services: Any
    rooms_quantity: int
    image_id: str

    model_config = ConfigDict(from_attributes=True)
