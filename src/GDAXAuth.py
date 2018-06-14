import hmac, hashlib, time, base64
from requests.auth import AuthBase


class GDAXAuth(AuthBase):

    def __init__(self, api_key, secret_key, passPhrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passPhrase = passPhrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or '')

        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message.encode('utf-8'), hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest())

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passPhrase,
            'Content-Type': 'application/json'
        })

        return request
