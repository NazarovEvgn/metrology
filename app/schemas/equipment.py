from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class EquipmentRead(BaseModel):
    id: UUID
    name: str
    type: str
    serial_number: str
    inventory_number: str

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # позволяет создавать схему из ORM-объекта
