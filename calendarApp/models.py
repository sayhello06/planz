from django.db import models


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "calendarApp_db"
