from pydantic import Field, BaseModel

from tds.calculator.models.binocs_model import BinocsModel

class UserTradeDetail(BaseModel):
   ''' from: string | mandatory | exchange-id of the user
       to: string | mandatory | exchange-id of the user
       tx-detail | json | mandatory | [{type: string, timestamp: int, value: int, value_coin: \
                                        string, value_decimal: int, fee: int, fee_coin: string, \
                                        fee_decimal: int}]
       tx_type: trade | lending | fixed-income | coupon
   '''
