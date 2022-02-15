import os

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.core.clients.StatisticsClient import StatisticsClient
from app.core.utils import Utils
from app.models import TotalCases


def index(request):
    if bool(int(os.getenv('MAINTENANCE_ENABLED'))) is False:
        total_cases = TotalCases.objects.all()
        date = total_cases.last().date
        response = GetStatisticsByDate.get(request=request, date=date).data
        dates = []
        for total in total_cases:
            dates.append(total.date)
        context = {
            "total_cases": response['data']['totalCases']['edges'][0]['node'],
            "statistics": response['data']['countryStatistics'],
            "date": date,
            "all_dates": dates,
            "map_box_access_token": os.getenv('MAP_BOX_ACCESS_TOKEN')
        }
        return render(request, 'index.html', context)
    else:
        return render(request, 'maintenance.html')


class GetStatisticsByDate(APIView):

    @staticmethod
    def get(request, date):
        with StatisticsClient() as statistics_client:
            query = Utils.graphql_query(date=date)
            payload = {"query": query}
            response = statistics_client.get_covid_statistics(body=payload)
            return Response(response.json(), status=status.HTTP_200_OK, content_type="text/json")
