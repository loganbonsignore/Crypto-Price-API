# PriceFetcher.py
# description: class used in PriceOracle.py

from requests import get, post
from ray import remote
from .urls import urls

class PriceFetcher:
    @remote
    def coinbase(self, symbol:str, currency:str) -> dict or None:
        url = urls["coinbase"]["price"].format(SYMBOL=symbol,CURRENCY=currency) # accepts upper and lower case params
        response = get(url).json()
        try:
            price = response["price"]
            return self.bundle_ouput("coinbase", price)
        except KeyError:
            return None

    @remote
    def coingecko(self, symbol:str, currency:str) -> dict or None:
        # normalize symbol (ex: btc -> bitcoin)
        coin_list_url = urls["coingecko"]["tokens"]
        token_list = get(coin_list_url).json()
        filtered_token = filter(lambda x: x["symbol"]==symbol.lower(), token_list)
        token = self.has_next(filtered_token)
        if token is None: return None
        # get price
        price_url = urls["coingecko"]["price"].format(SYMBOL=symbol,CURRENCY=currency)
        response = get(price_url).json()
        try:
            price = response[token["id"]][currency.lower()]
            return self.bundle_ouput("coingecko", price)
        except KeyError:
            return None
    
    @remote
    def binance(self, symbol:str, currency:str) -> dict or None:
        token_list_url = urls["binance"]["tokens"]
        token_list = get(token_list_url).json()["symbols"]
        # list of quote assets available
        quote_assets = {token["quoteAsset"] for token in token_list}
        if currency.upper() not in quote_assets: return None
        # get price
        price_url = urls["binance"]["price"].format(SYMBOL=symbol.upper(),CURRENCY=currency.upper()) # accepts only uppercase params
        response = get(price_url).json()
        try:
            price = response["price"]
            return self.bundle_ouput("binance", price)
        except KeyError:
            return None

    @remote
    def bancor(self, symbol:str, currency:str) -> dict or None:
        url = urls["bancor"]["tokens"]
        tokens_available = get(url).json()
        filtered_token = filter(lambda x: x["symbol"]==symbol.upper(), tokens_available["data"])
        token = self.has_next(filtered_token)
        if token is None: return None
        try:
            price = token["price"][currency.lower()]
            return self.bundle_ouput("bancor", price)
        except KeyError:
            return None

    @remote
    def kraken(self, symbol:str, currency:str) -> dict or None:
        url = urls["kraken"]["price"].format(SYMBOL=symbol,CURRENCY=currency) # accepts upper and lower case params
        response = get(url).json()
        try:
            price = response["result"]["price"]
            return self.bundle_ouput("kraken", price)
        except KeyError:
            return None
    
    @remote
    def bitfinex(self, symbol:str, currency:str) -> dict or None:
        url = urls["bitfinex"]["price"].format(SYMBOL=symbol,CURRENCY=currency) # accepts upper and lower case params
        response = get(url).json()
        try:
            price = response["result"]["price"]
            return self.bundle_ouput("bitfinex", price)
        except KeyError:
            return None
        
    @remote
    def cryptocompare(self, symbol:str, currency:str) -> dict or None:
        url = urls["cryptocompare"]["price"].format(SYMBOL=symbol,CURRENCY=currency) # accepts upper and lower case params
        response = get(url).json()
        try:
            price = response[currency.upper()]
            return self.bundle_ouput("cryptocompare", price)
        except KeyError:
            return None

    @remote
    def livecoinwatch(self, symbol:str, currency:str) -> dict or None:
        response = post(
            url=urls["livecoinwatch"]["price"].format(SYMBOL=symbol,CURRENCY=currency),
            headers={"x-api-key":"d960befc-10d2-4630-93cf-136f2e7f1558","content-type":"application/json"},
            json={"currency":currency.upper(),"code":symbol.upper(),"meta":True},
        )
        try:
            price = response.json()["rate"]
            return self.bundle_ouput("livecoinwatch", price)
        except KeyError:
            return None

    def bundle_ouput(self, source:str, price:str) -> dict:
        return {
            "source": source,
            "price": float(price),
        }
    
    def has_next(self, generator: object) -> object or None:
        try:
            first = next(generator)
        except StopIteration:
            return None
        return first