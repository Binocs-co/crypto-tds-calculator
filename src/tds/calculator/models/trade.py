from pydantic import Field, BaseModel
from tds.calculator.models.binocs_model import BinocsModel
from tds.calculator.models.user import User

class UserTradeDetail(BaseModel):
    ''' maker: User | mandatory | exchange-id of the maker
        taker: User | mandatory | exchange-id of the taker
        trade_id: string | mandatory
        trade_type: string | mandatory | buy OR sell
        timestamp: int | mandatory
        maker_amount: list | mandatory | [Amount]
        taker_amount: list | mandatory | [Amount]
    '''
    maker: User = Field(None)
    taker: User = Field(None)
    trade_id: str = Field(None)
    trade_type: str = Field(None)
    timestamp: int = Field(None)
    maker_amount: list = Field(None)
    taker_amount: list = Field(None)

class Amount(BaseModel):
    '''
        amount: [value: int, coin: string, decimal: int]}]
    '''
    value: int = Field(None)
    coin: str = Field(None)
    decimal: int = Field(None)
    coin_type: str = Field(None) #Fiat/VDA
