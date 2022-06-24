import math
from pydantic import Field, BaseModel
from tds.calculator.models.binocs_model import BinocsModel

class Amount(BaseModel):
    value: int = Field(None)
    coin: str = Field(None)
    decimal: int = Field(None)
    coin_type: str = Field(None) #Fiat/VDA

    def is_fiat(self):
        if coin_type == 'FIAT':
            return True
        return False

    def percent_amt(self, percent):
        percent_value = self.value * percent
        percent_decimal = self.decimal + 2 # = log10(100)
        percent_amt = Amount(percent_value, self.coin, percent_decimal, self.coin_type)
        return percent_amt

    def reduce_amt(self, deduct):
        if self.decimal < deduct.decimal:
            self.value = self.value * math.pow(10, (deduct.decimal - self.decimal))
            self.decimal = deduct.decimal
        elif self.decimal > deduct.decimal:
            logging.error('Incompatible Values') #TODO: add more detailed logging here
            return 1
        self.value -= deduct.value
        return 0
