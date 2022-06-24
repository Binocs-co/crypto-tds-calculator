from pydantic import Field, BaseModel

from tds.calculator.models.binocs_model import BinocsModel

class UserTDSDetails(BaseModel):
    '''
        exchange_user_id | string
        tds | [TDSDetails]
    '''

class TDSDetails(BaseModel):
    '''
    tds | {trade_id: string,
           amount: {value: int, coin: string, decimal: int}
           fiat: float,  currency: string, challan: url,
           status: string}}
    '''
