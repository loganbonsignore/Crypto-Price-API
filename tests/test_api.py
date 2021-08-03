import pytest
import time
from api.app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_health(client):
    assert client.get("/health").status_code == 200

def test_price(client):
    query_strings = [
        "btc_usd,eth_gbp,dot_aud,ksm_jpy",
        ",KYL_uSd,wbtc_eur,,ksm_DOT,bt,c_usd",
        ".btc_usd,none_Btc,dot_eth,eth,log.an",
    ]
    for query in query_strings:
        assert client.get(f"/price/{query}").status_code == 200, f"error on: {query}"
        time.sleep(2)