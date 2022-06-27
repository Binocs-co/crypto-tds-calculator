
class BinocsId(object):
    def __init__(self, id):
        self.id = id

    def __composite_values__(self):
        return self.id

    def __repr__(self):
        return f"BinocsId(id={self.id!r})"

    def __eq__(self, other):
        return (
            isinstance(other, BinocsId)
            and other.id == self.id
        )

    def __ne__(self, other):
        return not self.__eq__(other)

class TDSDetails(object):
    def __init__(self, amount, fiat, currency, challan, status):
        self.amount = amount
        self.fiat = fiat
        self.currency = currency
        self.challan = challan
        self.status = status

    @classmethod
    def _generate(self, value, coin, decimal, coin_type, fiat, currency, challan, status):
        return TDSDetails(
            Amount(value, coin, decimal, coin_type), fiat, currency, challan, status
        )

    def __composite_values__(self):
        return self.fiat, self.currency, self.challan, self.status
            #self.amount.__composite_values__() + \
            

    def __repr__(self):
        return f"TDSDetails(amount={self.amount!r}, fiat={self.fiat!r}, currency={self.currency!r}, challan={self.challan!r}, status={self.status!r})"

    def __eq__(self, other):
        return (
            isinstance(other, TDSDetails)
            and other.amount == self.amount
            and other.fiat == self.fiat
            and other.currency == self.currency
            and other.challan == self.challan
            and other.status == self.status
        )

    def __ne__(self, other):
        return not self.__eq__(other)

class Amount(object):
    def __init__(self, value, coin, decimal, coin_type):
        self.value = value
        self.coin = coin
        self.decimal = decimal
        self.coin_type = coin_type

    def __composite_values__(self):
        return self.value, self.coin, self.decimal, self.coin_type

    def __repr__(self):
        return f"Amount(value={self.value!r}, coin={self.coin!r}, decimal={self.decimal!r}, coin_type={self.coin_type!r})"

    def __eq__(self, other):
        return (
            isinstance(other, Amount)
            and other.value == self.value
            and other.coin == self.coin
            and other.decimal == self.decimal
            and other.coin_type == self.coin_type
        )

    def __ne__(self, other):
        return not self.__eq__(other)