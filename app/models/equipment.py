# app/models/equipment.py
import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Equipment(Base):
    __tablename__ = "equipment"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Название оборудования
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    # Тип оборудования
    type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)

    # Заводской номер
    serial_number: Mapped[str] = mapped_column(String(100), nullable=False, index=True)

    # Инвентарный номер
    inventory_number: Mapped[str] = mapped_column(String(100), nullable=False, index=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    verification = relationship(
        "Verification",
        back_populates="equipment",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return f"<Equipment {self.id} {self.name!r}>"
