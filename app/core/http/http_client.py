import os

import requests

from .response import Response


class HTTPClient:

    def __init__(self, url=f'https://api.covid19tracker.info/'):
        self.url = url

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @staticmethod
    def send_request(method, url, payload=None, cls=None):
        session = requests.Session()
        if method == 'post':
            response = session.request(method, url, json=payload)
            print(response)
            return Response(response, cls)
        return Response(session.request(method, url), cls)