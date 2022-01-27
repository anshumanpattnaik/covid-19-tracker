from django.shortcuts import render

from app.core.clients.StatisticClient import StatisticClient


def index(request):
    with StatisticClient() as statistics_client:
        date = "01-25-2022"

        total_cases_query_1 = f'totalCases(date: "{date}")'
        total_cases_query_2 = '{ edges { node { totalConfirmed, totalDeaths, totalRecovered, date } } }'
        query_2 = ' statistics { name flag coordinates '
        statistics_query = f'statistics(date: "{date}") '
        query_3 = '{ edges { node { area confirmed deaths recovered date } } } }'
        query = f'{total_cases_query_1}{total_cases_query_2}{query_2}{statistics_query}{query_3}'
        payload = {"query": "{" + query + "}"}
        response = statistics_client.get_covid_statistics(body=payload).obj()
        context = {
            "total_cases": response.data.totalCases.edges[0].node,
            "statistics": response.data.statistics,
            "date": date
        }
    return render(request, 'index.html', context)


def parse_csv(request):
    return render(request, 'parse-csv.html')
