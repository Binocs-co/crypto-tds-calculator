from pydantic import Field, BaseModel
from tds.calculator.models.binocs_model import BinocsModel

class Amount(BaseModel):
    '''
        amount: [value: int, coin: string, decimal: int]}]
    '''
    value: int = Field(None)
    coin: str = Field(None)
    decimal: int = Field(None)
    coin_type: str = Field(None) #Fiat/VDA
