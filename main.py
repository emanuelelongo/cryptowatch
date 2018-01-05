import requests 
from settings import totalInvested, offlineBalances
from gdax import gdax_client
from binance import binance_client
from gui import Gui

def check():
    gdax_balances = gdax_client.getBalances()
    binance_balances = binance_client.getBalances()

    currencies = set(dict.keys(gdax_balances)) | set(dict.keys(binance_balances)) | set(dict.keys(offlineBalances))
    balances = { c: gdax_balances.get(c, 0) + binance_balances.get(c, 0) + offlineBalances.get(c, 0) for c in currencies }

    prices_raw_data = binance_client.get_all_prices()
    btc_eur_price = gdax_client.get_btc_eur_price()
    
    prices = { p['symbol'][:3] : float(p['price']) * btc_eur_price for p in prices_raw_data if p['symbol'][-3:]=='BTC'}
    prices['BTC'] = btc_eur_price
    prices['EUR'] = 1

    balancesInEur = { c: prices[c] * balances.get(c, 0) for c in currencies }
    totalInEur = sum([balancesInEur[k] for k in balancesInEur])
    return balances, prices, balancesInEur, totalInEur

gui = Gui(totalInvested, lambda: check())
gui.render()