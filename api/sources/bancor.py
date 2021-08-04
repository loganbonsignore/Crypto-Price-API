# bancor.py
# description: class used in PriceApi.py

from requests import get
from ray import remote
from .base_source import BaseSource
from .source_config import urls

class Bancor(BaseSource):
    def __init__(self):
        self.price_url = urls["bancor"]["tokens"]

    @remote
    def get_price(self, symbol:str, currency:str) -> dict or None:
        tokens_available = get(self.price_url).json()
        filtered_token = filter(lambda x: x["symbol"]==symbol.upper(), tokens_available["data"])
        token = self.has_next(filtered_token)
        try:
            price = token["price"][currency.lower()]
            return self.bundle_ouput("bancor", price)
        except (KeyError, TypeError):
            return None