# livecryptowatch.py
# description: class used in PriceApi.py

from requests import post
from ray import remote
from .base_source import BaseSource
from .source_config import urls
from .config import LIVECOINWATCH_API_KEY

class Livecoinwatch(BaseSource):
    def __init__(self):
        self.price_url = urls["livecoinwatch"]["price"]

    @remote
    def get_price(self, symbol:str, currency:str) -> dict or None:
        response = post(
            url=self.price_url.format(SYMBOL=symbol,CURRENCY=currency),
            headers={"x-api-key":LIVECOINWATCH_API_KEY,"content-type":"application/json"},
            json={"currency":currency.upper(),"code":symbol.upper(),"meta":True},)
        try:
            price = response.json()["rate"]
            return self.bundle_ouput("livecoinwatch", price)
        except (KeyError, TypeError):
            return None