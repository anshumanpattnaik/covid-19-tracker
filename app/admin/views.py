import time

import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.admin.countries import COUNTRY
from app.models import TotalCases, Country, CovidStatistics

DAILY_REPORTS_BASE_URL = 'https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports'
CSV_FILE_PATH = '/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_daily_reports/'


def admin_panel_view(request):
    page = requests.get(DAILY_REPORTS_BASE_URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    csv_file_list = []
    for link in soup.find_all('a'):
        href = link.get('href')
        data = {}
        if '.csv' in href:
            csv_file_name = href.replace(CSV_FILE_PATH, "")
            csv_file_name = csv_file_name.replace(".csv", "")
            try:
                TotalCases.objects.get(date=csv_file_name)
                sync_status = 'Synced'
            except TotalCases.DoesNotExist:
                sync_status = 'Not Synced'
            data['csv_file'] = csv_file_name
            data['sync_status'] = sync_status
            csv_file_list.append(data)

    csv_file_list.sort(key=lambda x: time.mktime(time.strptime(x['csv_file'], "%m-%d-%Y")))
    csv_file_list.reverse()
    context = {
        "csv_list": csv_file_list
    }
    return render(request, 'admin-panel.html', context)


class AddCountries(APIView):

    def post(self, request):
        data = COUNTRY.COUNTRIES
        for c in data:
            Country.objects.create(code=c['code'], name=c['country'], flag=c['flag'], coordinates=c['coordinates'])
        return Response({"status": "success"}, status=status.HTTP_200_OK)


class AddStatistics(APIView):

    def post(self, request):
        try:
            TotalCases.objects.get(date=request.data['date'])
            print("{:<10}|{:<25}".format(request.data['date'], "ALREADY EXISTS"))
            print()
            return Response({"status": "Statistics already exists"}, status=status.HTTP_200_OK)
        except TotalCases.DoesNotExist:
            total_confirmed = request.data['total_confirmed']
            total_deaths = request.data['total_deaths']
            total_recovered = request.data['total_recovered']
            date = request.data['date']
            TotalCases.objects.create(total_confirmed=total_confirmed, total_deaths=total_deaths,
                                      total_recovered=total_recovered, date=date)

            countries = request.data['countries']
            for c in countries:
                country = c['country']
                country_name = country['name']
                confirmed = country['confirmed']
                deaths = country['deaths']
                recovered = country['recovered']

                try:
                    covid_statistics = CovidStatistics.objects.get(area=country_name, date=date)
                    covid_statistics.confirmed += confirmed
                    covid_statistics.deaths += deaths
                    covid_statistics.recovered += recovered
                    covid_statistics.save()
                except CovidStatistics.DoesNotExist:
                    country_statistics = CovidStatistics.objects.create(area=country_name, confirmed=confirmed,
                                                                        deaths=deaths, recovered=recovered, date=date)
                    try:
                        country_data = Country.objects.get(name=country_name)
                        country_data.statistics.add(country_statistics)
                    except Country.DoesNotExist:
                        pass
            print("{:<10}|{:<25}".format(request.data['date'], "COMPLETED"))
            print("\n")
            return Response({"status": "success", "data": request.data}, status=status.HTTP_200_OK)
