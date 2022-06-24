from typing import Optional
from pydantic import Field

from tds.calculator.models.binocs_model import BinocsModel

class User(BinocsModel):
    exchange_user_id: str = Field(None)
    pan: str = Field(None)
    itr_ack: bool = Field(True)
    exempt: bool = Field(False)

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "exchange_user_id": "user_id",
                "pan": "test_phone",
                "itr_ack": True,
                "exempt": False
            }
        }

    def is_resident(self, country_code: str):
        if country_code == 'IN':
            if self.pan and self.pan != 'NA':
                return True
        return False
