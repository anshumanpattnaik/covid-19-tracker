import json
import os

import requests
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.core.clients.StatisticsClient import StatisticsClient
from app.core.utils import Utils
from app.models import TotalCases, Country, CovidStatistics
from app.serializers import TotalCasesSerializer, CountrySerializer


def index(request):
    if bool(int(os.getenv('MAINTENANCE_ENABLED'))) is False:
        total_cases = TotalCases.objects.all()
        date = total_cases.last().date
        response = GetStatisticsByDate.get(request=request, date=date).data
        dates = []
        for total in total_cases:
            dates.append(total.date)
        context = {
            "total_cases": response["total_cases"],
            "statistics": response["country_statistics"],
            "date": date,
            "all_dates": dates,
            "map_box_access_token": os.getenv('MAP_BOX_ACCESS_TOKEN')
        }
        return render(request, 'index.html', context)
    else:
        response = requests.get("https://api.covid19tracker.info/graphql#query=query%20%7B%0A%20%20totalCases(date%3A%20%2202-12-2022%22)%20%7B%0A%20%20%20%20edges%20%7B%0A%20%20%20%20%20%20node%20%7B%0A%20%20%20%20%20%20%20%20totalConfirmed%0A%20%20%20%20%20%20%20%20totalDeaths%0A%20%20%20%20%20%20%20%20totalRecovered%0A%20%20%20%20%20%20%20%20date%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%20%20countryStatistics%20%7B%0A%20%20%20%20name%0A%20%20%20%20code%0A%20%20%20%20flag%0A%20%20%20%20coordinates%0A%20%20%20%20statistics(date%3A%20%2202-12-2022%22)%20%7B%0A%20%20%20%20%20%20edges%20%7B%0A%20%20%20%20%20%20%20%20node%20%7B%0A%20%20%20%20%20%20%20%20%20%20area%0A%20%20%20%20%20%20%20%20%20%20confirmed%0A%20%20%20%20%20%20%20%20%20%20deaths%0A%20%20%20%20%20%20%20%20%20%20recovered%0A%20%20%20%20%20%20%20%20%20%20date%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D")
        return render(request, 'maintenance.html')


class GetStatisticsByDate(APIView):

    @staticmethod
    def get(request, date):
        country_statistics = []
        try:
            total_cases = TotalCases.objects.get(date=date)
            total_cases_serializer = TotalCasesSerializer(total_cases)
            country_all = Country.objects.all()
            for country in country_all:
                try:
                    statistics = CovidStatistics.objects.filter(area=country.name, date=date)
                    country.statistics.set(statistics)
                    country_serializer = CountrySerializer(country)
                    country_statistics.append(json.loads(json.dumps(country_serializer.data)))
                except CovidStatistics.DoesNotExist:
                    pass
            response = {
                "total_cases": total_cases_serializer.data,
                "country_statistics": country_statistics
            }
            return Response(response, status=status.HTTP_200_OK, content_type="text/json")
        except TotalCases.DoesNotExist:
            return Response({'error': 'oops! nothing Found'}, status=status.HTTP_404_NOT_FOUND)
