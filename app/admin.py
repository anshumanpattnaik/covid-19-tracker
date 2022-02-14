from django.contrib import admin

from app.models import CovidStatistics, TotalCases, Country

admin.site.register(CovidStatistics)
admin.site.register(TotalCases)
admin.site.register(Country)
