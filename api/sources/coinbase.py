# coinbase.py
# description: class used in PriceApi.py

from requests import get
from ray import remote
from .base_source import BaseSource
from .source_config import urls

class Coinbase(BaseSource):
    def __init__(self):
        self.price_url = urls["coinbase"]["price"]

    @remote
    def get_price(self, symbol:str, currency:str) -> dict or None:
        url = self.price_url.format(SYMBOL=symbol,CURRENCY=currency) # accepts upper and lower case params
        response = get(url).json()
        try:
            price = response["price"]
            return self._bundle_ouput("coinbase", price)
        except KeyError:
            return None