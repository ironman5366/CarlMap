# Internal/Django imports
from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(unique=True, primary_key=False, max_length=20)
    flag = models.ImageField()


class Location(models.Model):
    raw_str = models.CharField(max_length=255)
    long_name = models.CharField(max_length=255, default=None, null=True, blank=True)
    lat = models.FloatField()
    lon = models.FloatField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    year = models.IntegerField(default=2019)
