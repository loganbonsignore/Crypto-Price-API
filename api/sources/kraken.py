# kraken.py
# description: class used in PriceOracle.py

from requests import get
from ray import remote
from .base_source import BaseSource

class Kraken(BaseSource):
    @remote
    def get_price(self, symbol:str, currency:str) -> dict or None:
        url = self.urls["kraken"]["price"].format(SYMBOL=symbol,CURRENCY=currency) # accepts upper and lower case params
        response = get(url).json()
        try:
            price = response["result"]["price"]
            return self._bundle_ouput("kraken", price)
        except KeyError:
            return None