# coingecko.py
# description: class used in PriceOracle.py

from requests import get
from ray import remote
from .base_source import BaseSource
from .source_config import urls

class Coingecko(BaseSource):
    def __init__(self):
        self.token_list_url = urls["coingecko"]["tokens"]
        self.price_url = urls["coingecko"]["price"]

    @remote
    def get_price(self, symbol:str, currency:str) -> dict or None:
        if symbol in ["btc", "BTC"]: symbol = "WBTC"
        # normalize symbol (ex: btc -> bitcoin)
        token_list = get(self.token_list_url).json()
        filtered_token = filter(lambda x: x["symbol"]==symbol.lower(), token_list)
        token = self._has_next(filtered_token)
        if token is None: return None
        # get price
        price_url = self.price_url.format(SYMBOL=symbol,CURRENCY=currency)
        response = get(price_url).json()
        try:
            price = response[token["id"]][currency.lower()]
            return self._bundle_ouput("coingecko", price)
        except KeyError:
            return None