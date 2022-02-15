import json
import os

import requests


class HTTPClient:

    def __init__(self, url=os.getenv('API_ENDPOINT')):
        self.url = url

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @staticmethod
    def send_request(url, payload=None):
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.post(url=url, data=json.dumps(payload), headers=headers)
        return response
