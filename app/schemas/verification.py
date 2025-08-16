from datetime import date

from pydantic import BaseModel


class VerificationRead(BaseModel):
    verification_date: date
    interval_months: int
    next_verification_date: date

    class Config:
        from_attributes = True
