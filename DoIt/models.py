from django.db import models


class List(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=400)
    is_done = models.BooleanField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    time_it_takes = models.IntegerField('How much time it takes')  # in minutes
    is_important = models.BooleanField()
    list = models.ForeignKey(List, on_delete=models.PROTECT)

    def __str__(self):
        return self.name
