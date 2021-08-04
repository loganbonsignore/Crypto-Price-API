# app.py
# description: aggregates cryptocurrency price data from ~7 different sources

from flask import Flask, Response, make_response
from .PriceApi import PriceApi
from datetime import datetime
from .errors import errors

price_api = PriceApi()
    
app = Flask(__name__)
app.register_blueprint(errors)

@app.route("/health")
def health():
    return Response("OK", status=200)

@app.route("/price/<pairs>")
def price(pairs):
    return_obj = {}
    for pair in pairs.split(","):
        try:
            symbol, currency = pair.split("_")
        except ValueError:
            continue
        return_obj[pair.lower()] = price_api.get_price_data(symbol, currency)
    return_obj["processed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return make_response(return_obj, 200)