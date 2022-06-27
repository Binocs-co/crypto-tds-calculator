import math
from pydantic import Field, BaseModel
from tds.calculator.models.binocs_model import BinocsModel
from tds.calculator.common.logger import get_logger

class Amount(BaseModel):
    value: int = Field(None)
    coin: str = Field(None)
    decimal: int = Field(None)
    coin_type: str = Field(None) #Fiat/VDA
 
    def is_fiat(self):
        if self.coin_type == 'FIAT':
            return True
        return False

    def percent_amt(self, percent):
        percent_value = self.value * percent
        percent_decimal = self.decimal + 2 # = log10(100)
        percent_amt = Amount(value = percent_value, coin = self.coin, decimal = percent_decimal, coin_type = self.coin_type)
        return percent_amt

    def reduce_amt(self, deduct):
        logger = get_logger(__name__)
        if self.decimal < deduct.decimal:
            self.value = self.value * math.pow(10, (deduct.decimal - self.decimal))
            self.decimal = deduct.decimal
        elif self.decimal > deduct.decimal:
            logger.error('Incompatible Values') #TODO: add more detailed logging here
            return 1
        self.value -= deduct.value
        return 0
