from pydantic import Field, BaseModel

from tds.calculator.models.binocs_model import BinocsModel

class TradeAcknowledgement(BaseModel):
    acknowledgement: bool = Field(True)

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "acknowledgement": True
            }
        }

class UserTradeDetail(BaseModel):
   ''' from: string | mandatory | email of the user
to: string | mandatory | email of the user
tx-detail | json | mandatory | [{type: string, timestamp: int, value: int, value_coin: string, value_decimal: int, fee: int, fee_coin: string, fee_decimal: int}]
tx_type: trade | lending | fixed-income | coupon'''


class TradeDetail(BaseModel):
    '''email | string | mandatory | email of the user
    tx-detail | json | mandatory | [{type: string, timestamp: int, value: int, value_coin: string, value_decimal: int, fee: int, fee_coin: string, fee_decimal: int}]
    type: trade | lending | fixed-income | coupon'''

class TradeLineItem(BaseModel) :
    '''tx-detail | json | mandatory | [{type: string, timestamp: int, value: int, value_coin: string, value_decimal: int, fee: int, fee_coin: string, fee_decimal: int}]
    '''
