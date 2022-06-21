from pydantic import Field, BaseModel

from tds.calculator.models.binocs_model import BinocsModel

class TDSAcknowledgement(BaseModel):
    '''tds: {email: {value: float, value_coin: string, value_decimal: int}}'''

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "acknowledgement": True
            }
        }

class TDSDeductionDetail(BaseModel):
    '''
    tds_escrow: {exchange-account-id: [{value: float, value_coin: string, value_decimal: int, tx-metadata: <TBD>}]},
Net_value: [{email: [{value: float, value_coin: string, value_decimal: int}]}]

    '''

class TDSDetail(BaseModel):
    '''
    tds: {email: {value: float, value_coin: string, value_decimal: int}}
    '''

class TradeLineItem(BaseModel) :
    '''
    tx-detail | json | mandatory | [{type: string, timestamp: int, value: int, value_coin: string, value_decimal: int, fee: int, fee_coin: string, fee_decimal: int}]
    '''