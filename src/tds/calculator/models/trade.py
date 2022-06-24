from pydantic import Field, BaseModel
from tds.calculator.models.binocs_model import BinocsModel

class UserTradeDetail(BaseModel):
   ''' buyer_id: string | mandatory | exchange-id of the user
       seller_id: string | mandatory | exchange-id of the user
       details: json | mandatory | [{trade_id: string, type: string, timestamp: int,
                                     amount: [value: int, coin: string, decimal: int]}]
   '''
   buyer_id: str = Field(None)
   seller_id: str = Field(None)
   details: list = Field(None)

class TradeDetail(BaseModel):
    '''
       details: json | mandatory | [{trade_id: string, type: string, timestamp: int,
                                     amount: [value: int, coin: string, decimal: int]}]
    '''
    trade_id: str = Field(None)
    trade_type: str = Field(None)
    timestamp: int = Field(None)
    amount: list = Field(None)

class Amount(BaseModel):
    '''
        amount: [value: int, coin: string, decimal: int]}]
    '''
    value: int = Field(None)
    coin: str = Field(None)
    decimal: int = Field(None)
