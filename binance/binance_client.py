import requests
from settings import binance_api_key, binance_api_secret
from binanceExchangeAuth import BinanceExchangeAuth
auth = BinanceExchangeAuth(binance_api_key, binance_api_secret)

def getBalances():
    if binance_api_key == '':
        return {}
    response = requests.get('https://api.binance.com/api/v3/account', auth=auth).json()
    balances = {b['asset']: float(b['free']) for b in response['balances'] if float(b['free']) != 0}
    return balances

def get_all_prices():
    return requests.get('https://api.binance.com/api/v1/ticker/allPrices').json()