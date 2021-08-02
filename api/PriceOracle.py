# PriceHandler.py
# description: class used in app.py

import ray
from .PriceHandler import PriceHandler

price_handler = PriceHandler()
ray.init(ignore_reinit_error=True, include_dashboard=False, log_to_driver=False)

class PriceOracle:
    def __init__(self):
        self.sources = [
            PriceHandler.coinbase,
            PriceHandler.coingecko, 
            PriceHandler.binance, 
            PriceHandler.bancor, 
            PriceHandler.kraken, 
            PriceHandler.bitfinex, 
            PriceHandler.cryptocompare, 
            PriceHandler.livecoinwatch, 
        ]

    def collect_price_data(self, symbol:str, currency:str) -> list:
        remote_processes = [func.remote(price_handler, symbol, currency) for func in self.sources]
        results = ray.get(remote_processes)
        return [result for result in results if result != None]