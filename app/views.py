from django.shortcuts import render

from app.core.clients.StatisticClient import StatisticClient


def index(request):
    with StatisticClient() as statistics_client:
        date = "2022-01-01"

        query_1 = '{ statistics { name flag latitude longitude '
        statistics_query = f'statistics(date: "{date}") '
        query_2 = '{ edges { node { area confirmed deaths recovered date } } } } }'
        query = f'{query_1}{statistics_query}{query_2}'
        payload = {"query": query}
        response = statistics_client.get_covid_statistics(body=payload).obj()
        context = {
            "statistics": response.data.statistics,
            "date": date
        }
    return render(request, 'index.html', context)


def parse_csv(request):
    return render(request, 'parse-csv.html')

