# binance.py
# description: class used in PriceApi.py

from requests import get
from ray import remote
from .base_source import BaseSource
from .source_config import urls

class Binance(BaseSource):
    def __init__(self):
        self.price_url = urls["binance"]["price"]
        self.token_list_url = urls["binance"]["tokens"]

    @remote
    def get_price(self, symbol:str, currency:str) -> dict or None:
        token_list = get(self.token_list_url).json()["symbols"]
        # set of quote assets available
        quote_assets = {token["quoteAsset"] for token in token_list}
        if currency.upper() not in quote_assets: return None
        # get price
        price_url = self.price_url.format(SYMBOL=symbol.upper(),CURRENCY=currency.upper()) # accepts only uppercase params
        response = get(price_url).json()
        try:
            price = response["price"]
            return self._bundle_ouput("binance", price)
        except (KeyError, TypeError):
            return None