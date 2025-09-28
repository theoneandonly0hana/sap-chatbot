from pydantic import BaseModel, Field, field_validator
from pydantic import BaseModel, Field, field_validator
from typing import Literal

Currency = Literal["THB","USD","EUR"]

class PurchaseOrderIn(BaseModel):
    material_code: str = Field(..., min_length=2)
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)
    vendor_code: str
    currency: Currency = "THB"

    def total_amount(self) -> float:
        return round(self.quantity * self.unit_price, 2)

class VendorIn(BaseModel):
    name: str
    tax_id: str
    country: str = "TH"

    @field_validator("tax_id")
    @classmethod
    def _taxid_len(cls, v):
        if len(v) < 10:
            raise ValueError("tax_id too short")
        return v
