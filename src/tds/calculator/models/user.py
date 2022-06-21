from typing import Optional
from pydantic import Field

from tds.calculator.models.binocs_model import BinocsModel

class User(BinocsModel):
    email: str = Field(None)
    pan: str = Field(None)
    itr_ack: bool = Field(True)
    trade_amount: Optional[float] = Field(0)

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "email": "test_email",
                "pan": "test_phone",
                "itr_ack": True,
                "trade_amount": 5000
            }
        }
