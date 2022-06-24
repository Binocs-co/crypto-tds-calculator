from pydantic import Field, BaseModel
from tds.calculator.models.binocs_model import BinocsModel
from tds.calculator.models.user import User
from tds.calculator.models.amount import Amount
from tds.calculator.models.tds import UserTradeDetails

class UserTradeDetail(BaseModel):
    '''
        trade_id: string | mandatory
        timestamp: int | mandatory
        trade_type: string | mandatory | 'TRADE' for now
        maker: User | mandatory | exchange-id of the maker
        maker_amount: list | mandatory | [Amount]
        taker: User | mandatory | exchange-id of the taker
        taker_amount: list | mandatory | [Amount]
    '''
    trade_id: str = Field(None)
    timestamp: int = Field(None)
    trade_type: str = Field(None)
    maker: User = Field(None)
    maker_amount: Amount = Field(None)
    taker: User = Field(None)
    taker_amount: Amount = Field(None)
    tds_details: List[UserTDSDetails] = Field(None)

    def add_tds(self, user_tds_details):
        self.tds_details.append(user_tds_details)
        return
