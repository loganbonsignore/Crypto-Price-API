# coingecko.py
# description: class used in PriceOracle.py

from requests import get
from ray import remote
from .generic_source import GenericSource

class Coingecko(GenericSource):
    @remote
    def get_price(self, symbol:str, currency:str) -> dict or None:
        # normalize symbol (ex: btc -> bitcoin)
        coin_list_url = self.urls["coingecko"]["tokens"]
        token_list = get(coin_list_url).json()
        filtered_token = filter(lambda x: x["symbol"]==symbol.lower(), token_list)
        token = self.has_next(filtered_token)
        if token is None: return None
        # get price
        price_url = self.urls["coingecko"]["price"].format(SYMBOL=symbol,CURRENCY=currency)
        response = get(price_url).json()
        try:
            price = response[token["id"]][currency.lower()]
            return self.bundle_ouput("coingecko", price)
        except KeyError:
            return None