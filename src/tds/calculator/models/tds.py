from pydantic import Field, BaseModel

from tds.calculator.models.binocs_model import BinocsModel

class TDSDetail(BaseModel):
    '''
    tds | [{exchange_user_id: amount: [value: int, coin: string, decimal: int]}]
    '''
