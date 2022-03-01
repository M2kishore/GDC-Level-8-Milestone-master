from django.db import models

from django.contrib.auth.models import User

import datetime


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)
    report_time = models.TimeField(default=datetime.time(9, 00))
    report_date = models.DateField(default=datetime.date.today, null=True)
