from django.db import models

class New(models.Model):
    title = models.CharField(max_length=100)
    short_desc = models.CharField(max_length=200)
    text = models.TextField()
    
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self. title} at {self.recorded_at}"