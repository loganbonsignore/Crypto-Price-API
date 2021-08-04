# kraken.py
# description: class used in PriceApi.py

from requests import get
from ray import remote
from .base_source import BaseSource
from .source_config import urls

class Kraken(BaseSource):
    def __init__(self):
        self.price_url = urls["kraken"]["price"]

    @remote
    def get_price(self, symbol:str, currency:str) -> dict or None:
        url = self.price_url.format(SYMBOL=symbol,CURRENCY=currency) # accepts upper and lower case params
        response = get(url).json()
        try:
            price = response["result"]["price"]
            return self.bundle_ouput("kraken", price)
        except (KeyError, TypeError):
            return None