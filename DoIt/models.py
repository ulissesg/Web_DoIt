from django.db import models


class List(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=400, blank=True, null=True)
    is_done = models.BooleanField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    time_it_takes = models.IntegerField('How much time it takes in minutes', blank=True, null=True)
    is_important = models.BooleanField(blank=True, null=True)
    list = models.ForeignKey(List, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
