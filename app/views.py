from django.shortcuts import render

from app.core.clients.StatisticClient import StatisticClient


def index(request):

    with StatisticClient() as statistics_client:
        query = '{ statistics { edges { node { name flag statistics { area confirmed deaths recovered date } } } } }'
        payload = {"query": query}
        response = statistics_client.get_covid_statistics(body=payload).obj()
        # print(response.data.statistics.edges)
        context = {
            "statistics": response.data.statistics.edges
        }
    return render(request, 'index.html', context)


def parse_csv(request):
    return render(request, 'parse-csv.html')
