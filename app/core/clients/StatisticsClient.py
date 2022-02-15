from app.core.http.http_client import HTTPClient


class StatisticsClient(HTTPClient):
    def __init__(self):
        super().__init__()

    def get_covid_statistics(self, body):
        return self.send_request(url=f'{self.url}/graphql', payload=body)
