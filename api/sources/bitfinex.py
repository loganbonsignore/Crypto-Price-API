# bitfinex.py
# description: class used in PriceApi.py

from requests import get
from ray import remote
from .base_source import BaseSource
from .source_config import urls

class Bitfinex(BaseSource): 
    def __init__(self):
        self.price_url = urls["bitfinex"]["price"]

    @remote
    def get_price(self, symbol:str, currency:str) -> dict or None:
        url = self.price_url.format(SYMBOL=symbol,CURRENCY=currency) # accepts upper and lower case params
        response = get(url).json()
        try:
            price = response["result"]["price"]
            return self._bundle_ouput("bitfinex", price)
        except KeyError:
            return None