# livecryptowatch.py
# description: class used in PriceOracle.py

from requests import post
from ray import remote
from .generic_source import GenericSource

class Livecoinwatch(GenericSource):
    @remote
    def get_price(self, symbol:str, currency:str) -> dict or None:
        response = post(
            url=self.urls["livecoinwatch"]["price"].format(SYMBOL=symbol,CURRENCY=currency),
            headers={"x-api-key":"d960befc-10d2-4630-93cf-136f2e7f1558","content-type":"application/json"},
            json={"currency":currency.upper(),"code":symbol.upper(),"meta":True},
        )
        try:
            price = response.json()["rate"]
            return self.bundle_ouput("livecoinwatch", price)
        except KeyError:
            return None