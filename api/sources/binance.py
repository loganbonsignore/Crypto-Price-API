# binance.py
# description: class used in PriceOracle.py

from requests import get
from ray import remote
from .generic_source import GenericSource
    
class Binance(GenericSource):
    @remote
    def get_price(self, symbol:str, currency:str) -> dict or None:
        token_list_url = self.urls["binance"]["tokens"]
        token_list = get(token_list_url).json()["symbols"]
        # list of quote assets available
        quote_assets = {token["quoteAsset"] for token in token_list}
        if currency.upper() not in quote_assets: return None
        # get price
        price_url = self.urls["binance"]["price"].format(SYMBOL=symbol.upper(),CURRENCY=currency.upper()) # accepts only uppercase params
        response = get(price_url).json()
        try:
            price = response["price"]
            return self.bundle_ouput("binance", price)
        except KeyError:
            return None