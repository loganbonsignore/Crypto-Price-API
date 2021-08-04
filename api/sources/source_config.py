urls = {
    "coinbase": {
        "price": "https://api.pro.coinbase.com/products/{SYMBOL}-{CURRENCY}/ticker"
    },
    "coingecko": {
        "tokens": "https://api.coingecko.com/api/v3/coins/list",
        "price": "https://api.coingecko.com/api/v3/simple/price?ids={SYMBOL}&vs_currencies={CURRENCY}",
    },
    "binance": {
        "tokens": "https://api.binance.com/api/v3/exchangeInfo",
        "price": "https://api.binance.com/api/v3/ticker/price?symbol={SYMBOL}{CURRENCY}",
    },
    "bancor": {
        "tokens": "https://api-v2.bancor.network/tokens",
    },
    "kraken": {
        "price": "https://api.cryptowat.ch/markets/kraken/{SYMBOL}{CURRENCY}/price",
    },
    "bitfinex": {
        "price": "https://api.cryptowat.ch/markets/bitfinex/{SYMBOL}{CURRENCY}/price",
    },
    "cryptocompare": {
        "price": "https://min-api.cryptocompare.com/data/price?fsym={SYMBOL}&tsyms={CURRENCY}",
    },
    "livecoinwatch": {
        "price": "https://api.livecoinwatch.com/coins/single",
    },
}
