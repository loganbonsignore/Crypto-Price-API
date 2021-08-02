# app.py
# description: aggregates cryptocurrency price data from ~7 different sources

from flask import Flask, Response, make_response
from .PriceOracle import PriceOracle
from .errors import errors

app = Flask(__name__)
app.register_blueprint(errors)
price_api = PriceOracle()

@app.route("/health")
def health():
    return Response("OK", status=200)

@app.route("/price/<pairs>")
def price(pairs):
    return_obj = {}
    for pair in pairs.split(","):
        symbol, currency = pair.split("_")
        return_obj[pair.lower()] = price_api.collect_price_data(symbol, currency)
    return make_response(return_obj, 200)