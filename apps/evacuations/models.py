from django.db import models

class Evacuation(models.Model):
    requested_at = models.DateTimeField()
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default='pending')

    def __str__(self):
        return f"Evacuation {self.id} at {self.location}"