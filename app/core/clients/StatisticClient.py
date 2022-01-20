from app.core.http.http_client import HTTPClient
from app.core.http.response import Response
from app.core.objects.statistics import StatisticsData


class StatisticClient(HTTPClient):
    def __init__(self):
        super().__init__()

    def get_covid_statistics(self, body) -> Response[StatisticsData]:
        return self.send_request(method='post', url=f'{self.url}/graphql/', payload=body, cls=StatisticsData)
