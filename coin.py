import requests
url = 'https://rest.coinapi.io/v1/exchangerate/BTC/USD'
headers = {'X-CoinAPI-Key' : '28F9AFB2-142E-4F4E-A95B-68CEE518CFE1'}
response = requests.get(url, headers=headers)
