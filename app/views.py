from django.shortcuts import render

from app.core.clients.StatisticClient import StatisticClient
from app.models import CovidStatistics, Country, States


def index(request):
    # countries = Country.objects.all()
    # for country in countries:
    #     print(country.name)

    with StatisticClient() as statistics_client:
        query = '{ statistics { name flag latitude longitude statistics { confirmed deaths recovered date } } }'
        payload = {"query": query}
        response = statistics_client.get_covid_statistics(body=payload).obj()
        # print(response.data.statistics.edges)
        context = {
            "statistics": response.data.statistics
        }
    return render(request, 'index.html', context)


def parse_csv(request):
    return render(request, 'parse-csv.html')
