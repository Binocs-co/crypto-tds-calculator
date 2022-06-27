from pydantic import Field, BaseModel

from tds.calculator.models.binocs_model import BinocsModel
from tds.calculator.models.user import User
from tds.calculator.models.amount import Amount

class TDSDetails(BaseModel):
    '''
    tds | {trade_id: string,
           amount: {value: int, coin: string, decimal: int}
           fiat: float,  currency: string, challan: url,
           status: string}}
    '''
    amount: Amount = Field(None)
    fiat: float = Field(None)
    currency: str = Field(None)
    challan: str = Field(None)
    status: str = Field(None)

class UserTDSDetails(BinocsModel):
    '''
        exchange_user_id | string
        tds | [TDSDetails]
    '''
    user: User = Field(None)
    trade_id: str = Field(None)
    timestamp: int = Field(None)
    tds_details: TDSDetails = Field(None)

