import json

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
        code = '/m/03rjj'
        page = requests.get(f"https://news.google.com/covid19/map?mid={code}&hl=en-IN&gl=IN&ceid=IN%3Aen")
        soup = BeautifulSoup(page.content, "html.parser")
        vaccine_statistics = soup.find_all("div", {"class": "UvMayb"})
        total_does = vaccine_statistics[2].decode_contents().strip()
        vaccinated = vaccine_statistics[3].decode_contents().strip()

        vaccine_status = {
            "total_does": total_does,
            "vaccinated": vaccinated
        }
        print(f'{vaccine_status}')

        top_news = []
        articles = soup.find_all("article")
        for article in articles:
            thumbnail = article.find("img")["src"]
            thumbnail = thumbnail.split("=")
            a = article.find("h4").find("a")
            title = a.text
            source = f'https://news.google.com{a["href"].replace(".", "")}'
            top_news.append({
                "title": title,
                "source": source,
                "thumbnail": thumbnail[0]
            })
        results = {
            "vaccine_status": vaccine_status,
            "top_news": top_news
        }
        print(json.dumps(results))
        return Response({"status": "success"}, status=status.HTTP_200_OK)
