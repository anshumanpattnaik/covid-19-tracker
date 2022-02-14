from rest_framework import serializers
from .models import TotalCases, Country, CovidStatistics


class TotalCasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TotalCases
        fields = ['total_confirmed', 'total_deaths', 'total_recovered', 'date']


class CovidStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CovidStatistics
        fields = ['area', 'confirmed', 'deaths', 'recovered', 'date']


class CountrySerializer(serializers.ModelSerializer):
    statistics = CovidStatisticsSerializer(many=True)

    class Meta:
        model = Country
        fields = ['name', 'code', 'flag', 'coordinates', 'statistics']
