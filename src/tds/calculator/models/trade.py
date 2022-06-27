from pydantic import Field

from tds.calculator.models.binocs_model import BinocsModel
from tds.calculator.models.user import User
from tds.calculator.models.amount import Amount
from tds.calculator.models.tds import UserTDSDetails

class UserTradeDetail(BinocsModel):
    '''
        trade_id: string | mandatory
        timestamp: int | mandatory
        trade_type: string | mandatory | 'TRADE' for now
        maker: User | mandatory | exchange-id of the maker
        maker_amount: list | mandatory | [Amount]
        taker: User | mandatory | exchange-id of the taker
        taker_amount: list | mandatory | [Amount]
    '''
    exchange_id: str = Field(None)
    trade_id: str = Field(None)
    timestamp: int = Field(None)
    trade_type: str = Field(None)
    maker: User = Field(None)
    maker_amount: Amount = Field(None)
    taker: User = Field(None)
    taker_amount: Amount = Field(None)
    txfee_amount: Amount = Field(None)
    gst_amount: Amount = Field(None)
    maker_tds_details: UserTDSDetails = Field(None)
    taker_tds_details: UserTDSDetails = Field(None)