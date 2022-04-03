from operator import mod
from re import search
from django.db import models


class Calculations(models.Model):
    year = models.CharField(max_length=4)
    month = models.CharField(max_length=2)

    area = models.IntegerField()

    flat_type = models.IntegerField()

    prediction = models.FloatField()

    search_frequency = models.IntegerField(default=1)

    def __str__(self) -> str:
        return f"Year: {self.year}, Month: {self.month}, Area: {self.area}, Flat: {self.flat_type}, Prediction: {self.prediction}, Frequency: {self.search_frequency}"
