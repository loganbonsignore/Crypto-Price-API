# coinbase.py
# description: class used in PriceOracle.py

from requests import get
from ray import remote
from .generic_source import GenericSource

class Coinbase(GenericSource):
    @remote
    def get_price(self, symbol:str, currency:str) -> dict or None:
        url = self.urls["coinbase"]["price"].format(SYMBOL=symbol,CURRENCY=currency) # accepts upper and lower case params
        response = get(url).json()
        try:
            price = response["price"]
            return self.bundle_ouput("coinbase", price)
        except KeyError:
            return None