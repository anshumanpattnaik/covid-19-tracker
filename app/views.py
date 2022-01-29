from django.shortcuts import render

from app.core.clients.StatisticClient import StatisticClient
from app.core.utils import Utils
from app.models import DateConfig, TotalCases


def index(request):
    with StatisticClient() as statistics_client:
        date = DateConfig.objects.all()[0].date
        query = Utils.graphql_query(date=date)
        payload = {"query": query}
        response = statistics_client.get_covid_statistics(body=payload).obj()
        total_cases = TotalCases.objects.all()
        dates = []
        for total in total_cases:
            dates.append(total.date)
        context = {
            "total_cases": response.data.totalCases.edges[0].node,
            "statistics": response.data.statistics,
            "date": date,
            "all_dates": dates,
            "graphql_query": payload
        }
    return render(request, 'index.html', context)
