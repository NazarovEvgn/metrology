# app/api/equipment.py
from typing import TypedDict

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from ..deps.db import get_db
from ..models.equipment import Equipment
from ..schemas.equipment import EquipmentRead

router = APIRouter(prefix="/equipment", tags=["equipment"])


class EquipmentQuery(TypedDict, total=False):
    q: str
    name: str
    equipment_type: str  # comes from ?type=
    serial_number: str
    inventory_number: str
    limit: int
    offset: int


def _to_int(
    value: str | None,
    default: int,
    min_v: int | None = None,
    max_v: int | None = None,
) -> int:
    try:
        v = int(value) if value is not None else default
    except ValueError:
        v = default
    if min_v is not None and v < min_v:
        v = min_v
    if max_v is not None and v > max_v:
        v = max_v
    return v


def get_equipment_query(request: Request) -> EquipmentQuery:
    """Parse query params without tripping PLR0913."""
    qp = request.query_params
    return {
        "q": qp.get("q"),
        "name": qp.get("name"),
        "equipment_type": qp.get("type"),
        "serial_number": qp.get("serial_number"),
        "inventory_number": qp.get("inventory_number"),
        "limit": _to_int(qp.get("limit"), 50, 1, 200),
        "offset": _to_int(qp.get("offset"), 0, 0, None),
    }


@router.get("/", response_model=list[EquipmentRead])
def list_equipment(
    params: EquipmentQuery = Depends(get_equipment_query),  # noqa: B008
    db: Session = Depends(get_db),  # noqa: B008
):
    """Equipment list (read-only) with filters and pagination."""
    stmt = select(Equipment)

    if params.get("q"):
        like = f"%{params['q']}%"
        stmt = stmt.where(
            or_(
                Equipment.name.ilike(like),
                Equipment.type.ilike(like),
                Equipment.serial_number.ilike(like),
                Equipment.inventory_number.ilike(like),
            )
        )

    if params.get("name") is not None:
        stmt = stmt.where(Equipment.name == params["name"])
    if params.get("equipment_type") is not None:
        stmt = stmt.where(Equipment.type == params["equipment_type"])
    if params.get("serial_number") is not None:
        stmt = stmt.where(Equipment.serial_number == params["serial_number"])
    if params.get("inventory_number") is not None:
        stmt = stmt.where(Equipment.inventory_number == params["inventory_number"])

    stmt = stmt.order_by(Equipment.name).offset(params["offset"]).limit(params["limit"])
    return list(db.execute(stmt).scalars())


@router.get("/{equipment_id}", response_model=EquipmentRead)
def get_equipment(
    equipment_id: str,
    db: Session = Depends(get_db),  # noqa: B008
):
    """Return equipment by UUID."""
    item = db.get(Equipment, equipment_id)
    if not item:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return item
