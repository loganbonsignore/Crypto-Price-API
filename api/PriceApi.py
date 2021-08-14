# PriceApi.py
# description: class used in app.py

import ray
from .sources.coinbase import Coinbase
from .sources.coingecko import Coingecko
from .sources.binance import Binance
from .sources.bancor import Bancor
from .sources.kraken import Kraken
from .sources.bitfinex import Bitfinex
from .sources.cryptocompare import Cryptocompare
try:
    from .sources.livecryptowatch import Livecoinwatch
except ModuleNotFoundError:
    print("Add LIVECOINWATCH_API_KEY = <YOUR LIVECOINWATCH API KEY> to api/sources/config.py to active Live Coin Watch as a source.")

ray.init(ignore_reinit_error=True, include_dashboard=False, log_to_driver=False)

class PriceApi:
    def __init__(self):
        self.sources = {Coinbase, Coingecko, Binance, Bancor, Kraken, Bitfinex, Cryptocompare}
        if "Livecoinwatch" in globals(): self.sources.add(Livecoinwatch)

    def get_price_data(self, symbol:str, currency:str) -> list:
        remote_processes = [source().get_price.remote(source(), symbol, currency) for source in self.sources]
        results = ray.get(remote_processes)
        return [result for result in results if result != None]