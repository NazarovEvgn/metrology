import uuid
from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Equipment(Base):
    __tablename__ = "equipment"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Название оборудования
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    # Тип оборудования
    type: Mapped[str] = mapped_column(String(100), nullable=False)

    # Заводской номер
    serial_number: Mapped[str] = mapped_column(String(100), nullable=False)

    # Инвентарный номер
    inventory_number: Mapped[str] = mapped_column(String(100), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Equipment {self.id} {self.name!r}>"
