from django.db import models

class Metric(models.Model):
    name = models.CharField(max_length=100)
    value = models.FloatField()
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} at {self.recorded_at}"