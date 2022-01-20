from django.shortcuts import render

from app.core.client.DBClient import DBClient


def index(request):
    with DBClient() as db_client:
        context = {
            "results": db_client.fetch_covid_statistics()
        }
    return render(request, 'index.html', context)


def parse_csv(request):
    return render(request, 'parse-csv.html')
