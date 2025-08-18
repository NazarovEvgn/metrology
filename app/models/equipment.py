# app/models/equipment.py
import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

# допустимые состояния (ровно как в твоём описании)
ALLOWED_STATES = (
    "в работе",
    "на консервации",
    "на верификации",
    "в ремонте",
    "списано",
)


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

    # состояние
    state: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        server_default="в работе",
        index=True,
    )

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

    __table_args__ = (
        # мягкая валидация на стороне БД
        CheckConstraint(
            f"state IN ('{'',''.join(ALLOWED_STATES)}')",
            name="ck_equipment_state_allowed",
        ),
    )

    def __repr__(self) -> str:
        return f"<Equipment {self.id} {self.name!r}>"
