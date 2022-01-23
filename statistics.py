import json
import os

import django

from datetime import date

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "covid19.settings")
django.setup()

from app.models import CovidStatistics, Country, States

# Country Data
country_list = json.load(open('data/country_list.json'))

data = json.load(open('data/2022-01-01.json'))
date = date(2022, 1, 1)

# CovidStatistics.objects.all().delete()
# Country.objects.all().delete()
# States.objects.all().delete()
#
# for c in country_list:
#     country = c['country']
#     code = c['code']
#     flag = c['flag']
#     latitude = c['coordinates'][0]
#     longitude = c['coordinates'][1]
#     Country.objects.create(country_code=code, name=country, flag=flag, latitude=latitude, longitude=longitude)


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

    # if len(country) > 1:
    #     try:
    #         print('INSIDE = {:<35}{:<35}{:<15}{:<15}'.format(country, confirmed, deaths, recovered))
    #         statistics = CovidStatistics.objects.get(area=country, date=date)
    #         statistics.confirmed += confirmed
    #         statistics.deaths += deaths
    #         statistics.recovered += recovered
    #         statistics.save()
    #     except CovidStatistics.DoesNotExist:
    #         print('\n')
    #         print('OUTSIDE = {:<35}{:<15}{:<15}{:<15}'.format(country, confirmed, deaths, recovered))
    #         country_statistics = CovidStatistics.objects.create(area=country, address=address, confirmed=confirmed,
    #                                                             deaths=deaths, recovered=recovered, date=date)
    #         try:
    #             country_data = Country.objects.get(name=country)
    #             country_data.statistics.add(country_statistics)
    #         except Country.DoesNotExist:
    #             pass

    if len(country) > 1 and len(state) > 1:
        print('STATE = {:<25}{:<35}{:<15}{:<15}{:<15}'.format(country, state, confirmed, deaths, recovered))
        try:
            state_statistics = CovidStatistics.objects.get(area=state, date=date)
            state_statistics.confirmed += confirmed
            state_statistics.deaths += deaths
            state_statistics.recovered += recovered
            state_statistics.save()
        except CovidStatistics.DoesNotExist:
            state_statistics = CovidStatistics.objects.create(area=state, address=address, confirmed=confirmed,
                                                              deaths=deaths, recovered=recovered, date=date)
            country_data = Country.objects.get(name=country)
            state_data = States.objects.create(name=state, latitude=latitude, longitude=longitude, date=date)
            state_data.country.add(country_data)
            state_data.statistics.add(state_statistics)
