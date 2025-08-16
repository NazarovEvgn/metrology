# app/api/equipment.py
from __future__ import annotations

from typing import TypedDict

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy import Date, cast, func, literal, literal_column, or_, select
from sqlalchemy.orm import Session

from ..deps.db import get_db
from ..models.equipment import Equipment
from ..models.verification import Verification
from ..schemas.equipment import EquipmentRead

router = APIRouter(prefix="/equipment", tags=["equipment"])


# -----------------------------
# Query params (as dependency)
# -----------------------------
class EquipmentQuery(TypedDict, total=False):
    q: str
    name: str
    equipment_type: str  # query alias: "type"
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
    """Safe int cast with bounds (for limit/offset)."""
    try:
        v = int(value) if value is not None else default
    except ValueError:
        v = default
    if min_v is not None and v < min_v:
        v = min_v
    if max_v is not None and v > max_v:
        v = max_v
    return v


async def get_equipment_query(
    request: Request,
    q: str | None = Query(None, description="Search by name/type/serial/inventory"),
    limit: int | None = Query(50, ge=1, le=200),
    offset: int | None = Query(0, ge=0),
) -> EquipmentQuery:
    """
    Collect query params without growing function signature (keeps linters happy).
    Extra filters are read from query string: name, type, serial_number, inventory_number.
    """
    qp = request.query_params
    params: EquipmentQuery = {}

    if q:
        params["q"] = q

    name = qp.get("name")
    if name:
        params["name"] = name

    equipment_type = qp.get("type")
    if equipment_type:
        params["equipment_type"] = equipment_type

    serial_number = qp.get("serial_number")
    if serial_number:
        params["serial_number"] = serial_number

    inventory_number = qp.get("inventory_number")
    if inventory_number:
        params["inventory_number"] = inventory_number

    params["limit"] = _to_int(str(limit) if limit is not None else None, 50, 1, 200)
    params["offset"] = _to_int(str(offset) if offset is not None else None, 0, 0, None)
    return params


NEXT_DATE_EXPR = cast(
    (
        Verification.verification_date
        + func.make_interval(
            literal(0), Verification.interval_months
        )  # years=0, months=interval_months
        - literal_column("interval '1 day'")
    ),
    Date,
).label("next_verification_date")


# -----------------------------
# Handlers
# -----------------------------
@router.get("/", response_model=list[EquipmentRead])
def list_equipment(
    params: EquipmentQuery = Depends(get_equipment_query),  # noqa: B008
    db: Session = Depends(get_db),  # noqa: B008
):
    """
    Equipment list (read-only) with filters & pagination.
    Response includes verification_date, interval_months, next_verification_date.
    """
    stmt = select(
        Equipment,
        Verification.verification_date,
        Verification.interval_months,
        NEXT_DATE_EXPR,
    ).join(Verification, Verification.equipment_id == Equipment.id, isouter=True)

    # Full-text-like search across several columns
    if "q" in params:
        like = f"%{params['q']}%"
        stmt = stmt.where(
            or_(
                Equipment.name.ilike(like),
                Equipment.type.ilike(like),
                Equipment.serial_number.ilike(like),
                Equipment.inventory_number.ilike(like),
            )
        )

    # Exact filters (if provided)
    if "name" in params:
        stmt = stmt.where(Equipment.name == params["name"])
    if "equipment_type" in params:
        stmt = stmt.where(Equipment.type == params["equipment_type"])
    if "serial_number" in params:
        stmt = stmt.where(Equipment.serial_number == params["serial_number"])
    if "inventory_number" in params:
        stmt = stmt.where(Equipment.inventory_number == params["inventory_number"])

    stmt = stmt.order_by(Equipment.name).offset(params["offset"]).limit(params["limit"])

    rows = db.execute(stmt).all()

    # Flatten JOIN into plain dicts that match EquipmentRead
    result: list[dict] = []
    for eq, ver_date, interval_months, next_date in rows:
        result.append(
            {
                "id": str(eq.id),
                "name": eq.name,
                "type": eq.type,
                "serial_number": eq.serial_number,
                "inventory_number": eq.inventory_number,
                "created_at": eq.created_at,
                "updated_at": eq.updated_at,
                "verification_date": ver_date,
                "interval_months": interval_months,
                "next_verification_date": next_date,
            }
        )
    return result


# Duplicate without trailing slash to avoid 307 in some WebViews.
@router.get("", response_model=list[EquipmentRead], include_in_schema=False)
def list_equipment_no_slash(
    params: EquipmentQuery = Depends(get_equipment_query),  # noqa: B008
    db: Session = Depends(get_db),  # noqa: B008
):
    return list_equipment(params, db)


@router.get("/{equipment_id}", response_model=EquipmentRead)
def get_equipment(
    equipment_id: str,
    db: Session = Depends(get_db),  # noqa: B008
):
    """
    Single equipment by UUID with verification fields if present.
    """
    stmt = (
        select(
            Equipment,
            Verification.verification_date,
            Verification.interval_months,
            NEXT_DATE_EXPR,
        )
        .join(Verification, Verification.equipment_id == Equipment.id, isouter=True)
        .where(Equipment.id == equipment_id)
        .limit(1)
    )

    row = db.execute(stmt).first()
    if not row:
        raise HTTPException(status_code=404, detail="Equipment not found")

    eq, ver_date, interval_months, next_date = row
    return {
        "id": str(eq.id),
        "name": eq.name,
        "type": eq.type,
        "serial_number": eq.serial_number,
        "inventory_number": eq.inventory_number,
        "created_at": eq.created_at,
        "updated_at": eq.updated_at,
        "verification_date": ver_date,
        "interval_months": interval_months,
        "next_verification_date": next_date,
    }
