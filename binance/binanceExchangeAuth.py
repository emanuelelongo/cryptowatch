import json, hmac, hashlib, requests, time, base64, urllib
from requests.auth import AuthBase

class BinanceExchangeAuth(AuthBase):
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def __call__(self, request):
        timestamp = int(round(time.time() * 1000.0))
        request.prepare_url(request.url, dict(
            timestamp=timestamp
        ))
        query = request.path_url.split('?')[1]
        message = urllib.unquote(query + (request.body or ''))
        signature = hmac.new(self.api_secret, message, hashlib.sha256).hexdigest()
        
        request.prepare_url(request.url, dict(
            signature=signature
        ))

        request.headers.update({
            'X-MBX-APIKEY': self.api_key,
            'Content-Type': 'application/json'
        })
        return request