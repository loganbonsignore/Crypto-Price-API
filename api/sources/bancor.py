# bancor.py
# description: class used in PriceOracle.py

from requests import get
from ray import remote
from .generic_source import GenericSource

class Bancor(GenericSource):
    @remote
    def get_price(self, symbol:str, currency:str) -> dict or None:
        url = self.urls["bancor"]["tokens"]
        tokens_available = get(url).json()
        filtered_token = filter(lambda x: x["symbol"]==symbol.upper(), tokens_available["data"])
        token = self.has_next(filtered_token)
        if token is None: return None
        try:
            price = token["price"][currency.lower()]
            return self.bundle_ouput("bancor", price)
        except KeyError:
            return None