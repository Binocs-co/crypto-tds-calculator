from pydantic import Field, BaseModel
from tds.calculator.models.binocs_model import BinocsModel
from tds.calculator.models.user import User

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
    maker_amount: list = Field(None)
    taker: User = Field(None)
    taker_amount: list = Field(None)

class Amount(BaseModel):
    '''
        amount: [value: int, coin: string, decimal: int]}]
    '''
    value: int = Field(None)
    coin: str = Field(None)
    decimal: int = Field(None)
    coin_type: str = Field(None) #Fiat/VDA
