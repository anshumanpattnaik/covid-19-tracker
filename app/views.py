import re

import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.core.clients.StatisticsClient import StatisticsClient
from app.core.utils import Utils
from app.models import DateConfig, TotalCases


def index(request):
    with StatisticsClient() as statistics_client:
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
            "statistics": response.data.countryStatistics,
            "date": date,
            "all_dates": dates,
            "graphql_query": payload
        }
    return render(request, 'index.html', context)


class ParseCOVIDNews(APIView):

    def get(self, request):
        page = requests.get("https://news.google.com/covid19/map?mid=%2Fm%2F03rjj&hl=en-IN&gl=IN&ceid=IN%3Aen")
        soup = BeautifulSoup(page.content, "html.parser")
        vaccine_statistics = soup.find_all("div", {"class": "tZjT9b"})
        print(vaccine_statistics)

        top_news = soup.find_all("div", {"class": "D5tATe pym81b"})
        for top in top_news[0].findAll('a'):
            # print(f'{top}')
            print(f'{top.get("href")}')
            print(f'{top.text}')
            print()
        return Response({"status": "success"}, status=status.HTTP_200_OK)
