from django.db import models


# Create your models here.
class WorldData(models.Model):
    country = models.CharField(
        null=False,
        blank=False,
        max_length=50,
    )
    Mag = models.FloatField()
    lat = models.FloatField(
        null=True,
    )
    lon = models.FloatField(
        null=True,
    )
    time = models.DateTimeField(
        blank=True,
    )


class WeeklyCsvFile(models.Model):
    csv_file = models.FileField(upload_to="downloadable_csv")
