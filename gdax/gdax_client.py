import requests 
from settings import gdax_api_key, gdax_api_secret, gdax_api_passphrase
from coinbaseExchangeAuth import CoinbaseExchangeAuth
auth = CoinbaseExchangeAuth(gdax_api_key, gdax_api_secret, gdax_api_passphrase)

def getBalances():
    if gdax_api_key == '':
        return {}
    account = requests.get('https://api.gdax.com/accounts', auth=auth).json()
    balances = { row['currency']: float(row['balance']) for row in account if float(row['balance']) > 0 }
    return balances

def get_btc_eur_price():
    return float(requests.get('https://api.gdax.com/products/BTC-EUR/ticker').json()['price'])