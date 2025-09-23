from django.db import models

class Fine(models.Model):
    issued_at = models.DateTimeField()  # дата штрафа
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Fine {self.id} at {self.issued_at}"