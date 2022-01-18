import json
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "covid19.settings")
django.setup()

from app.models import CovidStatistics, Country, States

# DATA = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data/data.json')
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

    if len(country) > 1 and len(state) == 0:
        country_statistics = CovidStatistics.objects.create(area=country, address=address, confirmed=confirmed,
                                                            deaths=deaths, recovered=recovered, date=date)
        country_data = Country.objects.create(name=country, latitude=latitude, longitude=longitude)
        country_data.statistics.add(country_statistics)
    if len(country) > 1 and len(state) > 1:
        state_statistics = CovidStatistics.objects.create(area=state, address=address, confirmed=confirmed,
                                                          deaths=deaths, recovered=recovered, date=date)
        state_data = States.objects.create(country=country, name=state, latitude=latitude, longitude=longitude)
        state_data.statistics.add(state_statistics)
