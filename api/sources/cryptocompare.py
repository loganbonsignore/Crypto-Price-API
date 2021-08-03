# cryptocompare.py
# description: class used in PriceOracle.py

from requests import get
from ray import remote
from .base_source import BaseSource
from .source_config import urls

class Cryptocompare(BaseSource): 
    def __init__(self):
        self.price_url = urls["cryptocompare"]["price"]

    @remote
    def get_price(self, symbol:str, currency:str) -> dict or None:
        url = self.price_url.format(SYMBOL=symbol,CURRENCY=currency) # accepts upper and lower case params
        response = get(url).json()
        try:
            price = response[currency.upper()]
            return self._bundle_ouput("cryptocompare", price)
        except KeyError:
            return None