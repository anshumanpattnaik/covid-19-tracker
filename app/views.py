import json
import os

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import TotalCases, Country, CovidStatistics
from app.serializers import TotalCasesSerializer, CountrySerializer


def index(request):
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
