from django.db import models


class CovidStatistics(models.Model):
    area = models.CharField(max_length=500, blank=True)
    address = models.CharField(max_length=500, blank=True)
    confirmed = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    recovered = models.IntegerField(default=0)
    date = models.CharField(max_length=500, blank=True)

    class Meta:
        managed = True
        db_table = 'covid_statistics'


class Country(models.Model):
    country_code = models.CharField(max_length=500, blank=True)
    name = models.CharField(max_length=500)
    flag = models.TextField(blank=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    statistics = models.ManyToManyField(CovidStatistics)

    class Meta:
        managed = True
        db_table = 'country'


class States(models.Model):
    country = models.ManyToManyField(Country)
    name = models.CharField(max_length=500)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    statistics = models.ManyToManyField(CovidStatistics)

    class Meta:
        managed = True
        db_table = 'states'
