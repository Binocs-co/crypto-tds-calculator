from pydantic import Field, BaseModel

from tds.calculator.models.binocs_model import BinocsModel

class TDSDetails(BaseModel):
    '''
    tds | {trade_id: string,
                                     amount: {value: int, coin: string, decimal: int}
                                     fiat: float,  currency: string, challan: url,
                                     status: string}}
    '''
