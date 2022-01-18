import json
import os

from django.shortcuts import render

from app.models import CovidStatistics, Country, States


def index(request):
    return render(request, 'index.html')


def parse_csv(request):
    return render(request, 'parse-csv.html')
