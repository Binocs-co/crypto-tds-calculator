from typing import Optional
from pydantic import Field
from datetime import datetime

from tds.calculator.models.binocs_model import BinocsModel, BinocsId

class User(BinocsModel):
    exchange_id: str = Field(None)
    exchange_user_id: str = Field(None)
    pan: str = Field(None)
    itr_ack: bool = Field(True)
    exempt: bool = Field(False)
    binocs_id: Optional[BinocsId] = Field(None)

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "exchange_id": "bitbns",
                "exchange_user_id": "user_id",
                "pan": "test_phone",
                "itr_ack": True,
                "exempt": False,
                "binocs_id": {"id" : "1131"},
                "create_time" : datetime.now(),
                "updated_date" : datetime.now()
            }
        }

    def is_resident(self, country_code: str):
        if country_code == 'IN':
            if self.pan and self.pan != 'NA':
                return True
        return False
