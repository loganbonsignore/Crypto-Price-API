# livecryptowatch.py
# description: class used in PriceOracle.py

from requests import post
from ray import remote
from .generic_source import GenericSource
from ..config import LIVECOINWATCH_API_KEY

class Livecoinwatch(GenericSource):
    @remote
    def get_price(self, symbol:str, currency:str) -> dict or None:
        response = post(
            url=self.urls["livecoinwatch"]["price"].format(SYMBOL=symbol,CURRENCY=currency),
            headers={"x-api-key":LIVECOINWATCH_API_KEY,"content-type":"application/json"},
            json={"currency":currency.upper(),"code":symbol.upper(),"meta":True},
        )
        try:
            price = response.json()["rate"]
            return self.bundle_ouput("livecoinwatch", price)
        except KeyError:
            return None