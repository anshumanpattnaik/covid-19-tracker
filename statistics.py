import json
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "covid19.settings")
django.setup()

from app.models import CovidStatistics, Country, States

# Delete all records
CovidStatistics.objects.all().delete()
Country.objects.all().delete()
States.objects.all().delete()

# Country Data
country_list = json.load(open('data/country_list.json'))

for data in country_list:
    country = data['country']
    code = data['code']
    flag = data['flag']
    latitude = data['coordinates'][0]
    longitude = data['coordinates'][1]

    # Save Country
    Country.objects.create(country_code=code, name=country, flag=flag, latitude=latitude, longitude=longitude)

data = json.load(open('data/data.json'))
date = '01-01-2022'
for i in data:
    country = i['Country_Region']
    state = i['Province_State']
    address = i['Combined_Key']

    confirmed = 0
    if i['Confirmed'] != 0 and isinstance(i['Confirmed'], int):
        confirmed = i['Confirmed']
    deaths = 0
    if i['Deaths'] != 0 and isinstance(i['Deaths'], int):
        deaths = i['Deaths']
    recovered = 0
    if i['Recovered'] != 0 and isinstance(i['Recovered'], int):
        recovered = i['Recovered']

    latitude = 0
    if i['Lat'] != 0 and isinstance(i['Lat'], float):
        latitude = i['Lat']
    longitude = 0
    if i['Long_'] != 0 and isinstance(i['Long_'], float):
        longitude = i['Long_']

    if len(country) > 1:
        try:
            statistics = CovidStatistics.objects.get(area=country)
            statistics.confirmed = confirmed
            statistics.deaths = deaths
            statistics.recovered = recovered
            statistics.save()
        except CovidStatistics.DoesNotExist:
            country_statistics = CovidStatistics.objects.create(area=country, address=address, confirmed=confirmed,
                                                                deaths=deaths, recovered=recovered, date=date)
            try:
                country_data = Country.objects.get(name=country)
                country_data.statistics.add(country_statistics)
            except Country.DoesNotExist:
                pass

    # if len(country) > 1 and len(state) > 1:
    #     state_statistics = CovidStatistics.objects.create(area=state, address=address, confirmed=confirmed,
    #                                                       deaths=deaths, recovered=recovered, date=date)
    #     try:
    #         country_data = Country.objects.get(name=country)
    #         state_data = States.objects.create(name=state, latitude=latitude, longitude=longitude)
    #         state_data.country.add(country_data)
    #         state_data.statistics.add(state_statistics)
    #     except Country.DoesNotExist:
    #         pass
