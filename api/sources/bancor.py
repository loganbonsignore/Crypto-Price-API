# bancor.py
# description: class used in PriceOracle.py

from requests import get
from ray import remote
from .base_source import BaseSource

class Bancor(BaseSource):
    @remote
    def get_price(self, symbol:str, currency:str) -> dict or None:
        url = self.urls["bancor"]["tokens"]
        tokens_available = get(url).json()
        filtered_token = filter(lambda x: x["symbol"]==symbol.upper(), tokens_available["data"])
        token = self._has_next(filtered_token)
        if token is None: return None
        try:
            price = token["price"][currency.lower()]
            return self._bundle_ouput("bancor", price)
        except KeyError:
            return None