# generic_source.py
# description: class used in PriceOracle.py

from .source_config import urls

class GenericSource:
    def __init__(self):
        self.urls = urls

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