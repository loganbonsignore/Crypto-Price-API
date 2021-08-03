# PriceHandler.py
# description: class used in app.py

import ray
from .PriceFetcher import PriceFetcher

ray.init(ignore_reinit_error=True, include_dashboard=False, log_to_driver=False)

class PriceOracle:
    def __init__(self):
        self.sources = [
            PriceFetcher.coinbase,
            PriceFetcher.coingecko, 
            PriceFetcher.binance, 
            PriceFetcher.bancor, 
            PriceFetcher.kraken, 
            PriceFetcher.bitfinex, 
            PriceFetcher.cryptocompare, 
            PriceFetcher.livecoinwatch, 
        ]

    def collect_price_data(self, symbol:str, currency:str) -> list:
        price_fetcher = PriceFetcher()
        remote_processes = [func.remote(price_fetcher, symbol, currency) for func in self.sources]
        results = ray.get(remote_processes)
        return [result for result in results if result != None]