from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def parse_csv(request):
    return render(request, 'parse-csv.html')
