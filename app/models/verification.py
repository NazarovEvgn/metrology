# app/models/verification.py
from __future__ import annotations

import uuid
from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Verification(Base):
    __tablename__ = "verification"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    equipment_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("equipment.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    verification_date: Mapped[date] = mapped_column(Date, nullable=False)
    interval_months: Mapped[int] = mapped_column(Integer, nullable=False)

    equipment = relationship(
        "Equipment",
        back_populates="verification",
        uselist=False,
        passive_deletes=True,
    )

    __table_args__ = (UniqueConstraint("equipment_id", name="uq_verification_equipment"),)
