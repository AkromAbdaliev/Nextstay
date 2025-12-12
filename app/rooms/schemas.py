from pydantic import BaseModel, ConfigDict
from sqlalchemy import Any


class SRooms(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str | None = None
    price: int
    services: Any | None = None
    quantity: int
    image_id: int | None = None

    model_config = ConfigDict(from_attributes=True)


class SRoomsPeriod(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str | None = None
    price: int
    services: Any | None = None
    quantity: int
    image_id: int | None = None
    total_days: int
    total_cost: int

    model_config = ConfigDict(from_attributes=True)
