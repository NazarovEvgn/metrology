# app/schemas/equipment.py
from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel

from .verification import VerificationRead


class EquipmentRead(BaseModel):
    id: str
    name: str
    type: str
    serial_number: str
    inventory_number: str
    created_at: datetime
    updated_at: datetime

    # вложенный объект (если хочешь показывать verification как под-структуру)
    verification: VerificationRead | None = None

    # плоские поля из verification (если показываем в той же таблице)
    verification_date: date | None = None
    interval_months: int | None = None
    next_verification_date: date | None = None

    class Config:
        from_attributes = True
