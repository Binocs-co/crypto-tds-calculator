from pydantic import Field, BaseModel

from tds.calculator.models.binocs_model import BinocsModel
from tds.calculator.models.user import User
from tds.calculator.models.trade import Amount

class UserTDSDetails(BaseModel):
    '''
        exchange_user_id | string
        tds | [TDSDetails]
    '''
    user: User = Field(None)
    tds_details: List[TDSDetails] = Field(None)

class TDSDetails(BaseModel):
    '''
    tds | {trade_id: string,
           amount: {value: int, coin: string, decimal: int}
           fiat: float,  currency: string, challan: url,
           status: string}}
    '''
    trade_id: str = Field(None)
    amount: Amount = Field(None)
    fiat: float = Field(None)
    currency: str = Field(None)
    challan: str = Field(None)
    status: str = Field(None)
