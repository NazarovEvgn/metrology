# app/schemas/equipment.py
from __future__ import annotations

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field

from .verification import VerificationRead

EquipmentState = Literal["в работе", "на консервации", "на верификации", "в ремонте", "списано"]


class EquipmentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    type: str = Field(min_length=1, max_length=100)
    serial_number: str = Field(min_length=1, max_length=100)
    inventory_number: str = Field(min_length=1, max_length=100)
    state: EquipmentState = "в работе"

    # поля верификации, которые приходят вместе с созданием
    verification_date: date | None = None
    interval_months: int | None = None


class EquipmentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    type: str | None = Field(default=None, min_length=1, max_length=100)
    serial_number: str | None = Field(default=None, min_length=1, max_length=100)
    inventory_number: str | None = Field(default=None, min_length=1, max_length=100)
    state: EquipmentState | None = None

    # разрешим обновлять и верификацию
    verification_date: date | None = None
    interval_months: int | None = None


class EquipmentRead(BaseModel):
    id: str
    name: str
    type: str
    serial_number: str
    inventory_number: str
    created_at: datetime
    updated_at: datetime

    # плоские поля из verification (если показываем в той же таблице)
    verification_date: date | None = None
    interval_months: int | None = None
    next_verification_date: date | None = None

    # status-модуль:
    state: str
    status: str

    # вложенный объект (если показывать verification как под-структуру)
    verification: VerificationRead | None = None

    class Config:
        from_attributes = True
