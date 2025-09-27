from django.db import models

class TrafficLight(models.Model):
    location_name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    type = models.CharField(max_length=100)
    install_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, default='operational')
    is_public = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def str(self):
        return self.location_name