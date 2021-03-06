import pytest
from api.app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_health(client):
    assert client.get("/health").status_code == 200

def test_price_valid_query(client):
    query = "btc_usd,eth_gbp,dot_aud,ksm_jpy"
    assert client.get(f"/price/{query}").status_code == 200

def test_price_invalid_query_1(client):
    query = ".btc_usd,none_Btc,do_t_eth,eth,log.an"
    assert client.get(f"/price/{query}").status_code == 200

def test_price_invalid_query_2(client):
    query = ",KYL_uSd,wbtc_eur,,ksm_DOT,bt,c_usd"
    assert client.get(f"/price/{query}").status_code == 200

def test_price_none(client):
    query = "sam_usd" # returns price==None from Livecoinwatch (8/4/21)
    assert client.get(f"/price/{query}").status_code == 200