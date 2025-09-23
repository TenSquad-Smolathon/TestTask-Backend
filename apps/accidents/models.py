from django.db import models

class Accident(models.Model):
    description = models.TextField(blank=True, null=True)
    latitude = models.FloatField()   # широта
    longitude = models.FloatField()  # долгота
    reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Авария {self.id} @ ({self.latitude}, {self.longitude})"